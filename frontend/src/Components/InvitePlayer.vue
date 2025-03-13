<template>
    <button v-if="!game.fulltime" class="btn btn-sm btn-success" data-bs-toggle="modal" data-bs-target="#gameInviteModal"><i
            class="bi bi-plus-circle-fill"></i></button>

    <!-- Sending Game Invite Modal -->
    <div v-if="user" class="modal fade" id="gameInviteModal" tabindex="-1" aria-labelledby="gameInviteModalLabel"
        aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="gameInviteModalLabel">Invite Friend</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body user-list">
                    <div class="mb-3">
                        <input v-model="userSearch" class="form-control mb-3" type="search" placeholder="Search Friend"
                            for="userSearch">
                        <ul class="overflow-auto list-group">
                            <li v-for="(u, index) in filteredFriends"
                                class="d-flex list-group-item justify-content-between p-3">
                                <label class="align-content-center">{{ u.username }}</label>
                                <div>
                                    <button class="btn btn-primary" v-if="game.players ? game.players.find(player => player.id == u.id) : ''">In Game</button>
                                    <button v-else class="btn btn-success" :class="{ 'btn btn-warning': u.sendInvite }"
                                        @click="sendInvite(index, u)">{{ u.sendInvite ? 'Invite Sent' : 'Send' }}</button>
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>

                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="">Close</button>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
export default {
    props: {
        user: {
            required: true
        },
        game: {
            required: true
        }
    },
    data() {
        return {
            userSearch: '',
        }
    },
    async unmounted() {
        // Reset the sendInvite property for each friend when the component is unmounted
        if (this.user) {
            this.user.friends.forEach(friend => {
                friend.sendInvite = false;
            });
        }
    },
    computed: {
        filteredFriends() {
            return this.user.friends.filter(user => {
                return user.username.toLowerCase().includes(this.userSearch.toLowerCase());
            });
        }
    },
    methods: {
        async sendInvite(i, user) {
            // this.user.friends[i].sendInvite = true
            user.sendInvite = true

            const response = await fetch(`http://localhost:8000/gameInvite/${this.game.id}`, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'to_user': user.id
                })
            })
        }
    }
}
</script>


<style scoped>
.user-list {
    max-height: 500px;
    overflow-y: auto;
}
</style>