<template>
  <q-page class="flex flex-center bg-grey-2 q-pa-md">
    <q-card class="q-pa-md shadow-2" style="min-width: 400px; max-width: 500px;">
      <q-card-section class="text-center">
        <q-avatar size="100px" font-size="52px" color="primary" text-color="white" icon="person_outline" />
        <div class="text-grey-9 text-h5 text-weight-bold q-mt-md">ثبت نام کاربر عادی</div>
        <div class="text-grey-8">برای پیوستن به جامعه محلی ما ثبت نام کنید.</div>
      </q-card-section>

      <q-card-section>
        <q-form @submit.prevent="handleRegister" class="q-gutter-md">
          <q-input filled v-model="formData.username" label="نام کاربری" lazy-rules :rules="[val => !!val || 'لطفا نام کاربری را وارد کنید']" outlined autocomplete="username" />
          <q-input filled v-model="formData.email" type="email" label="آدرس ایمیل" lazy-rules :rules="[ val => !!val || 'لطفا ایمیل را وارد کنید', val => /.+@.+\..+/.test(val) || 'ایمیل معتبر نیست' ]" outlined autocomplete="email" />
          <q-input filled type="password" v-model="formData.password" label="رمز عبور" lazy-rules :rules="[ val => !!val || 'لطفا رمز عبور را وارد کنید', val => val.length >= 8 || 'رمز عبور باید حداقل ۸ کاراکتر باشد' ]" outlined autocomplete="new-password" />
          <q-input filled type="password" v-model="formData.password2" label="تکرار رمز عبور" lazy-rules :rules="[ val => !!val || 'لطفا تکرار رمز عبور را وارد کنید', val => val === formData.password || 'رمزهای عبور مطابقت ندارند' ]" outlined autocomplete="new-password" />
          <div v-if="errorMessage" class="text-negative q-mb-sm text-caption" style="white-space: pre-line;">
            <q-icon name="warning" class="q-mr-xs" />{{ errorMessage }}
          </div>
          <q-btn label="ثبت نام کاربر عادی" type="submit" color="primary" class="full-width q-py-sm" :loading="loading" unelevated size="lg" />
        </q-form>
      </q-card-section>

      <q-card-section>
        <q-separator class="q-my-md" inset><span class="text-grey-7">یا</span></q-separator>
        <div class="column items-center q-gutter-y-sm">
          <!-- کامپوننت جدید برای ثبت نام با گوگل -->
          <GoogleLogin :callback="handleGoogleLoginCallback" />
          <div v-if="googleErrorMessage" class="text-negative q-mt-sm text-caption full-width text-center">
            {{ googleErrorMessage }}
          </div>
        </div>
      </q-card-section>

      <q-card-section class="text-center q-pt-none">
        <div class="text-grey-8">
          <router-link to="/register/business" class="text-secondary text-weight-bold" style="text-decoration: none">
            ثبت نام به عنوان کسب‌وکار یا سازمان
          </router-link>
        </div>
        <div class="text-grey-8 q-mt-sm">
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
import { ref } from 'vue';
import { GoogleLogin } from 'vue3-google-login';
import { useAuthStore } from 'stores/auth-store';
import { useRouter } from 'vue-router';
import { useQuasar } from 'quasar';
import { api } from 'boot/axios';

const formData = ref({ username: '', email: '', password: '', password2: '' });
const loading = ref(false);
const errorMessage = ref('');
const googleErrorMessage = ref('');

const authStore = useAuthStore();
const router = useRouter();
const $q = useQuasar();

async function handleRegister() {
  errorMessage.value = '';
  loading.value = true;
  const registrationPayload = {
      username: formData.value.username, email: formData.value.email,
      password1: formData.value.password, password2: formData.value.password2,
  };
  const result = await authStore.register(registrationPayload);
  loading.value = false;
  if (result.success) {
      $q.notify({ type: 'positive', message: 'ثبت نام با موفقیت انجام شد! لطفاً وارد شوید.' });
      router.push('/login');
  } else {
      errorMessage.value = result.message || "خطای نامشخص در ثبت نام.";
      $q.notify({ type: 'negative', message: errorMessage.value, html: true });
  }
}

// تابع callback برای لاگین با گوگل (مشابه LoginPage)
const handleGoogleLoginCallback = async (response) => {
  googleErrorMessage.value = '';
  if (!response.credential) {
    googleErrorMessage.value = 'پاسخ معتبری از گوگل دریافت نشد.';
    return;
  }
  try {
    const backendResponse = await api.post('/api/auth/google/', { // از users/urls.py می‌آید چون پیشوند /api/ دارد
    id_token: response.credential,});
    const { key, user, refresh_token } = backendResponse.data;
    if (!key || !user) { throw new Error('پاسخ سرور معتبر نیست.'); }
    await authStore.setTokenAndUser({
    access: key,
    refresh: refresh_token,
    user: user
  });
    $q.notify({ type: 'positive', message: 'ورود/ثبت نام با گوگل موفقیت‌آمیز بود!' });
    router.push('/');
  } catch (error) {
    console.error("Google login/register error:", error);
    googleErrorMessage.value = 'خطا در ارتباط با سرور.';
  }
};
</script>

<style scoped>
/* استایل‌های لازم */
</style>
