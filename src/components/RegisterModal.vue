<template>
  <q-dialog
    :model-value="modelValue"
    @update:model-value="val => emit('update:modelValue', val)"
    persistent
    transition-show="scale"
    transition-hide="scale"
  >
    <q-card class="register-dialog">
      <!-- Header -->
      <div class="dialog-header">
        <div class="header-background"></div>
        <div class="header-content">
          <div class="header-icon">
            <q-icon name="person_add" size="40px" />
          </div>
          <div class="header-text">
            <h2 class="dialog-title">ایجاد حساب کاربری</h2>
            <p class="dialog-subtitle">به جامعه ما بپیوندید و تجربه جدیدی را آغاز کنید</p>
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

      <!-- Tab Navigation -->
      <div class="tab-section">
        <q-tabs
          v-model="tab"
          class="custom-tabs"
          active-color="white"
          indicator-color="transparent"
          align="justify"
        >
          <q-tab
            name="user"
            class="custom-tab"
            :class="{ 'tab-active': tab === 'user' }"
          >
            <div class="tab-content">
              <q-icon name="person" size="20px" />
              <span>کاربر عادی</span>
            </div>
          </q-tab>
          <q-tab
            name="business"
            class="custom-tab"
            :class="{ 'tab-active': tab === 'business' }"
          >
            <div class="tab-content">
              <q-icon name="business" size="20px" />
              <span>کسب‌وکار</span>
            </div>
          </q-tab>
        </q-tabs>
      </div>

      <!-- Form Content -->
      <div class="form-container">
        <q-tab-panels v-model="tab" animated transition-prev="slide-right" transition-next="slide-left">
          <!-- User Registration Panel -->
          <q-tab-panel name="user" class="tab-panel">
            <div class="panel-header">
              <div class="panel-icon">
                <q-icon name="person" color="primary" size="32px" />
              </div>
              <div class="panel-text">
                <h3 class="panel-title">ثبت‌نام کاربر عادی</h3>
                <p class="panel-description">برای پیوستن به جامعه محلی ما ثبت نام کنید</p>
              </div>
            </div>

            <q-form @submit.prevent="handleRegister" class="registration-form">
              <div class="form-group">
                <label class="form-label">نام کاربری</label>
                <q-input
                  v-model="formData.username"
                  outlined
                  class="custom-input"
                  placeholder="نام کاربری خود را وارد کنید"
                  :rules="[val => !!val || 'لطفا نام کاربری را وارد کنید']"
                  autocomplete="username"
                >
                  <template v-slot:prepend>
                    <q-icon name="account_circle" color="primary" />
                  </template>
                </q-input>
              </div>

              <div class="form-group">
                <label class="form-label">آدرس ایمیل</label>
                <q-input
                  v-model="formData.email"
                  type="email"
                  outlined
                  class="custom-input"
                  placeholder="example@email.com"
                  :rules="[
                    val => !!val || 'لطفا ایمیل را وارد کنید',
                    val => /.+@.+\..+/.test(val) || 'ایمیل معتبر نیست'
                  ]"
                  autocomplete="email"
                >
                  <template v-slot:prepend>
                    <q-icon name="email" color="primary" />
                  </template>
                </q-input>
              </div>

              <div class="form-group">
                <label class="form-label">رمز عبور</label>
                <q-input
                  v-model="formData.password"
                  :type="showPassword ? 'text' : 'password'"
                  outlined
                  class="custom-input"
                  placeholder="رمز عبور قوی انتخاب کنید"
                  :rules="[
                    val => !!val || 'لطفا رمز عبور را وارد کنید',
                    val => val.length >= 8 || 'رمز عبور باید حداقل ۸ کاراکتر باشد'
                  ]"
                  autocomplete="new-password"
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

              <div class="form-group">
                <label class="form-label">تکرار رمز عبور</label>
                <q-input
                  v-model="formData.password2"
                  :type="showPassword2 ? 'text' : 'password'"
                  outlined
                  class="custom-input"
                  placeholder="رمز عبور را مجدداً وارد کنید"
                  :rules="[
                    val => !!val || 'لطفا تکرار رمز عبور را وارد کنید',
                    val => val === formData.password || 'رمزهای عبور مطابقت ندارند'
                  ]"
                  autocomplete="new-password"
                >
                  <template v-slot:prepend>
                    <q-icon name="lock_outline" color="primary" />
                  </template>
                  <template v-slot:append>
                    <q-btn
                      :icon="showPassword2 ? 'visibility_off' : 'visibility'"
                      flat
                      round
                      dense
                      @click="showPassword2 = !showPassword2"
                      class="password-toggle"
                    />
                  </template>
                </q-input>
              </div>

              <div v-if="errorMessage" class="error-message">
                <q-icon name="error" class="error-icon" />
                <span class="error-text">{{ errorMessage }}</span>
              </div>

              <q-btn
                type="submit"
                class="submit-btn user-btn"
                :loading="loading"
                unelevated
                size="lg"
              >
                <q-icon name="person_add" class="q-ml-sm" />
                ثبت نام کاربر عادی
              </q-btn>
            </q-form>
          </q-tab-panel>

          <!-- Business Registration Panel -->
          <q-tab-panel name="business" class="tab-panel">
            <div class="panel-header">
              <div class="panel-icon">
                <q-icon name="business" color="secondary" size="32px" />
              </div>
              <div class="panel-text">
                <h3 class="panel-title">ثبت‌نام کسب‌وکار</h3>
                <p class="panel-description">اطلاعات مدیر حساب و کسب‌وکار خود را وارد کنید</p>
              </div>
            </div>

            <q-form @submit.prevent="handleRegister" class="registration-form">
              <div class="form-group">
                <label class="form-label">نام کاربری مدیر حساب</label>
                <q-input
                  v-model="formData.username"
                  outlined
                  class="custom-input"
                  placeholder="نام کاربری مدیر را وارد کنید"
                  :rules="[val => !!val || 'لطفا نام کاربری را وارد کنید']"
                  autocomplete="username"
                >
                  <template v-slot:prepend>
                    <q-icon name="admin_panel_settings" color="secondary" />
                  </template>
                </q-input>
              </div>

              <div class="form-group">
                <label class="form-label">ایمیل مدیر حساب</label>
                <q-input
                  v-model="formData.email"
                  type="email"
                  outlined
                  class="custom-input"
                  placeholder="manager@business.com"
                  :rules="[
                    val => !!val || 'لطفا ایمیل را وارد کنید',
                    val => /.+@.+\..+/.test(val) || 'ایمیل معتبر نیست'
                  ]"
                  autocomplete="email"
                >
                  <template v-slot:prepend>
                    <q-icon name="business_center" color="secondary" />
                  </template>
                </q-input>
              </div>

              <div class="form-group">
                <label class="form-label">رمز عبور</label>
                <q-input
                  v-model="formData.password"
                  :type="showPassword ? 'text' : 'password'"
                  outlined
                  class="custom-input"
                  placeholder="رمز عبور امن انتخاب کنید"
                  :rules="[
                    val => !!val || 'لطفا رمز عبور را وارد کنید',
                    val => val.length >= 8 || 'رمز عبور باید حداقل ۸ کاراکتر باشد'
                  ]"
                  autocomplete="new-password"
                >
                  <template v-slot:prepend>
                    <q-icon name="security" color="secondary" />
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

              <div class="form-group">
                <label class="form-label">تکرار رمز عبور</label>
                <q-input
                  v-model="formData.password2"
                  :type="showPassword2 ? 'text' : 'password'"
                  outlined
                  class="custom-input"
                  placeholder="رمز عبور را تأیید کنید"
                  :rules="[
                    val => !!val || 'لطفا تکرار رمز عبور را وارد کنید',
                    val => val === formData.password || 'رمزهای عبور مطابقت ندارند'
                  ]"
                  autocomplete="new-password"
                >
                  <template v-slot:prepend>
                    <q-icon name="verified_user" color="secondary" />
                  </template>
                  <template v-slot:append>
                    <q-btn
                      :icon="showPassword2 ? 'visibility_off' : 'visibility'"
                      flat
                      round
                      dense
                      @click="showPassword2 = !showPassword2"
                      class="password-toggle"
                    />
                  </template>
                </q-input>
              </div>

              <div v-if="errorMessage" class="error-message">
                <q-icon name="error" class="error-icon" />
                <span class="error-text">{{ errorMessage }}</span>
              </div>

              <q-btn
                type="submit"
                class="submit-btn business-btn"
                :loading="loading"
                unelevated
                size="lg"
              >
                <q-icon name="business" class="q-ml-sm" />
                ثبت نام کسب‌وکار
              </q-btn>
            </q-form>
          </q-tab-panel>
        </q-tab-panels>

        <!-- Social Login Section -->
        <div class="social-section">
          <div class="divider">
            <span class="divider-text">یا</span>
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
            قبلاً ثبت نام کرده‌اید؟
            <a href="#" @click.prevent="switchToLogin" class="login-link">
              وارد شوید
            </a>
          </div>
        </div>
      </div>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { ref, watch } from 'vue';
