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
                        <router-link class="nav-link" exact-active-class="active" :to="{ name: 'Main' }">
                            Home
                        </router-link>

                        <router-link class="nav-link" exact-active-class="active" :to="{ name: 'Games' }">
                            Games
                        </router-link>

                        <router-link class="nav-link" exact-active-class="active" :to="{ name: 'Logout' }">
                            Logout
                        </router-link>
                    </div>
                </div>
            </div>
        </nav>
        <!-- <nav class="navbar navbar-expand-lg navbar-light bg-light p-2">
            <a class="navbar-brand" href="#">Navbar</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
                aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav mr-auto">
                    <li class="nav-item active">
                        <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Link</a>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button"
                            data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            Dropdown
                        </a>
                        <div class="dropdown-menu" aria-labelledby="navbarDropdown">
                            <a class="dropdown-item" href="#">Action</a>
                            <a class="dropdown-item" href="#">Another action</a>
                            <div class="dropdown-divider"></div>
                            <a class="dropdown-item" href="#">Something else here</a>
                        </div>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link disabled" href="#">Disabled</a>
                    </li>
                </ul>
                <form class="form-inline my-2 my-lg-0">
                    <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
                    <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
                </form>
            </div>
        </nav> -->
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
</style>
