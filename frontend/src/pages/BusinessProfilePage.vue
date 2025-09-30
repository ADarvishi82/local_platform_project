<!-- src/pages/BusinessProfilePage.vue -->
<template>
  <q-page class="business-profile-page">
    <!-- Header Section -->
    <div class="page-header">
      <div class="container">
        <div class="header-content">
          <div class="header-icon">
            <q-icon name="business" size="48px" color="primary" />
          </div>
          <div class="header-text">
            <h1 class="page-title">
              {{ editingProfile ? 'ویرایش پروفایل کسب‌وکار' : 'ایجاد پروفایل کسب‌وکار' }}
            </h1>
            <p class="page-subtitle">
              اطلاعات کسب‌وکار یا سازمان خود را به‌روزرسانی کنید و در نقشه نمایش دهید
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="page-content">
      <div class="container">
        <div class="form-wrapper">
          <q-stepper
            v-model="currentStep"
            ref="stepper"
            color="primary"
            animated
            flat
            bordered
            class="custom-stepper"
          >
            <!-- Step 1: Basic Information -->
            <q-step
              :name="1"
              title="اطلاعات پایه"
              icon="info"
              :done="currentStep > 1"
              class="step-content"
            >
              <div class="step-wrapper">
                <div class="step-header">
                  <q-icon name="info" size="24px" color="primary" />
                  <span class="step-title">اطلاعات اصلی کسب‌وکار</span>
                </div>

                <div class="form-grid">
                  <div class="form-group">
                    <label class="form-label">نوع حساب</label>
                    <q-select
                      v-model="profileData.account_type"
                      :options="accountTypeOptions"
                      emit-value
                      map-options
                      outlined
                      class="custom-select"
                      :rules="[val => !!val || 'لطفا نوع حساب را انتخاب کنید']"
                    >
                      <template v-slot:prepend>
                        <q-icon name="account_circle" color="primary" />
                      </template>
                    </q-select>
                  </div>

                  <div class="form-group">
                    <label class="form-label">نام کسب‌وکار/سازمان</label>
                    <q-input
                      v-model="profileData.business_name"
                      outlined
                      class="custom-input"
                      placeholder="نام کسب‌وکار خود را وارد کنید"
                      :rules="[val => !!val || 'لطفا نام را وارد کنید']"
                    >
                      <template v-slot:prepend>
                        <q-icon name="business" color="primary" />
                      </template>
                    </q-input>
                  </div>

                  <div class="form-group">
                    <label class="form-label">دسته‌بندی</label>
                    <q-select
                      v-model="profileData.category_id"
                      :options="categoryOptions"
                      emit-value
                      map-options
                      option-value="id"
                      option-label="name"
                      use-input
                      hide-selected
                      fill-input
                      @filter="filterCategoryFn"
                      :loading="categoriesLoading"
                      outlined
                      class="custom-select"
                      placeholder="دسته‌بندی مناسب را انتخاب کنید"
                      :rules="[val => !!val || 'لطفا دسته‌بندی را انتخاب کنید']"
                    >
                      <template v-slot:prepend>
                        <q-icon name="category" color="primary" />
                      </template>
                      <template v-slot:no-option>
                        <q-item>
                          <q-item-section class="text-grey-6">
                            <div class="flex items-center">
                              <q-icon name="search_off" class="q-mr-sm" />
                              نتیجه‌ای یافت نشد
                            </div>
                          </q-item-section>
                        </q-item>
                      </template>
                    </q-select>
                  </div>

                  <div class="form-group full-width">
                    <label class="form-label">تگ‌ها</label>
                    <q-select
                      v-model="profileData.tag_ids"
                      :options="tagOptions"
                      multiple
                      emit-value
                      map-options
                      option-value="id"
                      option-label="name"
                      use-chips
                      use-input
                      hide-selected
                      fill-input
                      @filter="filterTagFn"
                      :loading="tagsLoading"
                      outlined
                      class="custom-select"
                      placeholder="تگ‌های مرتبط با کسب‌وکار خود را انتخاب کنید"
                    >
                      <template v-slot:prepend>
                        <q-icon name="local_offer" color="primary" />
                      </template>
                    </q-select>
                  </div>

                  <div class="form-group full-width">
                    <label class="form-label">توضیحات</label>
                    <q-input
                      v-model="profileData.description"
                      type="textarea"
                      outlined
                      class="custom-textarea"
                      placeholder="توضیحات کاملی از کسب‌وکار خود ارائه دهید..."
                      rows="4"
                    >
                      <template v-slot:prepend>
                        <q-icon name="description" color="primary" />
                      </template>
                    </q-input>
                  </div>
                </div>

                <div class="step-navigation">
                  <q-btn
                    color="primary"
                    icon-right="arrow_forward"
                    label="مرحله بعد"
                    @click="nextStep"
                    unelevated
                    size="lg"
                    class="nav-btn"
                  />
                </div>
              </div>
            </q-step>

            <!-- Step 2: Location Information -->
            <q-step
              :name="2"
              title="اطلاعات مکانی"
              icon="location_on"
              :done="currentStep > 2"
              class="step-content"
            >
              <div class="step-wrapper">
                <div class="step-header">
                  <q-icon name="location_on" size="24px" color="primary" />
                  <span class="step-title">موقعیت جغرافیایی</span>
                </div>

                <div class="location-section">
                  <!-- Address Search -->
                  <div class="address-search-section">
                    <label class="form-label">جستجوی آدرس</label>
                    <q-input
                      v-model="profileData.address_string"
                      outlined
                      class="address-input"
                      placeholder="آدرس خود را جستجو کنید یا از روی نقشه انتخاب کنید"
                      :rules="[val => !!val || 'لطفا آدرس را وارد کنید']"
                      @keyup.enter="geocodeAddress"
                    >
                      <template v-slot:prepend>
                        <q-icon name="search" color="primary" />
                      </template>
                      <template v-slot:append>
                        <q-btn
                          round
                          dense
                          flat
                          icon="search"
                          color="primary"
                          @click="geocodeAddress"
                          :loading="geocodingLoading"
                          class="search-btn"
                        >
                          <q-tooltip>جستجوی آدرس</q-tooltip>
                        </q-btn>
                      </template>
                    </q-input>
                  </div>

                  <!-- Map Section -->
                  <div class="map-section">
                    <div class="map-header">
                      <div class="map-title">
                        <q-icon name="map" class="q-mr-sm" />
                        موقعیت را روی نقشه مشخص کنید
                      </div>
                      <q-btn
                        flat
                        round
                        icon="my_location"
                        color="primary"
                        @click="getCurrentLocation"
                        class="location-btn"
                      >
                        <q-tooltip>موقعیت فعلی من</q-tooltip>
                      </q-btn>
                    </div>

                    <div class="map-container">
                      <GoogleMap
                        :api-key="googleMapsApiKey"
                        style="width: 100%; height: 100%"
                        :center="mapCenter"
                        :zoom="mapZoom"
                        @click="handleMapClick"
                        ref="mapRef"
                        :options="mapOptions"
                      >
                        <Marker
                          :options="markerOptions"
                          @dragend="handleMarkerDragEnd"
                        />
                      </GoogleMap>

                      <!-- Map Overlay Instructions -->
                      <div class="map-instructions">
                        <q-icon name="info" />
                        <span>روی نقشه کلیک کنید یا مارکر را جابجا کنید</span>
                      </div>
                    </div>
                  </div>

                  <!-- Coordinates Display -->
                  <div class="coordinates-section">
                    <div class="coordinate-item">
                      <q-input
                        v-model.number="profileData.latitude"
                        label="عرض جغرافیایی"
                        type="number"
                        step="any"
                        readonly
                        outlined
                        class="coordinate-input"
                      >
                        <template v-slot:prepend>
                          <q-icon name="explore" color="primary" />
                        </template>
                      </q-input>
                    </div>
                    <div class="coordinate-item">
                      <q-input
                        v-model.number="profileData.longitude"
                        label="طول جغرافیایی"
                        type="number"
                        step="any"
                        readonly
                        outlined
                        class="coordinate-input"
                      >
                        <template v-slot:prepend>
                          <q-icon name="explore" color="primary" />
                        </template>
                      </q-input>
                    </div>
                  </div>
                </div>

                <div class="step-navigation">
                  <q-btn
                    flat
                    icon="arrow_back"
                    label="مرحله قبل"
                    @click="prevStep"
                    class="nav-btn-secondary"
                  />
                  <q-btn
                    color="primary"
                    icon-right="arrow_forward"
                    label="مرحله بعد"
                    @click="nextStep"
                    unelevated
                    size="lg"
                    class="nav-btn"
                  />
                </div>
              </div>
            </q-step>

            <!-- Step 3: Contact Information -->
            <q-step
              :name="3"
              title="اطلاعات تماس"
              icon="contact_phone"
              class="step-content"
            >
              <div class="step-wrapper">
                <div class="step-header">
                  <q-icon name="contact_phone" size="24px" color="primary" />
                  <span class="step-title">راه‌های ارتباطی</span>
                </div>

                <div class="contact-grid">
                  <div class="form-group">
                    <label class="form-label">شماره تلفن</label>
                    <q-input
                      v-model="profileData.phone_number"
                      outlined
                      class="custom-input"
                      placeholder="09123456789"
                      mask="###########"
                    >
                      <template v-slot:prepend>
                        <q-icon name="phone" color="primary" />
                      </template>
                    </q-input>
                  </div>

                  <div class="form-group">
                    <label class="form-label">وب‌سایت</label>
                    <q-input
                      v-model="profileData.website"
                      type="url"
                      outlined
                      class="custom-input"
                      placeholder="https://example.com"
                    >
                      <template v-slot:prepend>
                        <q-icon name="language" color="primary" />
                      </template>
                    </q-input>
                  </div>
                </div>

                <!-- Form Actions -->
                <div class="form-actions">
                  <q-btn
                    flat
                    icon="arrow_back"
                    label="مرحله قبل"
                    @click="prevStep"
                    class="nav-btn-secondary"
                  />

                  <div class="action-buttons">
                    <q-btn
                      :label="editingProfile ? 'ذخیره تغییرات' : 'ایجاد پروفایل'"
                      @click="handleSubmit"
                      color="primary"
                      :loading="formLoading"
                      unelevated
                      size="lg"
                      icon="save"
                      class="submit-btn"
                    />
                    <q-btn
                      label="پاک کردن فرم"
                      color="negative"
                      @click="resetForm"
                      unelevated
                      size="lg"
                      icon="clear"
                      outline
                      class="reset-btn"
                    />
                  </div>
                </div>
              </div>
            </q-step>
          </q-stepper>
        </div>
      </div>
    </div>

    <!-- Loading Overlay -->
    <q-loading :showing="formLoading" />
  </q-page>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import { useAuthStore } from 'stores/auth-store';
