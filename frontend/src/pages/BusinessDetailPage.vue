<template>
  <q-page padding class="q-pa-md">
    <div v-if="loading" class="row justify-center q-my-xl">
      <q-spinner-dots color="primary" size="3em" />
      <div class="q-ml-sm text-grey-7">در حال بارگذاری اطلاعات کسب‌وکار...</div>
    </div>

    <div v-else-if="error" class="text-negative text-center q-my-xl">
      <q-icon name="error_outline" size="2em" class="q-mr-sm" />
      {{ errorMessage || 'خطا در دریافت اطلاعات کسب‌وکار.' }}
      <div class="q-mt-md">
        <q-btn label="بازگشت به لیست" color="primary" to="/businesses" unelevated />
      </div>
    </div>

    <div v-else-if="!businessDetail" class="text-grey-7 text-center q-my-xl">
      <q-icon name="storefront" size="3em" class="q-mb-sm block" />
      اطلاعاتی برای این کسب‌وکار یافت نشد.
      <div class="q-mt-md">
        <q-btn label="بازگشت به لیست" color="primary" to="/businesses" unelevated />
      </div>
    </div>

    <div v-else class="q-gutter-y-lg">
      <!-- Business Details Card -->
      <q-card flat bordered>
        <q-img
          v-if="businessDetail.logo"
          :src="businessDetail.logo"
          :ratio="16/9"
          style="max-height: 300px;"
        >
          <div class="absolute-bottom text-h6 bg-transparent text-shadow">
            {{ businessDetail.business_name }}
            <q-badge v-if="businessDetail.is_verified" color="green" class="q-ml-sm" title="تایید شده">
              <q-icon name="check_circle" color="white" size="xs" />
            </q-badge>
          </div>
        </q-img>
        <q-card-section v-else>
          <div class="text-h4 q-mb-sm">{{ businessDetail.business_name }}
            <q-badge v-if="businessDetail.is_verified" color="green" class="q-ml-sm" title="تایید شده">
              <q-icon name="check_circle" color="white" size="xs" />
            </q-badge>
          </div>
        </q-card-section>

        <q-card-section>
          <div class="text-subtitle1 text-primary" v-if="businessDetail.category">
            <q-icon name="category" /> {{ businessDetail.category.name }}
          </div>
          <div class="text-caption text-grey-7 q-mt-xs" v-if="businessDetail.account_type_display">
            نوع: {{ businessDetail.account_type_display }}
          </div>

          <q-separator class="q-my-md" />

          <div class="text-body1 q-mb-md" style="white-space: pre-line;">
            {{ businessDetail.description || 'توضیحاتی برای این کسب‌وکار ارائه نشده است.' }}
          </div>

          <div v-if="businessDetail.tags && businessDetail.tags.length > 0" class="q-mb-md">
            <span class="text-weight-medium">تگ‌ها:</span>
            <q-chip
              v-for="tag in businessDetail.tags"
              :key="tag.id"
              color="blue-grey-1"
              text-color="blue-grey-9"
              size="sm"
              class="q-ml-xs"
            >
              {{ tag.name }}
            </q-chip>
          </div>
        </q-card-section>
      </q-card>

      <!-- Contact & Address Card -->
      <q-card flat bordered>
        <q-card-section>
          <div class="text-h6">اطلاعات تماس و آدرس</div>
        </q-card-section>
        <q-list separator>
          <q-item v-if="businessDetail.address_string">
            <q-item-section avatar>
              <q-icon color="grey-7" name="location_on" />
            </q-item-section>
            <q-item-section>
              <q-item-label>آدرس</q-item-label>
              <q-item-label caption>{{ businessDetail.address_string }}</q-item-label>
            </q-item-section>
          </q-item>
          <q-item v-if="businessDetail.phone_number">
            <q-item-section avatar>
              <q-icon color="grey-7" name="phone" />
            </q-item-section>
            <q-item-section>
              <q-item-label>شماره تلفن</q-item-label>
              <q-item-label caption>
                <a :href="`tel:${businessDetail.phone_number}`" class="text-primary" style="text-decoration: none;">
                  {{ businessDetail.phone_number }}
                </a>
              </q-item-label>
            </q-item-section>
          </q-item>
          <q-item v-if="businessDetail.website">
            <q-item-section avatar>
              <q-icon color="grey-7" name="language" />
            </q-item-section>
            <q-item-section>
              <q-item-label>وب‌سایت</q-item-label>
              <q-item-label caption>
                <a :href="businessDetail.website" target="_blank" rel="noopener noreferrer" class="text-primary" style="text-decoration: none;">
                  {{ businessDetail.website }}
                </a>
              </q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-card>

      <!-- Map Card -->
      <q-card flat bordered v-if="businessDetail.latitude && businessDetail.longitude && googleMapsApiKey">
        <q-card-section>
          <div class="text-h6">موقعیت مکانی</div>
        </q-card-section>
        <q-card-section class="q-pa-none">
          <div style="height: 300px; width: 100%;">
            <GoogleMap
              :api-key="googleMapsApiKey"
              style="width: 100%; height: 100%"
              :center="{ lat: businessDetail.latitude, lng: businessDetail.longitude }"
              :zoom="16"
              :options="{ zoomControl: true, mapTypeControl: false, streetViewControl: false, fullscreenControl: false }"
            >
              <Marker :options="{ position: { lat: businessDetail.latitude, lng: businessDetail.longitude } }" />
            </GoogleMap>
          </div>
        </q-card-section>
      </q-card>

      <!-- Posts Section -->
      <div class="q-mt-xl">
        <div class="text-h6 q-mb-md">آخرین پست‌ها از {{ businessDetail.business_name }}</div>

        <div v-if="loadingPosts" class="text-center q-py-lg">
          <q-spinner-dots color="primary" size="2em" />
        </div>

        <div v-else-if="businessPosts.length === 0" class="text-center text-grey q-py-lg">
          <q-icon name="feed" size="2em" class="q-mb-sm block" />
          این کسب‌وکار هنوز پستی منتشر نکرده است.
        </div>

        <div v-else class="q-gutter-y-md">
          <q-card v-for="post in businessPosts" :key="post.id" flat bordered>
            <!-- Post Header -->
            <q-card-section class="post-header">
              <div class="row items-center no-wrap">
                <router-link :to="getProfileLink(post.author)" class="author-link">
                  <q-avatar size="50px">
                    <img v-if="getAuthorAvatar(post.author)" :src="getAuthorAvatar(post.author)" alt="Avatar">
                    <q-icon v-else name="account_circle" size="30px" />
                  </q-avatar>
                  <div class="author-info q-ml-md">
                    <div class="author-name">{{ post.author?.username || 'کاربر ناشناس' }}</div>
                    <div class="post-meta">{{ formatDateTime(post.created_at) }}</div>
                  </div>
                </router-link>
              </div>
            </q-card-section>

            <!-- Post Content -->
            <q-card-section v-if="post.content" class="post-content">
              <p style="white-space: pre-line;">{{ post.content }}</p>
            </q-card-section>

            <!-- Post Images -->
            <div v-if="post.images && post.images.length > 0" class="post-images">
              <q-carousel v-model="post.slide" animated arrows navigation infinite height="300px">
                <q-carousel-slide v-for="(img, index) in post.images" :key="img.id" :name="index" class="q-pa-none">
                  <q-img :src="img.image" class="full-height full-width cursor-pointer" @click="showImageGallery(post.images, index)" />
                </q-carousel-slide>
              </q-carousel>
            </div>

            <!-- Post Actions -->
            <q-separator />
            <q-card-actions class="post-actions">
              <q-btn flat round :color="post.is_liked_by_user ? 'red' : 'grey-7'" :icon="post.is_liked_by_user ? 'favorite' : 'favorite_border'" @click="toggleLike(post)">
                <span v-if="post.likes_count > 0" class="q-ml-xs">{{ post.likes_count }}</span>
              </q-btn>
              <q-btn flat round icon="chat_bubble_outline" @click="toggleComments(post)">
                <span v-if="post.comments_count > 0" class="q-ml-xs">{{ post.comments_count }}</span>
              </q-btn>
            </q-card-actions>

            <!-- Comments Section -->
            <q-slide-transition>
              <div v-show="post.show_comments">
                <PostComments :post-id="post.id" @comment-count-updated="(count) => post.comments_count = count" />
              </div>
            </q-slide-transition>
          </q-card>
        </div>
      </div>
    </div>

    <!-- Image Gallery Modal -->
    <q-dialog v-model="galleryDialog">
      <q-carousel v-model="currentGallerySlide" animated arrows navigation infinite class="bg-black" style="width: 90vw; max-width: 90vw; height: 90vh;">
        <q-carousel-slide v-for="(img, index) in currentGalleryImages" :key="img.id" :name="index" class="q-pa-none">
          <q-img :src="img.image" class="full-height" fit="contain" />
        </q-carousel-slide>
      </q-carousel>
    </q-dialog>

  </q-page>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { api } from 'boot/axios';