import { GoogleLogin } from 'vue3-google-login';
import { useAuthStore } from 'stores/auth-store';
import { useQuasar } from 'quasar';
import { api } from 'boot/axios';

defineProps({
  modelValue: Boolean,
});
const emit = defineEmits(['update:modelValue', 'switchToLogin']);

const tab = ref('user');
const formData = ref({ username: '', email: '', password: '', password2: '' });
const loading = ref(false);
const errorMessage = ref('');
const googleErrorMessage = ref('');
const showPassword = ref(false);
const showPassword2 = ref(false);

const authStore = useAuthStore();
const $q = useQuasar();

// Reset form when tab changes
watch(tab, () => {
  formData.value = { username: '', email: '', password: '', password2: '' };
  errorMessage.value = '';
  showPassword.value = false;
  showPassword2.value = false;
});

async function handleRegister() {
  errorMessage.value = '';
  loading.value = true;

  const registrationPayload = {
    username: formData.value.username,
    email: formData.value.email,
    password1: formData.value.password,
    password2: formData.value.password2,
    // Optional: send flag based on active tab
    // is_business_registration: tab.value === 'business'
  };

  const result = await authStore.register(registrationPayload);
  loading.value = false;

  if (result.success) {
    $q.notify({
      type: 'positive',
      message: 'ثبت نام با موفقیت انجام شد! لطفاً وارد شوید.',
      position: 'top',
      icon: 'check_circle',
      timeout: 3000
    });
    switchToLogin();
  } else {
    errorMessage.value = result.message || "خطای نامشخص در ثبت نام.";
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

    if (!key || !user) {
      throw new Error('پاسخ سرور معتبر نیست.');
    }

    await authStore.setTokenAndUser({ access: key, user: user });
    $q.notify({
      type: 'positive',
      message: 'ورود/ثبت نام با گوگل موفقیت‌آمیز بود!',
      icon: 'check_circle',
      timeout: 3000
    });
    emit('update:modelValue', false);
  } catch (error) {
    console.error("Google login/register error:", error);
    googleErrorMessage.value = 'خطا در ارتباط با سرور.';
  }
};

