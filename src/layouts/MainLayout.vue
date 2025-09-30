<template>
  <q-layout view="lHh LpR lfr" class="rtl-layout">

    <!-- Header -->
    <q-header elevated class="custom-header shadow-2">
      <q-toolbar class="q-px-lg q-py-sm">
        <div class="row items-center full-width">
          <!-- Logo Section -->
          <div class="row items-center q-ml-lg">
            <q-avatar size="42px" class="logo-avatar">
              <img src="src\assets\Between Friends Logo.jpg">
            </q-avatar>
            <div class="q-mr-sm">
              <div class="logo-text">همسایه</div>
              <div class="logo-subtitle">شبکه همسایگی</div>
            </div>
          </div>

          <!-- Search Section -->
          <div class="col-grow q-mx-lg gt-sm">
            <q-input dense standout="bg-white/10 text-white" rounded v-model="search" placeholder="جستجو در محله..."
              class="search-input" input-class="text-white placeholder-white/70" color="white">
              <template v-slot:prepend>
                <q-icon name="search" color="white" />
              </template>
              <template v-slot:append v-if="search">
                <q-icon name="clear" color="white" @click="search = ''" class="cursor-pointer" />
              </template>
            </q-input>
          </div>

          <!-- Navigation Buttons -->
          <div class="row items-center q-gutter-x-xs gt-sm">
            <q-btn flat round icon="home" to="/" :color="$route.name === 'home' ? 'white' : 'white'"
              :class="$route.name === 'home' ? 'nav-btn-active' : 'nav-btn'" size="md">
              <q-tooltip class="bg-grey-8 text-white" anchor="bottom middle" self="top middle">خانه</q-tooltip>
            </q-btn>
            <q-btn flat round icon="dynamic_feed" to="/feed" :color="$route.name === 'feed' ? 'white' : 'white'"
              :class="$route.name === 'feed' ? 'nav-btn-active' : 'nav-btn'" size="md">
              <q-tooltip class="bg-grey-8 text-white" anchor="bottom middle" self="top middle">فید پست‌ها</q-tooltip>
            </q-btn>
            <q-btn flat round icon="storefront" to="/businesses"
              :color="$route.name === 'business-list' ? 'white' : 'white'"
              :class="$route.name === 'business-list' ? 'nav-btn-active' : 'nav-btn'" size="md">
              <q-tooltip class="bg-grey-8 text-white" anchor="bottom middle" self="top middle">کسب‌وکارها</q-tooltip>
            </q-btn>
            <q-btn flat round icon="holiday_village" to="/neighborhoods"
              :color="$route.name === 'neighborhood-list' ? 'white' : 'white'"
              :class="$route.name === 'neighborhood-list' ? 'nav-btn-active' : 'nav-btn'" size="md">
              <q-tooltip class="bg-grey-8 text-white" anchor="bottom middle" self="top middle">محله‌ها</q-tooltip>
            </q-btn>
          </div>

          <q-separator vertical spaced class="gt-sm separator-custom" />

          <!-- User Section -->
          <div v-if="authStore.isAuthenticated" class="q-mr-md">
            <q-btn-dropdown flat round class="user-dropdown" dropdown-icon="none">
              <template v-slot:label>
                <div class="row items-center q-gutter-xs">
                  <q-avatar size="32px" class="user-avatar">
                    <img v-if="userAvatarUrl" :src="userAvatarUrl" alt="Avatar">
                    <q-icon v-else name="account_circle" color="white" />
                  </q-avatar>
                  <q-icon name="keyboard_arrow_down" color="white" size="xs" />
                </div>
              </template>
              <q-list dense class="user-menu">
                <q-item-label header class="text-primary text-weight-bold q-pa-md">
                  <div class="row items-center">
                    <q-avatar size="40px" class="q-ml-sm">
                      <img v-if="userAvatarUrl" :src="userAvatarUrl" alt="Avatar">
                      <q-icon v-else name="account_circle" />
                    </q-avatar>
                    <div>
                      <div class="text-subtitle2">{{ authStore.user?.username }}</div>
                      <div class="text-caption text-grey-6">{{ authStore.user?.email }}</div>
                    </div>
                  </div>
                </q-item-label>
                <q-separator class="q-mb-sm" />
                <q-item clickable v-ripple to="/profile" class="menu-item">
                  <q-item-section avatar>
                    <q-icon name="person" color="primary" />
                  </q-item-section>
                  <q-item-section>پروفایل من</q-item-section>
                </q-item>
                <q-item clickable v-ripple to="/manage-business" class="menu-item">
                  <q-item-section avatar>
                    <q-icon name="store" color="primary" />
                  </q-item-section>
                  <q-item-section>مدیریت کسب‌وکار</q-item-section>
                </q-item>
                <q-separator class="q-my-sm" />
                <q-item clickable v-ripple @click="handleLogout" class="menu-item logout-item">
                  <q-item-section avatar>
                    <q-icon name="logout" color="negative" />
                  </q-item-section>
                  <q-item-section>خروج</q-item-section>
                </q-item>
              </q-list>
            </q-btn-dropdown>
          </div>
          <div v-else class="row q-gutter-x-sm q-mr-md">
            <q-btn label="ورود" color="white" text-color="primary" unelevated rounded @click="showLoginModal = true"
              class="login-btn" size="sm" />
            <q-btn label="ثبت نام" color="white" text-color="primary" unelevated rounded
              @click="showRegisterModal = true" class="register-btn" size="sm" />
          </div>
        </div>
      </q-toolbar>
    </q-header>

    <!-- Page Container -->
    <q-page-container class="page-background">
      <q-page class="q-pa-md">
        <div class="row q-col-gutter-lg justify-center">

          <!-- Right Sidebar (Main) -->
          <div class="col-12 col-lg-3 col-md-4 gt-sm">
            <div class="q-gutter-y-md sticky-sidebar">
              <q-card class="sidebar-card user-card" v-if="authStore.isAuthenticated">
                <div class="user-card-header">
                  <div class="user-card-background"></div>
                  <q-card-section class="text-center relative-position q-pb-none">
                    <q-avatar size="90px" class="user-main-avatar">
                      <img v-if="userAvatarUrl" :src="userAvatarUrl" alt="Avatar">
                      <q-icon v-else name="account_circle" size="90px" color="grey-5" />
                    </q-avatar>
                    <div class="q-mt-md">
                      <div class="text-h6 text-white text-weight-bold">{{ authStore.user?.username }}</div>
                      <div class="text-caption text-white/80">{{ authStore.user?.email }}</div>
                    </div>
                  </q-card-section>
                </div>
                <q-card-section class="q-pt-none">
                  <q-btn label="مشاهده پروفایل" color="primary" unelevated rounded class="full-width q-mt-sm" size="sm"
                    to="/profile" />
                </q-card-section>
              </q-card>

              <q-card class="sidebar-card guest-card" v-else>
                <q-card-section class="text-center">
                  <q-avatar size="80px" class="guest-avatar">
                    <q-icon name="person_off" size="40px" />
                  </q-avatar>
                  <div class="q-mt-md">
                    <div class="text-h6 text-weight-bold">کاربر مهمان</div>
                    <div class="text-caption text-grey-6 q-mb-md">برای دسترسی به امکانات بیشتر وارد شوید.</div>
                  </div>
                  <q-btn label="ورود / ثبت نام" color="primary" unelevated rounded class="full-width"
                    @click="showLoginModal = true" />
                </q-card-section>
              </q-card>

              <NeighborhoodStats v-if="authStore.isAuthenticated" />
              <PopularTags />

              <q-card class="sidebar-card">
                <q-card-section>
                  <div class="text-subtitle2 text-weight-bold q-mb-md text-primary">دسترسی سریع</div>
                  <div class="q-gutter-y-xs">
                    <q-btn flat class="full-width justify-start text-left" icon="add_circle" label="پست جدید"
                      color="primary" @click="showCreatePostModal = true"/>
                    <q-btn flat class="full-width justify-start text-left" icon="business" label="کسب‌وکار جدید"
                      color="primary" />
                    <q-btn flat class="full-width justify-start text-left" icon="location_on" label="محله من"
                      color="primary" />
                  </div>
                </q-card-section>
              </q-card>
            </div>
          </div>

          <!-- Main Content -->
          <div class="col-12 col-lg-6 col-md-8">
            <router-view :key="$route.fullPath" />
          </div>

          <!-- Left Sidebar (Secondary) -->
          <div class="col-12 col-lg-3 col-md-4 gt-sm">
            <div class="q-gutter-y-md sticky-sidebar">
              <ImportantNews v-if="authStore.isAuthenticated" />
              <UpcomingEvents v-if="authStore.isAuthenticated" />
            </div>
          </div>
        </div>
      </q-page>
    </q-page-container>

    <!-- Floating Action Button -->
    <q-page-sticky position="bottom-left" :offset="[18, 18]" v-if="authStore.isAuthenticated">
      <q-btn fab icon="add" color="primary" size="lg" class="floating-btn" @click="showCreatePostModal = true">
        <q-tooltip class="bg-grey-8 text-white" anchor="top middle" self="bottom middle">
          پست جدید
        </q-tooltip>
      </q-btn>
    </q-page-sticky>

    <!-- Chatbot Widget -->
    <q-page-sticky position="bottom-right" :offset="[18, 80]">
      <ChatbotWidget v-if="isChatOpen" class="chatbot-widget" />
    </q-page-sticky>
    <q-page-sticky position="bottom-right" :offset="[18, 18]">
      <q-btn
        fab
        :icon="isChatOpen ? 'close' : 'support_agent'"
        color="accent"
        @click="isChatOpen = !isChatOpen"
      />
    </q-page-sticky>

    <!-- Modals -->
    <LoginModal v-model="showLoginModal" @switchToRegister="openRegisterModal" @loginSuccess="onLoginSuccess" />
    <RegisterModal v-model="showRegisterModal" @switchToLogin="openLoginModal" />

    <q-dialog v-model="showCreatePostModal">
      <CreatePostForm @postCreated="handlePostCreation" />
    </q-dialog>

  </q-layout>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useAuthStore } from 'stores/auth-store';
