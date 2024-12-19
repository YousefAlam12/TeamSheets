import { createRouter, createWebHistory } from 'vue-router'

import Login from '../Pages/Login.vue'
import Main from '../Pages/Main.vue'
import Test from '../Pages/Test.vue'

// let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''

// Defining routes
const router = createRouter({
    history: createWebHistory(),
    routes: [
        {path: '/login', name: 'Login', component: Login},
        {path: '/', name: 'Main', component: Main, meta: {auth: true}},
        {path: '/test', name: 'Test', component: Test, meta: {auth: true}},
    ]
})

router.beforeEach((to, from, next) => {
    const isAuthenticated = true

    if (to.meta.auth && !isAuthenticated) {
        next({name: 'Login'})
    }
    else if (to.name == 'Login' && isAuthenticated) {
        next({name: 'Main'})
    }
    else {
        next()
    }
})

export default router