import { api } from 'boot/axios';
import { useRouter } from 'vue-router';
import { useQuasar } from 'quasar';
import { GoogleMap, Marker } from 'vue3-google-map';

const authStore = useAuthStore();
const router = useRouter();
const $q = useQuasar();

// Stepper control
const currentStep = ref(1);
const stepper = ref(null);

const editingProfile = ref(null);
const formLoading = ref(false);
const geocodingLoading = ref(false);

const profileData = ref({
  account_type: 'BUSINESS',
  business_name: '',
  category_id: null,
  tag_ids: [],
  description: '',
  address_string: '',
  latitude: null,
  longitude: null,
  phone_number: '',
  website: '',
});

const accountTypeOptions = [
  { label: 'کسب‌وکار عادی', value: 'BUSINESS' },
  { label: 'سازمان/اداره', value: 'ORGANIZATION' },
];

// Categories and Tags
const categories = ref([]);
const categoryOptions = ref([]);
const categoriesLoading = ref(false);
const tags = ref([]);
const tagOptions = ref([]);
const tagsLoading = ref(false);

// Google Maps
const googleMapsApiKey = 'AIzaSyDnWWhRvds75DoC8HIVwhq4rAlzZQkGGrI';
const mapRef = ref(null);
const mapCenter = ref({ lat: 35.6892, lng: 51.3890 });
const mapZoom = ref(12);
const markerPosition = ref({ lat: 35.6892, lng: 51.3890 });

