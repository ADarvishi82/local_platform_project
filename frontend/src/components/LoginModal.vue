<template>
  <q-dialog
    :model-value="modelValue"
    @update:model-value="val => emit('update:modelValue', val)"
    persistent
    transition-show="scale"
    transition-hide="scale"
  >
    <q-card class="login-dialog">
      <!-- Header -->
      <div class="dialog-header">
        <div class="header-background"></div>
        <div class="header-content">
          <div class="header-icon">
            <q-icon name="login" size="40px" />
          </div>
          <div class="header-text">
            <h2 class="dialog-title">ورود به حساب کاربری</h2>
            <p class="dialog-subtitle">به حساب کاربری خود دسترسی پیدا کنید</p>
          </div>
          <q-btn
            icon="close"
            flat
            round
            dense
            v-close-popup
            class="close-btn"
          />
        </div>
      </div>

      <!-- Welcome Section -->
      <div class="welcome-section">
        <div class="welcome-content">
          <div class="welcome-icon">
            <q-icon name="waving_hand" color="orange" size="24px" />
          </div>
          <div class="welcome-text">
            <h3 class="welcome-title">خوش آمدید!</h3>
            <p class="welcome-description">لطفاً اطلاعات ورود خود را وارد کنید</p>
          </div>
        </div>
      </div>

      <!-- Login Form (Scrollable Container) -->
      <div class="form-scroll-container">
        <div class="form-content-wrapper">
          <q-form @submit.prevent="handleLogin" class="login-form">
            <div class="form-group">
              <label class="form-label">نام کاربری یا ایمیل</label>
              <q-input
                v-model="loginIdentifier"
                outlined
                class="custom-input"
                placeholder="نام کاربری یا ایمیل خود را وارد کنید"
                :rules="[val => !!val || 'لطفا نام کاربری یا ایمیل را وارد کنید']"
                autocomplete="username"
              >
                <template v-slot:prepend>
                  <q-icon name="person" color="primary" />
                </template>
              </q-input>
            </div>

            <div class="form-group">
              <label class="form-label">رمز عبور</label>
              <q-input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                outlined
                class="custom-input"
                placeholder="رمز عبور خود را وارد کنید"
                :rules="[val => !!val || 'لطفا رمز عبور را وارد کنید']"
                autocomplete="current-password"
              >
                <template v-slot:prepend>
                  <q-icon name="lock" color="primary" />
                </template>
                <template v-slot:append>
                  <q-btn
                    :icon="showPassword ? 'visibility_off' : 'visibility'"
                    flat
                    round
                    dense
                    @click="showPassword = !showPassword"
                    class="password-toggle"
                  />
                </template>
              </q-input>
            </div>

            <!-- Remember Me & Forgot Password -->
            <div class="form-options">
              <q-checkbox
                v-model="rememberMe"
                label="مرا به خاطر بسپار"
                color="primary"
                class="remember-checkbox"
              />
              <a href="#" @click.prevent="handleForgotPassword" class="forgot-link">
                رمز عبور را فراموش کرده‌اید؟
              </a>
            </div>

            <div v-if="errorMessage" class="error-message">
              <q-icon name="error" class="error-icon" />
              <span class="error-text">{{ errorMessage }}</span>
            </div>

            <q-btn
              type="submit"
              class="login-btn"
              :loading="loading"
              unelevated
              size="lg"
            >
              <q-icon name="login" class="q-ml-sm" />
              ورود به حساب
            </q-btn>
          </q-form>

          <!-- Quick Login Options -->
          <div class="quick-login-section" v-if="recentUsers.length > 0">
            <div class="quick-login-header">
              <q-icon name="history" class="q-mr-sm" />
              <span>ورود سریع</span>
            </div>
            <div class="recent-users">
              <div
                v-for="user in recentUsers"
                :key="user.username"
                @click="selectQuickUser(user)"
                class="recent-user-item"
              >
                <q-avatar size="32px" color="primary" text-color="white">
                  {{ user.username.charAt(0).toUpperCase() }}
                </q-avatar>
                <span class="username">{{ user.username }}</span>
              </div>
            </div>
          </div>

          <!-- Social Login Section -->
          <div class="social-section">
            <div class="divider">
              <span class="divider-text">یا ورود با</span>
            </div>

            <div class="social-login">
              <GoogleLogin :callback="handleGoogleLoginCallback" />

              <div v-if="googleErrorMessage" class="error-message google-error">
                <q-icon name="error" class="error-icon" />
                <span class="error-text">{{ googleErrorMessage }}</span>
              </div>
            </div>
          </div>

          <!-- Footer -->
          <div class="dialog-footer">
            <div class="footer-text">
              حساب کاربری ندارید؟
              <a href="#" @click.prevent="switchToRegister" class="register-link">
                ثبت نام کنید
              </a>
            </div>
          </div>
        </div>
      </div>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { ref } from 'vue';
