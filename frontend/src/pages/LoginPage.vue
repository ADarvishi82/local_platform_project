<template>
  <q-page class="flex flex-center bg-grey-2 q-pa-md">
    <q-card class="q-pa-md shadow-2" style="min-width: 400px; max-width: 500px;">
      <q-card-section class="text-center">
        <q-avatar size="100px" font-size="52px" color="primary" text-color="white" icon="login" />
        <div class="text-grey-9 text-h5 text-weight-bold q-mt-md">ورود به حساب کاربری</div>
        <div class="text-grey-8">برای ادامه وارد شوید</div>
      </q-card-section>

      <q-card-section>
        <q-form @submit.prevent="handleLogin" class="q-gutter-md">
          <q-input
            filled
            v-model="loginIdentifier"
            label="نام کاربری یا ایمیل"
            lazy-rules
            :rules="[val => !!val || 'لطفا نام کاربری یا ایمیل را وارد کنید']"
            outlined
            autocomplete="username"
            name="username"
          />
          <q-input
            filled
            type="password"
            v-model="password"
            label="رمز عبور"
            lazy-rules
            :rules="[val => !!val || 'لطفا رمز عبور را وارد کنید']"
            outlined
            autocomplete="current-password"
            name="password"
          />
          <div v-if="errorMessage" class="text-negative q-mb-sm text-caption">
            <q-icon name="warning" class="q-mr-xs" />{{ errorMessage }}
          </div>
          <q-btn
            label="ورود"
            type="submit"
            color="primary"
            class="full-width q-py-sm"
            :loading="loading"
            unelevated
            size="lg"
          />
        </q-form>
      </q-card-section>

      <q-card-section>
        <q-separator class="q-my-md" inset><span class="text-grey-7">یا</span></q-separator>
        <div class="column items-center q-gutter-y-sm">
          <!-- کامپوننت جدید برای لاگین با گوگل -->
          <GoogleLogin :callback="handleGoogleLoginCallback" />
          <div v-if="googleErrorMessage" class="text-negative q-mt-sm text-caption full-width text-center">
            {{ googleErrorMessage }}
          </div>
        </div>
      </q-card-section>

      <q-card-section class="text-center q-pt-none">
        <div class="text-grey-8">
          حساب کاربری ندارید؟
          <router-link to="/register" class="text-secondary text-weight-bold" style="text-decoration: none">
            ثبت نام کنید
          </router-link>
        </div>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref } from 'vue';
import { GoogleLogin } from 'vue3-google-login'; // <<<< ایمپورت کامپوننت جدید
import { useAuthStore } from 'stores/auth-store';
import { useRouter } from 'vue-router';
import { useQuasar } from 'quasar';
import { api } from 'boot/axios';

const loginIdentifier = ref('');
const password = ref('');
const loading = ref(false);
const errorMessage = ref('');
const googleErrorMessage = ref(''); // خطای جداگانه برای گوگل

const authStore = useAuthStore();
const router = useRouter();
const $q = useQuasar();

// تابع برای لاگین معمولی
async function handleLogin() {
  errorMessage.value = '';
  loading.value = true;
  const credentials = { username: loginIdentifier.value, password: password.value };
  const result = await authStore.login(credentials);
  loading.value = false;
  if (result.success) {
    $q.notify({ type: 'positive', message: 'ورود با موفقیت انجام شد!', position: 'top' });
    router.push('/');
  } else {
    errorMessage.value = result.message || "خطای نامشخص در ورود.";
  }
}

// تابع callback برای لاگین با گوگل
const handleGoogleLoginCallback = async (response) => {
  googleErrorMessage.value = '';
  console.log("Google response received:", response);

  if (!response.credential) {
    googleErrorMessage.value = 'پاسخ معتبری از گوگل دریافت نشد.';
    console.error("Credential not found in Google response");
    return;
  }

  try {
    // ارسال id_token (که در فیلد credential است) به بک‌اند
    const backendResponse = await api.post('/api/auth/google/', {
      id_token: response.credential,
    });

    const { key, user, refresh_token } = backendResponse.data;
    if (!key || !user) { throw new Error('پاسخ سرور معتبر نیست.'); }    if (!key || !user) {
      throw new Error('پاسخ سرور برای ورود با گوگل معتبر نیست.');
    }

    // استفاده از اکشن setTokenAndUser برای لاگین کردن کاربر
    await authStore.setTokenAndUser({
    access: key,
    refresh: refresh_token,
    user: user
  });

    $q.notify({ type: 'positive', message: 'ورود با گوگل موفقیت‌آمیز بود!' });
    router.push('/');

  } catch (error) {
    console.error("Google login backend error:", error.response?.data || error);
    googleErrorMessage.value = 'خطا در ارتباط با سرور. لطفاً دوباره تلاش کنید.';
    authStore.logout();
  }
};
</script>

<style scoped>
/* استایل‌های لازم */
</style>
