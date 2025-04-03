<template>
    <div class="container d-flex justify-content-center align-items-center">
        <div class="card shadow" style="max-width: 600px; width: 100%; margin-top: 35%;">
            <div class="card-body">
                <h2 class="card-title text-center mb-4">Login</h2>
                <form @submit.prevent="login">
                    <div class="mb-3">
                        <label for="username" class="form-label">Username</label>
                        <input v-model="username" type="text" class="form-control" id="username" required />
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label">Password</label>
                        <input v-model="password" type="password" class="form-control" id="password" required />
                    </div>
                    <div class="d-grid">
                        <button type="submit" class="btn btn-primary">Login</button>
                        <a href="/signup" class="btn btn-secondary mt-2">Signup</a>
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
            username: '',
            password: '',
            errorMessage: ''
        }
    },
    async mounted() {
    },
    methods: {
        async login()
        {
            const response = await fetch('http://localhost:8000/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({
                    'username' : this.username,
                    'password' : this.password
                }) 
            })
            
            const data = await response.json()
            if (response.ok) {
                // const data = await response.json()
                console.log(data)
                this.$router.push('/')
            }
            else {
                // this.errorMessage = 'Invalid Details'
                // const data = await response.json()
                this.errorMessage = data.error
            }
        }
    }
}
</script>

<style>
</style>