import { GoogleLogin } from 'vue3-google-login';
import { useAuthStore } from 'stores/auth-store';
import { useQuasar } from 'quasar';
import { api } from 'boot/axios';

// ESLint error fixed: `props` constant is removed
defineProps({
  modelValue: Boolean,
});
const emit = defineEmits(['update:modelValue', 'switchToRegister', 'loginSuccess']);

const loginIdentifier = ref('');
const password = ref('');
const loading = ref(false);
const googleErrorMessage = ref('');
const errorMessage = ref('');
const showPassword = ref(false);
const rememberMe = ref(false);

// Mock recent users - you can replace this with actual data from localStorage
const recentUsers = ref([
  // { username: 'user1', lastLogin: '2023-01-01' },
  // { username: 'user2', lastLogin: '2023-01-02' },
]);

const authStore = useAuthStore();
const $q = useQuasar();

async function handleLogin() {
  errorMessage.value = '';
  loading.value = true;

  const result = await authStore.login({
    username: loginIdentifier.value,
    password: password.value,
    remember: rememberMe.value
  });

  loading.value = false;

  if (result.success) {
    // Save user to recent users if remember me is checked
    if (rememberMe.value) {
      saveToRecentUsers(loginIdentifier.value);
    }

    $q.notify({
      type: 'positive',
      message: 'ورود با موفقیت انجام شد!',
      position: 'top',
      icon: 'check_circle',
      timeout: 3000
    });
    emit('loginSuccess');
    emit('update:modelValue', false);
  } else {
    errorMessage.value = result.message || "خطای نامشخص در ورود.";
  }
}

const handleGoogleLoginCallback = async (response) => {
  googleErrorMessage.value = '';
  if (!response.credential) return;

  try {
    const backendResponse = await api.post('/api/auth/google/', {
      id_token: response.credential
    });
    const { key, user } = backendResponse.data;

    await authStore.setTokenAndUser({ access: key, user: user });
    $q.notify({
      type: 'positive',
      message: 'ورود با گوگل موفقیت‌آمیز بود!',
      icon: 'check_circle',
      timeout: 3000
    });
    emit('loginSuccess');
    emit('update:modelValue', false);
  } catch (error) {
    console.error("Google login error:", error);
    googleErrorMessage.value = 'خطا در ارتباط با سرور.';
  }
};

function selectQuickUser(user) {
  loginIdentifier.value = user.username;
  // Focus on password field
  setTimeout(() => {
    const passwordInput = document.querySelector('input[type="password"]');
    if (passwordInput) passwordInput.focus();
  }, 100);
}

function saveToRecentUsers(username) {
  // Implementation to save recent users to localStorage
  // This is just a placeholder - implement according to your needs
  const existingIndex = recentUsers.value.findIndex(u => u.username === username);
  if (existingIndex === -1) {
    recentUsers.value.unshift({
      username,
      lastLogin: new Date().toISOString()
    });
    // Keep only 3 recent users
    recentUsers.value = recentUsers.value.slice(0, 3);
  }
}

