<!-- src/components/PostComments.vue -->
<template>
    <div class="q-mt-md">
      <q-separator />
      <div class="q-pa-md">
        <div class="text-subtitle1 q-mb-md">نظرات ({{ comments.length }})</div>

        <!-- فرم ارسال کامنت جدید (فقط برای کاربران لاگین شده) -->
        <q-form @submit.prevent="submitComment" class="q-mb-md" v-if="authStore.isAuthenticated">
          <div class="row items-start q-gutter-sm">
            <q-avatar size="md">
              <img v-if="authStore.user?.profile?.profile_picture_url" :src="authStore.user.profile.profile_picture_url">
              <q-icon v-else name="account_circle" />
            </q-avatar>
            <div class="col">
              <q-input
                v-model="newComment"
                placeholder="نظر خود را بنویسید..."
                filled
                dense
                autogrow
                lazy-rules
                :rules="[val => !!val.trim() || 'نظر نمی‌تواند خالی باشد']"
              />
              <q-btn
                label="ارسال نظر"
                type="submit"
                color="primary"
                dense
                unelevated
                class="q-mt-sm"
                :loading="submittingComment"
              />
            </div>
          </div>
        </q-form>

        <div v-if="loadingComments" class="text-center q-my-md">
          <q-spinner-dots color="primary" size="2em" />
        </div>

        <div v-else-if="commentsError" class="text-negative text-center">
          خطا در دریافت نظرات.
        </div>

        <div v-else-if="comments.length === 0 && !authStore.isAuthenticated" class="text-grey text-center">
          هنوز نظری ثبت نشده است. برای ثبت نظر وارد شوید.
        </div>

        <div v-else-if="comments.length === 0" class="text-grey text-center">
          هنوز نظری ثبت نشده است. اولین نفر باشید!
        </div>

        <q-list separator v-else>
          <q-item v-for="comment in comments" :key="comment.id" class="q-py-md">
            <q-item-section avatar top>
              <q-avatar>
                <img v-if="comment.author?.profile?.profile_picture_url" :src="comment.author.profile.profile_picture_url">
                <q-icon v-else name="account_circle" />
              </q-avatar>
            </q-item-section>

            <q-item-section>
              <q-item-label class="text-weight-bold">{{ comment.author?.username || 'کاربر' }}</q-item-label>
              <q-item-label caption>{{ formatDateTime(comment.created_at) }}</q-item-label>
              <q-item-label class="q-mt-sm" style="white-space: pre-line;">
                {{ comment.content }}
              </q-item-label>
            </q-item-section>

            <!-- دکمه‌های ویرایش/حذف برای نویسنده کامنت -->
            <q-item-section side top v-if="authStore.isAuthenticated && authStore.user?.id === comment.author?.id">
               <q-btn flat round dense icon="more_vert" size="sm">
                  <q-menu auto-close>
                    <q-list>
                      <q-item clickable>
                        <q-item-section>ویرایش</q-item-section>
                      </q-item>
                      <q-item clickable @click="confirmDeleteComment(comment.id)">
                        <q-item-section>حذف</q-item-section>
                      </q-item>
                    </q-list>
                  </q-menu>
               </q-btn>
            </q-item-section>
          </q-item>
        </q-list>
      </div>
    </div>
  </template>

  <script setup>
  import { ref, onMounted, watch } from 'vue';
  import { api } from 'boot/axios';
  import { useQuasar } from 'quasar';
  import { useAuthStore } from 'stores/auth-store';
  import { format, parseISO } from 'date-fns';

  const props = defineProps({
    postId: {
      type: [Number, String],
      required: true,
    },
  });

  const emit = defineEmits(['commentCountUpdated']);

  const comments = ref([]);
  const loadingComments = ref(true);
  const commentsError = ref(false);
  const newComment = ref('');
  const submittingComment = ref(false);
  const $q = useQuasar();
  const authStore = useAuthStore();

async function fetchComments() {
  if (!props.postId) return;
  loadingComments.value = true;
  commentsError.value = false;
  try {
    const params = {
      post: props.postId // <<<< پارامتر فیلتر
    };

    // ***** لاگ بسیار مهم برای دیباگ *****
    console.log(`POST_COMMENTS: Fetching comments for postId: ${props.postId}. Requesting URL: /api/comments/ with params:`, params);

    const response = await api.get('/api/comments/', { params });

    // ... (بقیه کد)
    comments.value = response.data.results || response.data;
    console.log(`POST_COMMENTS: Received ${comments.value.length} comments for postId: ${props.postId}`, response.data);

  } catch (error) {
    console.error("POST_COMMENTS: Error fetching comments:", error);
    commentsError.value = true;
  } finally {
    loadingComments.value = false;
  }
}



  async function submitComment() {
    if (!newComment.value.trim()) return;
    submittingComment.value = true;
    try {
      const payload = {
        post: props.postId,
        content: newComment.value,
      };
      const response = await api.post('/api/comments/', payload);
      comments.value.push(response.data); // اضافه کردن کامنت جدید به لیست
      newComment.value = ''; // خالی کردن فیلد
      emit('commentCountUpdated', comments.value.length); // آپدیت تعداد کامنت‌ها در کامپوننت والد
      $q.notify({ type: 'positive', message: 'نظر شما با موفقیت ثبت شد.' });
    } catch (error) {
      console.error("Error submitting comment:", error);
      $q.notify({ type: 'negative', message: 'خطا در ثبت نظر.' });
    } finally {
      submittingComment.value = false;
    }
  }

  async function confirmDeleteComment(commentId) {
      $q.dialog({
          title: 'تأیید حذف نظر',
          message: 'آیا از حذف این نظر مطمئن هستید؟',
          cancel: true,
          persistent: true
      }).onOk(async () => {
          try {
              await api.delete(`/api/comments/${commentId}/`);
              comments.value = comments.value.filter(c => c.id !== commentId);
              emit('commentCountUpdated', comments.value.length);
              $q.notify({ type: 'positive', message: 'نظر با موفقیت حذف شد.' });
          } catch (error) {
              console.error("Error deleting comment:", error);
              $q.notify({ type: 'negative', message: 'خطا در حذف نظر.' });
          }
      });
  }

  function formatDateTime(dateTimeString) {
    if (!dateTimeString) return '';
    try {
      return format(parseISO(dateTimeString), 'yyyy/MM/dd HH:mm');
    } catch {
      return dateTimeString;
    }
  }

  onMounted(() => {
    fetchComments();
  });

  // اگر postId تغییر کرد، کامنت‌ها را دوباره واکشی کن
  watch(() => props.postId, (newId) => {
    if (newId) {
      fetchComments();
    }
  });
  </script>
