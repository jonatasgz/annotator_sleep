import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import router from './router/index.js'
import "bootstrap/dist/css/bootstrap.min.css"
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

axios.defaults.baseURL = import.meta.env.VITE_APP_API_URL;

createApp(App).use(router).mount('#app')
