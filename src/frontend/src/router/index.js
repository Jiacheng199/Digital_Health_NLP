import Vue from "vue";
import VueRouter from "vue-router";
import HomePage from "../components/HomePage.vue";
import Login from "../components/LoginPage.vue";
import Register from "../components/RegisterPage.vue";
import ViewMapping from "../components/ViewMapping.vue";
import MappingPage from "../components/MappingPage.vue";
Vue.use(VueRouter);
/* eslint-disable */
const routes = [
  {
    path: '/',
    name: 'index',
    component: HomePage
  },
  // {
  //   path: '/upload',
  //   name: 'upload',
  //   component: Upload
  // },
  {
    path: '/home',
    name: 'HomePage',
    component:HomePage,
    meta: { requiresAuth: true }
  },
  {
    path: '/mapping',
    name: 'MappingPage',
    component:MappingPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component:Login
  },
  {
    path:'/register',
    name:'Register',
    component: Register
  },
  {
    path:'/viewmapping',
    name:'ViewMapping',
    component: ViewMapping,
    meta: { requiresAuth: true }
  },
  // {
  //   path: '/chart',
  //   name: 'Chart',
  //   component: Charts
  // }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});
router.beforeEach((to, from, next) => {
  const loggedIn = localStorage.getItem('token');
  if (to.matched.some(record => record.meta.requiresAuth) && !loggedIn) next('/login')
  else next()
});
export default router;
