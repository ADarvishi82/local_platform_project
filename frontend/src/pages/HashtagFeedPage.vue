<template>
  <q-page padding class="q-pa-md">
    <!-- هدر صفحه که نام هشتگ را نمایش می‌دهد -->
    <div class="row items-center q-mb-md">
      <q-icon name="tag" color="primary" size="lg" class="q-mr-md" />
      <div>
        <div class="text-caption text-grey-7">پست‌های دارای هشتگ</div>
        <div class="text-h4 text-primary">#{{ tagName }}</div>
      </div>
    </div>

    <q-separator class="q-mb-lg" />

    <!-- وضعیت‌های لودینگ و خطا -->
    <div v-if="loadingPosts" class="row justify-center q-my-xl">
      <q-spinner-dots color="primary" size="3em" />
    </div>
    <div v-else-if="postsError" class="text-negative text-center q-my-xl">
      خطا در دریافت پست‌ها.
      <q-btn flat label="تلاش مجدد" @click="fetchPostsByTag(props.tagName)" icon="refresh" color="primary"/>
    </div>
    <div v-else-if="posts.length === 0" class="text-grey-7 text-center q-my-xl">
      هیچ پستی با هشتگ #{{ tagName }} یافت نشد.
    </div>

    <!-- لیست پست‌ها -->
    <div v-else class="q-gutter-y-md">
      <q-card v-for="post in posts" :key="post.id" class="post-card" flat bordered>
        <!-- Post Header -->
        <q-card-section class="post-header">
          <div class="row items-center no-wrap">
            <router-link :to="getProfileLink(post.author)" class="author-link">
              <q-avatar size="50px" class="author-avatar">
                <img v-if="getAuthorAvatar(post.author)" :src="getAuthorAvatar(post.author)" alt="Avatar">
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
              <q-badge v-if="post.visibility === 'NEIGHBORHOOD'" color="teal-6" class="visibility-badge" rounded>
                <q-icon name="holiday_village" size="14px" class="q-mr-xs" />
                محله‌ای
              </q-badge>
            </div>
            <q-btn v-if="authStore.isAuthenticated && authStore.user?.id === post.author?.id" flat round dense icon="more_vert" class="post-menu-btn">
              <q-menu auto-close>
                <q-list class="post-menu">
                  <q-item clickable @click="editPost(post)">
                    <q-item-section avatar><q-icon name="edit" /></q-item-section>
                    <q-item-section>ویرایش</q-item-section>
                  </q-item>
                  <q-separator />
                  <q-item clickable @click="confirmDeletePost(post.id)" class="text-negative">
                    <q-item-section avatar><q-icon name="delete" /></q-item-section>
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
          <q-carousel v-model="post.slide" animated arrows navigation infinite :height="post.images.length > 1 ? '400px' : 'auto'" class="post-carousel">
            <q-carousel-slide v-for="(img, index) in post.images" :key="img.id" :name="index" class="q-pa-none">
              <q-img :src="img.image" class="full-height full-width cursor-pointer post-image" fit="cover" @click="showImageGallery(post.images, index)">
                <template v-slot:loading>
                  <div class="image-loading"><q-spinner-puff color="primary" /></div>
                </template>
              </q-img>
            </q-carousel-slide>
          </q-carousel>
        </div>

        <!-- Post Tags -->
        <q-card-section v-if="post.tags && post.tags.length > 0" class="post-tags">
          <q-chip v-for="tag in post.tags" :key="tag" clickable color="blue-1" text-color="blue-8" class="tag-chip" :to="`/tags/${tag}`">
            <q-icon name="tag" size="14px" class="q-mr-xs" />
            {{ tag }}
          </q-chip>
        </q-card-section>

        <!-- Post Actions -->
        <q-separator class="action-separator" />
        <q-card-actions class="post-actions">
          <q-btn flat round :color="post.is_liked_by_user ? 'red-6' : 'grey-6'" :icon="post.is_liked_by_user ? 'favorite' : 'favorite_border'" @click="toggleLike(post)" :loading="post.is_liking" class="action-btn like-btn" size="md">
            <span v-if="post.likes_count > 0" class="action-count">{{ post.likes_count }}</span>
            <q-tooltip>{{ post.is_liked_by_user ? 'پسندیدن را بردار' : 'بپسند' }}</q-tooltip>
          </q-btn>
          <q-btn flat round icon="chat_bubble_outline" @click="toggleComments(post)" color="grey-6" class="action-btn comment-btn" size="md">
            <span v-if="post.comments_count > 0" class="action-count">{{ post.comments_count }}</span>
            <q-tooltip>نظرات</q-tooltip>
          </q-btn>
          <q-btn flat round icon="share" color="grey-6" class="action-btn share-btn" size="md">
            <q-tooltip>اشتراک‌گذاری</q-tooltip>
          </q-btn>
          <q-space />
          <q-btn flat dense :icon="post.show_comments ? 'expand_less' : 'expand_more'" color="grey-6" @click="toggleComments(post)" class="expand-comments-btn">
            {{ post.show_comments ? 'بستن نظرات' : 'نمایش نظرات' }}
          </q-btn>
        </q-card-actions>

        <!-- Comments Section -->
        <q-slide-transition>
          <div v-show="post.show_comments" class="comments-section">
            <PostComments :post-id="post.id" @comment-count-updated="(count) => post.comments_count = count" />
          </div>
        </q-slide-transition>
      </q-card>
    </div>

    <!-- Image Gallery Modal -->
    <q-dialog v-model="galleryDialog" class="image-gallery-dialog">
      <q-card class="gallery-card">
        <q-carousel v-model="currentGallerySlide" animated arrows navigation infinite class="gallery-carousel" swipeable>
          <q-carousel-slide v-for="(img, index) in currentGalleryImages" :key="img.id" :name="index" class="q-pa-none">
            <q-img :src="img.image" class="full-height gallery-image" fit="contain" />
          </q-carousel-slide>
        </q-carousel>
        <q-btn flat round dense icon="close" class="gallery-close-btn" @click="galleryDialog = false" />
      </q-card>
    </q-dialog>

  </q-page>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { api } from 'boot/axios';
