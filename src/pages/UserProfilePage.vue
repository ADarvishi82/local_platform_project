<template>
  <q-page class="enhanced-profile-page">
    <!-- Header Section -->
    <div class="page-header">
      <div class="container">
        <div class="header-content">
          <div class="header-text">
            <h1 class="header-title">پروفایل کاربری</h1>
            <p class="header-subtitle">مدیریت اطلاعات شخصی و پست‌های خود</p>
          </div>
          <div class="header-decoration">
            <q-icon name="account_circle" size="4rem" class="header-icon" />
          </div>
        </div>
      </div>
    </div>

    <div class="container q-pa-lg">
      <div class="row q-col-gutter-xl">
        <!-- Profile Information Column -->
        <div class="col-12 col-lg-5">
          <div class="profile-card-container">
            <q-card class="profile-card glass-effect">
              <div class="card-header">
                <div class="card-header-content">
                  <q-icon name="person" class="card-icon" />
                  <div>
                    <h3 class="card-title">اطلاعات پروفایل</h3>
                    <p class="card-subtitle">ویرایش اطلاعات شخصی خود</p>
                  </div>
                </div>
              </div>

              <q-card-section class="q-pa-lg">
                <!-- Profile Picture Section -->
                <div class="profile-picture-section">
                  <div class="profile-picture-container">
                    <q-avatar
                      size="120px"
                      class="profile-avatar"
                      :class="{ 'has-image': profilePicturePreviewUrl || (editingProfile && editingProfile.profile_picture_url) }"
                    >
                      <img
                        v-if="profilePicturePreviewUrl || (editingProfile && editingProfile.profile_picture_url)"
                        :src="profilePicturePreviewUrl || editingProfile.profile_picture_url"
                        alt="پروفایل"
                      />
                      <q-icon v-else name="person" size="4rem" color="grey-5" />
                    </q-avatar>
                    <q-btn
                      fab
                      mini
                      color="primary"
                      icon="photo_camera"
                      class="camera-btn"
                      @click="$refs.profilePictureInput.$el.click()"
                    />
                  </div>
                  <q-file
                    ref="profilePictureInput"
                    v-model="profilePictureFile"
                    accept=".jpg, .jpeg, .png"
                    style="display: none"
                    @update:model-value="handleProfilePictureUpload"
                  />
                </div>

                <q-form @submit.prevent="handleSubmit" class="profile-form">
                  <!-- Address Input -->
                  <div class="form-group">
                    <label class="form-label">
                      <q-icon name="location_on" class="label-icon" />
                      آدرس محل سکونت
                    </label>
                    <q-input
                      v-model="profileData.address_string"
                      outlined
                      autogrow
                      type="textarea"
                      placeholder="آدرس خود را وارد کنید..."
                      class="address-input"
                      @keyup.enter="geocodeAddress"
                    >
                      <template v-slot:append>
                        <q-btn
                          round
                          flat
                          icon="search"
                          color="primary"
                          @click="geocodeAddress"
                          :loading="geocodingLoading"
                          class="search-btn"
                        />
                      </template>
                    </q-input>
                  </div>

                  <!-- Map Section -->
                  <div class="form-group">
                    <label class="form-label">
                      <q-icon name="map" class="label-icon" />
                      موقعیت روی نقشه
                    </label>
                    <div class="map-container">
                      <GoogleMap
                        :api-key="googleMapsApiKey"
                        :center="mapCenter"
                        :zoom="mapZoom"
                        @click="handleMapClick"
                        ref="userMapRef"
                        class="google-map"
                      >
                        <Marker
                          :options="{ position: markerPosition, draggable: true }"
                          @dragend="handleMarkerDragEnd"
                        />
                      </GoogleMap>
                    </div>
                  </div>

                  <!-- Coordinates -->
                  <div class="coordinates-section">
                    <div class="row q-col-gutter-md">
                      <div class="col-6">
                        <q-input
                          v-model.number="profileData.latitude"
                          label="عرض جغرافیایی"
                          type="number"
                          step="any"
                          readonly
                          outlined
                          dense
                          class="coordinate-input"
                        />
                      </div>
                      <div class="col-6">
                        <q-input
                          v-model.number="profileData.longitude"
                          label="طول جغرافیایی"
                          type="number"
                          step="any"
                          readonly
                          outlined
                          dense
                          class="coordinate-input"
                        />
                      </div>
                    </div>
                  </div>

                  <!-- Submit Button -->
                  <div class="submit-section">
                    <q-btn
                      label="ذخیره تغییرات"
                      type="submit"
                      color="primary"
                      size="lg"
                      :loading="formLoading"
                      unelevated
                      class="submit-btn"
                      icon="save"
                    />
                  </div>
                </q-form>
              </q-card-section>
            </q-card>
          </div>
        </div>

        <!-- Posts Column -->
        <div class="col-12 col-lg-7">
          <div class="posts-section">
            <!-- Posts Header -->
            <div class="posts-header">
              <div class="posts-header-content">
                <div class="posts-title-section">
                  <q-icon name="article" class="posts-icon" />
                  <div>
                    <h3 class="posts-title">پست‌های من</h3>
                    <p class="posts-subtitle">مجموعه پست‌های منتشر شده</p>
                  </div>
                </div>
                <q-btn
                  label="پست جدید"
                  color="secondary"
                  icon="add_circle"
                  @click="openCreatePostModal"
                  unelevated
                  class="create-post-btn"
                />
              </div>
            </div>

            <!-- Posts Content -->
            <div class="posts-content">
              <!-- Loading State -->
              <div v-if="loadingPosts" class="loading-container">
                <q-spinner-dots color="primary" size="3rem" />
                <p class="loading-text">در حال بارگذاری پست‌ها...</p>
              </div>

              <!-- Empty State -->
              <div v-else-if="userPosts.length === 0" class="empty-state">
                <q-icon name="post_add" size="5rem" color="grey-4" />
                <h4 class="empty-title">هنوز پستی ندارید</h4>
                <p class="empty-subtitle">اولین پست خود را ایجاد کنید</p>
                <q-btn
                  label="ایجاد پست اول"
                  color="primary"
                  icon="add"
                  @click="openCreatePostModal"
                  unelevated
                  class="q-mt-md"
                />
              </div>

              <!-- Posts List -->
              <div v-else class="posts-list">
                <q-card
                  v-for="post in userPosts"
                  :key="post.id"
                  class="post-card"
                >
                  <!-- Post Image -->
                  <div v-if="post.images && post.images.length > 0" class="post-image-container">
                    <q-img
                      :src="post.images[0].image"
                      :ratio="16/9"
                      class="post-image"
                    >
                      <div class="image-overlay">
                        <q-icon name="image" size="2rem" color="white" />
                      </div>
                    </q-img>
                  </div>

                  <q-card-section class="post-content">
                    <div class="post-header">
                      <div class="post-meta">
                        <q-icon name="schedule" class="meta-icon" />
                        <span class="post-date">{{ formatDateTime(post.created_at) }}</span>
                      </div>
                      <q-btn-dropdown
                        flat
                        dense
                        round
                        icon="more_vert"
                        class="post-menu"
                      >
                        <q-list dense class="menu-list">
                          <q-item
                            clickable
                            v-close-popup
                            @click="openEditPostModal(post)"
                            class="menu-item"
                          >
                            <q-item-section avatar>
                              <q-icon name="edit" color="primary" />
                            </q-item-section>
                            <q-item-section>ویرایش</q-item-section>
                          </q-item>
                          <q-item
                            clickable
                            v-close-popup
                            @click="confirmDeletePost(post.id)"
                            class="menu-item delete-item"
                          >
                            <q-item-section avatar>
                              <q-icon name="delete" color="negative" />
                            </q-item-section>
                            <q-item-section>حذف</q-item-section>
                          </q-item>
                        </q-list>
                      </q-btn-dropdown>
                    </div>

                    <div class="post-text">
                      <p class="post-content-text">{{ post.content }}</p>
                    </div>
                  </q-card-section>
                </q-card>
              </div>
            </div>
          </div> <!-- <<-- تگ بسته نشده در اینجا اضافه شد -->
        </div>
      </div>
    </div>

    <!-- Post Edit Modal -->
    <PostEditModal
      v-model="showPostModal"
      :post-to-edit="selectedPost"
      @postSaved="onPostSaved"
    />
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from 'stores/auth-store';
import { api } from 'boot/axios';
import { useRoute, useRouter } from 'vue-router';
import { useQuasar } from 'quasar';
import { GoogleMap, Marker } from 'vue3-google-map';
import PostEditModal from 'components/PostEditModal.vue';
import { format, parseISO } from 'date-fns';

