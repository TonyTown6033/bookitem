import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/rooms',
    name: 'Rooms',
    component: () => import('../views/Rooms.vue')
  },
  {
    path: '/bookings',
    name: 'Bookings',
    component: () => import('../views/Bookings.vue')
  },
  {
    path: '/users',
    name: 'Users',
    component: () => import('../views/Users.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