// Map options for better styling
const mapOptions = {
  styles: [
    {
      featureType: "poi",
      elementType: "labels",
      stylers: [{ visibility: "off" }]
    }
  ],
  mapTypeControl: false,
  streetViewControl: false,
  fullscreenControl: false,
};

// Marker options
const markerOptions = computed(() => ({
  position: markerPosition.value,
  draggable: true,
  animation: window.google?.maps?.Animation?.DROP,
}));

// Stepper Navigation
function nextStep() {
  if (currentStep.value < 3) {
    currentStep.value++;
  }
}

function prevStep() {
  if (currentStep.value > 1) {
    currentStep.value--;
  }
}

// Map Functions
function handleMapClick(event) {
  if (event.latLng) {
    const lat = event.latLng.lat();
    const lng = event.latLng.lng();
    markerPosition.value = { lat, lng };
    profileData.value.latitude = lat;
    profileData.value.longitude = lng;
    reverseGeocode(lat, lng);
  }
}

function handleMarkerDragEnd(event) {
  if (event.latLng) {
    const lat = event.latLng.lat();
    const lng = event.latLng.lng();
    markerPosition.value = { lat, lng };
    profileData.value.latitude = lat;
    profileData.value.longitude = lng;
    reverseGeocode(lat, lng);
  }
}