import { useRouter } from 'vue-router';
import LoginModal from 'components/LoginModal.vue';
import RegisterModal from 'components/RegisterModal.vue';
import ImportantNews from 'components/sidebars/ImportantNews.vue';
import UpcomingEvents from 'components/sidebars/UpcomingEvents.vue';
import NeighborhoodStats from 'components/sidebars/NeighborhoodStats.vue';
import PopularTags from 'components/sidebars/PopularTags.vue';
import ChatbotWidget from 'components/ChatbotWidget.vue';
import CreatePostForm from 'components/CreatePostForm.vue';

const authStore = useAuthStore();
const router = useRouter();
const search = ref('');
const showLoginModal = ref(false);
const showRegisterModal = ref(false);
const isChatOpen = ref(false);
const showCreatePostModal = ref(false);

const userAvatarUrl = computed(() => {
  const user = authStore.user;
  if (!user) return null;
  if (user.profile && user.profile.profile_picture_url) return user.profile.profile_picture_url;
  if (user.business_profile && user.business_profile.logo_url) return user.business_profile.logo_url;
  return null;
});

function openLoginModal() {
  showRegisterModal.value = false;
  showLoginModal.value = true;
}

function openRegisterModal() {
  showLoginModal.value = false;
  showRegisterModal.value = true;
}

