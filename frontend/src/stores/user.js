import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
    state: () => ({
        user: {}
    }),
    getters: {

    },
    actions: {
        saveUser(user) {
            this.user = user
        }
    }
})