async function geocodeAddress() {
  if (!profileData.value.address_string) return;
  geocodingLoading.value = true;

  try {
    if (window.google && window.google.maps && window.google.maps.Geocoder) {
      const geocoder = new window.google.maps.Geocoder();
      geocoder.geocode({ address: profileData.value.address_string, region: 'IR' }, (results, status) => {
        if (status === 'OK' && results[0]) {
          const location = results[0].geometry.location;
          const lat = location.lat();
          const lng = location.lng();
          mapCenter.value = { lat, lng };
          markerPosition.value = { lat, lng };
          profileData.value.latitude = lat;
          profileData.value.longitude = lng;
          mapZoom.value = 17;
        } else {
          $q.notify({ type: 'negative', message: `خطا در یافتن آدرس: ${status}` });
        }
        geocodingLoading.value = false;
      });
    }
  } catch (error) {
    console.error("Error geocoding address", error);
    $q.notify({ type: 'negative', message: 'خطا در پردازش درخواست جستجوی آدرس' });
    geocodingLoading.value = false;
  }
}

async function reverseGeocode(lat, lng) {
  if (window.google && window.google.maps && window.google.maps.Geocoder) {
    const geocoder = new window.google.maps.Geocoder();
    geocoder.geocode({ location: { lat, lng } }, (results, status) => {
      if (status === 'OK' && results[0]) {
        profileData.value.address_string = results[0].formatted_address;
      }
    });
  }
}

function getCurrentLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      position => {
        const lat = position.coords.latitude;
        const lng = position.coords.longitude;
        mapCenter.value = { lat, lng };
        markerPosition.value = { lat, lng };
        profileData.value.latitude = lat;
        profileData.value.longitude = lng;
        mapZoom.value = 15;
        reverseGeocode(lat, lng);
        $q.notify({ type: 'positive', message: 'موقعیت فعلی شما تشخیص داده شد' });
      },
      () => {
        $q.notify({ type: 'warning', message: 'دسترسی به موقعیت مکانی امکان‌پذیر نیست' });
      }
    );
  }
}

// Categories and Tags Functions
async function fetchCategories() {
  categoriesLoading.value = true;
  try {
    const response = await api.get('/api/categories/');
    categories.value = response.data;
    categoryOptions.value = response.data;
  } catch (error) {
    console.error('Error fetching categories:', error);
    $q.notify({ type: 'negative', message: 'خطا در دریافت دسته‌بندی‌ها' });
  } finally {
    categoriesLoading.value = false;
  }
}

function filterCategoryFn(val, update) {
  if (val === '') {
    update(() => {
      categoryOptions.value = categories.value;
    });
    return;
  }

  update(() => {
    const needle = val.toLowerCase();
    categoryOptions.value = categories.value.filter(
      category => category.name.toLowerCase().indexOf(needle) > -1
    );
  });
}

async function fetchTags() {
  tagsLoading.value = true;
  try {
    const response = await api.get('/api/tags/');
    tags.value = response.data;
    tagOptions.value = response.data;
  } catch (error) {
    console.error('Error fetching tags:', error);
    $q.notify({ type: 'negative', message: 'خطا در دریافت تگ‌ها' });
  } finally {
    tagsLoading.value = false;
  }
}

function filterTagFn(val, update) {
  if (val === '') {
    update(() => {
      tagOptions.value = tags.value;
    });
    return;
  }

  update(() => {
    const needle = val.toLowerCase();
    tagOptions.value = tags.value.filter(
      tag => tag.name.toLowerCase().indexOf(needle) > -1
    );
  });
}

