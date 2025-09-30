<template>
  <q-dialog :model-value="modelValue" @update:model-value="val => emit('update:modelValue', val)" persistent @before-show="onBeforeShow">
    <q-card style="min-width: 50vw; max-width: 600px;">
      <q-card-section class="row items-center q-pb-none">
        <div class="text-h6">{{ isEditing ? 'ویرایش پست' : 'ایجاد پست جدید' }}</div>
        <q-space />
        <q-btn icon="close" flat round dense v-close-popup />
      </q-card-section>

      <q-card-section class="q-pt-md">
        <q-form @submit.prevent="submitPost" class="q-gutter-md">
          <q-input
            v-model="postData.content"
            label="محتوا"
            type="textarea"
            filled
            autogrow
          />

          <!-- مدیریت عکس‌ها (موجود و جدید) -->
          <!-- نمایش عکس‌های موجود (برای حالت ویرایش) -->
          <div v-if="isEditing && existingImages.length > 0" class="q-mb-sm">
            <div class="text-caption text-grey-7">عکس‌های فعلی:</div>
            <div class="row q-col-gutter-sm q-mt-xs">
              <div v-for="img in existingImages" :key="img.id" class="col-4 col-sm-3">
                <q-img :src="img.image" :ratio="1" class="rounded-borders">
                  <q-btn class="absolute-top-right" size="sm" flat dense round icon="delete" color="white" @click="confirmDeleteImage(img.id)" style="background: rgba(0,0,0,0.5)" title="حذف عکس" />
                </q-img>
              </div>
            </div>
          </div>

          <q-file
            v-model="newImageFiles"
            label="افزودن عکس‌های جدید"
            filled
            clearable
            multiple
            append
            accept=".jpg, .jpeg, .png, image/*"
            @rejected="onRejected"
          >
            <template v-slot:prepend><q-icon name="add_a_photo" /></template>
          </q-file>

          <q-select
            v-model="postData.tags"
            label="هشتگ‌ها"
            filled
            use-input
            use-chips
            multiple
            hide-dropdown-icon
            input-debounce="0"
            new-value-mode="add-unique"
            @new-value="createTagValue"
          />

          <q-select
            v-model="postData.visibility"
            :options="visibilityOptions"
            label="قابلیت مشاهده"
            filled
            emit-value
            map-options
            dense
          />

          <q-card-actions align="right" class="q-pt-md">
            <q-btn flat label="لغو" v-close-popup />
            <q-btn :label="isEditing ? 'ذخیره تغییرات' : 'ارسال پست'" color="primary" type="submit" :loading="submitting" unelevated />
          </q-card-actions>
        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { ref, computed,  } from 'vue';
import { api } from 'boot/axios';
import { useQuasar } from 'quasar';

const props = defineProps({
  modelValue: Boolean, // برای v-model
  postToEdit: {        // پستی که برای ویرایش پاس داده می‌شود
    type: Object,
    default: null
  }
});

const emit = defineEmits(['update:modelValue', 'postSaved']);

const $q = useQuasar();
const isEditing = computed(() => !!props.postToEdit);
const submitting = ref(false);

// State برای فرم
const postData = ref({});
const newImageFiles = ref([]); // برای q-file
const existingImages = ref([]); // عکس‌هایی که از قبل روی پست بوده‌اند

const visibilityOptions = [
  { label: 'عمومی (برای همه)', value: 'PUBLIC' },
  { label: 'فقط هم‌محله‌ای‌ها', value: 'NEIGHBORHOOD' }
];

// این تابع قبل از نمایش مودال اجرا می‌شود و فرم را مقداردهی می‌کند
function onBeforeShow() {
  newImageFiles.value = []; // همیشه فایل‌های جدید را ریست کن
  if (isEditing.value) {
    // حالت ویرایش: فرم را با داده‌های پست موجود پر کن
    postData.value = {
      id: props.postToEdit.id,
      content: props.postToEdit.content,
      tags: [...props.postToEdit.tags], // کپی کردن آرایه برای جلوگیری از تغییر ناخواسته prop
      visibility: props.postToEdit.visibility,
    };
    existingImages.value = [...props.postToEdit.images];
  } else {
    // حالت ایجاد: فرم را ریست کن
    postData.value = {
      content: '',
      tags: [],
      visibility: 'PUBLIC',
    };
    existingImages.value = [];
  }
}