import { useQuasar } from 'quasar';
import { GoogleMap, Marker } from 'vue3-google-map';
import { format, parseISO } from 'date-fns';
import { useAuthStore } from 'stores/auth-store';
import PostComments from 'components/PostComments.vue';

const props = defineProps({
  id: {
    type: [String, Number],
    required: true,
  },
});

const businessDetail = ref(null);
const loading = ref(true);
const error = ref(false);
const errorMessage = ref('');
const $q = useQuasar();
const authStore = useAuthStore();

const businessPosts = ref([]);
const loadingPosts = ref(true);
const galleryDialog = ref(false);
const currentGalleryImages = ref([]);
const currentGallerySlide = ref(0);

const googleMapsApiKey = ref('AIzaSyDnWWhRvds75DoC8HIVwhq4rAlzZQkGGrI');

async function fetchBusinessDetail(businessId) {
  loading.value = true;
  error.value = false;
  errorMessage.value = '';
  try {
    const response = await api.get(`/api/business-profiles/${businessId}/`);
    businessDetail.value = response.data;
  } catch (err) {
    error.value = true;
    errorMessage.value = (err.response?.status === 404) ? 'کسب‌وکار مورد نظر یافت نشد.' : (err.response?.data?.detail || 'خطا در دریافت اطلاعات از سرور.');
    $q.notify({ type: 'negative', message: errorMessage.value });
  } finally {
    loading.value = false;
  }
}

