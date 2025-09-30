<template>
  <q-card class="create-post-card" flat>
    <!-- Header -->
    <q-card-section class="create-post-header">
      <div class="row items-center no-wrap">
        <q-avatar size="45px" class="user-avatar">
          <img
            v-if="authStore.user?.profile?.profile_picture_url"
            :src="authStore.user.profile.profile_picture_url"
            alt="Avatar"
          >
          <q-icon v-else name="account_circle" size="30px" />
        </q-avatar>
        <div class="q-ml-md">
          <div class="user-name">{{ authStore.user?.username || 'کاربر' }}</div>
          <div class="create-prompt">چه چیزی در ذهن دارید؟</div>
        </div>
        <q-space />
        <q-icon name="edit" class="create-icon" />
      </div>
    </q-card-section>

    <!-- Main Form -->
    <q-card-section class="create-post-body">
      <q-form @submit.prevent="submitPost" class="post-form">
        <!-- Content Input -->
        <div class="content-input-section">
          <q-input
            v-model="content"
            placeholder="پست خود را اینجا بنویسید..."
            type="textarea"
            outlined
            autogrow
            :rows="3"
            class="content-input"
            borderless
          >
            <template v-slot:prepend>
              <q-icon name="create" class="input-icon" />
            </template>
          </q-input>
        </div>

        <!-- Image Upload Section -->
        <div class="upload-section">
          <q-file
            v-model="imageFiles"
            outlined
            multiple
            append
            accept=".jpg, .jpeg, .png, image/*"
            @update:model-value="handleImagesUpload"
            max-files="5"
            max-file-size="5242880"
            @rejected="onRejected"
            class="image-upload"
            borderless
          >
            <template v-slot:prepend>
              <q-icon name="photo_camera" class="upload-icon" />
            </template>
            <template v-slot:default>
              <div class="upload-area">
                <q-icon name="add_photo_alternate" size="2em" class="upload-placeholder-icon" />
                <div class="upload-text">
                  <span class="upload-main-text">عکس اضافه کنید</span>
                  <span class="upload-sub-text">تا 5 عکس، هر کدام حداکثر 5MB</span>
                </div>
              </div>
            </template>
            <template v-slot:append>
              <q-badge v-if="imageFiles.length > 0" color="primary" class="file-count-badge">
                {{ imageFiles.length }}
              </q-badge>
            </template>
          </q-file>
        </div>

        <!-- Image Preview Section -->
        <div v-if="imagePreviewUrls.length > 0" class="image-preview-section">
          <div class="preview-header">
            <span class="preview-title">پیش‌نمایش تصاویر</span>
            <q-btn
              flat
              dense
              round
              icon="clear_all"
              @click="clearAllImages"
              class="clear-all-btn"
              size="sm"
            >
              <q-tooltip>حذف همه تصاویر</q-tooltip>
            </q-btn>
          </div>
          <div class="image-grid">
            <div
              v-for="(url, index) in imagePreviewUrls"
              :key="index"
              class="image-preview-item"
            >
              <q-img
                :src="url"
                :ratio="1"
                class="preview-image"
                fit="cover"
              >
                <div class="preview-overlay">
                  <q-btn
                    round
                    dense
                    icon="close"
                    color="white"
                    @click="removeImage(index)"
                    class="remove-image-btn"
                    size="sm"
                  />
                </div>
              </q-img>
              <div class="image-index">{{ index + 1 }}</div>
            </div>
          </div>
        </div>

        <!-- Tags Section -->
        <div class="tags-section">
          <q-select
            v-model="tags"
            outlined
            use-input
            use-chips
            multiple
            hide-dropdown-icon
            input-debounce="0"
            @new-value="createValue"
            placeholder="هشتگ‌ها را اضافه کنید..."
            class="tags-input"
            borderless
          >
            <template v-slot:prepend>
              <q-icon name="tag" class="input-icon" />
            </template>
            <template v-slot:hint>
              <span class="tags-hint">مثال: تخفیف، افتتاحیه، جدید</span>
            </template>
            <template v-slot:selected-item="scope">
              <q-chip
                removable
                dense
                @remove="scope.removeAtIndex(scope.index)"
                color="blue-1"
                text-color="blue-8"
                class="tag-chip"
              >
                <q-icon name="tag" size="14px" class="q-mr-xs" />
                {{ scope.opt }}
              </q-chip>
            </template>
          </q-select>
        </div>

        <!-- Visibility Section -->
        <div class="visibility-section">
          <q-select
            v-model="visibility"
            :options="visibilityOptions"
            outlined
            emit-value
            map-options
            class="visibility-select"
            borderless
          >
            <template v-slot:prepend>
              <q-icon :name="getVisibilityIcon(visibility)" class="input-icon" />
            </template>
            <template v-slot:selected-item="scope">
              <div class="visibility-item">
                <q-icon :name="getVisibilityIcon(scope.opt.value)" class="q-mr-xs" />
                {{ scope.opt.label }}
              </div>
            </template>
            <template v-slot:option="scope">
              <q-item v-bind="scope.itemProps" class="visibility-option">
                <q-item-section avatar>
                  <q-icon :name="getVisibilityIcon(scope.opt.value)" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>{{ scope.opt.label }}</q-item-label>
                  <q-item-label caption class="visibility-desc">
                    {{ getVisibilityDescription(scope.opt.value) }}
                  </q-item-label>
                </q-item-section>
              </q-item>
            </template>
          </q-select>
        </div>

        <!-- Action Buttons -->
        <div class="action-section">
          <div class="row justify-between items-center">
            <div class="col-auto">
              <div class="post-stats">
                <span v-if="content.length > 0" class="char-count">
                  {{ content.length }} کاراکتر
                </span>
              </div>
            </div>
            <div class="col-auto">
              <div class="action-buttons">
                <q-btn
                  flat
                  label="پیش‌نویس"
                  icon="save"
                  color="grey-7"
                  class="draft-btn"
                  @click="saveDraft"
                  :disable="!content.trim()"
                />
                <q-btn
                  label="انتشار پست"
                  type="submit"
                  color="primary"
                  :loading="submitting"
                  unelevated
                  class="submit-btn"
                  icon="send"
                  :disable="!canSubmit"
                />
              </div>
            </div>
          </div>
        </div>
      </q-form>
    </q-card-section>
  </q-card>
