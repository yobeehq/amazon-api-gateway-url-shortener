import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import moment from 'moment'
import './assets/main.css'

const app = createApp(App)

// filters
app.config.globalProperties.$filters = {
  formatDate(value) {
    return moment(value, 'DD/MMM/YYYY:HH:mm:ss Z').format("YYYY-MM-DD HH:mm:ss A")
  }
}

app.use(router).use(store).mount('#app')