const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();
const $q = useQuasar();

// State برای فرم پروفایل
const editingProfile = ref(null);
const formLoading = ref(false);
const geocodingLoading = ref(false);
const profileData = ref({ address_string: '', latitude: null, longitude: null });
const profilePictureFile = ref(null);
const profilePicturePreviewUrl = ref('');

// State برای نقشه
const googleMapsApiKey = ref('AIzaSyDnWWhRvds75DoC8HIVwhq4rAlzZQkGGrI');
const userMapRef = ref(null);
const mapCenter = ref({ lat: 35.6892, lng: 51.3890 });
const mapZoom = ref(12);
const markerPosition = ref({ lat: 35.6892, lng: 51.3890 });

// State برای پست‌ها
const userPosts = ref([]);
const loadingPosts = ref(true);
const showPostModal = ref(false);
const selectedPost = ref(null);

function handleProfilePictureUpload(file) {
  if (file) {
    profilePicturePreviewUrl.value = URL.createObjectURL(file);
  } else {
    profilePicturePreviewUrl.value = '';
  }
}

async function fetchMyUserProfile() {
  formLoading.value = true;
  try {
    const response = await api.get('/api/user-profiles/me/');
    if (response.data && response.data.id) {
      editingProfile.value = response.data;
      profileData.value.address_string = response.data.address_string || '';
      profileData.value.latitude = response.data.latitude;
      profileData.value.longitude = response.data.longitude;
      profilePictureFile.value = null;
      profilePicturePreviewUrl.value = '';
      if (response.data.latitude && response.data.longitude) {
        const lat = response.data.latitude;
        const lng = response.data.longitude;
        mapCenter.value = { lat, lng };
        markerPosition.value = { lat, lng };
        mapZoom.value = 16;
      } else {
        initializeMapToUserLocationOrDefault();
      }
    } else {
      editingProfile.value = null;
      initializeMapToUserLocationOrDefault();
    }
  } catch (error) {
    if (error.response?.status === 404) {
      editingProfile.value = null;
      initializeMapToUserLocationOrDefault();
    } else {
      console.error("Error fetching user profile:", error);
      $q.notify({ type: 'negative', message: 'خطا در دریافت اطلاعات پروفایل' });
    }
  } finally {
    formLoading.value = false;
  }
}

