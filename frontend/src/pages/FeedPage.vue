<template>
  <q-page class="feed-page">
    <!-- Header Section -->
    <div class="page-header">
      <div class="container q-pa-lg">
        <div class="row items-center">
          <div class="col">
            <h4 class="page-title q-ma-none">
              <q-icon name="dynamic_feed" class="q-mr-sm" />
              آخرین پست‌ها
            </h4>
            <p class="page-subtitle q-ma-none q-mt-xs">آخرین فعالیت‌های جامعه را دنبال کنید</p>
          </div>
          <div class="col-auto">
            <q-btn
              round
              color="primary"
              icon="refresh"
              @click="fetchPosts"
              :loading="loadingPosts"
              size="md"
              unelevated
            >
              <q-tooltip>به‌روزرسانی</q-tooltip>
            </q-btn>
          </div>
        </div>
      </div>
    </div>

    <div class="container q-pa-lg">
      <!-- Advanced Filter Section -->
      <q-card class="filter-card q-mb-lg" flat>
        <q-card-section class="q-pb-sm">
          <div class="filter-header">
            <q-icon name="tune" class="filter-icon" />
            <span class="filter-title">فیلتر هوشمند پست‌ها</span>
            <q-space />
            <q-btn
              flat
              dense
              round
              icon="expand_more"
              @click="showFilters = !showFilters"
              :class="{ 'rotate-180': showFilters }"
              class="filter-toggle"
            />
          </div>
        </q-card-section>

        <q-slide-transition>
          <div v-show="showFilters">
            <q-card-section class="q-pt-none">
              <div class="row q-col-gutter-lg">
                <div class="col-12 col-sm-6 col-lg-4">
                  <q-select
                    v-model="filters.neighborhood"
                    :options="neighborhoodOptions"
                    label="انتخاب محله"
                    filled
                    emit-value
                    map-options
                    option-value="id"
                    option-label="name"
                    clearable
                    :loading="loadingNeighborhoods"
                    class="modern-select"
                  >
                    <template v-slot:prepend>
                      <q-icon name="location_on" />
                    </template>
                    <template v-slot:no-option>
                      <q-item>
                        <q-item-section class="text-grey">هیچ محله‌ای یافت نشد</q-item-section>
                      </q-item>
                    </template>
                  </q-select>
                </div>

                <div class="col-12 col-sm-6 col-lg-4">
                  <q-select
                    v-model="filters.post_type"
                    :options="postTypeOptions"
                    label="نوع پست"
                    filled
                    emit-value
                    map-options
                    clearable
                    class="modern-select"
                  >
                    <template v-slot:prepend>
                      <q-icon name="category" />
                    </template>
                  </q-select>
                </div>

                <div class="col-12 col-lg-4">
                  <div class="row q-gutter-sm">
                    <div class="col">
                      <q-btn
                        label="اعمال فیلتر"
                        color="primary"
                        @click="applyFilters"
                        unelevated
                        class="full-width filter-btn"
                        icon="filter_alt"
                        :loading="loadingPosts"
                      />
                    </div>
                    <div class="col-auto">
                      <q-btn
                        icon="clear"
                        color="grey-7"
                        @click="resetFilters"
                        flat
                        round
                        class="reset-btn"
                      >
                        <q-tooltip>حذف فیلترها</q-tooltip>
                      </q-btn>
                    </div>
                  </div>
                </div>
              </div>
            </q-card-section>
          </div>
        </q-slide-transition>
      </q-card>

      <!-- Content Section -->
      <div class="content-section">
        <!-- Loading State -->
        <div v-if="loadingPosts" class="loading-state">
          <div class="loading-content">
            <q-spinner-dots color="primary" size="4em" />
            <p class="q-mt-md text-grey-6">در حال بارگذاری پست‌ها...</p>
          </div>
        </div>

        <!-- Error State -->
        <div v-else-if="postsError" class="error-state">
          <q-icon name="error_outline" size="4em" color="negative" />
          <h6 class="q-mt-md q-mb-sm">خطا در دریافت پست‌ها</h6>
          <p class="text-grey-6 q-mb-md">لطفاً دوباره تلاش کنید</p>
          <q-btn
            label="تلاش مجدد"
            @click="fetchPosts"
            icon="refresh"
            color="primary"
            unelevated
          />
        </div>

        <!-- Empty State -->
        <div v-else-if="posts.length === 0" class="empty-state">
          <q-icon name="post_add" size="4em" color="grey-5" />
          <h6 class="q-mt-md q-mb-sm">هیچ پستی یافت نشد</h6>
          <p class="text-grey-6">با فیلترهای انتخاب شده پستی وجود ندارد</p>
        </div>

        <!-- Posts List -->
        <div v-else class="posts-container">
          <q-card
            v-for="post in posts"
            :key="post.id"
            class="post-card q-mb-lg"
            flat
            bordered
          >
            <!-- Post Header -->
            <q-card-section class="post-header">
              <div class="row items-center no-wrap">
                <router-link
                  :to="getProfileLink(post.author)"
                  class="author-link"
                >
                  <q-avatar size="50px" class="author-avatar">
                    <img
                      v-if="getAuthorAvatar(post.author)"
                      :src="getAuthorAvatar(post.author)"
                      alt="Avatar"
                    >
                    <q-icon v-else name="account_circle" size="30px" />
                  </q-avatar>
                  <div class="author-info q-ml-md">
                    <div class="author-name">{{ post.author?.username || 'کاربر ناشناس' }}</div>
                    <div class="post-meta">
                      {{ formatDateTime(post.created_at) }}
                      <span v-if="post.created_at !== post.updated_at" class="edited-badge">
                        <q-icon name="edit" size="12px" />
                        ویرایش شده
                      </span>
                    </div>
                  </div>
                </router-link>

                <q-space />

                <div class="post-badges">
                  <q-badge
                    v-if="post.visibility === 'NEIGHBORHOOD'"
                    color="teal-6"
                    class="visibility-badge"
                    rounded
                  >
                    <q-icon name="holiday_village" size="14px" class="q-mr-xs" />
                    محله‌ای
                  </q-badge>
                </div>

                <q-btn
                  v-if="authStore.isAuthenticated && authStore.user?.id === post.author?.id"
                  flat
                  round
                  dense
                  icon="more_vert"
                  class="post-menu-btn"
                >
                  <q-menu auto-close>
                    <q-list class="post-menu">
                      <q-item clickable @click="editPost(post)">
                        <q-item-section avatar>
                          <q-icon name="edit" />
                        </q-item-section>
                        <q-item-section>ویرایش</q-item-section>
                      </q-item>
                      <q-separator />
                      <q-item clickable @click="confirmDeletePost(post.id)" class="text-negative">
                        <q-item-section avatar>
                          <q-icon name="delete" />
                        </q-item-section>
                        <q-item-section>حذف</q-item-section>
                      </q-item>
                    </q-list>
                  </q-menu>
                </q-btn>
              </div>
            </q-card-section>

            <!-- Post Content -->
            <q-card-section v-if="post.content" class="post-content">
              <p class="content-text">{{ post.content }}</p>
            </q-card-section>

            <!-- Post Images -->
            <div v-if="post.images && post.images.length > 0" class="post-images">
              <q-carousel
                v-model="post.slide"
                animated
                arrows
                navigation
                infinite
                :height="post.images.length > 1 ? '400px' : 'auto'"
                class="post-carousel"
              >
                <q-carousel-slide
                  v-for="(img, index) in post.images"
                  :key="img.id"
                  :name="index"
                  class="q-pa-none"
                >
                  <q-img
                    :src="img.image"
                    class="full-height full-width cursor-pointer post-image"
                    fit="cover"
                    @click="showImageGallery(post.images, index)"
                  >
                    <template v-slot:loading>
                      <div class="image-loading">
                        <q-spinner-puff color="primary" />
                      </div>
                    </template>
                  </q-img>
                </q-carousel-slide>
              </q-carousel>
            </div>

            <!-- Post Tags -->
            <q-card-section v-if="post.tags && post.tags.length > 0" class="post-tags">
              <q-chip
                v-for="tag in post.tags"
                :key="tag"
                clickable
                color="blue-1"
                text-color="blue-8"
                class="tag-chip"
                @click="goToTagPage(tag)"
              >
                <q-icon name="tag" size="14px" class="q-mr-xs" />
                {{ tag }}
              </q-chip>
            </q-card-section>

            <!-- Post Actions -->
            <q-separator class="action-separator" />
            <q-card-actions class="post-actions">
              <q-btn
                flat
                round
                :color="post.is_liked_by_user ? 'red-6' : 'grey-6'"
                :icon="post.is_liked_by_user ? 'favorite' : 'favorite_border'"
                @click="toggleLike(post)"
                :loading="post.is_liking"
                class="action-btn like-btn"
                size="md"
              >
                <span v-if="post.likes_count > 0" class="action-count">{{ post.likes_count }}</span>
                <q-tooltip>{{ post.is_liked_by_user ? 'پسندیدن را بردار' : 'بپسند' }}</q-tooltip>
              </q-btn>

              <q-btn
                flat
                round
                icon="chat_bubble_outline"
                @click="toggleComments(post)"
                color="grey-6"
                class="action-btn comment-btn"
                size="md"
              >
                <span v-if="post.comments_count > 0" class="action-count">{{ post.comments_count }}</span>
                <q-tooltip>نظرات</q-tooltip>
              </q-btn>

              <q-btn
                flat
                round
                icon="share"
                color="grey-6"
                class="action-btn share-btn"
                size="md"
              >
                <q-tooltip>اشتراک‌گذاری</q-tooltip>
              </q-btn>

              <q-space />

              <q-btn
                flat
                dense
                :icon="post.show_comments ? 'expand_less' : 'expand_more'"
                color="grey-6"
                @click="toggleComments(post)"
                class="expand-comments-btn"
              >
                {{ post.show_comments ? 'بستن نظرات' : 'نمایش نظرات' }}
              </q-btn>
            </q-card-actions>

            <!-- Comments Section -->
            <q-slide-transition>
              <div v-show="post.show_comments" class="comments-section">
                <PostComments
                  :post-id="post.id"
                  @comment-count-updated="(count) => post.comments_count = count"
                />
              </div>
            </q-slide-transition>
          </q-card>
        </div>
      </div>
    </div>

    <!-- Image Gallery Modal -->
    <q-dialog v-model="galleryDialog" class="image-gallery-dialog">
      <q-card class="gallery-card">
        <q-carousel
          v-model="currentGallerySlide"
          animated
          arrows
          navigation
          infinite
          class="gallery-carousel"
          swipeable
        >
          <q-carousel-slide
            v-for="(img, index) in currentGalleryImages"
            :key="img.id"
            :name="index"
            class="q-pa-none"
          >
            <q-img
              :src="img.image"
              class="full-height gallery-image"
              fit="contain"
            />
          </q-carousel-slide>
        </q-carousel>

        <q-btn
          flat
          round
          dense
          icon="close"
          class="gallery-close-btn"
          @click="galleryDialog = false"
        />
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { api } from 'boot/axios';
import { useQuasar } from 'quasar';
import { useAuthStore } from 'stores/auth-store';
import { useRouter } from 'vue-router';
import PostComments from 'components/PostComments.vue';
import { format, parseISO } from 'date-fns';

