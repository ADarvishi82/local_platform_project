<template>
  <q-card>
    <q-card-section>
      <div class="text-h6">رویدادهای آینده</div>
    </q-card-section>

    <div v-if="loading" class="q-pa-md"><q-skeleton type="text" v-for="n in 3" :key="n" class="q-my-sm" /></div>
    <div v-else-if="error" class="q-pa-md text-negative">خطا در دریافت رویدادها.</div>
    <div v-else-if="events.length === 0" class="q-pa-md text-grey">رویداد نزدیکی در محله شما وجود ندارد.</div>

    <q-list v-else separator dense>
      <q-item v-for="event in events" :key="event.id" clickable>
        <q-item-section>
          <q-item-label lines="1" class="text-weight-medium">{{ event.title }}</q-item-label>
          <q-item-label caption>{{ event.location_name || event.neighborhood_name }}</q-item-label>
          <q-item-label caption class="text-primary">{{ formatDateTime(event.start_time) }}</q-item-label>
        </q-item-section>
      </q-item>
    </q-list>
  </q-card>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import { api } from 'boot/axios';
import { format, parseISO } from 'date-fns';
import { faIR } from 'date-fns/locale';

const events = ref([]);
const loading = ref(true);
const error = ref(false);

async function fetchEvents() {
  loading.value = true;
  try {
    const response = await api.get('/api/upcoming-events/');
    events.value = response.data.results || response.data;
  } catch (err) {
    console.error("Error fetching upcoming events:", err);
    error.value = true;
  } finally {
    loading.value = false;
  }
}

function formatDateTime(dateTimeString) {
  if (!dateTimeString) return '';
  try { return format(parseISO(dateTimeString), 'eeee, d MMMM, ساعت H:mm', { locale: faIR }); }
  catch { return dateTimeString; }
}

onMounted(fetchEvents);
</script>
