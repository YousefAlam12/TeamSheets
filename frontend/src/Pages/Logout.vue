<template></template>

<script>
import { useUserStore } from '../stores/user.js';

export default {
    data() {
        return {
            response_data: '',
        }
    },
    async beforeMount() {
        const response = await fetch(`http://localhost:8000/logout`, {
            method: 'GET',
            credentials: 'include',
        })

        const data = await response.json()
        console.log(data)
        useUserStore().user = null
        this.$router.push('/')
    },
    methods: {
    }
}
</script>