const posts = ref([]);
const loadingPosts = ref(true);
const postsError = ref(false);
const errorMessage = ref('');
const showFilters = ref(false);

const $q = useQuasar();
const authStore = useAuthStore();
const router = useRouter();

const galleryDialog = ref(false);
const currentGalleryImages = ref([]);
const currentGallerySlide = ref(0);

const filters = ref({
  neighborhood: null,
  post_type: null,
});
const loadingNeighborhoods = ref(false);
const neighborhoodOptions = ref([]);
const postTypeOptions = [
  { label: 'همه انواع', value: null },
  { label: 'پست‌های شخصی', value: 'personal' },
  { label: 'کسب‌وکار و سازمان‌ها', value: 'business' },
];

async function fetchNeighborhoodsForFilter() {
  loadingNeighborhoods.value = true;
  try {
    const response = await api.get('/api/neighborhoods/');
    neighborhoodOptions.value = response.data;
  } catch (error) {
    console.error("Error fetching neighborhoods for filter:", error);
  } finally {
    loadingNeighborhoods.value = false;
  }
}

async function fetchPosts() {
  loadingPosts.value = true;
  postsError.value = false;
  try {
    const params = { ...filters.value };
    Object.keys(params).forEach(key => (params[key] === null || params[key] === '') && delete params[key]);

    const response = await api.get('/api/posts/', { params });
    let fetchedPosts = response.data.results || response.data;
    posts.value = fetchedPosts.map(p => ({ ...p, is_liking: false, slide: 0, show_comments: false }));
  } catch (error) {
    console.error("Error fetching posts:", error);
    postsError.value = true;
    errorMessage.value = error.response?.data?.detail || 'خطا در دریافت پست‌ها.';
  } finally {
    loadingPosts.value = false;
  }
}

