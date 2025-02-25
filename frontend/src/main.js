import { createApp } from 'vue'
import App from './App.vue'
import router from './router';

import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";

// createApp(App).mount('#app')

const app = createApp(App)

app.config.globalProperties.$store = {user: null}

app.use(router)
app.mount('#app')