function onLoginSuccess() {
  console.log('User has successfully logged in from layout.');
}

async function handleLogout() {
  await authStore.logout();
  router.push('/');
}

function handlePostCreation() {
  showCreatePostModal.value = false;
  if (router.currentRoute.value.path === '/feed') {
    router.go(0);
  } else {
    router.push('/feed');
  }
}
</script>

<style scoped>
.rtl-layout {
  direction: rtl;
}

/* Header Styles */
.custom-header {
  background: linear-gradient(135deg, #27f204 0%, #146701 100%);
  backdrop-filter: blur(10px);
}

.logo-avatar {
  border: 2px solid rgba(255, 255, 255, 0.2);
  transition: transform 0.3s ease;
}

.logo-avatar:hover {
  transform: scale(1.05);
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  line-height: 1;
}

.logo-subtitle {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1;
}

.search-input {
  max-width: 400px;
}

.search-input :deep(.q-field__control) {
  border-radius: 25px;
  backdrop-filter: blur(10px);
}

.nav-btn {
  transition: all 0.3s ease;
  opacity: 0.8;
}

.nav-btn:hover {
  opacity: 1;
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-btn-active {
  background-color: rgba(255, 255, 255, 0.2);
  opacity: 1;
}

.separator-custom {
  opacity: 0.3;
  color: white;
}

.user-dropdown {
  transition: all 0.3s ease;
}

.user-dropdown:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.user-avatar {
  border: 2px solid rgba(255, 255, 255, 0.3);
  transition: transform 0.3s ease;
}

.user-menu {
  min-width: 280px;
  border-radius: 12px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.menu-item {
  transition: all 0.2s ease;
  border-radius: 8px;
  margin: 2px 8px;
}

.menu-item:hover {
  background-color: rgba(103, 126, 234, 0.1);
}

.logout-item:hover {
  background-color: rgba(244, 67, 54, 0.1);
}

.login-btn, .register-btn {
  font-weight: 600;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.login-btn:hover, .register-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 255, 255, 0.3);
}

/* Page Styles */
.page-background {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
}

/* Sidebar Styles */
.sticky-sidebar {
  position: sticky;
  top: 80px;
  max-height: calc(100vh - 100px);
  overflow-y: auto;
}

.sidebar-card {
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.sidebar-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.user-card {
  overflow: hidden;
  position: relative;
}

.user-card-header {
  position: relative;
}

.user-card-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 120px;
  background: linear-gradient(135deg, #2ae04b 0%, #53ea31 100%);
  z-index: 1;
}

.user-card-header .q-card-section {
  position: relative;
  z-index: 2;
  padding-top: 2rem;
}

.user-main-avatar {
  border: 4px solid rgba(255, 255, 255, 0.9);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.guest-card .guest-avatar {
  background: linear-gradient(135deg, #3ce439 0%, #77f557 100%);
  color: white;
}

.trending-item, .suggestion-item {
  padding: 8px 12px;
  border-radius: 8px;
  transition: background-color 0.2s ease;
  display: flex;
  align-items: center;
}

.trending-item:hover, .suggestion-item:hover {
  background-color: rgba(103, 126, 234, 0.05);
}

/* Floating Button */
.floating-btn {
  box-shadow: 0 8px 25px rgba(48, 215, 93, 0.4);
  transition: all 0.3s ease;
}

.floating-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 12px 35px rgba(56, 224, 115, 0.5);
}

/* Chatbot Widget Style */
.chatbot-widget {
  transition: all 0.3s ease-in-out;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

/* Responsive Design */
@media (max-width: 768px) {
  .sticky-sidebar {
    position: static;
    max-height: none;
  }

  .custom-header .q-toolbar {
    padding-left: 1rem;
    padding-right: 1rem;
  }

  .logo-text {
    font-size: 1.2rem;
  }

  .logo-subtitle {
    display: none;
  }
}

/* Scrollbar Styling */
.sticky-sidebar::-webkit-scrollbar {
  width: 4px;
}

.sticky-sidebar::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 2px;
}

.sticky-sidebar::-webkit-scrollbar-thumb {
  background: rgba(51, 225, 68, 0.3);
  border-radius: 2px;
}

.sticky-sidebar::-webkit-scrollbar-thumb:hover {
  background: rgba(58, 237, 88, 0.847);
}

/* Animations */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.sidebar-card {
  animation: fadeInUp 0.6s ease-out;
}

.sidebar-card:nth-child(2) {
  animation-delay: 0.1s;
}

.sidebar-card:nth-child(3) {
  animation-delay: 0.2s;
}
</style>
