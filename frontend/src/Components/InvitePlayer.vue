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
                                class="d-flex list-group-item justify-content-between align-items-center p-3">
                                <div class="d-flex align-items-start flex-column">
                                    <label class="align-content-center">{{ u.username }}</label>
                                    <small class="form-text text-muted">
                                        <div v-if="u.stats" class="d-flex flex-row bd-highlight">
                                            <div class="pe-2 bd-highlight">atk: {{ u.stats.attack }}</div>
                                            <div class="pe-2 bd-highlight">def: {{ u.stats.defence }}</div>
                                            <div class="pe-2 bd-highlight">str: {{ u.stats.strength }}</div>
                                            <div class="pe-2 bd-highlight">spd: {{ u.stats.speed }}</div>
                                            <div class="pe-2 bd-highlight">teq: {{ u.stats.technique }}</div>
                                        </div>
                                        <div v-else class="d-flex flex-row bd-highlight">
                                            <div class="pe-2 bd-highlight">New Player</div>
                                        </div>
                                    </small>
                                </div>
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
        // search for user in friends 
        filteredFriends() {
            return this.user.friends.filter(user => {
                return user.username.toLowerCase().includes(this.userSearch.toLowerCase());
            });
        }
    },
    methods: {
        // sends game invite to chosen user
        async sendInvite(i, user) {
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
            if (response.ok) {
                user.sendInvite = true
            }
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