async function handleSubmit() {
  formLoading.value = true;
  const formData = new FormData();
  if (profileData.value.address_string) formData.append('address_string', profileData.value.address_string);
  if (profileData.value.latitude !== null) formData.append('latitude', profileData.value.latitude);
  if (profileData.value.longitude !== null) formData.append('longitude', profileData.value.longitude);
  if (profilePictureFile.value) {
    formData.append('profile_picture', profilePictureFile.value);
  }
  try {
    if (editingProfile.value && editingProfile.value.id) {
      await api.patch(`/api/user-profiles/${editingProfile.value.id}/`, formData);
      $q.notify({
        type: 'positive',
        message: 'پروفایل با موفقیت ویرایش شد!',
        icon: 'check_circle'
      });
    } else {
      await api.post('/api/user-profiles/', formData);
      $q.notify({
        type: 'positive',
        message: 'پروفایل با موفقیت ایجاد شد!',
        icon: 'check_circle'
      });
    }
    const userResponse = await api.get('/api/auth/user/');
    if (userResponse.data) {
      authStore.updateUserInStore(userResponse.data);
    }
    fetchMyUserProfile();
  } catch (error) {
    console.error("Error submitting user profile:", error);
    $q.notify({
      type: 'negative',
      message: 'خطا در ذخیره اطلاعات پروفایل.',
      icon: 'error'
    });
  } finally {
    formLoading.value = false;
  }
}

