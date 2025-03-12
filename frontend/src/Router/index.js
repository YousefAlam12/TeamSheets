import { createRouter, createWebHistory } from 'vue-router'

import Login from '../Pages/Login.vue'
import Main from '../Pages/Main.vue'
import Games from '../Pages/Games.vue'
import Signup from '../Pages/Signup.vue'
import Logout from '../Pages/Logout.vue'
import GameDetails from '../Pages/GameDetails.vue'
import FriendsList from '../Pages/FriendsList.vue'
import { useUserStore } from '../stores/user'
import Profile from '../Pages/Profile.vue'

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
        {path: '/friendsList', name: 'FriendsList', component: FriendsList, meta: {auth: true}},
        {path: '/profile', name: 'Profile', component: Profile, meta: {auth: true}},


        {
            // path: '/gameDetails/:id', name: 'GameDetails', component: GameDetails, meta: {auth: true}, props: true,
            path: '/gameDetails/:id', name: 'GameDetails', component: GameDetails, meta: {auth: true},
            // check if game exists before going to page
            beforeEnter: async (to, from, next) => {
                const response = await fetch('http://localhost:8000/allGames', {
                    credentials: 'include'
                })
                const user = useUserStore().user
                const data = await response.json()
                const gameExists = await data.games.find(game => game.id == to.params.id)

                // prevent access to game that does not exist
                if (gameExists) {
                    // prevents access to private game if not a player/invited
                    if (gameExists.is_private && gameExists.admin.id != user.id) {
                        if (!user.game_invites.some(invite => invite.game_id === gameExists.id) && !gameExists.players.some(player => player.id == user.id)) {
                            next({name: 'Main'})
                        }
                        else {
                            next()
                        }
                    }
                    else {
                        next()
                    }
                }
                else {
                    next({name: 'Main'})
                }
            }
        },

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