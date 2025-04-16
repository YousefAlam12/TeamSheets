<template>
    <div class="container pt-3">
        <div class="h1 text-center border rounded bg-light p-2 mb-3">
            Game Details
        </div>
        <!-- <h5 class="card-title">{{ x.name }} <span class="badge bg-primary">{{ x.players ? x.players.length : '' }}/{{ x.totalPlayers }}</span></h5> -->

        <div class="card mt-3">
                <div class="card-header d-flex justify-content-between align-items-center">
                    {{ game.date }}
                    <div v-if="user && (user.id == game.admin.id && !game.fulltime)" @click="togglePrivacy">
                        <span class="badge bg-primary btn btn-primary">
                            {{ game.is_private ? 'Private' : 'Public' }} 
                            <i class="bi bi-arrow-repeat"></i>
                        </span>
                    </div>

                    <div v-else>
                        <span class="badge bg-primary">
                            {{ game.is_private ? 'Private' : 'Public' }}  
                        </span>
                    </div>
                </div>
                
                <div class="card-body">
                    <!-- <h5 class="card-title">{{ game.name }} <span class="badge bg-primary">{{ game.players.length }}/{{ game.totalPlayers }}</span></h5> -->
                    <h5 class="card-title">
                        {{ game.name }} 
                        <span class="badge bg-primary">{{ game.players ? game.players.length : '' }}/{{ game.totalPlayers }}</span>
                        <button v-if="!isSubscribed" class="btn btn-sm btn-success ms-2" @click="subscribe"><i class="bi bi-bell-fill"></i></button>
                        <button v-else class="btn btn-sm btn-danger ms-2" @click="unsubscribe"><i class="bi bi-bell-slash"></i></button>
                    </h5>
                    <div class="border rounded bg-info p-2">
                        <div class="mb-3">
                            <h6 class="card-text"><u>Description:</u> 
                                <button v-if="user && game && (user.id == game.admin.id && !game.fulltime)" class="btn btn-info btn-sm" @click="changeDescription = game.description"><i class="bi bi-pencil-square" data-bs-toggle="modal" data-bs-target="#descriptionModal"></i></button>
                            </h6>
                            <!-- <p class="card-text">{{ game.description }}</p> -->
                            <p class="card-text" v-html="formatText(game.description)"></p>
                        </div>
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item" >Time: {{ game.start_time }} - {{ game.end_time }}</li>
                            <li class="list-group-item" >Price: £{{ game.price }}</li>
                            <li class="list-group-item" >Pitch: {{ game.address }} {{ game.postcode }}</li>
                            <li v-if="game.admin" class="list-group-item" >Admin: {{ game.admin.username }}</li>
                        </ul>
                    </div>
                </div>

                <!-- temp -->
                 <!-- ------------------------------------------------------------------------------ -->
                 <div class="alert alert-danger mt-3" role="alert" v-if="error">
                    {{ error }}
                </div>
                
                 <div v-if="user.id && (user.id == game.admin.id && !game.fulltime)" class="text-center d-flex flex-column align-items-center p-2 mb-2">
                    <button @click="balanceTeams" class="btn btn-primary">Balance Teams</button>
                    <button @click="fulltime" class="btn btn-info mt-3">Fulltime</button>
                </div>
                <!-- ------------------------------------------------------------------------------ -->
                <div v-if="loading" class="d-flex justify-content-center w-100 mb-3">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>

                <div v-else class="card-body d-flex align-items-start teams">
                    <table class="table table-primary">
                        <thead>
                            <tr class="text-center">
                                <th class="bg-primary">Team A</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="player in game.players">
                                <td v-if="player.team == 'A'" class="d-flex justify-content-between">
                                    <div>
                                        <div class="d-flex">
                                            <button class="nav-link player-inspect" @click="setSelectedPlayer(player)" data-bs-toggle="modal" data-bs-target="#PlayerModal">{{ player.username }}</button>
                                            <PlayerInspect :isFulltime="game.fulltime" :player="selectedPlayer" :user="user" :isAdmin="user.id == game.admin.id" @sendFriendRequest="sendFriendRequest" @kickPlayer="kickPlayer"/>
                                            <button v-if="player.paid" class="btn btn-sm btn-success ms-1"><i class="bi bi-hand-thumbs-up"></i></button>
                                        </div>
                                        <small class="form-text text-muted">
                                            <div v-if="player.stats" class="d-flex flex-row bd-highlight">
                                                <div class="pe-2 bd-highlight">atk: {{ player.stats.attack }}</div>
                                                <div class="pe-2 bd-highlight">def: {{ player.stats.defence }}</div>
                                                <div class="pe-2 bd-highlight">str: {{ player.stats.strength }}</div>
                                                <div class="pe-2 bd-highlight">spd: {{ player.stats.speed }}</div>
                                                <div class="pe-2 bd-highlight">teq: {{ player.stats.technique }}</div>
                                            </div>
                                            <div v-else class="d-flex flex-row bd-highlight">
                                                <div class="pe-2 bd-highlight">New Player</div>
                                            </div>
                                        </small>
                                    </div>

                                    <div class="d-flex align-items-center" v-if="user.id == game.admin.id && !game.fulltime">
                                        <button class="btn btn-sm btn-primary" @click="changeTeam(player, 'A')">A</button>
                                        <button class="btn btn-sm btn-danger" @click="changeTeam(player, 'B')">B</button>
                                    </div>

                                    <div v-else class="d-flex align-items-center">
                                        <button v-if="ratedPlayers ? !ratedPlayers.find(user => user.id == player.id) && isPlaying : ''" class="btn btn-success" data-bs-toggle="modal" data-bs-target="#exampleModal" @click="setSelectedPlayer(player)">Rate</button>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>

                    <table class="table table-light">
                        <thead>
                            <tr class="text-center">
                                <th>
                                    Players
                                    <!-- <button class="btn btn-sm btn-success"><i class="bi bi-plus-circle-fill"></i></button> -->
                                    <InvitePlayer :user="user" :game="game"/>
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="player in game.players">
                                <td v-if="player.team == null" class="d-flex justify-content-between">
                                    <div>
                                        <div class="d-flex">
                                            <button class="nav-link player-inspect" @click="setSelectedPlayer(player)" data-bs-toggle="modal" data-bs-target="#PlayerModal">{{ player.username }}</button>
                                            <PlayerInspect :isFulltime="game.fulltime" :player="selectedPlayer" :user="user" :isAdmin="user.id == game.admin.id" @sendFriendRequest="sendFriendRequest" @kickPlayer="kickPlayer"/>                                            <button v-if="player.paid" class="btn btn-sm btn-success ms-1"><i class="bi bi-hand-thumbs-up"></i></button>
                                        </div>
                                        <small class="form-text text-muted">
                                            <div v-if="player.stats" class="d-flex flex-row bd-highlight">
                                                <div class="pe-2 bd-highlight">atk: {{ player.stats.attack }}</div>
                                                <div class="pe-2 bd-highlight">def: {{ player.stats.defence }}</div>
                                                <div class="pe-2 bd-highlight">str: {{ player.stats.strength }}</div>
                                                <div class="pe-2 bd-highlight">spd: {{ player.stats.speed }}</div>
                                                <div class="pe-2 bd-highlight">teq: {{ player.stats.technique }}</div>
                                            </div>
                                            <div v-else class="d-flex flex-row bd-highlight">
                                                <div class="pe-2 bd-highlight">New Player</div>
                                            </div>
                                        </small>
                                    </div>

                                    <div class="d-flex align-items-center" v-if="user.id == game.admin.id && !game.fulltime">
                                        <button class="btn btn-sm btn-primary" @click="changeTeam(player, 'A')">A</button>
                                        <button class="btn btn-sm btn-danger" @click="changeTeam(player, 'B')">B</button>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>

                    <table class="table table-danger">
                        <thead>
                            <tr class="text-center">
                                <th class="bg-danger">Team B</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="player in game.players">
                                <td v-if="player.team == 'B'" class="d-flex justify-content-between">
                                    <div>
                                        <div class="d-flex">
                                            <button class="nav-link player-inspect" @click="setSelectedPlayer(player)" data-bs-toggle="modal" data-bs-target="#PlayerModal">{{ player.username }}</button>
                                            <PlayerInspect :isFulltime="game.fulltime" :player="selectedPlayer" :user="user" :isAdmin="user.id == game.admin.id" @sendFriendRequest="sendFriendRequest" @kickPlayer="kickPlayer"/>                                            <button v-if="player.paid" class="btn btn-sm btn-success ms-1"><i class="bi bi-hand-thumbs-up"></i></button>
                                        </div>
                                        <small class="form-text text-muted">
                                            <div v-if="player.stats" class="d-flex flex-row bd-highlight">
                                                <div class="pe-2 bd-highlight">atk: {{ player.stats.attack }}</div>
                                                <div class="pe-2 bd-highlight">def: {{ player.stats.defence }}</div>
                                                <div class="pe-2 bd-highlight">str: {{ player.stats.strength }}</div>
                                                <div class="pe-2 bd-highlight">spd: {{ player.stats.speed }}</div>
                                                <div class="pe-2 bd-highlight">teq: {{ player.stats.technique }}</div>
                                            </div>
                                            <div v-else class="d-flex flex-row bd-highlight">
                                                <div class="pe-2 bd-highlight">New Player</div>
                                            </div>
                                        </small>
                                    </div>

                                    <div class="d-flex align-items-center" v-if="user.id == game.admin.id && !game.fulltime">
                                        <button class="btn btn-sm btn-primary" @click="changeTeam(player, 'A')">A</button>
                                        <button class="btn btn-sm btn-danger" @click="changeTeam(player, 'B')">B</button>
                                    </div>

                                    <div v-else class="d-flex align-items-center">
                                        <button v-if="ratedPlayers ? !ratedPlayers.find(user => user.id == player.id) && isPlaying : ''" class="btn btn-success" data-bs-toggle="modal" data-bs-target="#exampleModal" @click="setSelectedPlayer(player)">Rate</button>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div v-if="loading == false" class="text-center d-flex flex-column align-items-center p-2 mb-2">
                    <!-- <button v-if="!game.players.find(player => player.id == user.id)" @click="joinGame">Join</button> -->
                    <button v-if="paid == false" class="btn btn-success mb-2" @click="payGame">Pay</button>
                    <div v-if="!game.fulltime">
                        <label class="border p-2 rounded text-white bg-secondary" v-if="game.players ? game.players.length >= game.totalPlayers : ''">Game is full</label>
                        
                        <div class="mt-2">
                            <!-- <button v-if="game.players ? !game.players.find(player => player.id == user.id) && game.players.length < game.totalPlayers : ''" @click="joinGame" class="btn btn-success">Join</button> -->
                            <button v-if="user && !isPlaying && game.players.length < game.totalPlayers" @click="joinGame" class="btn btn-success">Join</button>
                            <!-- <button v-if="game.players ? game.players.find(player => player.id == user.id) : ''" @click="leaveGame" class="btn btn-warning">Leave</button> -->
                            <button v-if="user && isPlaying" @click="leaveGame" class="btn btn-warning">Leave</button>
                        </div>
                        <button v-if="user && (user.id == game.admin.id && !game.fulltime)" class="btn btn-danger mt-4" @click="cancelGame">Cancel Game</button>
                    </div>
                </div>
            </div>