function handleMapClick(event) {
  if (event.latLng) {
    const lat = event.latLng.lat();
    const lng = event.latLng.lng();
    markerPosition.value = { lat, lng };
    profileData.value.latitude = parseFloat(lat.toFixed(7));
    profileData.value.longitude = parseFloat(lng.toFixed(7));
    reverseGeocode(lat, lng);
  }
}

function handleMarkerDragEnd(event) {
  if (event.latLng) {
    const lat = event.latLng.lat();
    const lng = event.latLng.lng();
    markerPosition.value = { lat, lng };
    profileData.value.latitude = parseFloat(lat.toFixed(7));
    profileData.value.longitude = parseFloat(lng.toFixed(7));
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
          profileData.value.latitude = parseFloat(lat.toFixed(7));
          profileData.value.longitude = parseFloat(lng.toFixed(7));
          profileData.value.address_string = results[0].formatted_address;
          mapZoom.value = 17;
          if (userMapRef.value?.map) {
            userMapRef.value.map.setCenter({ lat, lng });
            userMapRef.value.map.setZoom(17);
          }
        } else {
          $q.notify({ type: 'negative', message: `خطا در یافتن آدرس: ${status}` });
        }
        geocodingLoading.value = false;
      });
    } else {
      $q.notify({ type: 'warning', message: 'سرویس Geocoding در دسترس نیست.' });
      geocodingLoading.value = false;
    }
  } catch (error) {
    console.error("Error geocoding address:", error);
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
      } else {
        console.warn(`Reverse geocoding failed: ${status}`);
      }
    });
  }
}

function initializeMapToUserLocationOrDefault() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(position => {
      const lat = position.coords.latitude;
      const lng = position.coords.longitude;
      mapCenter.value = { lat, lng };
      markerPosition.value = { lat, lng };
      profileData.value.latitude = parseFloat(lat.toFixed(7));
      profileData.value.longitude = parseFloat(lng.toFixed(7));
      mapZoom.value = 15;
      reverseGeocode(lat, lng);
    }, () => {
      console.warn("Geolocation failed or permission denied. Using default map center for UserProfile.");
      mapCenter.value = { lat: 35.6892, lng: 51.3890 };
      markerPosition.value = { lat: 35.6892, lng: 51.3890 };
      mapZoom.value = 12;
    });
  } else {
    console.warn("Geolocation not supported. Using default map center for UserProfile.");
    mapCenter.value = { lat: 35.6892, lng: 51.3890 };
    markerPosition.value = { lat: 35.6892, lng: 51.3890 };
    mapZoom.value = 12;
  }
}

async function fetchUserPosts() {
  if (!authStore.user?.pk) return;
  loadingPosts.value = true;
  try {
    const response = await api.get(`/api/users/${authStore.user.pk}/posts/`);
    userPosts.value = response.data.results || response.data;
  } catch (error) {
    console.error("Error fetching user posts:", error);
  } finally {
    loadingPosts.value = false;
  }
}

function openCreatePostModal() {
  selectedPost.value = null;
  showPostModal.value = true;
}

function openEditPostModal(post) {
  selectedPost.value = { ...post };
  showPostModal.value = true;
}

function onPostSaved(savedPost) {
  const index = userPosts.value.findIndex(p => p.id === savedPost.id);
  if (index !== -1) {
    userPosts.value[index] = savedPost;
  } else {
    userPosts.value.unshift(savedPost);
  }
}