</template>

<script setup>
import { ref, computed } from 'vue';
import { api } from 'boot/axios';
import { useQuasar } from 'quasar';
import { useAuthStore } from 'stores/auth-store';

const content = ref('');
const imageFiles = ref([]);
const imagePreviewUrls = ref([]);
const submitting = ref(false);
const tags = ref([]);
const visibility = ref('PUBLIC');

const visibilityOptions = [
  { label: 'عمومی (برای همه)', value: 'PUBLIC' },
  { label: 'فقط هم‌محله‌ای‌ها', value: 'NEIGHBORHOOD' }
];

const $q = useQuasar();
const authStore = useAuthStore();
const emit = defineEmits(['postCreated']);

// Computed Properties
const canSubmit = computed(() => {
  return (content.value.trim() || imageFiles.value.length > 0) && !submitting.value;
});

// Methods
function getVisibilityIcon(value) {
  switch (value) {
    case 'PUBLIC':
      return 'public';
    case 'NEIGHBORHOOD':
      return 'holiday_village';
    default:
      return 'visibility';
  }
}

function getVisibilityDescription(value) {
  switch (value) {
    case 'PUBLIC':
      return 'همه کاربران می‌توانند ببینند';
    case 'NEIGHBORHOOD':
      return 'فقط کاربران همان محله';
    default:
      return '';
  }
}

// <<< FIX: پارامتر (files) حذف شد >>>
function handleImagesUpload() {
  imagePreviewUrls.value = imageFiles.value.map(file => URL.createObjectURL(file));
}

function removeImage(index) {
  imageFiles.value.splice(index, 1);
  imagePreviewUrls.value.splice(index, 1);

  $q.notify({
    type: 'positive',
    message: 'تصویر حذف شد',
    timeout: 1500
  });
}

function clearAllImages() {
  imageFiles.value = [];
  imagePreviewUrls.value = [];

  $q.notify({
    type: 'positive',
    message: 'همه تصاویر حذف شدند',
    timeout: 1500
  });
}

function clearForm() {
  content.value = '';
  imageFiles.value = [];
  imagePreviewUrls.value = [];
  visibility.value = 'PUBLIC';
  tags.value = [];
}

function onRejected(rejectedEntries) {
  $q.notify({
    type: 'negative',
    message: `${rejectedEntries.length} فایل به دلیل حجم یا نوع نامعتبر، رد شد.`,
    timeout: 3000
  });
}

function createValue(inputValue, doneFn) {
  const newTag = inputValue.trim();
  if (newTag.length > 0) {
    if (newTag.includes(',') || newTag.includes(' ')) {
      const tagList = newTag.split(/[, ]+/).filter(tag => tag.length > 0);
      tagList.forEach(tag => {
        const cleanTag = tag.startsWith('#') ? tag.substring(1).trim() : tag.trim();
        if (cleanTag) {
          doneFn(cleanTag, 'add-unique');
        }
      });
    } else {
      const cleanTag = newTag.startsWith('#') ? newTag.substring(1).trim() : newTag.trim();
      if (cleanTag) {
        doneFn(cleanTag, 'add-unique');
      }
    }
  }
}

