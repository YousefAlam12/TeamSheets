<template>
    <div class="container pt-3">
        <div class="h1 text-center border rounded bg-light p-2 mb-3">
            Profile
        </div>

        <div v-if="user" class="container d-flex justify-content-center align-items-center mt-5 mb-5">
            <div class="card shadow" style="max-width: 600px; width: 100%;">
                <div class="card-body">
                    <h2 class="card-title text-center mb-4">{{ user.username }}</h2>
                    <div class="mb-3">
                        <h5 class="text-center">Player Stats:</h5>
                        <StatsChart v-if="user.stats" :stats="user.stats" />
                        <div v-else class="text-center p-2">
                            <p>New Player</p>
                            <p>Play in some games and get rated to increase your stats!</p>
                        </div>
                    </div>
                    <div class="d-flex justify-content-between">
                        <button class="btn btn-warning" data-bs-toggle="modal" data-bs-target="#editModal">Edit Profile</button>
                        <button class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#passwordModal">Change Password</button>
                    </div>
                    <p v-if="errorMessage" class="alert alert-danger mt-3" role="alert">{{ errorMessage }}</p>
                    <p v-if="successMessage" class="alert alert-success mt-3" role="alert">{{ successMessage }}</p>
                </div>
            </div>
        </div>

        <div class="modal fade" id="editModal" tabindex="-1" aria-labelledby="editModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="editModalLabel">Edit Profile</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <form @submit.prevent="editProfile">
                        <div class="modal-body">
                            <div class="mb-3">
                                <label class="form-label">Email</label>
                                <input v-model="email" type="email" class="form-control" id="email">
                            </div>

                            <div class="mb-3">
                                <label class="form-label">Postcode</label>
                                <input v-model="postcode" type="text" class="form-control" id="postcode">
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button type="submit" class="btn btn-primary" @click="editUser" data-bs-dismiss="modal">Save changes</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <div class="modal fade" id="passwordModal" tabindex="-1" aria-labelledby="passwordModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="passwordModalLabel">Change Password</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label for="oldPassword" class="form-label">Old Password</label>
                            <input v-model="password.old" type="password" class="form-control" id="oldPassword">
                        </div>
                        <div class="mb-3">
                            <label for="newPassword" class="form-label">New Password</label>
                            <input v-model="password.new" type="password" class="form-control" id="newPassword">
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary" @click="editPassword" data-bs-dismiss="modal">Save changes</button>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<script>
import StatsChart from '../Components/StatsChart.vue';
import { useUserStore } from '../stores/user';

export default {
    components: {
        StatsChart
    },
    computed: {

    },
    data() {
        return {
            user: null,
            email: null,
            postcode: null,
            longitude: null,
            latitude: null,
            password: {
                old: '',
                new: ''
            },
            errorMessage: '',
            successMessage: ''
        }
    },
    async mounted() {
        const response = await fetch('http://localhost:8000/profile', {
            credentials: 'include'
        })
        const data = await response.json()
        console.log(data)
        useUserStore().saveUser(data.user)
        this.user = useUserStore().user
        this.email = data.email
        this.postcode = data.postcode
    },
    methods: {
        async editProfile() {
            await this.findGeo(this.postcode)
            if (!this.longitude || !this.latitude) {
                this.errorMessage = "Invalid Postcode."
                this.successMessage = ''
                return
            }

            const response = await fetch('http://localhost:8000/profile', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({
                    'email' : this.email,
                    'postcode' : this.postcode,
                    'longitude' : this.longitude,
                    'latitude' : this.latitude
                }) 
            })

            const data = await response.json()
            if (response.ok) {
                useUserStore().saveUser(data.user)
                this.email = data.email
                this.postcode = data.postcode
                this.errorMessage = ''
                this.successMessage = "Profile change successful"
            }
            else {
                this.errorMessage = data.error
                this.successMessage = ''
            }
        },
        async findGeo(postcode) {
            console.log(postcode)
            const response = await fetch(`https://api.postcodes.io/postcodes/${postcode}`)
            const data = await response.json()
            if (response.ok) {
                this.longitude = data.result.longitude
                this.latitude = data.result.latitude
            }
            else {
                this.longitude = null
                this.latitude = null
            }
        },
        async editPassword() {
            const response = await fetch('http://localhost:8000/password', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({
                    'old': this.password.old,
                    'new': this.password.new
                })
            })
            const data = await response.json()
            if (response.ok) {
                this.password.old = ''
                this.password.new = ''
                this.errorMessage = ""
                this.successMessage = "Password change successfully"
            }
            else {
                this.errorMessage = "Invalid Details"
                this.successMessage = ''
            }
        }
    }
}
</script>