function confirmDeletePost(postId) {
  $q.dialog({
    title: 'تأیید حذف پست',
    message: 'آیا از حذف این پست مطمئن هستید؟',
    cancel: true,
    persistent: true,
    color: 'negative'
  }).onOk(async () => {
    try {
      await api.delete(`/api/posts/${postId}/`);
      userPosts.value = userPosts.value.filter(p => p.id !== postId);
      $q.notify({
        type: 'positive',
        message: 'پست با موفقیت حذف شد.',
        icon: 'delete'
      });
    } catch (error) {
      console.error("Error deleting post:", error);
      $q.notify({
        type: 'negative',
        message: 'خطا در حذف پست.',
        icon: 'error'
      });
    }
  });
}

function formatDateTime(dateTimeString) {
  if (!dateTimeString) return '';
  try {
    return format(parseISO(dateTimeString), 'yyyy/MM/dd HH:mm');
  } catch (error) {
    console.error(`Could not format date: "${dateTimeString}"`, error);
    return dateTimeString;
  }
}

onMounted(() => {
  if (!authStore.isAuthenticated) {
    router.push({ name: 'login', query: { redirect: route.fullPath } });
  } else {
    fetchMyUserProfile();
    fetchUserPosts();
  }
});
</script>

<style scoped>
.enhanced-profile-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* Header Styles */
.page-header {
  background: linear-gradient(135deg, #66a267 0%, #08b406 100%);
  color: white;
  padding: 3rem 0 2rem;
  margin-bottom: 2rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 0.5rem;
  text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.header-subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin: 0;
}

.header-icon {
  opacity: 0.3;
  transform: rotate(-15deg);
}

/* Profile Card Styles */
.profile-card-container {
  position: sticky;
  top: 2rem;
}

.profile-card {
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
  border: none;
  overflow: hidden;
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.95);
}

.glass-effect {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(13, 183, 7, 0.2);
}

.card-header {
  background: linear-gradient(135deg, #08af26 0%, #60c462 100%);
  color: white;
  padding: 1.5rem;
}

.card-header-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.card-icon {
  font-size: 2rem;
  opacity: 0.9;
}

.card-title {
  font-size: 1.3rem;
  font-weight: 600;
  margin: 0 0 0.25rem;
}

.card-subtitle {
  font-size: 0.9rem;
  opacity: 0.8;
  margin: 0;
}

/* Profile Picture Styles */
.profile-picture-section {
  text-align: center;
  margin-bottom: 2rem;
}

.profile-picture-container {
  position: relative;
  display: inline-block;
}

.profile-avatar {
  border: 4px solid #f0f0f0;
  transition: all 0.3s ease;
  background: #fafafa;
}

.profile-avatar.has-image {
  border-color: #025f12;
  transform: scale(1.02);
}

.camera-btn {
  position: absolute;
  bottom: 0;
  right: 0;
  background: linear-gradient(135deg, #327409 0%, #5ca90a 100%);
  border: 2px solid white;
  transition: all 0.3s ease;
}

.camera-btn:hover {
  transform: scale(1.1);
}

/* Form Styles */
.profile-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: #555;
  margin-bottom: 0.75rem;
  font-size: 0.95rem;
}

.label-icon {
  color: #07a50c;
  font-size: 1.1rem;
}

.address-input {
  transition: all 0.3s ease;
}

.address-input:focus-within {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(7, 169, 20, 0.15);
}

.search-btn {
  transition: all 0.3s ease;
}

.search-btn:hover {
  transform: scale(1.1);
}

/* Map Styles */
.map-container {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 25px rgba(0,0,0,0.1);
  height: 300px;
  transition: all 0.3s ease;
}

.map-container:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 35px rgba(0,0,0,0.15);
}

.google-map {
  width: 100%;
  height: 100%;
}

/* Coordinates Styles */
.coordinates-section {
  margin-top: 1rem;
}

.coordinate-input {
  background: rgba(102, 126, 234, 0.05);
  border-radius: 8px;
}

/* Submit Button */
.submit-section {
  margin-top: 1rem;
}

