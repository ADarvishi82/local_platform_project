<template>
  <q-card>
    <q-card-section><div class="text-h6">موضوعات محبوب</div></q-card-section>
    <q-card-section v-if="loading"><q-skeleton type="QChip" :count="5" /></q-card-section>
    <q-card-section v-else class="q-pt-none">
      <q-chip v-for="tag in tags" :key="tag.name" clickable :to="`/tags/${tag.name}`">
        #{{ tag.name }} 
      </q-chip>
    </q-card-section>
  </q-card>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import { api } from 'boot/axios';
const tags = ref([]);
const loading = ref(true);
async function fetchTags() {
  loading.value = true;
  try {
    const response = await api.get('/api/popular-tags/');
    tags.value = response.data;
  } catch (error) { console.error("Error fetching popular tags:", error); }
  finally { loading.value = false; }
}
onMounted(fetchTags);
</script>
