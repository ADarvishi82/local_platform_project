<template>
  <q-page padding class="q-pa-md">
    <div v-if="loading" class="row justify-center q-my-xl">
      <q-spinner-dots color="primary" size="3em" />
      <div class="q-ml-sm text-grey-7">در حال بارگذاری اطلاعات محله...</div>
    </div>

    <div v-else-if="error" class="text-negative text-center q-my-xl">
      <q-icon name="error_outline" size="2em" class="q-mr-sm" />
      {{ errorMessage || 'خطا در دریافت اطلاعات محله.' }}
      <div class="q-mt-md">
        <q-btn label="بازگشت به لیست محله‌ها" color="primary" to="/neighborhoods" unelevated icon="arrow_back" />
      </div>
    </div>

    <div v-else-if="!neighborhoodDetail" class="text-grey-7 text-center q-my-xl">
      <q-icon name="explore_off" size="3em" class="q-mb-sm block" />
      اطلاعاتی برای این محله یافت نشد.
      <div class="q-mt-md">
        <q-btn label="بازگشت به لیست محله‌ها" color="primary" to="/neighborhoods" unelevated icon="arrow_back" />
      </div>
    </div>

    <div v-else class="q-gutter-y-lg">
      <!-- Neighborhood Info Card -->
      <q-card flat bordered>
        <q-card-section>
          <div class="text-h4 q-mb-sm text-primary">
            <q-icon name="location_city" class="q-mr-sm" />
            {{ neighborhoodDetail.name }}
          </div>
          <div class="text-subtitle1 text-grey-8">شهر: {{ neighborhoodDetail.city }}</div>
          <div v-if="neighborhoodDetail.center_latitude && neighborhoodDetail.center_longitude" class="text-caption text-grey-7">
            مرکز محله: ({{ neighborhoodDetail.center_latitude.toFixed(4) }}, {{ neighborhoodDetail.center_longitude.toFixed(4) }})
          </div>
        </q-card-section>

        <q-separator />

        <q-card-section class="row items-center q-col-gutter-md">
          <div class="col-xs-12 col-sm-6 text-center">
            <q-avatar size="xl" color="green-2" text-color="green-8" icon="groups" />
            <div class="text-h6 q-mt-sm">{{ neighborhoodDetail.user_profile_count }}</div>
            <div class="text-caption text-grey-7">همسایه (کاربر ثبت شده)</div>
          </div>
          <div class="col-xs-12 col-sm-6 text-center">
            <q-avatar size="xl" color="orange-2" text-color="orange-8" icon="storefront" />
            <div class="text-h6 q-mt-sm">{{ neighborhoodDetail.business_profile_count }}</div>
            <div class="text-caption text-grey-7">کسب‌وکار و سازمان</div>
          </div>
        </q-card-section>
      </q-card>

      <!-- ============ Recommendation Section ============ -->
      <q-card flat bordered class="q-mb-lg">
        <q-card-section class="row items-center">
          <q-icon name="lightbulb_outline" color="amber-8" size="md" class="q-mr-md" />
          <div class="col">
            <div class="text-subtitle1">تحلیل نیازهای محله</div>
            <div class="text-caption text-grey-7">ببینید چه کسب‌وکارهایی بر اساس الگوهای موفق، در این محله پتانسیل رشد دارند.</div>
          </div>
          <div class="col-auto">
            <q-btn
              label="دریافت پیشنهاد"
              color="amber-8"
              @click="getRecommendations"
              :loading="loadingRecommendations"
              unelevated
              icon="insights"
            />
          </div>
        </q-card-section>
      </q-card>
      <!-- ============================================= -->

      <!-- Users in Neighborhood -->
      <q-card flat bordered v-if="neighborhoodDetail.user_profiles_in_neighborhood && neighborhoodDetail.user_profiles_in_neighborhood.length > 0">
        <q-card-section>
          <div class="text-h6">همسایه‌های این محله</div>
        </q-card-section>
        <q-list separator>
          <q-item v-for="profile in neighborhoodDetail.user_profiles_in_neighborhood" :key="`user-${profile.id}`">
            <q-item-section avatar>
              <q-avatar>
                <img :src="profile.profile_picture_url || 'https://cdn.quasar.dev/img/boy-avatar.png'">
              </q-avatar>
            </q-item-section>
            <q-item-section>
              <q-item-label>{{ profile.username }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-card>

      <!-- Businesses in Neighborhood -->
      <q-card flat bordered v-if="neighborhoodDetail.business_profiles_in_neighborhood && neighborhoodDetail.business_profiles_in_neighborhood.length > 0">
        <q-card-section>
          <div class="text-h6">کسب‌وکارهای این محله</div>
        </q-card-section>
        <q-list separator>
          <q-item
            v-for="business in neighborhoodDetail.business_profiles_in_neighborhood"
            :key="`biz-${business.id}`"
            clickable
            v-ripple
            :to="`/business/${business.id}`"
          >
            <q-item-section avatar v-if="business.logo_url">
              <q-avatar rounded>
                <img :src="business.logo_url">
              </q-avatar>
            </q-item-section>
            <q-item-section>
              <q-item-label>{{ business.business_name }}</q-item-label>
              <q-item-label caption v-if="business.category_name">{{ business.category_name }}</q-item-label>
            </q-item-section>
            <q-item-section side>
              <q-icon name="chevron_left" />
            </q-item-section>
          </q-item>
        </q-list>
      </q-card>

      <div class="q-mt-lg text-center">
        <q-btn label="بازگشت به لیست محله‌ها" color="primary" icon="arrow_back" to="/neighborhoods" unelevated />
      </div>

      <!-- ============ Recommendations Dialog ============ -->
      <q-dialog v-model="showRecommendationsDialog">
        <q-card style="min-width: 400px;">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6">کسب‌وکارهای پیشنهادی برای محله "{{ neighborhoodDetail.name }}"</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section v-if="loadingRecommendations" class="text-center q-py-xl">
            <q-spinner-dots color="primary" size="2em" />
            <div class="q-mt-sm">در حال تحلیل...</div>
          </q-card-section>

          <q-card-section v-else-if="recommendationError" class="text-negative text-center">
            {{ recommendationError }}
          </q-card-section>

          <q-card-section v-else-if="recommendations.length === 0" class="text-grey text-center">
            در حال حاضر پیشنهاد خاصی برای این محله یافت نشد.
          </q-card-section>

          <q-list v-else separator bordered>
            <q-item v-for="(rec, index) in recommendations" :key="rec.business_category">
              <q-item-section avatar>
                <q-avatar color="primary" text-color="white" :label="String(index + 1)" />
              </q-item-section>
              <q-item-section>
                <q-item-label class="text-weight-medium">{{ rec.business_category }}</q-item-label>
                <q-item-label caption>امتیاز پیشنهاد: {{ rec.score.toFixed(2) }}</q-item-label>
              </q-item-section>
              <q-item-section side>
                <q-icon name="trending_up" color="green" />
              </q-item-section>
            </q-item>
          </q-list>
        </q-card>
      </q-dialog>
      <!-- ============================================== -->

    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { api } from 'boot/axios';
import { useQuasar } from 'quasar';
import { useAuthStore } from 'stores/auth-store';

const props = defineProps({
  id: {
    type: [String, Number],
    required: true,
  },
});

const neighborhoodDetail = ref(null);
const loading = ref(true);
const error = ref(false);
const errorMessage = ref('');

// New refs for recommender system
const recommendations = ref([]);
const loadingRecommendations = ref(false);
const recommendationError = ref('');
const showRecommendationsDialog = ref(false);

const $q = useQuasar();
const authStore = useAuthStore();

async function fetchNeighborhoodDetail(neighborhoodId) {
  loading.value = true;
  error.value = false;
  errorMessage.value = '';
  try {
    const response = await api.get(`/api/neighborhoods/${neighborhoodId}/`);
    neighborhoodDetail.value = response.data;
  } catch (err) {
    error.value = true;
    if (err.response && err.response.status === 404) {
        errorMessage.value = 'محله مورد نظر یافت نشد.';
    } else {
        errorMessage.value = err.response?.data?.detail || 'خطا در دریافت اطلاعات از سرور.';
    }
    if ($q && typeof $q.notify === 'function') {
      $q.notify({ type: 'negative', message: errorMessage.value, position: 'top' });
    }
  } finally {
    loading.value = false;
  }
}

// New function to call the recommender API
async function getRecommendations() {
  if (!authStore.isAuthenticated) {
    $q.notify({ type: 'negative', message: 'برای استفاده از این قابلیت باید وارد شوید.' });
    return;
  }

  loadingRecommendations.value = true;
  recommendationError.value = '';
  showRecommendationsDialog.value = true;

  try {
    const response = await api.get('/api/recommendations/businesses/', {
      params: {
        neighborhood_id: props.id
      }
    });
    recommendations.value = response.data;
  } catch (err) {
    console.error("Error fetching recommendations:", err.response?.data || err);
    recommendationError.value = err.response?.data?.error || 'خطا در دریافت پیشنهادها.';
  } finally {
    loadingRecommendations.value = false;
  }
}

onMounted(() => {
  if (props.id) {
    fetchNeighborhoodDetail(props.id);
  } else {
    error.value = true;
    errorMessage.value = "شناسه محله نامعتبر است.";
    loading.value = false;
  }
});

watch(() => props.id, (newId) => {
  if (newId) {
    fetchNeighborhoodDetail(newId);
  }
});
</script>

<style scoped>
/* Scoped styles can be added here if needed */
</style>
