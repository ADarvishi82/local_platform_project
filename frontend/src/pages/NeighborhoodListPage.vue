<template>
  <q-page padding class="q-pa-md">
    <div class="row items-center justify-between q-mb-md">
      <div class="text-h5 text-primary">لیست محله‌ها</div>
      <!-- می‌توانید دکمه یا فیلترهایی در اینجا اضافه کنید -->
    </div>

    <q-separator class="q-mb-lg" />

    <div v-if="loading" class="row justify-center q-my-xl">
      <q-spinner-dots color="primary" size="3em" />
      <div class="q-ml-sm text-grey-7">در حال بارگذاری لیست محله‌ها...</div>
    </div>

    <div v-else-if="error" class="text-negative text-center q-my-xl">
      <q-icon name="error_outline" size="2em" class="q-mr-sm" />
      {{ errorMessage || 'خطا در دریافت اطلاعات محله‌ها.' }}
      <div class="q-mt-md">
        <q-btn label="تلاش مجدد" color="primary" @click="fetchNeighborhoods" unelevated icon="refresh" />
      </div>
    </div>

    <div v-else-if="neighborhoods.length === 0" class="text-grey-7 text-center q-my-xl">
      <q-icon name="explore_off" size="3em" class="q-mb-sm block" />
      در حال حاضر هیچ محله‌ای برای نمایش وجود ندارد.
    </div>

    <q-list v-else bordered separator>
      <q-item
        v-for="neighborhood in neighborhoods"
        :key="neighborhood.id"
        clickable
        v-ripple
        :to="`/neighborhood/${neighborhood.id}`"
        class="q-py-md"
      >
        <q-item-section avatar>
          <q-avatar color="secondary" text-color="white" icon="location_city" />
        </q-item-section>

        <q-item-section>
          <q-item-label class="text-subtitle1 text-weight-medium">{{ neighborhood.name }}</q-item-label>
          <q-item-label caption lines="1">شهر: {{ neighborhood.city }}</q-item-label>
          <!-- می‌توانید اطلاعات بیشتری مانند مختصات مرکز را هم اینجا نمایش دهید اگر لازم است -->
          <!-- <q-item-label caption lines="1" v-if="neighborhood.center_latitude && neighborhood.center_longitude">
            مرکز: {{ neighborhood.center_latitude.toFixed(4) }}, {{ neighborhood.center_longitude.toFixed(4) }}
          </q-item-label> -->
        </q-item-section>

        <q-item-section side top>
          <q-icon name="chevron_left" color="grey-6" />
        </q-item-section>
      </q-item>
    </q-list>

  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { api } from 'boot/axios'; // برای فراخوانی API
import { useQuasar } from 'quasar';

const neighborhoods = ref([]);
const loading = ref(true);
const error = ref(false);
const errorMessage = ref('');

const $q = useQuasar();

async function fetchNeighborhoods() {
  loading.value = true;
  error.value = false;
  errorMessage.value = '';
  try {
    console.log("NEIGHBORHOOD_LIST_PAGE: Fetching neighborhoods...");
    const response = await api.get('/api/neighborhoods/'); // API لیست محله‌ها

    // فرض می‌کنیم API شما مستقیماً آرایه‌ای از محله‌ها را برمی‌گرداند
    // اگر pagination دارید، باید response.data.results و غیره را استفاده کنید
    if (Array.isArray(response.data)) {
      neighborhoods.value = response.data;
    } else if (response.data && Array.isArray(response.data.results)) { // برای سازگاری با DRF pagination
      neighborhoods.value = response.data.results;
      // اینجا می‌توانید اطلاعات pagination را هم ذخیره کنید اگر لازم است
    } else {
      console.warn("NEIGHBORHOOD_LIST_PAGE: API response is not in expected format.", response.data);
      neighborhoods.value = []; // بازنشانی به آرایه خالی
    }

    console.log("NEIGHBORHOOD_LIST_PAGE: Neighborhoods fetched:", neighborhoods.value);
    if (neighborhoods.value.length === 0) {
        console.log("NEIGHBORHOOD_LIST_PAGE: No neighborhoods found.");
    }

  } catch (err) {
    console.error("NEIGHBORHOOD_LIST_PAGE: Error fetching neighborhoods:", err.response?.data || err.message);
    error.value = true;
    errorMessage.value = err.response?.data?.detail || 'خطا در دریافت لیست محله‌ها از سرور.';
    if ($q && typeof $q.notify === 'function') {
      $q.notify({ type: 'negative', message: errorMessage.value, position: 'top' });
    }
  } finally {
    loading.value = false;
  }
}

// تابع برای هدایت به صفحه جزئیات (اگر از @click به جای :to استفاده می‌کردید)
// function goToNeighborhoodDetail(neighborhoodId) {
//   router.push(`/neighborhood/${neighborhoodId}`);
// }

onMounted(() => {
  fetchNeighborhoods();
});
</script>

<style scoped>
.q-item__section--avatar {
  min-width: 40px; /* برای اندازه بهتر آواتار */
}
</style>