function applyFilters() {
  fetchPosts();
}

function resetFilters() {
  filters.value = { neighborhood: null, post_type: null };
  fetchPosts();
}

function showImageGallery(images, startIndex) {
  currentGalleryImages.value = images;
  currentGallerySlide.value = startIndex;
  galleryDialog.value = true;
}

function toggleComments(post) {
  post.show_comments = !post.show_comments;
}

function toggleLike(post) {
  if (!authStore.isAuthenticated) {
    $q.notify({
      type: 'info',
      message: 'برای پسندیدن پست‌ها باید ابتدا وارد شوید.',
      actions: [{ label: 'ورود', color: 'white', handler: () => { router.push('/login') } }]
    });
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

function formatDateTime(dateTimeString) {
  if (!dateTimeString) return '';
  try { return format(parseISO(dateTimeString), 'yyyy/MM/dd HH:mm'); }
  catch (error) { console.error(`Could not format date: "${dateTimeString}"`, error); return dateTimeString; }
}

function getProfileLink(author) {
  if (!author) return '#';
  if (author.business_profile && author.business_profile.id) { return { name: 'business-detail', params: { id: author.business_profile.id } }; }
  else if (author.profile && author.profile.id) { return '#'; }
  return '#';
}

function getAuthorAvatar(author) {
  if (!author) return null;
  if (author.business_profile && author.business_profile.logo_url) { return author.business_profile.logo_url; }
  else if (author.profile && author.profile.profile_picture_url) { return author.profile.profile_picture_url; }
  return null;
}

function editPost(post) {
  $q.dialog({
    title: 'ویرایش پست',
    message: 'محتوای جدید را وارد کنید:',
    prompt: { model: post.content, type: 'textarea' },
    cancel: true,
    persistent: true
  }).onOk(async (data) => {
    if (!data || !data.trim()) {
      $q.notify({ type: 'warning', message: 'محتوا نمی‌تواند خالی باشد.' });
      return;
    }
    try {
      const response = await api.patch(`/api/posts/${post.id}/`, { content: data });
      const index = posts.value.findIndex(p => p.id === post.id);
      if (index !== -1) { posts.value[index] = { ...posts.value[index], ...response.data }; }
      $q.notify({ type: 'positive', message: 'پست با موفقیت ویرایش شد.' });
    } catch (error) {
      console.error("Error editing post:", error);
      $q.notify({ type: 'negative', message: 'خطا در ویرایش پست.' });
    }
  });
}

function confirmDeletePost(postId) {
  $q.dialog({
    title: 'تأیید حذف',
    message: 'آیا از حذف این پست مطمئن هستید؟',
    cancel: { label: 'لغو', color: 'grey' },
    ok: { label: 'حذف کن', color: 'negative' },
    persistent: true
  }).onOk(async () => {
    try {
      await api.delete(`/api/posts/${postId}/`);
      posts.value = posts.value.filter(p => p.id !== postId);
      $q.notify({ type: 'positive', message: 'پست با موفقیت حذف شد.' });
    } catch (error) {
      console.error("Error deleting post:", error);
      $q.notify({ type: 'negative', message: 'خطا در حذف پست.' });
    }
  });
}
function goToTagPage(tagName) {
  const encodedTagName = encodeURIComponent(tagName);
  router.push(`/tags/${encodedTagName}`);
}

onMounted(() => {
  fetchPosts();
  fetchNeighborhoodsForFilter();
});
</script>

<style scoped>
/* تمام استایل‌های قبلی شما بدون تغییر اینجا قرار می‌گیرند */
.feed-page {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
}

.page-header {
  background: linear-gradient(135deg, #0e9458 0%, #16d708 100%);
  color: white;
  position: relative;
  overflow: hidden;
}

.page-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 20"><defs><radialGradient id="a" cx="50%" cy="40%"><stop offset="0%" stop-color="%23ffffff" stop-opacity=".1"/><stop offset="100%" stop-color="%23ffffff" stop-opacity="0"/></radialGradient></defs><rect width="100" height="20" fill="url(%23a)"/></svg>');
  opacity: 0.1;
}

.container {
  max-width: 900px;
  margin: 0 auto;
}

.page-title {
  font-size: 1.8rem;
  font-weight: 600;
  margin: 0;
}

.page-subtitle {
  opacity: 0.9;
  font-size: 1rem;
}

.filter-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.filter-header {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.filter-icon {
  color: #0cb520;
  font-size: 1.2rem;
  margin-left: 8px;
}

.filter-title {
  font-weight: 600;
  font-size: 1.1rem;
  color: #2d3748;
}

.filter-toggle {
  transition: transform 0.3s ease;
}

.filter-toggle.rotate-180 {
  transform: rotate(180deg);
}

.modern-select {
  border-radius: 12px;
}

.filter-btn {
  border-radius: 12px;
  font-weight: 600;
}

.reset-btn {
  border-radius: 50%;
}

.create-post-section {
  margin-bottom: 2rem;
}

.loading-state,
.error-state,
.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.loading-content,
.error-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.posts-container {
  position: relative;
}

.post-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.post-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.post-header {
  padding: 1.5rem;
  border-bottom: 1px solid #f7fafc;
}

.author-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: inherit;
  transition: opacity 0.2s ease;
}

.author-link:hover {
  opacity: 0.8;
}

.author-avatar {
  border: 3px solid #e2e8f0;
  transition: border-color 0.2s ease;
}

.author-avatar:hover {
  border-color: #1fad09af;
}

.author-info {
  margin-right: 12px;
}

.author-name {
  font-weight: 600;
  font-size: 1rem;
  color: #2d3748;
  margin-bottom: 4px;
}

.post-meta {
  font-size: 0.85rem;
  color: #718096;
  display: flex;
  align-items: center;
  gap: 8px;
}

.edited-badge {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.8rem;
  color: #a0aec0;
}

.post-badges {
  margin-left: 1rem;
}

.visibility-badge {
  font-size: 0.8rem;
  padding: 6px 12px;
}

.post-menu-btn {
  opacity: 0.6;
  transition: opacity 0.2s ease;
}

.post-menu-btn:hover {
  opacity: 1;
}

.post-menu {
  min-width: 150px;
  border-radius: 8px;
}

.post-content {
  padding: 1rem 1.5rem;
}

.content-text {
  font-size: 1rem;
  line-height: 1.7;
  color: #2d3748;
  white-space: pre-line;
  margin: 0;
}

.post-images {
  position: relative;
}

.post-carousel {
  border-radius: 0;
  background: #f7fafc;
}

.post-image {
  border-radius: 0;
  transition: transform 0.3s ease;
}

.post-image:hover {
  transform: scale(1.02);
}

.image-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.post-tags {
  padding: 1rem 1.5rem 0.5rem;
}

.tag-chip {
  margin: 0 8px 8px 0;
  border-radius: 20px;
  font-weight: 500;
  font-size: 0.85rem;
  transition: transform 0.2s ease;
}

.tag-chip:hover {
  transform: scale(1.05);
}

.action-separator {
  margin: 0 1rem;
  opacity: 0.1;
}

.post-actions {
  padding: 1rem 1.5rem;
  background: #f8fafc;
  border-radius: 0 0 16px 16px;
}

.action-btn {
  position: relative;
  transition: all 0.2s ease;
  border-radius: 50%;
  margin-left: 8px;
}

.action-btn:hover {
  transform: scale(1.1);
}

.like-btn:hover {
  background: rgba(239, 68, 68, 0.1);
}

.comment-btn:hover {
  background: rgba(59, 130, 246, 0.1);
}

.share-btn:hover {
  background: rgba(16, 185, 129, 0.1);
}

.action-count {
  margin-right: 6px;
  font-size: 0.85rem;
  font-weight: 600;
}

.expand-comments-btn {
  font-size: 0.85rem;
  color: #718096;
  border-radius: 20px;
  padding: 8px 16px;
  transition: all 0.2s ease;
}

.expand-comments-btn:hover {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
}

.comments-section {
  background: #f8fafc;
  border-radius: 0 0 16px 16px;
  border-top: 1px solid #e2e8f0;
}

.image-gallery-dialog .q-dialog__inner {
  padding: 0;
}

.gallery-card {
  position: relative;
  width: 90vw;
  height: 90vh;
  max-width: none;
  border-radius: 12px;
  overflow: hidden;
  background: #000;
}

.gallery-carousel {
  width: 100%;
  height: 100%;
}

.gallery-image {
  width: 100%;
  height: 100%;
}

.gallery-close-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  z-index: 1000;
  transition: background 0.2s ease;
}

.gallery-close-btn:hover {
  background: rgba(0, 0, 0, 0.9);
}

/* Responsive Design */
@media (max-width: 768px) {
  .page-header .container {
    padding: 1rem;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .container {
    padding: 1rem;
  }

  .post-card {
    margin-bottom: 1rem;
  }

  .post-header,
  .post-content,
  .post-tags,
  .post-actions {
    padding: 1rem;
  }

  .author-avatar {
    width: 40px;
    height: 40px;
  }

  .filter-card .q-card-section {
    padding: 1rem;
  }

  .gallery-card {
    width: 95vw;
    height: 80vh;
  }
}

/* Dark Mode Support */
@media (prefers-color-scheme: dark) {
  .feed-page {
    background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
  }

  .filter-card,
  .post-card {
    background: #2d3748;
    border-color: #4a5568;
  }

  .author-name,
  .content-text {
    color: #e2e8f0;
  }

  .post-meta {
    color: #a0aec0;
  }

  .post-actions {
    background: #1a202c;
  }

  .comments-section {
    background: #1a202c;
    border-color: #4a5568;
  }
}

/* Animation Keyframes */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

.post-card {
  animation: fadeInUp 0.6s ease forwards;
}

.like-btn.liked {
  animation: pulse 0.3s ease;
}

/* Smooth Transitions */
* {
  transition: color 0.2s ease, background-color 0.2s ease, border-color 0.2s ease;
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
  background: #c1c1c1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