import { useQuasar } from 'quasar';
import { useAuthStore } from 'stores/auth-store';
import { useRouter } from 'vue-router';
import PostComments from 'components/PostComments.vue';
import { format, parseISO } from 'date-fns';

const props = defineProps({
  tagName: {
    type: String,
    required: true,
  },
});

const posts = ref([]);
const loadingPosts = ref(true);
const postsError = ref(false);

const $q = useQuasar();
const authStore = useAuthStore();
const router = useRouter();

const galleryDialog = ref(false);
const currentGalleryImages = ref([]);
const currentGallerySlide = ref(0);

async function fetchPostsByTag(tag) {
  loadingPosts.value = true;
  postsError.value = false;
  try {
    const response = await api.get('/api/posts/', { params: { tag: tag } });
    let fetchedPosts = response.data.results || response.data;
    posts.value = fetchedPosts.map(p => ({
      ...p,
      is_liking: false,
      slide: 0,
      show_comments: false
    }));
  } catch (error) {
    console.error(`Error fetching posts for tag #${tag}:`, error);
    postsError.value = true;
  } finally {
    loadingPosts.value = false;
  }
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
  catch { // Removed unused catch parameter to fix ESLint error
    // Optional: console.error('Could not format date:', dateTimeString);
    return dateTimeString;
  }
}

function getProfileLink(author) {
  if (!author) return '#';
  if (author.business_profile?.id) { return { name: 'business-detail', params: { id: author.business_profile.id } }; }
  else if (author.profile?.id) { return '#'; }
  return '#';
}

function getAuthorAvatar(author) {
  if (!author) return null;
  if (author.business_profile?.logo_url) { return author.business_profile.logo_url; }
  else if (author.profile?.profile_picture_url) { return author.profile.profile_picture_url; }
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

onMounted(() => {
  if (props.tagName) {
    fetchPostsByTag(props.tagName);
  }
});

watch(() => props.tagName, (newTag) => {
  if (newTag) {
    fetchPostsByTag(newTag);
  }
});
</script>

<style scoped>
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
}
.author-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: inherit;
}
.author-avatar {
  border: 3px solid #e2e8f0;
}
.author-info {
  margin-right: 12px;
}
.author-name {
  font-weight: 600;
  font-size: 1rem;
}
.post-meta {
  font-size: 0.85rem;
  color: #718096;
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
  white-space: pre-line;
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
}
.action-separator {
  margin: 0 1rem;
  opacity: 0.1;
}
.post-actions {
  padding: 1rem 1.5rem;
}
.action-btn {
  margin-left: 8px;
}
.action-count {
  margin-right: 6px;
}
.expand-comments-btn {
  font-size: 0.85rem;
  color: #718096;
}
.comments-section {
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
}
.gallery-card {
  width: 90vw;
  height: 90vh;
  background: #000;
}
.gallery-close-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  z-index: 1000;
}
</style>
