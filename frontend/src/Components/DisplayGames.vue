<template>
    <div class="card mt-3" v-for="game in games">
        <div class="card-header">
            {{ game.date }}
            <span v-if="game.fulltime" class="badge bg-warning">Fulltime</span>
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
        }
    },
    data() {
        return {
        }
    },
    async mounted() {

    },
    methods: {
    }
}
</script>
