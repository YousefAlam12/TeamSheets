<template>
    <div class="container pt-3">
        <div class="h1 text-center border rounded bg-light p-2 mb-3">
            Home
        </div>

        <!-- notification bar -->
        <div v-if="user && isNotification" class="card mb-5">
            <div class="d-flex card-header bg-primary text-white justify-content-between p-3">
                <label class="align-content-center">Notifications</label>
            </div>
            <ul class="list-group list-group-flush">
                <li v-for="notif in user.game_invites" class="list-group-item">
                    <div class="d-flex justify-content-between align-items-center p-1">
                        <span>
                            You have been invited to a game by {{ notif.from_user }}
                            <button class="btn btn-sm btn-success" @click="this.$router.push(`/gameDetails/${notif.game_id}`)">View</button>
                        </span>
                        <button class="btn-close ms-3" @click="clearNotification(notif)"></button>
                    </div>
                </li>

                <li v-if="user.received_requests.length > 0 && showFriendNotification" class="list-group-item">
                    <div class="d-flex justify-content-between align-items-center p-1">
                        <span>
                            You have been sent some friend requests
                            <button class="btn btn-sm btn-success" @click="this.$router.push(`/friendsList`)">View</button>
                        </span>
                        <button class="btn-close ms-3" @click="showFriendNotification = false"></button>
                    </div>
                </li>
            </ul>
        </div>

        <ul class="nav nav-tabs">
            <li class="nav-item">
                <button class="nav-link" :class="{ active: activeTab === 'myGames' }" @click="setActiveTab('myGames')">My Games</button>
            </li>
            
            <li class="nav-item">
                <button class="nav-link" :class="{ active: activeTab === 'adminGames' }" @click="setActiveTab('adminGames')">Admin Games</button>
            </li>
            
            <li class="nav-item">
                <button class="nav-link" :class="{ active: activeTab === 'playedGames' }" @click="setActiveTab('playedGames')">Played Games</button>
            </li>

        </ul>

        <div class="tab-content mt-3">
            <!-- <p v-if="activeTab == 'myGames'">Show my games</p> -->
            <DisplayGames v-if="activeTab == 'myGames'" :games="myGames" />
            
            <DisplayGames v-if="activeTab == 'playedGames'" :games="playedGames" />

            <DisplayGames v-if="activeTab == 'adminGames'" :games="adminGames" />
        </div>

    </div>
</template>
  
<script>
import DisplayGames from '../Components/DisplayGames.vue';
import { useUserStore } from '../stores/user';

export default {
    components: {
        DisplayGames
    },
    computed: {
        isNotification() {
            return this.user.game_invites.length > 0 || this.showFriendNotification ? true : false
        },

    },
    data() {
        return {
            activeTab: 'myGames',
            myGames : [],
            adminGames : [],
            playedGames : [],
            user: null,
            showFriendNotification: null
        }
    },
    async mounted() {
        const response = await fetch('http://localhost:8000/myGames', {
            credentials: 'include'
        })
        const data = await response.json()
        this.myGames = data.myGames
        this.adminGames = data.adminGames
        this.playedGames = data.playedGames
        this.user = useUserStore().user
        this.showFriendNotification = data.user.received_requests.length > 0 ? true : false
        console.log(this.user)
    },
    methods: {
        setActiveTab(tab) {
            this.activeTab = tab
        },
        async clearNotification(notif) {
            const response = await fetch(`http://localhost:8000/gameInvite/${notif.game_id}`, {
                method: 'DELETE',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'game_invite': notif.id
                })
            })
            const data = await response.json()
            if (response.ok) {
                useUserStore().saveUser(data.user)
                this.user = useUserStore().user
            }
        },
    }
}
</script>
