// src/router/index.js
import { route } from 'quasar/wrappers'
import { createRouter, createMemoryHistory, createWebHistory, createWebHashHistory } from 'vue-router'
import routes from './routes'
import { useAuthStore } from 'stores/auth-store' // <<<< اضافه کنید

export default route(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : (process.env.VUE_ROUTER_MODE === 'history' ? createWebHistory : createWebHashHistory)

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,
    history: createHistory(process.env.VUE_ROUTER_BASE)
  })

  // Navigation Guard
  Router.beforeEach((to, from, next) => {
    const authStore = useAuthStore(); // دسترسی به store در اینجا
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);

    console.log(`ROUTER: Navigating to ${to.path}, requiresAuth: ${requiresAuth}, isAuthenticated: ${authStore.isAuthenticated}`);

    if (requiresAuth && !authStore.isAuthenticated) {
      console.log('ROUTER: Auth required and not authenticated, redirecting to login.');
      next({ name: 'login', query: { redirect: to.fullPath } }); // به صفحه ورود هدایت کن و مسیر فعلی را به عنوان query بفرست
    } else if ((to.name === 'login' || to.name === 'register') && authStore.isAuthenticated) {
      console.log('ROUTER: Already authenticated, redirecting from login/register to home.');
      next({ name: 'home' }); // اگر کاربر لاگین کرده و به صفحه ورود/ثبت‌نام می‌رود، به خانه هدایتش کن
    }
    else {
      next(); // در غیر این صورت، اجازه عبور بده
    }
  })

  return Router
})