<template>
    <main class="container pt-4">
        <nav v-if="!hideNavbar" class="navbar navbar-expand-lg navbar-light bg-light rounded" :class="{'expanded-navbar': isExpanded}">
            <div class="container-fluid">
                <!-- Navbar toggle button for mobile -->
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                    aria-controls="navbarNav" :aria-expanded="isExpanded.toString()" aria-label="Toggle navigation" @click="toggleNavbar">
                    <span class="navbar-toggler-icon"></span>
                </button>

                <!-- Navbar links that collapse on smaller screens -->
                <div class="collapse navbar-collapse" id="navbarNav">
                    <div class="navbar-nav">
                        <router-link class="nav-link" :to="{ name: 'Main' }">
                            Main Page
                        </router-link>

                        <router-link class="nav-link" :to="{ name: 'Test' }">
                            Test Page
                        </router-link>

                        <router-link class="nav-link" :to="{ name: 'Logout' }">
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
export default {
    data() {
        return {
            response_data: '',
            isExpanded: false,
        }
    },
    computed: {
        hideNavbar() {
            return this.$route.name == 'Login' || this.$route.name == 'Signup'
        }
    },
    methods: {
        toggleNavbar() {
            this.isExpanded = !this.isExpanded
        }
    }
}
</script>

<style scoped>
@media (max-width: 991px) {
    .bg-light {
        background: none !important;
    }

    .expanded-navbar {
        background-color: rgba(var(--bs-light-rgb),var(--bs-bg-opacity))!important;
    }
}
</style>
