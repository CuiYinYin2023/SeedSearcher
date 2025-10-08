import { createWebHistory, createRouter } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/home/home.vue')
  },
  {
    path: '/weather-forecast',
    name: 'WeatherForecast',
    component: () => import('../views/weather-forecast/weather-forecast.vue')
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router