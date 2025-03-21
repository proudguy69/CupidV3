import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Signup from '@/views/signup.vue'
import Swipe from '@/views/Swipe.vue'
import Matches from '@/views/Matches.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/signup',
      name: 'signup',
      component: Signup
    },
    {
      path: '/swipe',
      name: 'swipe',
      component: Swipe
    },
    {
      path: '/matches',
      name: 'matches',
      component: Matches
    },
  ]
})

export default router
