// src/stores/auth-store.js
import { defineStore } from 'pinia';
import { api } from 'boot/axios';
import { LocalStorage } from 'quasar';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: LocalStorage.getItem('accessToken') || null,
    refreshToken: LocalStorage.getItem('refreshToken') || null,
    user: LocalStorage.getItem('user') ? JSON.parse(LocalStorage.getItem('user')) : null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken,
    getUser: (state) => state.user,
    getAccessToken: (state) => state.accessToken,
  },

  // ***** فقط یک آبجکت actions برای تمام توابع *****
  actions: {
    async login(credentials) {
      console.log("AUTH_STORE: Attempting login with credentials:", credentials);
      try {
        const response = await api.post('/api/auth/login/', credentials);
        const accessToken = response.data.access;
        const refreshToken = response.data.refresh;
        const userData = response.data.user;

        if (!accessToken) {
          this.logout();
          return { success: false, message: 'پاسخ سرور شامل توکن دسترسی نبود.' };
        }

        this.setTokenAndUser({ access: accessToken, refresh: refreshToken, user: userData });
        console.log("AUTH_STORE: Login successful.");
        return { success: true, user: userData };

      } catch (error) {
        console.error('AUTH_STORE: Login error:', error.response?.data || error.message);
        let errorMessage = 'خطا در ورود.';
        if (error.response?.data?.non_field_errors) {
          errorMessage = error.response.data.non_field_errors.join(' ');
        }
        this.logout();
        return { success: false, message: errorMessage };
      }
    },

    async register(registrationData) {
      console.log("AUTH_STORE: Attempting registration with data:", registrationData);
      try {
        const response = await api.post('/api/auth/registration/', registrationData);
        return { success: true, data: response.data };
      } catch (error) {
        console.error('AUTH_STORE: Registration error:', error.response?.data || error.message);
        let errorMessage = 'خطا در ثبت نام.';
        if (error.response && error.response.data) {
          const errors = error.response.data;
          const messages = [];
          for (const field in errors) {
            if (Array.isArray(errors[field])) {
              messages.push(errors[field].join(', '));
            } else {
              messages.push(String(errors[field]));
            }
          }
          if (messages.length > 0) errorMessage = messages.join('\n');
        }
        return { success: false, message: errorMessage };
      }
    },

    logout() {
      console.log("AUTH_STORE: Logging out...");
      this.accessToken = null;
      this.refreshToken = null;
      this.user = null;
      LocalStorage.remove('accessToken');
      LocalStorage.remove('refreshToken');
      LocalStorage.remove('user');
      delete api.defaults.headers.common['Authorization'];
    },

    setTokenAndUser({ access, refresh, user }) {
      console.log("AUTH_STORE: Setting token and user.");
      this.accessToken = access;
      this.refreshToken = refresh || null;
      this.user = user;

      LocalStorage.set('accessToken', this.accessToken);
      if (this.refreshToken) {
        LocalStorage.set('refreshToken', this.refreshToken);
      }
      LocalStorage.set('user', JSON.stringify(this.user));
      api.defaults.headers.common['Authorization'] = `Bearer ${this.accessToken}`;
    },

    updateUserInStore(updatedUserData) {
      console.log("AUTH_STORE: Updating user data in store.");
      this.user = updatedUserData;
      LocalStorage.set('user', JSON.stringify(this.user));
      console.log("AUTH_STORE: State after update:", JSON.parse(JSON.stringify(this.user)));
    },

    async refreshTokenAction() {
      if (!this.refreshToken) {
        this.logout();
        return false;
      }
      try {
        const response = await api.post('/api/auth/token/refresh/', { refresh: this.refreshToken });
        this.accessToken = response.data.access;
        LocalStorage.set('accessToken', this.accessToken);
        api.defaults.headers.common['Authorization'] = `Bearer ${this.accessToken}`;
        return true;
      } catch  {
        this.logout();
        return false;
      }
    },

    checkAuthOnLoad() {
      if (this.accessToken) {
        api.defaults.headers.common['Authorization'] = `Bearer ${this.accessToken}`;
        console.log("AUTH_STORE: Auth check on load: Token found.");
      } else {
        console.log("AUTH_STORE: Auth check on load: No token found.");
      }
    }
  }, // <<<< پایان آبجکت actions
});
