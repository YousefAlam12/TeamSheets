<template>
    <div class="container pt-3">
        <div class="h1 text-center border rounded bg-light p-2 mb-3">
            Games
        </div>
        <div>
            <div class="alert alert-danger mt-3" role="alert" v-if="errorMessage">
                {{ errorMessage }}
            </div>

            <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
                Create Game
            </button>
            <div class="card mt-3" v-for="game in games">
                <div class="card-header">{{ game.date }}</div>
                <div class="card-body">
                    <h5 class="card-title">{{ game.name }} <span class="badge bg-primary">{{ game.players.length }}/{{ game.totalPlayers }}</span></h5>
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item" >{{ game.start_time }} - {{ game.end_time }}</li>
                        <li class="list-group-item" >£{{ game.price }}</li>
                        <li class="list-group-item" >Pitch: {{ game.address }}</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- Modal -->
        <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">Create Game</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label for="name" class="form-label">Name</label>
                            <input v-model="newGame.name" type="text" class="form-control" id="name">
                        </div>

                        <div class="mb-3">
                            <label for="date" class="form-label">Date</label>
                            <input v-model="newGame.date" type="date" class="form-control" id="date">
                        </div>

                        <div class="mb-3">
                            <label for="start-time" class="form-label">Start Time</label>
                            <input v-model="newGame.start_time" type="time" class="form-control" id="start-time">
                        </div>

                        <div class="mb-3">
                            <label for="end-time" class="form-label">End Time</label>
                            <input v-model="newGame.end_time" type="time" class="form-control" id="end-time">
                        </div>

                        <div class="mb-3">
                            <label for="description" class="form-label">Description</label>
                            <textarea v-model="newGame.description" name="description" id="description" class="form-control"></textarea>
                        </div>

                        <div class="mb-3">
                            <label for="total-players" class="form-label">Total Players</label>
                            <input v-model="newGame.totalPlayers" type="number" class="form-control" id="total-players">
                        </div>

                        <div class="mb-3">
                            <label for="price" class="form-label">Price</label>
                            <input v-model="newGame.price" type="number" class="form-control" id="price">
                        </div>

                        <div class="mb-3">
                            <label for="address" class="form-label">Pitch Address</label>
                            <input v-model="newGame.address" type="text" class="form-control" id="address">
                        </div>

                        <div class="mb-3">
                            <label for="postcode" class="form-label">Postcode</label>
                            <input v-model="newGame.postcode" type="text" class="form-control" id="postcode">
                        </div>
                    </div>

                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="createGame">Save changes</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            games: [],
            newGame: {
                name: '',
                date: '',
                start_time: null,
                end_time: null,
                description: '',
                totalPlayers: null,
                price: null,
                address: '',
                postcode: '',
                longitude: null,
                latitude: null
            },
            errorMessage : ''
        }
    },
    async mounted() {
        const response = await fetch('http://localhost:8000/games', {
            credentials: 'include'
        })
        const data = await response.json()
        console.log(data)
        this.games = data.games
    },
    methods: {
        async createGame() {
            await this.findGeo(this.newGame.postcode)
            if (!this.newGame.longitude || !this.newGame.latitude) {
                this.errorMessage = "Invalid Postcode.";
                return
            }
            const response = await fetch('http://localhost:8000/games', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({
                    'game' : this.newGame
                }) 
            })

            const data = await response.json()
            if (response.ok) {
                console.log(data)
                this.resetNewGame()
            }
            else {
                this.errorMessage = data.error
                this.errorMessage = 'Invalid details'
            }
        },
        async findGeo(postcode) {
            console.log(postcode)
            const response = await fetch(`https://api.postcodes.io/postcodes/${postcode}`)
            const data = await response.json()
            if (response.ok) {
                console.log(data.result.longitude)
                this.newGame.longitude = data.result.longitude
                this.newGame.latitude = data.result.latitude
            }
            else {
                console.log(data.error)
            }
        },
        resetNewGame() {
            this.newGame = {
                name: '',
                start_time: null,
                end_time: null,
                description: '',
                totalPlayers: null,
                price: null,
                address: '',
                postcode: '',
                longitude: null,
                latitude: null
            }
            this.errorMessage = ''
        }
    }
}
</script>