async function fetchMyBusinessProfile() {
  if (!authStore.isAuthenticated || !authStore.user) {
    router.push('/login');
    return;
  }

  formLoading.value = true;
  try {
    const response = await api.get('/api/business-profiles/my-business/');
    if (response.data && response.data.id) {
      editingProfile.value = response.data;
      profileData.value.account_type = response.data.account_type;
      profileData.value.business_name = response.data.business_name;
      profileData.value.category_id = response.data.category?.id || null;
      profileData.value.tag_ids = response.data.tags?.map(tag => tag.id) || [];
      profileData.value.description = response.data.description;
      profileData.value.address_string = response.data.address_string;
      profileData.value.latitude = response.data.latitude;
      profileData.value.longitude = response.data.longitude;
      profileData.value.phone_number = response.data.phone_number;
      profileData.value.website = response.data.website;

      if (response.data.latitude && response.data.longitude) {
        const lat = response.data.latitude;
        const lng = response.data.longitude;
        mapCenter.value = { lat, lng };
        markerPosition.value = { lat, lng };
        mapZoom.value = 17;
      }
    } else {
      editingProfile.value = null;
      getCurrentLocation();
    }
  } catch (error) {
    console.error("Error fetching profile", error);
    $q.notify({ type: 'negative', message: 'خطا در دریافت اطلاعات پروفایل' });
  } finally {
    formLoading.value = false;
  }
}

async function handleSubmit() {
  formLoading.value = true;
  try {
    const data = { ...profileData.value };
    if (editingProfile.value) {
      await api.put(`/api/business-profiles/${editingProfile.value.id}/`, data);
      $q.notify({
        type: 'positive',
        message: 'پروفایل با موفقیت بروزرسانی شد',
        icon: 'check_circle'
      });
    } else {
      await api.post('/api/business-profiles/', data);
      $q.notify({
        type: 'positive',
        message: 'پروفایل با موفقیت ایجاد شد',
        icon: 'check_circle'
      });
    }
    router.push('/profile');
  } catch (error) {
    console.error('Error submitting profile:', error);
    $q.notify({
      type: 'negative',
      message: 'خطا در ذخیره پروفایل',
      icon: 'error'
    });
  } finally {
    formLoading.value = false;
  }
}

function resetForm() {
  profileData.value = {
    account_type: 'BUSINESS',
    business_name: '',
    category_id: null,
    tag_ids: [],
    description: '',
    address_string: '',
    latitude: null,
    longitude: null,
    phone_number: '',
    website: '',
  };
  mapCenter.value = { lat: 35.6892, lng: 51.3890 };
  markerPosition.value = { lat: 35.6892, lng: 51.3890 };
  mapZoom.value = 12;
  currentStep.value = 1;
}

onMounted(() => {
  if (!authStore.isAuthenticated) {
    router.push('/login');
    return;
  }
  fetchCategories();
  fetchTags();
  fetchMyBusinessProfile();
});

watch(() => authStore.isAuthenticated, (newAuthStatus) => {
  if (!newAuthStatus) {
    router.push('/login');
  }
});
</script>

<style scoped lang="scss">
.business-profile-page {
  background: linear-gradient(135deg, #08ae24 0%, #88cf79 100%);
  min-height: 100vh;
}

.page-header {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem;
  }

  .header-content {
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    color: white;

    .header-icon {
      margin-bottom: 1rem;
    }

    .page-title {
      font-size: 2.5rem;
      font-weight: 700;
      margin: 0 0 0.5rem 0;
      text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }

    .page-subtitle {
      font-size: 1.1rem;
      opacity: 0.9;
      margin: 0;
    }
  }
}

.page-content {
  padding: 2rem 0;

  .container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 0 1rem;
  }
}