function saveDraft() {
  // ذخیره پیش‌نویس در localStorage یا ارسال به سرور
  $q.notify({
    type: 'info',
    message: 'پیش‌نویس ذخیره شد',
    timeout: 2000
  });
}

async function submitPost() {
  if (!authStore.isAuthenticated) {
    $q.notify({
      type: 'negative',
      message: 'برای ارسال پست باید ابتدا وارد شوید.',
      actions: [{
        label: 'ورود',
        color: 'white',
        handler: () => {
          // redirect to login
        }
      }]
    });
    return;
  }

  if (!canSubmit.value) {
    $q.notify({
      type: 'warning',
      message: 'پست شما باید شامل متن یا حداقل یک عکس باشد.'
    });
    return;
  }

  submitting.value = true;

  const formData = new FormData();
  formData.append('content', content.value);
  formData.append('visibility', visibility.value);

  if (imageFiles.value.length > 0) {
    for (const file of imageFiles.value) {
      formData.append('uploaded_images', file);
    }
  }

  if (tags.value.length > 0) {
    const cleanTags = tags.value.map(tag =>
      tag.startsWith('#') ? tag.substring(1).trim() : tag.trim()
    );
    for (const tag of cleanTags) {
      formData.append('tags', tag);
    }
  }

  try {
    const response = await api.post('/api/posts/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    $q.notify({
      type: 'positive',
      message: 'پست شما با موفقیت منتشر شد!',
      icon: 'celebration',
      timeout: 3000
    });

    clearForm();
    emit('postCreated', response.data);

  } catch (error) {
    console.error("Error creating post:", error.response?.data || error.message);

    let errorMsg = 'خطا در انتشار پست.';
    if (error.response?.data) {
      const errors = error.response.data;
      if (errors.detail) {
        errorMsg = errors.detail;
      } else {
        const messages = [];
        for (const field in errors) {
          if (Array.isArray(errors[field])) {
            messages.push(errors[field].join(', '));
          } else {
            messages.push(String(errors[field]));
          }
        }
        if (messages.length > 0) errorMsg = messages.join('\n');
      }
    }

    $q.notify({
      type: 'negative',
      message: errorMsg,
      html: true,
      timeout: 5000
    });
  } finally {
    submitting.value = false;
  }
}
</script>

<style scoped>
.create-post-card {
  background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
  border-radius: 20px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.2);
  overflow: hidden;
  transition: all 0.3s ease;
}

.create-post-card:hover {
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.create-post-header {
  background: linear-gradient(135deg, #04b01e 0%, #054104 100%);
  color: white;
  padding: 1.5rem;
  position: relative;
}

.create-post-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 20"><defs><radialGradient id="a" cx="50%" cy="40%"><stop offset="0%" stop-color="%23ffffff" stop-opacity=".1"/><stop offset="100%" stop-color="%23ffffff" stop-opacity="0"/></radialGradient></defs><rect width="100" height="20" fill="url(%23a)"/></svg>');
  opacity: 0.1;
}

.user-avatar {
  border: 3px solid rgba(255, 255, 255, 0.3);
  position: relative;
  z-index: 1;
}

.user-name {
  font-weight: 600;
  font-size: 1.1rem;
  margin-bottom: 4px;
}

.create-prompt {
  opacity: 0.9;
  font-size: 0.9rem;
}

.create-icon {
  font-size: 1.5rem;
  opacity: 0.8;
}

.create-post-body {
  padding: 2rem;
}

.post-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.content-input-section {
  position: relative;
}

.content-input {
  background: #f8fafc;
  border-radius: 16px;
  transition: all 0.3s ease;
}

.content-input:focus-within {
  background: white;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
}

.content-input .q-field__control {
  border-radius: 16px;
}

.upload-section {
  position: relative;
}

.image-upload {
  border: 2px dashed #e2e8f0;
  border-radius: 16px;
  transition: all 0.3s ease;
  background: #f8fafc;
}

.image-upload:hover {
  border-color: #667eea;
  background: #f0f4ff;
}

.upload-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  text-align: center;
}

.upload-placeholder-icon {
  color: #cbd5e0;
  margin-bottom: 1rem;
}

.upload-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.upload-main-text {
  font-weight: 600;
  color: #4a5568;
  font-size: 1rem;
}

