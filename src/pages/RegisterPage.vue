<template>
  <q-page class="flex flex-center bg-grey-2 q-pa-md">
    <q-card class="q-pa-md shadow-2" style="min-width: 400px; max-width: 500px;">
      <q-card-section class="text-center">
        <q-avatar size="100px" font-size="52px" color="secondary" text-color="white" icon="person_add" />
        <div class="text-grey-9 text-h5 text-weight-bold q-mt-md">ایجاد حساب کاربری جدید</div>
        <div class="text-grey-8">اطلاعات خود را وارد کنید</div>
      </q-card-section>

      <q-card-section>
        <q-form @submit.prevent="handleRegister" class="q-gutter-md">
          <q-input
            filled
            v-model="username"
            label="نام کاربری"
            lazy-rules
            :rules="[val => !!val || 'لطفا نام کاربری را وارد کنید']"
            outlined
            autocomplete="username"
            name="username"
          />

          <q-input
            filled
            v-model="email"
            type="email"
            label="آدرس ایمیل"
            lazy-rules
            :rules="[
              val => !!val || 'لطفا ایمیل را وارد کنید',
              val => /.+@.+\..+/.test(val) || 'ایمیل معتبر نیست'
            ]"
            outlined
            autocomplete="email"
            name="email"
          />

          <q-input
            filled
            type="password"
            v-model="password"
            label="رمز عبور"
            lazy-rules
            :rules="[
              val => !!val || 'لطفا رمز عبور را وارد کنید',
              val => val.length >= 8 || 'رمز عبور باید حداقل ۸ کاراکتر باشد'
            ]"
            outlined
            autocomplete="new-password"
            name="password_first"
          />

          <q-input
            filled
            type="password"
            v-model="password2"
            label="تکرار رمز عبور"
            lazy-rules
            :rules="[
              val => !!val || 'لطفا تکرار رمز عبور را وارد کنید',
              val => val === password || 'رمزهای عبور مطابقت ندارند'
            ]"
            outlined
            autocomplete="new-password"
            name="password_confirmation"
          />

          <div v-if="errorMessage" class="text-negative q-mb-sm text-caption" style="white-space: pre-line;">
            <q-icon name="warning" class="q-mr-xs" />{{ errorMessage }}
          </div>

          <q-btn
            label="ثبت نام"
            type="submit"
            color="secondary"
            class="full-width q-py-sm"
            :loading="loading"
            unelevated
            size="lg"
          />
        </q-form>
      </q-card-section>

      <!-- بخش اضافه شده برای گوگل -->
      <q-card-section>
        <q-separator class="q-my-md" />
        <div class="row items-center justify-center">
          <q-btn
            label="ادامه با گوگل"
            @click="handleGoogleLogin"
            color="red"
            unelevated
            icon="img:https://developers.google.com/identity/images/g-logo.png"
            :loading="googleLoading"
          />
        </div>
      </q-card-section>

      <q-card-section class="text-center q-pt-none">
        <div class="text-grey-8">
          قبلاً ثبت نام کرده‌اید؟
          <router-link to="/login" class="text-primary text-weight-bold" style="text-decoration: none">
            وارد شوید
          </router-link>
        </div>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref, inject } from 'vue';
import { useAuthStore } from 'stores/auth-store';
import { useRouter } from 'vue-router';
import { useQuasar } from 'quasar';
import api from 'src/boot/axios';

const username = ref('');
const email = ref('');
const password = ref('');
const password2 = ref('');
const loading = ref(false);
const errorMessage = ref('');
const googleLoading = ref(false);

const authStore = useAuthStore();
const router = useRouter();
const $q = useQuasar();
const VueGAuth = inject('VueGAuth');

function showNotification(type, message) {
  if ($q && typeof $q.notify === 'function') {
    $q.notify({ type, message, position: 'top', html: type === 'negative', timeout: type === 'negative' ? 7000 : 3000 });
  } else {
    console.warn(`Quasar Notify is not available. Type: ${type}, Message: ${message}`);
    if (type === 'negative' || type === 'warning') {
      errorMessage.value = message;
    }
  }
}

async function handleRegister() {
  errorMessage.value = '';

  if (!username.value || !email.value || !password.value || !password2.value) {
    showNotification('warning', 'لطفا تمام فیلدها را پر کنید.');
    return;
  }
  if (password.value !== password2.value) {
    showNotification('warning', 'رمزهای عبور مطابقت ندارند.');
    return;
  }
  if (password.value.length < 8) {
    showNotification('warning', 'رمز عبور باید حداقل ۸ کاراکتر باشد.');
    return;
  }

  loading.value = true;

  const registrationData = {
    username: username.value,
    email: email.value,
    password1: password.value,
    password2: password2.value,
  };

  const result = await authStore.register(registrationData);
  loading.value = false;

  if (result.success) {
    showNotification('positive', 'ثبت نام با موفقیت انجام شد! لطفاً وارد شوید.');
    router.push('/login');
  } else {
    showNotification('negative', result.message || 'خطای نامشخص در ثبت نام.');
  }
}

async function handleGoogleLogin() {
  googleLoading.value = true;
  try {
    const googleUser = await VueGAuth.signIn();
    if (!googleUser) throw new Error('Google sign in failed.');

    const accessToken = googleUser.getAuthResponse().access_token;
    const backendResponse = await api.post('/api/auth/google/', {
      access_token: accessToken,
    });

    const { key } = backendResponse.data;
    const user = backendResponse.data.user;

    await authStore.setTokenAndUser({ access: key, user });
    showNotification('positive', 'ورود با گوگل موفقیت‌آمیز بود!');
    router.push('/');
  } catch (error) {
    console.error("Google login error:", error);
    showNotification('negative', 'خطا در ورود با گوگل.');
    authStore.logout();
  } finally {
    googleLoading.value = false;
  }
}
</script>

<style scoped>
/* استایل‌های سفارشی خودت رو می‌تونی اینجا بنویسی */
</style>