.submit-btn {
  background: linear-gradient(135deg, #04ab0a 0%, #15a505 100%);
  border-radius: 12px;
  padding: 0.75rem 2rem;
  font-weight: 600;
  font-size: 1rem;
  width: 100%;
  transition: all 0.3s ease;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(9, 175, 3, 0.3);
}

/* Posts Section */
.posts-section {
  animation: fadeInUp 0.6s ease-out;
}

.posts-header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 8px 25px rgba(0,0,0,0.08);
}

.posts-header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.posts-title-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.posts-icon {
  font-size: 2rem;
  color: #07aa1a;
}

.posts-title {
  font-size: 1.4rem;
  font-weight: 600;
  margin: 0 0 0.25rem;
  color: #333;
}

.posts-subtitle {
  font-size: 0.9rem;
  color: #666;
  margin: 0;
}

.create-post-btn {
  background: linear-gradient(135deg, #08b60b 0%, #01a609 100%);
  border-radius: 25px;
  padding: 0.5rem 1.5rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.create-post-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(21, 176, 4, 0.3);
}

/* Posts Content */
.posts-content {
  min-height: 400px;
}

/* Loading State */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 0;
  text-align: center;
}

.loading-text {
  margin-top: 1rem;
  color: #666;
  font-size: 1.1rem;
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 20px;
  backdrop-filter: blur(10px);
}

.empty-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 1rem 0 0.5rem;
  color: #555;
}

.empty-subtitle {
  color: #888;
  font-size: 1rem;
  margin: 0;
}

/* Posts List */
.posts-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.post-card {
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 25px rgba(0,0,0,0.08);
  border: none;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  animation: fadeInUp 0.5s ease-out;
}

.post-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 35px rgba(0,0,0,0.12);
}

/* Post Image */
.post-image-container {
  position: relative;
  overflow: hidden;
}

.post-image {
  transition: all 0.3s ease;
}

.post-card:hover .post-image {
  transform: scale(1.02);
}

.image-overlay {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(0,0,0,0.5);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: all 0.3s ease;
}

.post-card:hover .image-overlay {
  opacity: 1;
}

/* Post Content */
.post-content {
  padding: 1.5rem;
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.post-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #666;
  font-size: 0.9rem;
}

.meta-icon {
  font-size: 1rem;
  color: #999;
}

.post-date {
  font-weight: 500;
}

.post-menu {
  transition: all 0.3s ease;
}

.post-menu:hover {
  background: rgba(6, 164, 27, 0.1);
  transform: scale(1.1);
}

.menu-list {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 8px 25px rgba(0,0,0,0.1);
}

.menu-item {
  transition: all 0.2s ease;
  padding: 0.75rem 1rem;
}

.menu-item:hover {
  background: rgba(12, 199, 40, 0.05);
  transform: translateX(4px);
}

.delete-item:hover {
  background: rgba(7, 172, 5, 0.05);
}

/* Post Text */
.post-text {
  margin-top: 0.5rem;
}

.post-content-text {
  line-height: 1.6;
  color: #13c50d;
  font-size: 1rem;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Animations */
@keyframes fadeInUp {
  0% {
    opacity: 0;
    transform: translateY(30px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* Responsive Design */
@media (max-width: 1023px) {
  .profile-card-container {
    position: static;
  }

  .page-header {
    padding: 2rem 0 1.5rem;
  }

  .header-title {
    font-size: 2rem;
  }

  .header-decoration {
    display: none;
  }
}

@media (max-width: 767px) {
  .container {
    padding: 0 0.5rem;
  }

  .posts-header-content {
    flex-direction: column;
    align-items: stretch;
  }

  .create-post-btn {
    align-self: center;
  }

  .post-content {
    padding: 1rem;
  }

  .coordinates-section .row {
    gap: 0.5rem;
  }
}

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #18a006 0%, #05ae19 100%);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #059d0f 0%, #069c15 100%);
}

/* Focus States */
.q-field--focused .q-field__control {
  box-shadow: 0 0 0 2px rgba(1, 182, 23, 0.2);
}

/* Button Hover Effects */
.q-btn {
  transition: all 0.3s ease;
}

.q-btn:hover {
  transform: translateY(-1px);
}

/* Card Transitions */
.q-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
</style>
