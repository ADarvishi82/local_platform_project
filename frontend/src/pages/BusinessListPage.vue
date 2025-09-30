<template>
  <q-page class="business-list-page q-pa-md">
    <div class="container">
      <!-- Header Section -->
      <div class="page-header q-mb-lg">
        <h4 class="page-title q-ma-none">خدمات محلی</h4>
        <p class="page-subtitle text-grey-7 q-ma-none q-mt-xs">بهترین خدمات و کسب‌وکارهای محله خود را پیدا کنید.</p>
      </div>

      <!-- Categories Section -->
      <div class="categories-bar q-mb-lg">
        <q-btn unelevated color="primary" label="همه خدمات" icon="apps" class="category-btn" @click="selectCategory(null)" :outline="filters.category_name !== null" />
        <q-btn
          v-for="cat in categories"
          :key="cat.id"
          unelevated
          :label="cat.name"
          :icon="getCategoryIcon(cat.name)"
          class="category-btn"
          @click="selectCategory(cat.name)"
          :outline="filters.category_name !== cat.name"
          :color="filters.category_name === cat.name ? 'primary' : 'grey-7'"
        />
      </div>

      <!-- Filter Sidebar - Moved Above Grid -->
      <q-card class="filter-sidebar q-mb-lg" flat bordered>
        <q-card-section>
          <div class="text-h6">فیلترها</div>
        </q-card-section>
        <q-separator />
        <q-card-section>
          <div class="row q-col-gutter-lg">
            <div class="col-12 col-sm-6 col-md-3">
              <div class="text-subtitle2 q-mb-sm">محله</div>
              <q-select v-model="filters.neighborhood" :options="neighborhoodOptions" label="همه محله‌ها" filled dense emit-value map-options option-value="id" option-label="name" clearable :loading="loadingNeighborhoods" />
            </div>
            <div class="col-12 col-sm-6 col-md-3">
              <div class="text-subtitle2 q-mb-sm">محدوده قیمت (تومان)</div>
              <q-range v-model="priceRange" :min="0" :max="5000000" :step="50000" label-always class="q-px-sm" />
              <div class="row justify-between text-caption q-mt-sm">
                <span>{{ priceRange.min.toLocaleString() }}</span>
                <span>{{ priceRange.max.toLocaleString() }}</span>
              </div>
            </div>
            <div class="col-12 col-sm-6 col-md-3">
              <div class="text-subtitle2 q-mb-sm">امتیاز</div>
              <q-select v-model="filters.min_rating" :options="ratingOptions" label="همه امتیازها" filled dense emit-value map-options option-value="value" option-label="label" clearable />
            </div>
            <div class="col-12 col-sm-6 col-md-3 flex items-end">
              <div class="row q-gutter-sm full-width">
                <q-btn label="اعمال فیلتر" color="primary" @click="applyFilters" unelevated class="col" :loading="loadingBusinesses" />
                <q-btn label="پاک کردن" @click="resetFilters" flat class="col-auto" />
              </div>
            </div>
          </div>
        </q-card-section>
      </q-card>

      <!-- Main Content -->
      <div>
        <!-- Sort & Count Header -->
        <div class="row items-center q-mb-md">
          <div class="text-subtitle1 text-grey-8">{{ totalBusinesses }} خدمت یافت شد</div>
          <q-space />
          <q-select v-model="sortBy" :options="sortOptions" label="مرتب‌سازی" filled dense emit-value map-options style="min-width: 180px;" @update:model-value="applyFilters" />
        </div>

        <!-- States (Loading, Error, Empty) -->
        <div v-if="loadingBusinesses" class="text-center q-py-xl"><q-spinner-dots color="primary" size="3em" /></div>
        <div v-else-if="errorBusinesses" class="text-center q-py-xl text-negative">خطا در دریافت اطلاعات.</div>
        <div v-else-if="businesses.length === 0" class="text-center q-py-xl text-grey">هیچ خدمتی با این مشخصات یافت نشد.</div>

        <!-- Businesses Grid -->
        <div v-else class="row q-col-gutter-md">
          <div v-for="biz in businesses" :key="biz.id" class="col-12 col-sm-6 col-lg-4">
            <q-card class="business-card full-height cursor-pointer" @click="goToBusinessDetail(biz.id)">
              <q-img :src="biz.logo_url || 'https://cdn.quasar.dev/img/material.png'" :ratio="4/3">
                <q-chip v-if="biz.category" :label="biz.category.name" color="white" text-color="primary" class="absolute-bottom-left q-ma-sm" size="sm" />
              </q-img>
              <q-card-section>
                <div class="row items-center no-wrap">
                  <div class="col">
                    <div class="text-h6 ellipsis">{{ biz.business_name }}</div>
                    <div class="text-caption text-grey-7 ellipsis"><q-icon name="location_on" size="xs" /> {{ biz.neighborhood ? biz.neighborhood.name : 'نامشخص' }}</div>
                  </div>
                  <div v-if="biz.rating_count > 0" class="col-auto text-right">
                    <q-rating v-model="biz.average_rating" :max="5" size="16px" color="orange" icon="star" readonly />
                    <div class="text-caption text-grey-7 q-ml-xs">({{ biz.rating_count }})</div>
                  </div>
                </div>
              </q-card-section>
              <q-card-section class="q-pt-none">
                <div class="text-h6 text-green-8 text-weight-bold">
                  {{ biz.price_string || 'تماس بگیرید' }}
                </div>
              </q-card-section>
              <q-separator />
              <q-card-actions class="q-px-md q-py-sm">
                <q-avatar size="30px">
                  <img v-if="biz.user.profile?.profile_picture_url" :src="biz.user.profile.profile_picture_url">
                  <q-icon v-else name="account_circle" />
                </q-avatar>
                <span class="q-ml-sm text-grey-8">{{ biz.user.username }}</span>
                <q-space />
                <q-btn label="جزئیات" color="primary" flat dense :to="`/business/${biz.id}`" />
                <q-btn label="رزرو" color="primary" unelevated dense />
              </q-card-actions>
            </q-card>
          </div>
        </div>

        <!-- Pagination -->
        <div class="q-pa-lg flex flex-center" v-if="totalPages > 1">
          <q-pagination v-model="currentPage" :max="totalPages" @update:model-value="applyFilters" direction-links />
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { api } from 'boot/axios';
import { useRouter } from 'vue-router';

