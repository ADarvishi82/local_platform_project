// src/router/routes.js
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', name: 'home', component: () => import('pages/IndexPage.vue') },
      { path: 'login', name: 'login', component: () => import('pages/LoginPage.vue') },
      { path: 'register/user', name: 'register-user', component: () => import('pages/RegisterUserPage.vue') },
      { path: 'register/business', name: 'register-business', component: () => import('pages/RegisterBusinessPage.vue') },
      { path: 'register', redirect: '/register/user' },

      {
        path: 'manage-business',
        name: 'manage-business',
        component: () => import('pages/BusinessProfilePage.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'profile',
        name: 'user-profile',
        component: () => import('pages/UserProfilePage.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'businesses',
        name: 'business-list',
        component: () => import('pages/BusinessListPage.vue')
      },
      {
        path: 'business/:id',
        name: 'business-detail',
        component: () => import('pages/BusinessDetailPage.vue'),
        props: true
      },

      // مسیر جدید برای لیست محله‌ها
      {
        path: 'neighborhoods',
        name: 'neighborhood-list',
        component: () => import('pages/NeighborhoodListPage.vue')
        // این صفحه معمولاً نیازی به requiresAuth ندارد
      },
      {
        path: 'neighborhood/:id', // <<<< مسیر داینامیک برای جزئیات محله
        name: 'neighborhood-detail',
        component: () => import('pages/NeighborhoodDetailPage.vue'),
        props: true // برای پاس دادن id به عنوان prop
      },
      {
        path: 'feed', // یا هر نامی که برای فید می‌خواهید
        name: 'feed',
        component: () => import('pages/FeedPage.vue')
      },
      {
        path: 'tags/:tagName', // <<<< مسیر داینامیک برای فید هشتگ
        name: 'hashtag-feed',
        component: () => import('pages/HashtagFeedPage.vue'),
        props: true // برای پاس دادن tagName به عنوان prop
      }
    ]
  },

  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
