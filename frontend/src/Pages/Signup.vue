<template>
    <div class="container d-flex justify-content-center align-items-center">
        <div class="card shadow" style="max-width: 600px; width: 100%; margin-top: 10%;">
            <div class="card-body">
                <h2 class="card-title text-center mb-4">Signup</h2>
                <form @submit.prevent="createAccount">

                    <div class="mb-3">
                        <label for="firstname" class="form-label">First Name</label>
                        <input v-model="firstname" type="text" class="form-control" id="firstname" required />
                    </div>

                    <div class="mb-3">
                        <label for="lastname" class="form-label">Last Name</label>
                        <input v-model="lastname" type="text" class="form-control" id="lastname" required />
                    </div>

                    <div class="mb-3">
                        <label for="email" class="form-label">Email</label>
                        <input v-model="email" type="email" class="form-control" id="email" required />
                    </div>

                    <div class="mb-3">
                        <label for="dob" class="form-label">Date of Birth</label>
                        <input v-model="dob" type="date" class="form-control" id="dob" required />
                    </div>

                    <div class="mb-3">
                        <label for="username" class="form-label">Username</label>
                        <input v-model="username" type="text" class="form-control" id="username" required />
                    </div>

                    <div class="mb-3">
                        <label for="password1" class="form-label">Password</label>
                        <input v-model="password1" type="password" class="form-control" id="password1" required />
                        <small id="passwordInfo" class="form-text text-muted">Must be at least 8 characters and not a common password.</small>
                    </div>

                    <div class="mb-3">
                        <label for="password2" class="form-label">Confirm Password</label>
                        <input v-model="password2" type="password" class="form-control" id="password2" required />
                    </div>

                    <div class="d-grid">
                        <button type="submit" class="btn btn-primary">Create</button>
                    </div>
                </form>

                <p v-if="errorMessage" class="alert alert-danger mt-3" role="alert">{{ errorMessage }}</p>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            firstname: '',
            lastname: '',
            email: '',
            dob: '',
            username: '',
            password1: '',
            password2: '',
            errorMessage: ''
        }
    },
    async mounted() {
    },
    methods: {
        async createAccount() {
            const response = await fetch('http://localhost:8000/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({
                    'firstname' : this.firstname,
                    'lastname' : this.lastname,
                    'email' : this.email,
                    'dob' : this.dob,
                    'username' : this.username,
                    'password1' : this.password1,
                    'password2' : this.password2,
                }) 
            })

            const data = await response.json()
            if (response.ok) {
                console.log(data)
                this.$router.push('/')
            }
            else {
                this.errorMessage = data.error
            }
        }
    }
}
</script>

<style>
</style>