.upload-sub-text {
  font-size: 0.85rem;
  color: #718096;
}

.file-count-badge {
  background: linear-gradient(135deg, #07a219 0%, #069a0b 100%);
  color: white;
  border-radius: 20px;
  padding: 6px 12px;
}

.image-preview-section {
  background: #f8fafc;
  border-radius: 16px;
  padding: 1rem;
  border: 1px solid #e2e8f0;
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.preview-title {
  font-weight: 600;
  color: #2d3748;
  font-size: 0.9rem;
}

.clear-all-btn {
  color: #718096;
  transition: color 0.2s ease;
}

.clear-all-btn:hover {
  color: #e53e3e;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 1rem;
}

.image-preview-item {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.image-preview-item:hover {
  transform: scale(1.02);
}

.preview-image {
  border-radius: 12px;
}

.preview-overlay {
  position: absolute;
  top: 0;
  right: 0;
  left: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.image-preview-item:hover .preview-overlay {
  opacity: 1;
}

.remove-image-btn {
  background: rgba(239, 68, 68, 0.8);
  backdrop-filter: blur(4px);
}

.image-index {
  position: absolute;
  bottom: 6px;
  right: 6px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  font-weight: 600;
}

.tags-section {
  position: relative;
}

.tags-input {
  background: #f8fafc;
  border-radius: 16px;
  transition: all 0.3s ease;
}

.tags-input:focus-within {
  background: white;
  box-shadow: 0 0 0 2px rgba(7, 170, 88, 0.2);
}

.tags-hint {
  color: #718096;
  font-size: 0.85rem;
}

.tag-chip {
  border-radius: 20px;
  font-weight: 500;
  transition: transform 0.2s ease;
}

.tag-chip:hover {
  transform: scale(1.05);
}

.visibility-section {
  position: relative;
}

.visibility-select {
  background: #f8fafc;
  border-radius: 16px;
  transition: all 0.3s ease;
}

.visibility-select:focus-within {
  background: white;
  box-shadow: 0 0 0 2px rgba(11, 167, 2, 0.2);
}

.visibility-item {
  display: flex;
  align-items: center;
  color: #4a5568;
}

.visibility-option {
  border-radius: 8px;
  margin: 2px;
}

.visibility-desc {
  font-size: 0.8rem;
  color: #718096;
}

.input-icon {
  color: #05aa0d;
  opacity: 0.8;
}

.action-section {
  background: #f8fafc;
  border-radius: 16px;
  padding: 1rem 1.5rem;
  border: 1px solid #e2e8f0;
}

.post-stats {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.char-count {
  font-size: 0.85rem;
  color: #718096;
  font-weight: 500;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.draft-btn {
  border-radius: 12px;
  font-weight: 600;
  color: #718096;
  transition: all 0.2s ease;
}

.draft-btn:hover {
  background: rgba(113, 128, 150, 0.1);
  color: #16ad05;
}

.submit-btn {
  border-radius: 12px;
  font-weight: 600;
  background: linear-gradient(135deg, #069910 0%, #14c304 100%);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
  transition: all 0.2s ease;
  padding: 12px 24px;
}

.submit-btn:hover {
  box-shadow: 0 6px 20px rgba(9, 194, 12, 0.4);
  transform: translateY(-1px);
}

.submit-btn:disabled {
  background: #cbd5e0;
  box-shadow: none;
  transform: none;
}

/* Responsive Design */
@media (max-width: 768px) {
  .create-post-header,
  .create-post-body {
    padding: 1rem;
  }

  .post-form {
    gap: 1rem;
  }

  .image-grid {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: 0.5rem;
  }

  .action-buttons {
    flex-direction: column;
    gap: 0.5rem;
    width: 100%;
  }

  .draft-btn,
  .submit-btn {
    width: 100%;
  }

  .upload-area {
    padding: 1rem;
  }
}

/* Animations */
@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.create-post-card {
  animation: slideInUp 0.4s ease forwards;
}

/* Dark Mode Support */
@media (prefers-color-scheme: dark) {
  .create-post-card {
    background: linear-gradient(145deg, #2d3748 0%, #1a202c 100%);
    border-color: #4a5568;
  }

  .content-input,
  .tags-input,
  .visibility-select,
  .image-upload {
    background: #1a202c;
    color: #e2e8f0;
  }

  .image-preview-section,
  .action-section {
    background: #1a202c;
    border-color: #4a5568;
  }

  .upload-main-text {
    color: #e2e8f0;
  }

  .upload-sub-text,
  .char-count {
    color: #a0aec0;
  }
}
</style>
