import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Login from '../views/Login.vue'

const routes = [
  {
    path: '/dashboard',
    name: 'user-dashboard',
    component: Dashboard
  }, 
  {
    path: '/', // Add a new route for the Login page
    name: 'login',
    component: Login
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router