function switchToLogin() {
  emit('update:modelValue', false);
  emit('switchToLogin');
}
</script>

<style scoped lang="scss">
/* --- استایل‌های راست‌چین --- */
.register-dialog {
  direction: rtl;
}
.header-text, .panel-text {
  text-align: right;
}
.form-label {
  text-align: right;
}
.error-message {
  flex-direction: row-reverse;
}
.error-text {
  text-align: right;
}
.dialog-footer {
  text-align: right;
}
/* -------------------------- */

.register-dialog {
  min-width: 500px;
  max-width: 550px;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(27, 94, 32, 0.2);
  background: linear-gradient(135deg, #dcedc8 0%, #ffffff 100%);

  /* --- تغییرات اصلی برای اسکرول --- */
  display: flex;
  flex-direction: column;
  max-height: 90vh;
  /* ------------------------------ */

  @media (max-width: 600px) {
    min-width: 90vw;
    max-width: 95vw;
    margin: 1rem;
    max-height: 95vh;
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
    background: linear-gradient(135deg, #10cf19 0%, #537954 100%);
    z-index: 1;
  }

  .header-content {
    position: relative;
    z-index: 2;
    padding: 2rem;
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
        margin: 0 0 0.5rem 0;
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

.tab-section {
  padding: 0;
  background: linear-gradient(90deg, #179d0996 0%, #ffffff 100%);
  border-bottom: 1px solid #aed581;
}

/* --- تغییرات اصلی برای اسکرول --- */
.form-container {
  flex: 1;
  overflow-y: auto;
  padding: 0;
  background: linear-gradient(135deg, #e8f5e8 0%, #ffffff 100%);
}
/* ------------------------------ */

.tab-panel {
  padding: 1.5rem 2rem;
}

.panel-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #c8e6c9;
}

.registration-form .form-group {
  margin-bottom: 1.2rem;
}

.dialog-footer {
  padding: 1rem 2rem 1.5rem;
}

/* --- بقیه استایل‌ها --- */
.custom-tabs .custom-tab {
  padding: 1rem 1.5rem;
  transition: all 0.3s ease;
  border-radius: 0;
  background: transparent;

  &.tab-active {
    background: linear-gradient(135deg, #2e7d32, #388e3c);
    color: white;

    .tab-content {
      color: white;
    }
  }

  .tab-content {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 600;
    color: #000000;
    transition: color 0.3s ease;
  }
}

.panel-header .panel-icon {
  background: rgba(139, 195, 74, 0.2);
  border-radius: 50%;
  padding: 0.75rem;
}

.panel-header .panel-text {
  flex: 1;
}

.panel-header .panel-text .panel-title {
  margin: 0 0 0.25rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #000000;
}

.panel-header .panel-text .panel-description {
  margin: 0;
  color: #000000;
  opacity: 0.8;
  font-size: 0.9rem;
}

.registration-form .form-group .form-label {
  display: block;
  font-weight: 600;
  color: #000000;
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
}

.registration-form .form-group .custom-input :deep(.q-field__control) {
  border-radius: 12px;
  border: 2px solid #aed581;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.9);
}

.registration-form .form-group .custom-input :deep(.q-field__control:hover) {
  border-color: #66bb6a;
}

.registration-form .form-group .custom-input :deep(.q-field--focused .q-field__control) {
  border-color: #4caf50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.2);
}

.registration-form .form-group .custom-input :deep(.q-field__prepend .q-icon) {
  transition: all 0.3s ease;
}

.registration-form .form-group .custom-input :deep(.q-field--focused .q-field__prepend .q-icon) {
  transform: scale(1.1);
}

.registration-form .form-group .password-toggle {
  color: #000000;
}

.registration-form .form-group .password-toggle:hover {
  color: #4caf50;
  background: rgba(76, 175, 80, 0.1);
}

.registration-form .error-message {
  padding: 0.75rem 1rem;
  background: rgba(244, 67, 54, 0.1);
  border: 1px solid rgba(244, 67, 54, 0.3);
  border-radius: 8px;
  margin-bottom: 1rem;
}

.registration-form .error-message .error-icon {
  color: #f44336;
  font-size: 18px;
}

.registration-form .error-message .error-text {
  color: #f44336;
  font-size: 0.9rem;
  white-space: pre-line;
}

.registration-form .submit-btn {
  width: 100%;
  padding: 1rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
  color: #000000;
}

.registration-form .submit-btn.user-btn {
  background: linear-gradient(135deg, #4caf50, #66bb6a);
}

.registration-form .submit-btn.user-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(76, 175, 80, 0.4);
}

.registration-form .submit-btn.business-btn {
  background: linear-gradient(135deg, #388e3c, #4caf50);
}

.registration-form .submit-btn.business-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(56, 142, 60, 0.4);
}

.social-section {
  padding: 1.5rem 2rem 1rem;
}

.social-section .divider {
  position: relative;
  text-align: center;
  margin-bottom: 1.5rem;
}

.social-section .divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: #aed581;
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

.dialog-footer .footer-text {
  color: #000000;
  font-size: 0.95rem;
}

.dialog-footer .footer-text .login-link {
  color: #08810e;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.3s ease;
  margin-right: 5px;
}

.dialog-footer .footer-text .login-link:hover {
  color: #2e7d32;
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
  box-shadow: 0 4px 12px rgba(2, 33, 3, 0.2);
}

:deep(.q-loading) {
  background: rgba(220, 237, 200, 0.9);
  backdrop-filter: blur(5px);
}

@media (max-width: 600px) {
  .dialog-header .header-content {
    padding: 1.5rem;
  }
  .dialog-header .header-content .header-text .dialog-title {
    font-size: 1.25rem;
  }
  .tab-panel {
    padding: 1.5rem;
  }
  .panel-header {
    flex-direction: column;
    text-align: center;
    gap: 0.75rem;
  }
  .social-section {
    padding: 1rem 1.5rem;
  }
  .dialog-footer {
    padding: 1rem 1.5rem 1.5rem;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

:deep(.q-tab-panel) {
  padding: 0;
}

:deep(.q-tab-panels) {
  background: transparent;
}
</style>
