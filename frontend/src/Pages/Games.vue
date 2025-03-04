<template>
    <div class="container pt-3">
        <div class="h1 text-center border rounded bg-light p-2 mb-3">
            Games
        </div>
        <div>
            <div class="alert alert-danger mt-3" role="alert" v-if="errorMessage">
                {{ errorMessage }}
            </div>

            <div class="d-flex">
                <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
                    Create Game
                </button>

                <button type="button" class="btn btn-info ms-auto" data-bs-toggle="modal" data-bs-target="#filterModal">
                    Filter
                </button>
            </div>

            <!-- <DisplayGames :games="games"/> -->
            <DisplayGames :games="shownGames"/>
        </div>

        <!-- Create new game Modal -->
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
                            <input v-model="newGame.totalPlayers" type="number" class="form-control" id="total-players" min="10" max="22">
                        </div>

                        <div class="mb-3">
                            <label for="price" class="form-label">Price</label>
                            <input v-model="newGame.price" type="number" class="form-control" id="price" min="0">
                        </div>

                        <div class="mb-3">
                            <label for="address" class="form-label">Pitch Address</label>
                            <input v-model="newGame.address" type="text" class="form-control" id="address">
                        </div>

                        <div class="mb-3">
                            <label for="postcode" class="form-label">Postcode</label>
                            <input v-model="newGame.postcode" type="text" class="form-control" id="postcode">
                        </div>

                        <div class="mb-3">
                            <label for="privacy" class="form-label">Privacy Status</label>
                            <select v-model="newGame.is_private" id="privacy" class="form-select">
                                <option :value="false">Public</option>
                                <option :value="true">Private</option>
                            </select>
                        </div>
                    </div>

                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="createGame">Create</button>
                    </div>
                </div>
            </div>
        </div>


        <!-- Filter Modal -->
        <div class="modal fade" id="filterModal" tabindex="-1" aria-labelledby="filterModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="filterModalLabel">Filter</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label for="filter-date" class="form-label">Date</label>
                            <!-- <input v-model="filter.date" type="date" class="form-control" id="filter-date"> -->
                            <input v-model="filter.date" type="month" class="form-control" id="filter-date">
                        </div>

                        <div class="mb-3">
                            <label for="price" class="form-label">Price</label>
                            <input v-model="filter.price" type="number" class="form-control" id="filter-price" min="0">
                            <small id="priceInfo" class="form-text text-muted">All games upto selected price</small>
                        </div>
                    </div>

                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="resetFilters">Clear Filters</button>
                        <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="filterGames(games)">Apply Filters</button>
                    </div>
                </div>
            </div>
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
                latitude: null,
                is_private: false
            },
            errorMessage : '',
            shownGames : [],
            filter : {
                date: null,
                price: null
            }
        }
    },
    async mounted() {
        const response = await fetch('http://localhost:8000/games', {
            credentials: 'include'
        })
        const data = await response.json()
        console.log(data)
        this.games = data.games
        this.shownGames = data.games
    },
    methods: {
        async createGame() {
            // validating fields 
            await this.findGeo(this.newGame.postcode)
            if (!this.newGame.longitude || !this.newGame.latitude) {
                this.errorMessage = "Invalid Postcode.";
                return
            }
            if (this.newGame.totalPlayers < 10 || this.newGame.totalPlayers > 22 || this.newGame.totalPlayers % 2 != 0) {
                this.errorMessage = "Total players must be between 10-22 (11-5 aside)"
                return
            }
            if (this.newGame.price < 0) {
                this.errorMessage = "Invalid price"
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
                this.games = data.games
                this.shownGames = data.games
            }
            else {
                this.errorMessage = data.error
                // this.errorMessage = 'Invalid details'
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
                this.newGame.longitude = null
                this.newGame.latitude = null
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
        },
        filterGames(filteredGames) {
            if (this.filter.date != null) {
                // Extract year and month from filter
                const filterYear = this.filter.date.substring(0, 4)
                const filterMonth = this.filter.date.substring(5, 7)

                // Filter games based on matching year and month
                filteredGames = filteredGames.filter(game => {
                    const gameDate = new Date(game.date)
                    const gameYear = gameDate.getFullYear()
                    const gameMonth = (gameDate.getMonth() + 1).toString().padStart(2, '0')
                    
                    return gameYear === parseInt(filterYear) && gameMonth === filterMonth
                })
            }
            if (this.filter.price != null && typeof this.filter.price == 'number') {
                filteredGames = filteredGames.filter(game => game.price <= this.filter.price)
            }
            this.shownGames = filteredGames
        },
        resetFilters() {
            this.shownGames = this.games
            Object.keys(this.filter).forEach(key => {
                this.filter[key] = null})
        }
    }
}
</script>
