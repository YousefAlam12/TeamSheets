<template>
    <div v-if="isEmpty" class="card mt-3 d-flex justify-content-between align-items-center">
        No games found...
    </div>

    <div v-else class="card mt-3 mb-3 hover-effect" v-for="game in games">
        <router-link class="nav-link" :to="{ name: 'GameDetails', params: { id: game.id } }">
            <div class="card-header d-flex justify-content-between align-items-center">
                <div>
                    {{ game.date }}
                    <span v-if="game.fulltime" class="badge bg-warning">Fulltime</span>
                    <span v-if="isFinished(game)" class="badge bg-danger"> Call Fulltime</span>
                    <span v-if="isPlaying(game)" class="badge bg-success">Playing</span>
                </div>

                <span class="badge bg-primary btn btn-primary">
                    {{ game.is_private ? 'Private' : 'Public' }}  
                </span>
            </div>
            <div class="card-body">
                    <h5 class="card-title">{{ game.name }} <span class="badge bg-primary">{{ game.players.length }}/{{
                            game.totalPlayers }}</span></h5>
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item">{{ game.start_time }} - {{ game.end_time }}</li>
                        <li class="list-group-item">£{{ game.price }}</li>
                        <li class="list-group-item">Pitch: {{ game.address }} {{ game.postcode }}</li>
                    </ul>
            </div>
        </router-link>
    </div>
</template>

<script>
export default {
    props: {
        games: {
            type: Array,
        },
        user_id: {}
    },
    computed: {
        isEmpty() {
            if (this.games == null) {
                return true
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
        },
        isFinished(game) {
            if (!game.fulltime) {
                const now = new Date()
                const game_date = new Date(`${game.end_date}T${game.end_time}`)
                return game_date < now   
            }
        }
    }
}
</script>

<style>
.hover-effect:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    transform: scale(1.02);
    transition: all 0.3s ease-in-out;
}
</style>