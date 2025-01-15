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
                            <li class="list-group-item" >Pitch: {{ game.address }}</li>
                        </ul>
                    </div>
                </div>
                
                <div class="card-body text-center d-flex">
                    <table class="table table-primary">
                        <thead>
                            <tr>
                                <th class="bg-primary">Team A</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="player in game.players">
                                <td v-if="player.team == 'A'">{{ player.username }}</td>
                            </tr>
                        </tbody>
                    </table>

                    <table class="table table-light">
                        <thead>
                            <tr>
                                <th>Players</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="player in game.players">
                                <td v-if="player.team == null">{{ player.username }}</td>
                            </tr>
                        </tbody>
                    </table>

                    <table class="table table-danger">
                        <thead>
                            <tr>
                                <th class="bg-danger">Team B</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="player in game.players">
                                <td v-if="player.team == 'B'">{{ player.username }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div class="text-center p-2">
                    <!-- <button v-if="!game.players.find(player => player.id == user.id)" @click="joinGame">Join</button> -->
                    <button v-if="game.players ? !game.players.find(player => player.id == user.id) : ''" @click="joinGame">Join</button>
                    <button v-else @click="">Leave</button>
                </div>
            </div>
    </div>
</template>

<script>
export default {
    props: {
        x: {
            type: Object,
            // required: true
        }
    },
    computed: {
        id() {
            return this.$route.params.id
        }
    },
    data() {
        return {
            user: '',
            game: [],
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
                // window.location.reload()
            }
        }
    }
}
</script>