.form-wrapper {
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.custom-stepper {
  border: none;
  box-shadow: none;

  :deep(.q-stepper__header) {
    background: linear-gradient(90deg, #f8f9ff 0%, #f0f4ff 100%);
    border-bottom: 1px solid #e1e5e9;
  }

  /* --- FIX START --- */
  :deep(.q-stepper__tab) {
    padding: 1.5rem;
  }

  :deep(.q-stepper__tab--active) {
    color: var(--q-primary);
  }
  /* --- FIX END --- */
}

.step-content {
  padding: 0;
}

.step-wrapper {
  padding: 2rem;
}

.step-header {
  display: flex;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f0f4ff;

  .step-title {
    font-size: 1.5rem;
    font-weight: 600;
    margin-right: 0.75rem;
    color: #2c3e50;
  }
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.form-group {
  &.full-width {
    grid-column: 1 / -1;
  }
}

.form-label {
  display: block;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
}

.custom-input,
.custom-select,
.custom-textarea {
  :deep(.q-field__control) {
    border-radius: 12px;
    border: 2px solid #e1e5e9;
    transition: all 0.3s ease;

    &:hover {
      border-color: var(--q-primary);
    }
  }

  :deep(.q-field--focused .q-field__control) {
    border-color: var(--q-primary);
    box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.1);
  }
}

.location-section {
  margin-bottom: 2rem;
}

.address-search-section {
  margin-bottom: 1.5rem;

  .address-input {
    :deep(.q-field__control) {
      border-radius: 12px;
      border: 2px solid #e1e5e9;
    }
  }
}

.map-section {
  margin-bottom: 1.5rem;

  .map-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;

    .map-title {
      display: flex;
      align-items: center;
      font-weight: 600;
      color: #2c3e50;
      font-size: 1.1rem;
    }

    .location-btn {
      background: rgba(25, 118, 210, 0.1);
      color: var(--q-primary);

      &:hover {
        background: rgba(25, 118, 210, 0.2);
      }
    }
  }

  .map-container {
    position: relative;
    height: 400px;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    border: 3px solid #f0f4ff;

    .map-instructions {
      position: absolute;
      top: 1rem;
      left: 1rem;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(10px);
      padding: 0.75rem 1rem;
      border-radius: 8px;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 0.85rem;
      color: #666;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
      z-index: 1;
    }
  }
}

.coordinates-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;

  .coordinate-item {
    .coordinate-input {
      :deep(.q-field__control) {
        border-radius: 8px;
        background: #f8f9ff;
      }
    }
  }
}

.contact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.step-navigation {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 1rem;
  padding-top: 2rem;
  border-top: 1px solid #f0f4ff;
}

.nav-btn {
  min-width: 150px;
  border-radius: 10px;
  font-weight: 600;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(45deg, var(--q-primary), #4fc3f7);

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(25, 118, 210, 0.3);
  }
}

.nav-btn-secondary {
  color: #666;
  border-radius: 10px;

  &:hover {
    background: #f5f5f5;
  }
}

.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 2rem;
  border-top: 1px solid #f0f4ff;

  .action-buttons {
    display: flex;
    gap: 1rem;
  }

  .submit-btn {
    min-width: 180px;
    border-radius: 12px;
    font-weight: 600;
    padding: 1rem 2rem;
    background: linear-gradient(45deg, #4caf50, #8bc34a);

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 20px rgba(76, 175, 80, 0.3);
    }
  }

  .reset-btn {
    min-width: 150px;
    border-radius: 12px;
    border: 2px solid #f44336;

    &:hover {
      background: rgba(244, 67, 54, 0.05);
    }
  }
}

// Responsive Design
@media (max-width: 768px) {
  .page-header {
    .header-content {
      .page-title {
        font-size: 2rem;
      }

      .page-subtitle {
        font-size: 1rem;
      }
    }
  }

  .step-wrapper {
    padding: 1rem;
  }

  .form-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .contact-grid {
    grid-template-columns: 1fr;
  }

  .coordinates-section {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
    gap: 1rem;

    .action-buttons {
      width: 100%;

      .submit-btn,
      .reset-btn {
        flex: 1;
        min-width: auto;
      }
    }
  }

  .step-navigation {
    flex-direction: column;
    gap: 0.5rem;

    .nav-btn {
      width: 100%;
    }
  }
}

// Animation Classes
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

// Custom Scrollbar
:deep(.q-scrollarea__thumb) {
  background: var(--q-primary);
  border-radius: 4px;
}

// Loading Improvements
:deep(.q-loading) {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(5px);
}

// Chip Styling for Tags
:deep(.q-chip) {
  background: linear-gradient(45deg, var(--q-primary), #4fc3f7);
  color: white;
  border-radius: 20px;

  .q-chip__icon {
    color: rgba(255, 255, 255, 0.8);
  }
}

// Input Focus Effects
:deep(.q-field--focused) {
  .q-field__prepend {
    .q-icon {
      color: var(--q-primary) !important;
      transform: scale(1.1);
      transition: all 0.3s ease;
    }
  }
}

// Button Hover Effects
.q-btn {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

  &:hover:not(.q-btn--disable) {
    transform: translateY(-1px);
  }
}

// Card and Section Styling
.q-card {
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

// Notification Styling Overrides
:deep(.q-notification) {
  border-radius: 12px;
  backdrop-filter: blur(10px);
}

// Success State
.success-state {
  color: #4caf50;

  .q-icon {
    color: #4caf50;
  }
}

// Error State
.error-state {
  color: #f44336;

  .q-icon {
    color: #f44336;
  }
}
</style>
