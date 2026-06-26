import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import CoursesView from '../views/CoursesView.vue'
import CourseDetailView from '../views/CourseDetailView.vue'
import ProfileView from '../views/ProfileView.vue'

const routes = [
  {
    path: '/',
    component: HomeView
  },
  {
    path: '/courses',
    component: CoursesView
  },
  {
    path: '/courses/:id',
    component: CourseDetailView
  },
  {
    path: '/profile',
    component: ProfileView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  console.log('Navigating to:', to.path)
  next()
})

export default router