<template>
  <q-card>
    <q-card-section v-if="loading">
      <q-skeleton type="text" width="60%" class="q-mb-sm" />
      <q-skeleton type="text" height="80px" />
    </q-card-section>
    <q-card-section v-else-if="error">
      <div class="text-grey text-center">{{ error }}</div>
    </q-card-section>
    <div v-else-if="stats">
      <q-card-section>
        <div class="text-h6">{{ stats.name }}</div>
        <div class="text-caption text-grey">{{ stats.city }}</div>
      </q-card-section>
      <q-list separator>
        <q-item><q-item-section>همسایه</q-item-section><q-item-section side>{{ stats.resident_count }}</q-item-section></q-item>
        <q-item><q-item-section>کسب‌وکار</q-item-section><q-item-section side>{{ stats.business_count }}</q-item-section></q-item>
        <q-item><q-item-section>پست‌ها</q-item-section><q-item-section side>{{ stats.post_count }}</q-item-section></q-item>
      </q-list>
    </div>
  </q-card>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import { api } from 'boot/axios';
const stats = ref(null);
const loading = ref(true);
const error = ref('');
async function fetchStats() {
  loading.value = true;
  try {
    const response = await api.get('/api/my-neighborhood/stats/');
    stats.value = response.data;
  } catch (error) {
    error.value = 'محله شما مشخص نیست.';
  } finally {
    loading.value = false;
  }
}
onMounted(fetchStats);
</script>
