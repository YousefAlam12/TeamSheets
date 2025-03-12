<template>
    <!-- Filter Modal -->
    <div class="modal fade" id="PlayerModal" tabindex="-1" aria-labelledby="PlayerModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div v-if="player" class="modal-content">
                <div class="modal-header">
                    <!-- <h5 class="modal-title" id="PlayerModalLabel">{{ player ? player.username : '' }}</h5> -->
                    <h5 class="modal-title" id="PlayerModalLabel">{{ player.username }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">

                    <div class="mb-3">
                        <!-- <label v-if="player">{{ player.stats ? player.stats  : 'New player' }}</label> -->
                        <!-- <label>{{ player.stats ? player.stats : 'New player' }}</label> -->
                    </div>

                </div>

                <div v-if="player.id != user.id" class="d-flex justify-content-between p-2">
                    <!-- friend request labels/buttons -->
                    <label v-if="user.sent_requests.some(request => request.id === player.id)"
                        class="btn btn-warning">Sent Friend Request</label>
                    <label v-else-if="user.friends.some(friend => friend.id === player.id)" class="btn btn-primary">Friends</label>
                    <label v-else-if="user.received_requests.some(request => request.id === player.id)"
                        class="btn btn-warning">Received Request</label>
                    <button v-else type="button" class="btn btn-success" data-bs-dismiss="modal"
                        @click="$emit('sendFriendRequest', player)">Send Friend Request</button>

                    <button v-if="isAdmin && !isFulltime" type="button" class="btn btn-danger" data-bs-dismiss="modal" @click="$emit('kickPlayer', player)">Kick
                        Player</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    emits: ['sendFriendRequest', 'kickPlayer'],
    props: {
        player: {},
        user: {
            required: true
        },
        isFulltime: {

        },
        isAdmin: {
            required: true
        },
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