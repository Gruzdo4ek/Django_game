import { createRouter, createWebHistory } from 'vue-router';
import GameView from '../views/GameView.vue';
import DeveloperView from '../views/DeveloperView.vue';
import GenreView from '@/views/GenreView.vue';
import CountryDeveloperView from '@/views/CountryDeveloperView.vue';
import PlatformView from '@/views/PlatformView.vue';


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path:"/",
      name: "GameView",
      component: GameView,
    },
    {
      path:"/developer",
      name: "DeveloperView",
      component: DeveloperView,
    },
    {
      path:"/genre",
      name: "GenreView",
      component: GenreView,
    },
    {
      path:"/platform",
      name: "PlatformView",
      component: PlatformView,
    },
    {
      path:"/country_developer",
      name: "CountryDeveloperView",
      component: CountryDeveloperView,
    }
  ]
})

export default router
