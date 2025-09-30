<template>
  <q-card>
    <q-card-section>
      <div class="text-h6">اخبار مهم محله</div>
    </q-card-section>

    <div v-if="loading" class="q-pa-md"><q-skeleton type="text" v-for="n in 3" :key="n" class="q-my-sm" /></div>
    <div v-else-if="error" class="q-pa-md text-negative">خطا در دریافت اخبار.</div>
    <div v-else-if="news.length === 0" class="q-pa-md text-grey">خبر مهمی وجود ندارد.</div>

    <q-list v-else separator dense>
      <q-item v-for="item in news" :key="item.id" clickable :to="`/posts/${item.id}`">
        <q-item-section>
          <q-item-label lines="2">{{ item.content }}</q-item-label>
          <q-item-label caption>{{ formatDateTime(item.created_at) }}</q-item-label>
        </q-item-section>
         <q-item-section side top>
          <q-icon name="chevron_left" />
        </q-item-section>
      </q-item>
    </q-list>
  </q-card>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import { api } from 'boot/axios';
import { format, parseISO } from 'date-fns';

const news = ref([]);
const loading = ref(true);
const error = ref(false);

async function fetchNews() {
  loading.value = true;
  try {
    const response = await api.get('/api/important-news/');
    news.value = response.data.results || response.data;
  } catch (err) {
    console.error("Error fetching important news:", err);
    error.value = true;
  } finally {
    loading.value = false;
  }
}

function formatDateTime(dateTimeString) {
  if (!dateTimeString) return '';
  try { return format(parseISO(dateTimeString), 'yyyy/MM/dd'); }
  catch { return dateTimeString; }
}

onMounted(fetchNews);
</script>