async function fetchBusinessPosts(businessId) {
  if (!businessId) return;
  loadingPosts.value = true;
  try {
    const response = await api.get(`/api/business-profiles/${businessId}/posts/`);
    const postsData = response.data.results || response.data;
    businessPosts.value = postsData.map(p => ({ ...p, is_liking: false, show_comments: false, slide: 0 }));
  } catch (error) {
    console.error("Error fetching business posts:", error);
    $q.notify({ type: 'warning', message: 'خطا در دریافت پست‌های کسب‌وکار.' });
  } finally {
    loadingPosts.value = false;
  }
}

function toggleLike(post) {
  if (!authStore.isAuthenticated) {
    $q.notify({ type: 'info', message: 'برای پسندیدن پست‌ها باید ابتدا وارد شوید.' });
    return;
  }
  post.is_liking = true;
  api.post(`/api/posts/${post.id}/like/`).then(() => {
    post.is_liked_by_user = !post.is_liked_by_user;
    post.likes_count += post.is_liked_by_user ? 1 : -1;
  }).catch(error => {
    console.error("Error toggling like:", error);
    $q.notify({ type: 'negative', message: 'خطا در عملیات پسندیدن.' });
  }).finally(() => {
    post.is_liking = false;
  });
}

function toggleComments(post) {
  post.show_comments = !post.show_comments;
}

function showImageGallery(images, startIndex) {
  currentGalleryImages.value = images;
  currentGallerySlide.value = startIndex;
  galleryDialog.value = true;
}

function formatDateTime(dateTimeString) {
  if (!dateTimeString) return '';
  try { return format(parseISO(dateTimeString), 'yyyy/MM/dd HH:mm'); }
  catch  { return dateTimeString; }
}

function getProfileLink(author) {
  if (!author) return '#';
  if (author.business_profile?.id) { return { name: 'business-detail', params: { id: author.business_profile.id } }; }
  return '#'; // Link to personal profile if available
}

function getAuthorAvatar(author) {
  if (!author) return null;
  if (author.business_profile?.logo_url) { return author.business_profile.logo_url; }
  else if (author.profile?.profile_picture_url) { return author.profile.profile_picture_url; }
  return null;
}

onMounted(() => {
  fetchBusinessDetail(props.id);
  fetchBusinessPosts(props.id);
});

watch(() => props.id, (newId) => {
  if (newId) {
    fetchBusinessDetail(newId);
    fetchBusinessPosts(newId);
  }
});
</script>

<style lang="scss" scoped>
// <<< FIX: Import Quasar Sass variables to use them in this file >>>
@import 'quasar/src/css/variables.sass';

.text-shadow {
  text-shadow: 1px 1px 2px rgba(0,0,0,0.7);
}
.bg-transparent {
    background-color: transparent !important;
}

// Scoped styles for post cards (can be shared with FeedPage)
.post-header {
  padding-bottom: 8px;
}
.author-link {
  text-decoration: none;
  color: inherit;
}
.author-info {
  line-height: 1.2;
}
.author-name {
  font-weight: 600;
}
.post-meta {
  font-size: 0.8rem;
  color: $grey-7;
}
.post-content {
  padding-top: 8px;
  padding-bottom: 8px;
}
.post-actions {
  padding: 4px 8px;
  justify-content: space-around;
}
</style>
