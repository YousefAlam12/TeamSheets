<template>
    <div class="container pt-3">
        <div class="h1 text-center border rounded bg-light p-2 mb-3">
            Main
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

            <p v-if="activeTab == 'adminGames'">Show admined games</p>

            <p v-if="activeTab == 'playedGames'">Show played games</p>
        </div>

    </div>
  </template>
  
<script>
import DisplayGames from '../Components/DisplayGames.vue';

export default {
    components: {
        DisplayGames
    },
    data() {
        return {
            activeTab: 'myGames',
            myGames : []
        }
    },
    async mounted() {
        const response = await fetch('http://localhost:8000/myGames', {
            credentials: 'include'
        })
        const data = await response.json()
        this.myGames = data.myGames
    },
    methods: {
        setActiveTab(tab) {
            this.activeTab = tab
        }
    }
}
</script>