<!-- ------------------------------------------------------------------------------------------------------------------------------ -->
            <!-- modal for rating players -->
            <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalLabel">Rating {{ selectedPlayer ? selectedPlayer.username : '' }}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <div class="mb-3">
                                <label for="atk" class="form-label">Attack</label>
                                <select v-model="ratings.attack" class="form-control" id="atk">
                                    <option v-for="n in 10" >{{ n }}</option>
                                </select>
                            </div>
        
                            <div class="mb-3">
                                <label for="def" class="form-label">Defence</label>
                                <select v-model="ratings.defence" class="form-control" id="def">
                                    <option v-for="n in 10" >{{ n }}</option>
                                </select>
                            </div>
        
                            <div class="mb-3">
                                <label for="str" class="form-label">Strength</label>
                                <select v-model="ratings.strength" class="form-control" id="str">
                                    <option v-for="n in 10" >{{ n }}</option>
                                </select>
                            </div>
        
                            <div class="mb-3">
                                <label for="spd" class="form-label">Speed</label>
                                <select v-model="ratings.speed" class="form-control" id="spd">
                                    <option v-for="n in 10" >{{ n }}</option>
                                </select>
                            </div>
        
                            <div class="mb-3">
                                <label for="teq" class="form-label">Technique</label>
                                <select v-model="ratings.technique" class="form-control" id="teq">
                                    <option v-for="n in 10" >{{ n }}</option>
                                </select>
                            </div>
                        </div>
        
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button type="button" class="btn btn-success" data-bs-dismiss="modal" @click="ratePlayer">Rate</button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Edit Description Modal -->
        <div class="modal fade" id="descriptionModal" tabindex="-1" aria-labelledby="descriptionModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="descriptionModalLabel">Edit Description</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label for="description" class="form-label">Description</label>
                            <textarea v-model="changeDescription" name="description" id="description" class="form-control"></textarea>
                        </div>
                    </div>

                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="editDescription">Save</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
