<template>
    <div class="container pt-3">
        <div class="h1 text-center border rounded bg-light p-2 mb-3">
            Games
        </div>
        <div>
            <div class="alert alert-danger mt-3" role="alert" v-if="errorMessage">
                {{ errorMessage }}
            </div>
            <div class="alert alert-success mt-3" role="alert" v-if="successMessage">
                {{ successMessage }}
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
            <DisplayGames :games="shownGames" :user_id="store.user.id"/>
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
                            <div class="input-group">
                                <input v-model="newGame.name" type="text" class="form-control" id="name">
                                <span class="input-group-text"><i class="bi bi-exclamation-circle"></i></span>
                            </div>
                        </div>

                        <div class="mb-3">
                            <label for="date" class="form-label">Date</label>
                            <div class="input-group">
                                <input v-model="newGame.date" type="date" class="form-control" id="date">
                                <span class="input-group-text"><i class="bi bi-exclamation-circle"></i></span>
                            </div>
                        </div>

                        <div class="mb-3">
                            <label for="start-time" class="form-label">Start Time</label>
                            <div class="input-group">
                                <input v-model="newGame.start_time" type="time" class="form-control" id="start-time">
                                <span class="input-group-text"><i class="bi bi-exclamation-circle"></i></span>
                            </div>
                        </div>

                        <div class="mb-3">
                            <label for="end-time" class="form-label">End Time</label>
                            <div class="input-group">
                                <input v-model="newGame.end_time" type="time" class="form-control" id="end-time">
                                <span class="input-group-text"><i class="bi bi-exclamation-circle"></i></span>
                            </div>
                        </div>

                        <div class="mb-3">
                            <label for="description" class="form-label">Description</label>
                            <textarea v-model="newGame.description" name="description" id="description" class="form-control"></textarea>
                        </div>

                        <div class="mb-3">
                            <label for="total-players" class="form-label">Total Players</label> <i class="bi bi-info-circle" data-toggle="tooltip" data-placement="top" title="Must be even and between 10-22 (11-5 aside)"></i>
                            <div class="input-group">
                                <input v-model="newGame.totalPlayers" type="number" class="form-control" id="total-players" min="10" max="22">
                                <span class="input-group-text"><i class="bi bi-exclamation-circle"></i></span>
                            </div>
                        </div>

                        <div class="mb-3">
                            <label for="price" class="form-label">Price</label>
                            <div class="input-group">
                                <input v-model="newGame.price" type="number" class="form-control" id="price" min="0">
                                <span class="input-group-text"><i class="bi bi-exclamation-circle"></i></span>
                            </div>
                        </div>

                        <div class="mb-3">
                            <label for="address" class="form-label">Pitch Address</label>
                            <div class="input-group">
                                <input v-model="newGame.address" type="text" class="form-control" id="address">
                                <span class="input-group-text"><i class="bi bi-exclamation-circle"></i></span>
                            </div>
                        </div>

                        <div class="mb-3">
                            <label for="postcode" class="form-label">Postcode</label>
                            <div class="input-group">
                                <input v-model="newGame.postcode" type="text" class="form-control" id="postcode">
                                <span class="input-group-text"><i class="bi bi-exclamation-circle"></i></span>
                            </div>
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
                            <input v-model="filter.date" type="date" class="form-control" id="filter-date">
                        </div>

                        <div class="mb-3">
                            <label for="price" class="form-label">Price</label>
                            <input v-model="filter.price" type="number" class="form-control" id="filter-price" min="0">
                            <small id="priceInfo" class="form-text text-muted">All games upto selected price</small>
                        </div>

                        <div class="mb-3">
                            <label for="filter-address" class="form-label">Address</label>
                            <input v-model="filter.address" type="search" class="form-control" id="filter-address">
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
import { useUserStore } from '../stores/user';

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
            successMessage : '',
            shownGames : [],
            filter : {
                date: null,
                price: null,
                address: null,
            },
            store: useUserStore()
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
                this.successMessage = `${this.newGame.name} was successfully created`
                this.resetNewGame()
                this.games = data.games
                this.shownGames = data.games
            }
            else {
                this.errorMessage = data.error
                this.successMessage = ''
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
                filteredGames = filteredGames.filter(game => game.date == this.filter.date)
            }
            if (this.filter.price != null && typeof this.filter.price == 'number') {
                filteredGames = filteredGames.filter(game => game.price <= this.filter.price)
            }
            if (this.filter.address != null) {
                filteredGames = filteredGames.filter(game => {
                    return (game.address+game.postcode).toLowerCase().includes(this.filter.address)
                })
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
