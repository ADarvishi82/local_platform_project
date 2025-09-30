<!-- src/pages/HashtagFeedPage.vue -->
<template>
  <q-page padding class="q-pa-md">
    <div class="text-h5 q-mb-md text-primary">
      پست‌های دارای هشتگ: <span class="text-weight-bold">#{{ tagName }}</span>
    </div>
    <!-- می‌توانید اینجا از یک کامپوننت جداگانه برای نمایش لیست پست‌ها استفاده کنید تا کد تکراری نشود -->
    <!-- ولی برای سادگی، منطق واکشی را دوباره اینجا می‌نویسیم -->
    <div v-if="loadingPosts" class="q-pa-md flex flex-center">
      <q-spinner color="primary" size="2em" />
      <span class="q-ml-sm">در حال بارگذاری پست‌ها...</span>
    </div>
    <div v-else-if="postsError" class="q-pa-md text-negative">
      خطا در بارگذاری پست‌ها. لطفا دوباره تلاش کنید.
    </div>
    <div v-else-if="posts.length === 0" class="q-pa-md text-grey">
      هیچ پستی با این هشتگ یافت نشد.
    </div>
    <div v-else class="q-gutter-y-md">
      <!-- همان حلقه v-for و q-card از FeedPage.vue را اینجا کپی کنید -->
      <q-card v-for="post in posts" :key="post.id" flat bordered>
        <!-- ... محتوای کارت پست ... -->
      </q-card>
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { api } from 'boot/axios';
// ... سایر import های لازم از FeedPage.vue

const props = defineProps({
  tagName: { // این prop از طریق router پاس داده می‌شود
    type: String,
    required: true,
  },
});

const posts = ref([]);
const loadingPosts = ref(true);
const postsError = ref(false);
// ...

async function fetchPostsByTag(tag) {
  loadingPosts.value = true;
  postsError.value = false;
  try {
    const response = await api.get('/api/posts/', {
      params: { tag: tag } // <<<< ارسال تگ به عنوان پارامتر کوئری
    });
    // ... (منطق پر کردن posts.value مشابه FeedPage) ...
    let fetchedPosts = response.data.results || response.data;
    posts.value = fetchedPosts.map(p => ({...p, is_liking: false, slide: 0}));

  } catch (error) {
    console.error(`Error fetching posts for tag #${tag}:`, error);
    postsError.value = true;
  } finally {
    loadingPosts.value = false;
  }
}

onMounted(() => {
  fetchPostsByTag(props.tagName);
});

// اگر کاربر بین صفحات تگ جابجا شد، دوباره واکشی کن
watch(() => props.tagName, (newTag) => {
  if (newTag) {
    fetchPostsByTag(newTag);
  }
});

// می‌توانید توابع دیگر (like, delete, formatDateTime, ...) را هم از FeedPage.vue به اینجا منتقل کنید
// یا آنها را در یک فایل composable جداگانه قرار دهید تا کد تکراری نشود.
</script>
