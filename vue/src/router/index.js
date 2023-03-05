import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/TryLogin.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/TryRegister.vue')
    },
    {
      path: '/create',
      name: 'create',
      component: () => import('../views/Create.vue')
    },
    {
      path: '/post/:post_id',
      name: 'post',
      component: () => import('../views/Post.vue')
    },
    {
      path: '/update/:post_id',
      name: 'update',
      component: () => import('../views/Update.vue')
    }
  ]
})

export default router
