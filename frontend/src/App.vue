<template>
    <main class="container pt-4">
        <nav v-if="!hideNavbar && store.user" class="navbar navbar-expand-lg navbar-light bg-light rounded"
            :class="{ 'expanded-navbar': isExpanded }">
            <div class="container-fluid">
                <router-link class="navbar-brand" :to="{ name: 'Main' }">TeamSheets</router-link>
                <!-- Navbar toggle button for mobile -->
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                    aria-controls="navbarNav" :aria-expanded="isExpanded.toString()" aria-label="Toggle navigation"
                    @click="toggleNavbar">
                    <span class="navbar-toggler-icon"></span>
                </button>

                <!-- Navbar links that collapse on smaller screens -->
                <div class="collapse navbar-collapse" id="navbarNav">
                    <div class="navbar-nav">
                        <router-link 
                        class="nav-link"
                        :class="{ 'text-warning': store.user.game_invites != null && store.user.game_invites.length > 0}"
                        exact-active-class="active" :to="{ name: 'Main' }">
                            Home
                        </router-link>
                        
                        <router-link class="nav-link" exact-active-class="active" :to="{ name: 'Games' }">
                            Games
                        </router-link>

                        <router-link
                            :class="{ 'nav-link': true, 'text-warning': store.user.received_requests != null && store.user.received_requests.length > 0}"
                            exact-active-class="active" :to="{ name: 'FriendsList' }">
                            Friends List
                        </router-link>

                        <router-link class="nav-link" exact-active-class="active" :to="{ name: 'Profile' }">
                            Profile
                        </router-link>

                        <router-link class="nav-link" exact-active-class="active" :to="{ name: 'Logout' }">
                            Logout
                        </router-link>
                    </div>
                </div>
            </div>
        </nav>

        <RouterView class="flex-shrink-0" />
    </main>
</template>

<script>
import { useUserStore } from "./stores/user";

export default {
    data() {
        return {
            response_data: '',
            isExpanded: false,
            store: useUserStore(),
        }
    },
    computed: {
        hideNavbar() {
            return this.$route.name == 'Login' || this.$route.name == 'Signup'
        },

    },
    async mounted() {

    },
    methods: {
        toggleNavbar() {
            this.isExpanded = !this.isExpanded
        },
    }
}
</script>

<style scoped>
@media (max-width: 991px) {
    .bg-light {
        background: none !important;
    }

    .expanded-navbar {
        background-color: rgba(var(--bs-light-rgb), var(--bs-bg-opacity)) !important;
    }
}

.mr-auto {
    margin-right: auto !important
}

.form-inline {
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-orient: horizontal;
    -webkit-box-direction: normal;
    -ms-flex-flow: row wrap;
    flex-flow: row wrap;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
}

.nav-link.active {
    font-weight: bold;
    border-bottom: solid blue;
}

@media (min-width: 1600px) {
    .container {
        max-width: 1520px;
    }
}

@media (min-width: 1800px) {
    .container {
        max-width: 1700px;
    }
}
@media (min-width: 2000px) {
    .container {
        max-width: 2000px;
    }
}
@media (min-width: 2500px) {
    .container {
        max-width: 2500px;
    }
}
</style>
