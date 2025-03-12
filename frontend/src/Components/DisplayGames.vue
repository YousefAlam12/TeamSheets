<template>
    <div v-if="isEmpty" class="card mt-3 d-flex justify-content-between align-items-center">
        No games found...
    </div>

    <div v-else class="card mt-3" v-for="game in games">
        <div class="card-header d-flex justify-content-between align-items-center">
            <div>
                {{ game.date }}
                <span v-if="game.fulltime" class="badge bg-warning">Fulltime</span>
                <span v-if="isPlaying(game)" class="badge bg-success">Playing</span>
            </div>

            <span class="badge bg-primary btn btn-primary">
                {{ game.is_private ? 'Private' : 'Public' }}  
            </span>
        </div>
        <div class="card-body">
            <!-- <router-link class="nav-link" :to="{ name: 'GameDetails', params: {id: game.id, game: game} }"> -->
            <router-link class="nav-link" :to="{ name: 'GameDetails', params: { id: game.id } }">
                <h5 class="card-title">{{ game.name }} <span class="badge bg-primary">{{ game.players.length }}/{{
                        game.totalPlayers }}</span></h5>
                <ul class="list-group list-group-flush">
                    <li class="list-group-item">{{ game.start_time }} - {{ game.end_time }}</li>
                    <li class="list-group-item">£{{ game.price }}</li>
                    <li class="list-group-item">Pitch: {{ game.address }} {{ game.postcode }}</li>
                </ul>
            </router-link>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        games: {
            type: Array,
            required: true
        },
        user_id: {}
    },
    computed: {
        isEmpty() {
            if (this.games) {
                return this.games.length <= 0
            }
        },
        
    },
    data() {
        return {
        }
    },
    async mounted() {

    },
    methods: {
        isPlaying(game) {
            if (this.user_id) {
                return game.players.find(player => player.id == this.user_id)
            }
        }
    }
}
</script>