// تابع برای مدیریت هوشمند ورود هشتگ (مشابه CreatePostForm)
function createTagValue(inputValue, doneFn) {
  const newTag = inputValue.trim();
  if (newTag.length > 0) {
    if (newTag.includes(',') || newTag.includes(' ')) {
      const tagList = newTag.split(/[, ]+/).filter(tag => tag.length > 0);
      tagList.forEach(tag => {
        const cleanTag = tag.startsWith('#') ? tag.substring(1).trim() : tag.trim();
        if (cleanTag) doneFn(cleanTag, 'add-unique');
      });
    } else {
      const cleanTag = newTag.startsWith('#') ? newTag.substring(1).trim() : newTag.trim();
      if (cleanTag) doneFn(cleanTag, 'add-unique');
    }
  }
}

function onRejected(rejectedEntries) {
  $q.notify({ type: 'negative', message: `${rejectedEntries.length} فایل رد شد.` });
}

async function submitPost() {
  submitting.value = true;
  const formData = new FormData();

  // اضافه کردن فیلدهای متنی
  formData.append('content', postData.value.content);
  formData.append('visibility', postData.value.visibility);

  // اضافه کردن تگ‌ها
  if (postData.value.tags.length > 0) {
    const cleanTags = postData.value.tags.map(tag => tag.startsWith('#') ? tag.substring(1).trim() : tag.trim());
    formData.append('tags', cleanTags.join(',')); // django-taggit-serializer می‌تواند رشته جدا شده با کاما را هم پردازش کند
  } else {
    formData.append('tags', ''); // ارسال رشته خالی برای پاک کردن همه تگ‌ها
  }

  // اضافه کردن عکس‌های جدید
  if (newImageFiles.value.length > 0) {
    for (const file of newImageFiles.value) {
      formData.append('uploaded_images', file);
    }
  }

  try {
    let response;
    if (isEditing.value) {
      // حالت ویرایش (با PATCH)
      // توجه: این API فقط فیلدهای ارسالی را آپدیت می‌کند (content, tags, visibility)
      // و عکس‌های جدید را اضافه می‌کند. حذف عکس‌های قدیمی نیاز به یک API جداگانه دارد.
      response = await api.patch(`/api/posts/${postData.value.id}/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      $q.notify({ type: 'positive', message: 'پست با موفقیت ویرایش شد!' });
    } else {
      // حالت ایجاد
      response = await api.post('/api/posts/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      $q.notify({ type: 'positive', message: 'پست با موفقیت ایجاد شد!' });
    }

    emit('postSaved', response.data); // به والد اطلاع بده که پست ذخیره شد
    emit('update:modelValue', false); // مودال را ببند

  } catch (error) {
    console.error("Error submitting post:", error.response?.data || error);
    $q.notify({ type: 'negative', message: 'خطا در ذخیره پست.' });
  } finally {
    submitting.value = false;
  }
}

// تابع برای حذف عکس‌های موجود (نیاز به API Endpoint سفارشی در بک‌اند دارد)
function confirmDeleteImage(imageId) {
  $q.dialog({
    title: 'تأیید حذف عکس',
    message: 'آیا از حذف این عکس مطمئن هستید؟',
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      // **نکته:** شما باید یک API برای حذف عکس بسازید، مثلاً:
      // DELETE /api/posts/images/{image_id}/
      // await api.delete(`/api/posts/images/${imageId}/`);

      // به عنوان یک راه حل موقت (اگر API حذف عکس ندارید)، فقط از لیست UI حذف می‌کنیم
      // اما در رفرش بعدی برمی‌گردد.
      existingImages.value = existingImages.value.filter(img => img.id !== imageId);

      $q.notify({ type: 'info', message: 'قابلیت حذف عکس از سرور هنوز پیاده‌سازی نشده است.' });

      // پس از پیاده‌سازی API:
      // emit('postSaved'); // یا یک event خاص برای آپدیت
    } catch {
       $q.notify({ type: 'negative', message: 'خطا در حذف عکس.' });
    }
  });
}
</script>
