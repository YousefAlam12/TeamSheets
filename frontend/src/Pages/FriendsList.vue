<template>
    <div v-if="user" class="container pt-3">
        <div class="h1 text-center border rounded bg-light p-2 mb-3">
            Friends List
        </div>

        <div v-if="user.received_requests.length > 0" class="card mb-4">
            <div class="card-header bg-dark text-white">
                Received Friend Requests
            </div>
            <ul class="list-group list-group-flush">
                <li v-for="user in user.received_requests"
                    class="list-group-item d-flex justify-content-between align-items-center p-3">
                    <span>{{ user.username }}</span>
                    <div>
                        <button class="btn btn-success btn-sm me-2" @click="handleFriendRequest(user, true)">
                            Accept
                        </button>
                        <button class="btn btn-danger btn-sm" @click="handleFriendRequest(user, false)">
                            Reject
                        </button>
                    </div>
                </li>
            </ul>
        </div>

        <div class="card">
            <div class="d-flex card-header bg-warning text-white justify-content-between p-3">
                <label class="align-content-center">Friends</label>
                <button class="btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#requestModal">Send
                    Request</button>
            </div>
            <ul class="list-group list-group-flush">
                <li v-for="user in user.friends" class="list-group-item">
                    <div>
                        <span>{{ user.username }}</span>
                        <small class="form-text text-muted">
                            <div v-if="user.stats" class="d-flex flex-row bd-highlight">
                                <div class="pe-2 bd-highlight">atk: {{ user.stats.attack }}</div>
                                <div class="pe-2 bd-highlight">def: {{ user.stats.defence }}</div>
                                <div class="pe-2 bd-highlight">str: {{ user.stats.strength }}</div>
                                <div class="pe-2 bd-highlight">spd: {{ user.stats.speed }}</div>
                                <div class="pe-2 bd-highlight">teq: {{ user.stats.technique }}</div>
                            </div>
                            <div v-else class="d-flex flex-row bd-highlight">
                                <div class="pe-2 bd-highlight">New Player</div>
                            </div>
                        </small>
                    </div>
                </li>
                <li v-if="user.friends.length === 0" class="list-group-item text-center text-muted">
                    No friends added yet.
                </li>
            </ul>
        </div>

        <!-- Sending Friend Request Modal -->
        <div class="modal fade" id="requestModal" tabindex="-1" aria-labelledby="requestModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="requestModalLabel">Send Friend Request</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body user-list">
                        <div class="mb-3">
                            <input v-model="userSearch" class="form-control mb-3" type="search"
                                placeholder="Search Users" for="userSearch">
                            <ul class="overflow-auto list-group">
                                <li v-for="u in filteredUserList"
                                    class="d-flex list-group-item justify-content-between p-3">
                                    <label class="align-content-center">{{ u.username }}</label>
                                    <div>
                                        <label v-if="user.sent_requests.some(request => request.id === u.id)"
                                            class="btn btn-warning">Sent</label>
                                        <label v-else-if="user.friends.some(friend => friend.id === u.id)"
                                            class="btn btn-primary">Friends</label>
                                        <label
                                            v-else-if="user.received_requests.some(request => request.id === u.id)"
                                            class="btn btn-warning">Received</label>
                                        <button v-else type="button" class="btn btn-success"
                                            @click="sendFriendRequest(u)">Send</button>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>

                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="">Close</button>
                        <!-- <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="">Apply Filters</button> -->
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { store } from '../store.js';

export default {
    data() {
        return {
            user: null,
            userList: null,
            userSearch: ''
        }
    },
    computed: {
        // Filters the user list based on the search input
        filteredUserList() {
            return this.userList.filter(user => {
                return user.username.toLowerCase().includes(this.userSearch.toLowerCase());
            });
        }
    },
    async mounted() {
        const response = await fetch('http://localhost:8000/friends', {
            credentials: 'include'
        })
        const data = await response.json()
        // this.user = data.user
        this.user = store.user
        this.userList = data.userList
    },
    methods: {
        // accepts request and adds user to friends
        async handleFriendRequest(requestUser, accept) {
            const response = await fetch('http://localhost:8000/friends', {
                method: (accept ? 'POST' : 'DELETE'),
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ 'from_user': requestUser.id })
            })
            if (response.ok) {
                const data = await response.json()
                // this.user = data.user
                Object.assign(store.user, data.user)
            }
        },
        // send friend request to a user in the userlist
        async sendFriendRequest(user) {
            const response = await fetch(`http://localhost:8000/send_friend_request`, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'to_user': user.id
                })
            })
            if (response.ok) {
                const data = await response.json()
                // this.user = data.user
                // store.user = data.user
                Object.assign(store.user, data.user)
            }
        },
    }
}
</script>

<style scoped>
.user-list {
    max-height: 500px;
    overflow-y: auto;
}
</style>