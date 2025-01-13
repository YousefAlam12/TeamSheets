import { createRouter, createWebHistory } from 'vue-router'

import Login from '../Pages/Login.vue'
import Main from '../Pages/Main.vue'
import Games from '../Pages/Games.vue'
import Signup from '../Pages/Signup.vue'
import Logout from '../Pages/Logout.vue'

// let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''

// Defining routes
const router = createRouter({
    history: createWebHistory(),
    routes: [
        {path: '/login', name: 'Login', component: Login},
        {path: '/logout', name: 'Logout', component: Logout, meta: {auth: true}},
        {path: '/signup', name: 'Signup', component: Signup},
        {path: '/', name: 'Main', component: Main, meta: {auth: true}},
        {path: '/games', name: 'Games', component: Games, meta: {auth: true}},

        // catches invalid paths
        { path: '/:catchAll(.*)', redirect: '/' }
    ]
})

router.beforeEach(async (to, from, next) => {
    // const isAuthenticated = false
    const response = await fetch('http://localhost:8000/isAuthenticated', {
        credentials: 'include'
    })
    const data = await response.json()
    console.log(data.isAuth)

    if (to.meta.auth && !data.isAuth) {
        next({name: 'Login'})
    }
    else if ((to.name == 'Login' || to.name == 'Signup') && data.isAuth) {
        next({name: 'Main'})
    }
    else {
        next()
    }
})

export default router