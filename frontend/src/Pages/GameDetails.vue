<template>
    <div class="container pt-3">
        <div class="h1 text-center border rounded bg-light p-2 mb-3">
            Game Details
        </div>
        <!-- <h5 class="card-title">{{ x.name }} <span class="badge bg-primary">{{ x.players ? x.players.length : '' }}/{{ x.totalPlayers }}</span></h5> -->

        <div class="card mt-3">
                <div class="card-header">{{ game.date }}</div>
                <div class="card-body">
                    <!-- <h5 class="card-title">{{ game.name }} <span class="badge bg-primary">{{ game.players.length }}/{{ game.totalPlayers }}</span></h5> -->
                    <h5 class="card-title">{{ game.name }} <span class="badge bg-primary">{{ game.players ? game.players.length : '' }}/{{ game.totalPlayers }}</span></h5>
                    <div class="border rounded bg-info p-2">
                        <p class="card-text">Description: {{ game.description }}</p>
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item" >{{ game.start_time }} - {{ game.end_time }}</li>
                            <li class="list-group-item" >£{{ game.price }}</li>
                            <li class="list-group-item" >Pitch: {{ game.address }} {{ game.postcode }}</li>
                        </ul>
                    </div>
                </div>

                <!-- temp -->
                 <!-- ------------------------------------------------------------------------------ -->
                <div v-if="user.id && (user.id == game.admin.id && !game.fulltime)" class="text-center d-flex flex-column align-items-center p-2 mb-2">
                    <button @click="balanceTeams">Balance Teams</button>
                </div>
                <!-- ------------------------------------------------------------------------------ -->
                <div v-if="loading" class="d-flex justify-content-center w-100">
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
                                        {{ player.username }} 
                                        <button v-if="player.paid" class="btn btn-sm btn-success"><i class="bi bi-hand-thumbs-up"></i></button>
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

                    <table class="table table-light">
                        <thead>
                            <tr class="text-center">
                                <th>Players</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="player in game.players">
                                <td v-if="player.team == null" class="d-flex justify-content-between">
                                    <div>
                                        {{ player.username }} 
                                        <button v-if="player.paid" class="btn btn-sm btn-success"><i class="bi bi-hand-thumbs-up"></i></button>
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

                                    <div v-if="user.id == game.admin.id && !game.fulltime">
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
                                        {{ player.username }} 
                                        <button v-if="player.paid" class="btn btn-sm btn-success"><i class="bi bi-hand-thumbs-up"></i></button>
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

                                    <div v-if="user.id == game.admin.id && !game.fulltime">
                                        <button class="btn btn-sm btn-primary" @click="changeTeam(player, 'A')">A</button>
                                        <button class="btn btn-sm btn-danger" @click="changeTeam(player, 'B')">B</button>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div class="text-center d-flex flex-column align-items-center p-2 mb-2">
                    <!-- <button v-if="!game.players.find(player => player.id == user.id)" @click="joinGame">Join</button> -->
                    <button v-if="paid == false" class="btn btn-success mb-2" @click="payGame">Pay</button>
                    <div v-if="!game.fulltime">
                        <label class="border p-2 rounded text-white bg-primary" v-if="game.players ? game.players.length >= game.totalPlayers : ''">Game is full</label>
                        <!-- <button v-else-if="game.players ? !game.players.find(player => player.id == user.id) : ''" @click="joinGame" class="btn btn-success">Join</button> -->
                        <div v-else class="mt-2">
                            <button v-if="game.players ? !game.players.find(player => player.id == user.id) : ''" @click="joinGame" class="btn btn-success">Join</button>
                            <button v-else @click="leaveGame" class="btn btn-warning">Leave</button>
                        </div>
                    </div>
                </div>
            </div>
    </div>
</template>

<script>
export default {
    // props: {
    //     x: {
    //         type: Object,
    //         // required: true
    //     }
    // },
    computed: {
        id() {
            return this.$route.params.id
        }
    },
    data() {
        return {
            user: '',
            game: [],
            paid: null,
            loading: false
        }
    },
    async mounted() {
        const response = await fetch(`http://localhost:8000/game/${this.id}`, {
            credentials: 'include'
        })
        const data = await response.json()
        console.log(data)
        this.user = data.user
        this.game = data.game
        this.paid = data.paid
        // console.log(user)
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
            }
        },
        async leaveGame() {
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
    }
}
</script>

<style scoped>
@media (max-width: 991px) {
    .teams {
        flex-direction: column;
    }
}
</style>