function handleForgotPassword() {
  $q.notify({
    type: 'info',
    message: 'لینک بازیابی رمز عبور به ایمیل شما ارسال خواهد شد',
    timeout: 3000,
    actions: [
      {
        label: 'ارسال',
        color: 'white',
        handler: () => {
          // Implement forgot password logic
          console.log('Send forgot password email');
        }
      }
    ]
  });
}

function switchToRegister() {
  emit('update:modelValue', false);
  emit('switchToRegister');
}
</script>

<style scoped lang="scss">
/* --- استایل‌های راست‌چین --- */
.login-dialog {
  direction: rtl;
}
.header-text, .welcome-text, .form-label, .dialog-footer {
  text-align: right;
}
.error-message {
  flex-direction: row-reverse;
}
.error-text {
  text-align: right;
}
.form-options {
  direction: ltr;
  text-align: right;
}
/* -------------------------- */

.login-dialog {
  min-width: 450px;
  max-width: 500px;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(11, 196, 20, 0.15);
  background: linear-gradient(135deg, #e8f5e8 0%, #ffffff 100%);

  /* --- تغییرات اصلی برای اسکرول --- */
  display: flex;
  flex-direction: column;
  max-height: 95vh;
  /* ------------------------------ */

  @media (max-width: 600px) {
    min-width: 90vw;
    max-width: 95vw;
    margin: 1rem;
  }
}

.dialog-header {
  position: relative;
  padding: 0;
  margin: 0;

  .header-background {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, #0eaa15 0%, #81c784 100%);
    z-index: 1;
  }

  .header-content {
    position: relative;
    z-index: 2;
    padding: 1.5rem 2rem;
    color: #000000;
    display: flex;
    align-items: center;
    gap: 1rem;

    .header-icon {
      background: rgba(255, 255, 255, 0.3);
      border-radius: 50%;
      padding: 1rem;
      backdrop-filter: blur(10px);
    }

    .header-text {
      flex: 1;

      .dialog-title {
        margin: 0 0 0.25rem 0;
        font-size: 1.5rem;
        font-weight: 700;
        color: #000000;
        text-shadow: none;
      }

      .dialog-subtitle {
        margin: 0;
        color: #000000;
        opacity: 0.8;
        font-size: 0.95rem;
      }
    }

    .close-btn {
      background: rgba(255, 255, 255, 0.2);
      color: #000000;
      backdrop-filter: blur(10px);

      &:hover {
        background: rgba(255, 255, 255, 0.3);
      }
    }
  }
}

.welcome-section {
  background: linear-gradient(90deg, #a5d6a7 0%, #ffffff 100%);
  padding: 1rem 2rem;
  border-bottom: 1px solid #c8e6c9;
  flex-shrink: 0;
}

/* --- تغییرات اصلی برای اسکرول --- */
.form-scroll-container {
  flex: 1;
  overflow-y: auto;
  background: linear-gradient(135deg, #f1f8e9 0%, #ffffff 100%);
}
.form-content-wrapper {
  padding: 1.5rem 2rem;
}
/* ------------------------------ */

.login-form .form-group {
  margin-bottom: 1.2rem;
}

/* --- بقیه استایل‌ها --- */
.welcome-section .welcome-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.welcome-section .welcome-content .welcome-icon {
  background: rgba(255, 255, 255, 0.5);
  border-radius: 50%;
  padding: 0.75rem;
}

.welcome-section .welcome-content .welcome-text .welcome-title {
  margin: 0 0 0.25rem 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #000000;
}

.welcome-section .welcome-content .welcome-text .welcome-description {
  margin: 0;
  color: #000000;
  opacity: 0.8;
  font-size: 0.9rem;
}

.login-form .form-group .form-label {
  display: block;
  font-weight: 600;
  color: #000000;
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
}

.login-form .form-group .custom-input :deep(.q-field__control) {
  border-radius: 12px;
  border: 2px solid #c8e6c9;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.8);
}

.login-form .form-group .custom-input :deep(.q-field__control:hover) {
  border-color: #81c784;
}

.login-form .form-group .custom-input :deep(.q-field--focused .q-field__control) {
  border-color: #66bb6a;
  box-shadow: 0 0 0 3px rgba(102, 187, 106, 0.2);
}

.login-form .form-group .custom-input :deep(.q-field__prepend .q-icon) {
  transition: all 0.3s ease;
}

.login-form .form-group .custom-input :deep(.q-field--focused .q-field__prepend .q-icon) {
  transform: scale(1.1);
}

.login-form .form-group .password-toggle {
  color: #000000;
}

.login-form .form-group .password-toggle:hover {
  color: #66bb6a;
  background: rgba(102, 187, 106, 0.1);
}

.login-form .form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.login-form .form-options .remember-checkbox :deep(.q-checkbox__label) {
  color: #000000;
  font-size: 0.9rem;
  padding-right: 0.5em;
}

.login-form .form-options .forgot-link {
  color: #66bb6a;
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.3s ease;
}

.login-form .form-options .forgot-link:hover {
  color: #4caf50;
  text-decoration: underline;
}

.login-form .error-message {
  padding: 0.75rem 1rem;
  background: rgba(244, 67, 54, 0.1);
  border: 1px solid rgba(244, 67, 54, 0.3);
  border-radius: 8px;
  margin-bottom: 1rem;
}

.login-form .error-message .error-icon {
  color: #f44336;
  font-size: 18px;
}

.login-form .error-message .error-text {
  color: #f44336;
  font-size: 0.9rem;
}

.login-form .login-btn {
  width: 100%;
  padding: 1rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  background: linear-gradient(135deg, #66bb6a, #81c784);
  color: #000000;
  transition: all 0.3s ease;
}

.login-form .login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 187, 106, 0.3);
}

.quick-login-section {
  margin: 1.5rem 0;
  padding: 1rem;
  background: rgba(232, 245, 232, 0.8);
  border-radius: 12px;
  border: 1px solid #c8e6c9;
}

.quick-login-section .quick-login-header {
  display: flex;
  align-items: center;
  color: #000000;
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.quick-login-section .recent-users {
  display: flex;
  gap: 0.75rem;
}

.quick-login-section .recent-users .recent-user-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.quick-login-section .recent-users .recent-user-item:hover {
  border-color: #81c784;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(129, 199, 132, 0.2);
}

.quick-login-section .recent-users .recent-user-item .username {
  font-size: 0.8rem;
  color: #000000;
  font-weight: 500;
}

.social-section .divider {
  position: relative;
  text-align: center;
  margin: 2rem 0 1.5rem;
}

.social-section .divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: #c8e6c9;
}

.social-section .divider .divider-text {
  background: rgba(255, 255, 255, 0.9);
  padding: 0 1rem;
  color: #000000;
  font-size: 0.9rem;
  position: relative;
  z-index: 1;
}

.social-section .social-login {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.social-section .social-login .google-error {
  width: 100%;
  text-align: center;
}

.dialog-footer {
  padding-top: 1.5rem;
  border-top: 1px solid #c8e6c9;
  margin-top: 1.5rem;
}

.dialog-footer .footer-text {
  color: #000000;
  font-size: 0.95rem;
}

.dialog-footer .footer-text .register-link {
  color: #66bb6a;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.3s ease;
  margin-right: 5px;
}

.dialog-footer .footer-text .register-link:hover {
  color: #4caf50;
  text-decoration: underline;
}

:deep(.google-login-button) {
  width: 100%;
  max-width: 300px;
  border-radius: 12px;
  padding: 0.75rem 1rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

:deep(.google-login-button:hover) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 187, 106, 0.15);
}

:deep(.q-loading) {
  background: rgba(232, 245, 232, 0.9);
  backdrop-filter: blur(5px);
}
</style>
