import Vue from 'vue'
import VueRouter from 'vue-router'

import HomePage from '../pages/home/Page.vue'
import Home from '../pages/home/Home.vue'
import Room from '../pages/home/Room.vue'

import LoginPage from '../pages/login/Page.vue'
import Login from '../pages/login/Login.vue'

import Page404 from '../pages/404.vue'

Vue.use(VueRouter)

const routes = [
  { path: '', redirect: '/home' },
  {
    path: '/home',
    component: HomePage,
    children: [
      {
        path: '',
        name: 'home',
        component: Home,
      },
      {
        path: '/room',
        name: 'room',
        component: Room,
        props: true,
      }
    ],
  },
  {
    path: '/login',
    component: LoginPage,
    children: [
      {
        path: '',
        name: 'login',
        component: Login,
      },
    ]
  },
  {
    path: '*',
    name: '404',
    component: Page404
  },
]

const router = new VueRouter({
  routes
})

export default router