const router = useRouter();

const businesses = ref([]);
const loadingBusinesses = ref(true);
const errorBusinesses = ref(false);
const totalBusinesses = ref(0);

const filters = ref({
  neighborhood: null,
  min_price: 0,
  max_price: 5000000,
  min_rating: null,
  category_name: null,
});
const priceRange = ref({ min: 0, max: 5000000 });
const ratingOptions = [
  { label: 'همه امتیازها', value: null },
  { label: '۵ ستاره', value: 5 },
  { label: '۴ ستاره و بیشتر', value: 4 },
  { label: '۳ ستاره و بیشتر', value: 3 },
];
const sortBy = ref('-created_at'); // مرتب‌سازی پیش‌فرض
const sortOptions = [
  { label: 'جدیدترین', value: '-created_at' },
  { label: 'محبوب‌ترین (امتیاز)', value: '-average_rating' },
  { label: 'ارزان‌ترین', value: 'base_price' },
  { label: 'گران‌ترین', value: '-base_price' },
];

const loadingNeighborhoods = ref(false);
const neighborhoodOptions = ref([]);
const categories = ref([]);

const currentPage = ref(1);
const totalPages = ref(1);

watch(priceRange, (newRange) => {
  filters.value.min_price = newRange.min;
  filters.value.max_price = newRange.max === 5000000 ? null : newRange.max;
});

// Watch for changes in sortBy to refetch data
watch(sortBy, () => {
  applyFilters();
});

async function fetchData() {
  loadingBusinesses.value = true;
  errorBusinesses.value = false;
  try {
    const params = {
      ...filters.value,
      ordering: sortBy.value,
      page: currentPage.value,
    };

    Object.keys(params).forEach(key => (params[key] === null || params[key] === '') && delete params[key]);

    const response = await api.get('/api/business-profiles/', { params });
    if (response.data && Array.isArray(response.data.results)) {
      businesses.value = response.data.results;
      totalBusinesses.value = response.data.count;
      totalPages.value = Math.ceil(totalBusinesses.value / (response.data.page_size || 10));
    } else if (Array.isArray(response.data)) {
      businesses.value = response.data;
      totalBusinesses.value = response.data.length;
      totalPages.value = 1;
    } else {
      console.warn("Invalid response structure for business list:", response.data);
      businesses.value = [];
      totalBusinesses.value = 0;
      totalPages.value = 1;
    }
  }
  catch (error) {
    console.error("Error fetching businesses:", error);
    errorBusinesses.value = true;
  } finally {
    loadingBusinesses.value = false;
  }
}

async function fetchNeighborhoodsForFilter() {
  loadingNeighborhoods.value = true;
  try {
    const response = await api.get('/api/neighborhoods/');
    neighborhoodOptions.value = response.data.results || response.data;
  } catch (error) {
    console.error("Error fetching neighborhoods for filter:", error);
  } finally {
    loadingNeighborhoods.value = false;
  }
}

async function fetchInitialData() {
  // Fetch categories for the top bar
  try {
    const catResponse = await api.get('/api/categories/');
    categories.value = catResponse.data.results || catResponse.data;
  } catch (e) { console.error(e); }

  // Fetch neighborhoods for the filter
  await fetchNeighborhoodsForFilter();
}

function applyFilters() {
  currentPage.value = 1;
  fetchData();
}

function resetFilters() {
  filters.value = { neighborhood: null, min_price: 0, max_price: 5000000, min_rating: null, category_name: null };
  priceRange.value = { min: 0, max: 5000000 };
  sortBy.value = '-created_at';
  applyFilters();
}

function selectCategory(categoryName) {
  filters.value.category_name = categoryName;
  applyFilters();
}

function getCategoryIcon(categoryName) {
  const icons = { 'باغبانی': 'yard', 'نظافت': 'cleaning_services', 'تعمیرات': 'build', 'پزشکی': 'local_hospital', 'حمل و نقل': 'local_shipping', 'آموزش': 'school', 'زیبایی': 'spa' };
  return icons[categoryName] || 'miscellaneous_services';
}

function goToBusinessDetail(bizId) {
  router.push(`/business/${bizId}`);
}

onMounted(() => {
  fetchData();
  fetchInitialData();
});
</script>

<style lang="scss" scoped>
.business-list-page { background-color: #f8f9fa; }
.container { max-width: 1200px; margin: 0 auto; }
.page-header { border-bottom: 1px solid #e0e0e0; padding-bottom: 1rem; }
.categories-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.category-btn {
  text-transform: none;
  font-weight: 500;
}
.filter-sidebar {
  border-radius: 12px;
  border: 1px solid #e0e0e0;
}
.business-card {
  transition: all 0.3s ease;
  border-radius: 12px;
  border: 1px solid #e0e0e0;
}
.business-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
  border-color: var(--q-primary);
}
</style>
