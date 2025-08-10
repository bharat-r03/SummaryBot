import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { vueAxios } from '@baloise/vue-axios'
import axios from 'axios'

const app = createApp(App)
app.use(vueAxios, axios).mount("#app")