import PlayerInspect from '../Components/PlayerInspect.vue';
import InvitePlayer from '../Components/InvitePlayer.vue';
import { useUserStore } from '../stores/user.js';

export default {
    components: {
        PlayerInspect, InvitePlayer
    },
    computed: {
        id() {
            return this.$route.params.id
        },
        isSubscribed() {
            if (this.user) {
                return this.user.subscribed_games.some(g => g.game === this.game.id)
            }
        },
        isPlaying() {
            if (this.game) {
                return this.game.players.find(player => player.id == this.user.id)
            }
        }
    },
    data() {
        return {
            user: '',
            game: [],
            paid: null,
            loading: false,
            ratedPlayers: null,
            selectedPlayer: null,
            ratings: {
                attack: null,
                defence: null,
                strength: null,
                speed: null,
                technique: null,
            },
            error: '',
            changeDescription: null
        }
    },
    async mounted() {
        const response = await fetch(`http://localhost:8000/game/${this.id}`, {
            credentials: 'include'
        })
        const data = await response.json()
        if (response.ok) {
            this.user = useUserStore().user
            this.game = data.game
            this.paid = data.paid
        }
        // user is not allowed to view game
        else {
            this.$router.push('/')
        }

        if (this.game.fulltime) {
            const response2 = await fetch(`http://localhost:8000/ratings/${this.id}`, {
                credentials: 'include'
            })
            const data = await response2.json()
            this.ratedPlayers = data.ratedPlayers
        }
    },
    methods: {
        async joinGame() {
            const response = await fetch(`http://localhost:8000/game/${this.id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({
                    'join' : true
                }) 
            })

            const data = await response.json()
            if (response.ok) {
                console.log(data)
                this.game = data.game
                this.paid = data.paid
                useUserStore().saveUser(data.user)
                this.user = useUserStore().user
            }
        },
        async leaveGame() {
            if (confirm('Are you sure you want to leave this game?')) {
                const response = await fetch(`http://localhost:8000/game/${this.id}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    credentials: 'include',
                    body: JSON.stringify({
                        'leave' : true
                    }) 
                })
    
                const data = await response.json()
                if (response.ok) {
                    this.game = data.game
                    this.paid = null
                    useUserStore().saveUser(data.user)
                    this.user = useUserStore().user
                }
                if (this.game.is_private && this.user.id != this.game.admin.id) {
                    this.$router.push('/')
                }
            }
        },
        async payGame() {
            const response = await fetch(`http://localhost:8000/game/${this.id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({
                    'paid' : true
                }) 
            })

            const data = await response.json()
            if (response.ok) {
                this.game = data.game
                this.paid = data.paid
            }
        },
        async changeTeam(player, team) {
            const response = await fetch(`http://localhost:8000/teams/${this.id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({
                    'player' : player.id,
                    'team' : team
                })
            })
            const data = await response.json()
            if (response.ok) {
                this.game = data.game
            }
        },
        async balanceTeams() {
            if (this.loading == false) {
                this.loading = true
                const response = await fetch(`http://localhost:8000/balanceTeams/${this.id}`, {
                    credentials: 'include'
                })
                const data = await response.json()
                if (response.ok) {
                    this.game = data.game
                }
                this.loading = false
            }
        },
        async fulltime() {
            if (confirm("Are you sure you want to call fulltime? This is irreversible.")) {
                if (this.loading == false) {
                    const response = await fetch(`http://localhost:8000/game/${this.id}`, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        credentials: 'include',
                        body: JSON.stringify({
                            'fulltime' : true
                        }) 
                    })
                    const data = await response.json()
                    if (response.ok) {
                        this.game = data.game
                        
                        // updates page to rating view
                        const response2 = await fetch(`http://localhost:8000/ratings/${this.id}`, {
                            credentials: 'include'
                        })
                        const data2 = await response2.json()
                        this.ratedPlayers = data2.ratedPlayers
                    }
                }
            }
        },
        async setSelectedPlayer(currentPlayer) {
            this.selectedPlayer = currentPlayer
        },
        async ratePlayer() {
            const response = await fetch(`http://localhost:8000/ratings/${this.id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({
                    'ratings' : this.ratings,
                    'player': this.selectedPlayer.id
                })
            })

            const data = await response.json()
            if (response.ok) {
                this.game = data.game
                this.ratedPlayers = data.ratedPlayers
                this.error = ''
            }
            else {
                this.error = data.error
            }
        },
        async sendFriendRequest(player) {
            const response = await fetch(`http://localhost:8000/send_friend_request`, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'to_user': player.id 
                })
            })
            if (response.ok) {
                const data = await response.json()
                useUserStore().saveUser(data.user)
                this.user = useUserStore().user
            }
        },
        async kickPlayer(player) {
            if (confirm(`Are you sure you want to kick ${player.username} from the game?`)) {
                if (this.loading == false) {
                    this.loading = true
                    const response = await fetch(`http://localhost:8000/game/${this.id}`, {
                        method: 'DELETE',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        credentials: 'include',
                        body: JSON.stringify({
                            'kick' : player.id
                        }) 
                    })
        
                    const data = await response.json()
                    if (response.ok) {
                        this.game = data.game
                    }
                    this.loading = false
                }
            }
        },
        async togglePrivacy() {
            if (confirm(`Are you sure you want to change the privacy status of the game?`)) {
                const response = await fetch(`http://localhost:8000/game/${this.id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    credentials: 'include',
                    body: JSON.stringify({
                        'toggle_privacy' : true
                    }) 
                })
    
                const data = await response.json()
                if (response.ok) {
                    this.game = data.game
                }
            }
        },
        async cancelGame() {
            if (confirm(`Are you sure you want to CANCEL this game?`)) {
                if (this.loading == false) {
                    this.loading = true
                    const response = await fetch(`http://localhost:8000/game/${this.id}`, {
                        method: 'DELETE',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        credentials: 'include',
                        body: JSON.stringify({
                            'cancel_game' : true
                        }) 
                    })
        
                    const data = await response.json()
                    if (response.ok) {
                        this.$router.push('/games')
                    }
                    this.loading = false
                }
            }
        },
        async subscribe() {
            const response = await fetch(`http://localhost:8000/game/${this.id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({
                    'subscribe': true
                })
            })
            const data = await response.json()
            if (response.ok) {
                useUserStore().saveUser(data.user)
                this.user = useUserStore().user
            }
        },
        async unsubscribe() {
            const response = await fetch(`http://localhost:8000/game/${this.id}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({
                    'unsubscribe': true
                })
            })
            const data = await response.json()
            if (response.ok) {
                useUserStore().saveUser(data.user)
                this.user = useUserStore().user
            }
        },
        async editDescription() {
            const response = await fetch(`http://localhost:8000/game/${this.id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({
                    'description': this.changeDescription
                })
            })
            const data = await response.json()
            if (response.ok) {
                this.game = data.game
            }
        },
        formatText(text) {
            if (typeof text === 'string') {
                return text.replace(/\n/g, '<br>')
            }
        }
    }
}
</script>

<style scoped>
@media (max-width: 991px) {
    .teams {
        flex-direction: column;
    }
}

.player-inspect:hover {
    color: #007bff; /* Change color on hover (e.g., Bootstrap primary color) */
}
</style>