<template>
    <!-- <div class="container pt-3">
        <div class="h1 text-center border rounded bg-light p-2 mb-3">
            API Client
        </div>
    </div> -->
    <main class="container pt-4">
        <RouterView class="flex-shrink-0"/>
    </main>
  </template>
  
<script>

export default {
    data() {
        return {
            response_data: '',
        }
    },
    async mounted() {
        
    }
}
</script>
