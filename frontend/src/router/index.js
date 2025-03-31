import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Dashboard from '../views/Dashboard.vue'
import Tasks from '../views/Tasks.vue'
import Groups from '../views/Groups.vue'
import Events from '../views/Events.vue'
import AskForHelp from '../views/AskForHelp.vue'
import ChatBox from '../views/ChatBox.vue'
import Donations from '../views/Donations.vue'
import CreateGroup from '../views/CreateGroup.vue'
import CreateEvent from '../views/CreateEvent.vue'
import HelpRequestDetail from '../views/HelpRequestDetail.vue'
import Notifications from '../components/Notifications.vue'




const routes = [
  { path: '/home', name: 'home', component: Home },
  { path: '/login', name: 'login', component: Login },
  { path: '/register', name: 'register', component: Register },
  { path: '/groups', name: 'groups', component: Groups },
  { path: '/dashboard', name: 'dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/events', name: 'events', component: Events, meta: { requiresAuth: true } },
  { path: '/tasks', name: 'tasks', component: Tasks, meta: { requiresAuth: true } },
  { path: '/post', name: 'post', component: AskForHelp, meta: { requiresAuth: true } },
  { path: '/chatbox', name: 'chatbox', component: ChatBox, meta: { requiresAuth: true } },
  { path: '/donations', name: 'donations', component: Donations, meta: { requiresAuth: true } },
  { path: '/create-post', name: 'create-post', component: () => import('../components/CreateCommunityPost.vue'), meta: { requiresAuth: true } },
  {path: '/groups/create', name: 'create-group' , component: CreateGroup, meta: { requiresAuth: true }},
  {path: '/events/create', name: 'create-events' , component: CreateEvent, meta: { requiresAuth: true }},
  {
    path: '/groups/:id',
    name: 'GroupDetails',
    component: () => import('../views/GroupDetails.vue')
  } , 
  {
    path: '/events/:id',
    name: 'EventDetails',
    component: () => import('../views/EventDetails.vue')
  },
  {
    path: '/help-request/:id',
    name: 'HelpRequestDetail',
    component: HelpRequestDetail
  },

  { path: '/notifications', component: Notifications },
  {
    path: '/chat/:roomName',
    name: 'ChatRoom',
    component: () => import('../views/ChatRoom.vue')
  },
]



const router = createRouter({
  history: createWebHistory(),
  routes
})

// 🔹 ✅ Protect routes that require authentication
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('access_token')  // ✅ Check if token exists

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')  // 🚀 Redirect to login if not authenticated
  } else {
    next()  // ✅ Proceed to the route
  }
})

export default router
