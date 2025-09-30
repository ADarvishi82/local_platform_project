<template>
  <q-card class="chatbot-widget" style="width: 350px; height: 500px; display: flex; flex-direction: column;">
    <q-card-section class="bg-primary text-white row items-center q-py-sm">
      <q-avatar icon="support_agent" size="md" />
      <div class="text-subtitle1 q-ml-sm">دستیار هوشمند محلی</div>
      <q-space />
    </q-card-section>

    <q-scroll-area class="col q-pa-md" ref="chatAreaRef">
      <!-- تاریخچه پیام‌ها -->
      <div v-for="(msg, index) in messages" :key="index" class="q-mb-md">
        <!-- پیام‌های متنی -->
        <q-chat-message
          :name="msg.from === 'bot' ? 'دستیار' : 'شما'"
          :text="[msg.text]"
          :sent="msg.from === 'user'"
          :bg-color="msg.from === 'user' ? 'primary' : 'grey-3'"
          :text-color="msg.from === 'user' ? 'white' : 'black'"
        />

        <!-- نمایش نتایج کسب‌وکار (اگر وجود دارد) -->
        <div v-if="msg.from === 'bot' && msg.results && msg.results.length > 0" class="q-mt-sm q-gutter-y-sm">
          <q-card
            v-for="biz in msg.results"
            :key="biz.id"
            flat
            bordered
            class="business-result-card"
            @click="goToBusiness(biz.id)"
          >
            <q-item>
              <q-item-section avatar>
                <q-avatar rounded>
                  <img :src="biz.logo_url || 'https://cdn.quasar.dev/img/generic-avatar.png'">
                </q-avatar>
              </q-item-section>
              <q-item-section>
                <q-item-label class="text-weight-bold ellipsis">{{ biz.business_name }}</q-item-label>
                <q-item-label caption v-if="biz.category">{{ biz.category.name }}</q-item-label>
              </q-item-section>
              <q-item-section side top>
                <q-rating
                  v-if="biz.average_rating > 0"
                  :model-value="biz.average_rating"
                  size="14px"
                  color="orange"
                  icon="star"
                  readonly
                />
              </q-item-section>
            </q-item>
          </q-card>
        </div>
      </div>
    </q-scroll-area>

    <q-separator />

    <q-card-section>
      <q-form @submit.prevent="sendMessage" class="row items-center q-gutter-sm">
        <q-input
          v-model="userInput"
          placeholder="پیام خود را بنویسید..."
          outlined
          dense
          rounded
          class="col"
          :disable="loading"
          @keyup.enter.prevent="sendMessage"
        />
        <q-btn round dense flat icon="send" type="submit" color="primary" :loading="loading" />
      </q-form>
    </q-card-section>
  </q-card>
</template>

<script setup>
import { ref, nextTick } from 'vue';
import { api } from 'boot/axios';
import { useRouter } from 'vue-router';

const messages = ref([
  { from: 'bot', text: 'سلام! دنبال چه چیزی در محله می‌گردید؟ (مثلاً: کافه در ونک)' }
]);
const userInput = ref('');
const loading = ref(false);
const chatAreaRef = ref(null);
const router = useRouter();

const N8N_WEBHOOK_URL = 'https://alidarvishi82.app.n8n.cloud/webhook-test/cba75afc-9abf-475c-b4f7-78575230b0c7'; // <<< آدرس وبهوک n8n

async function sendMessage() {
  if (!userInput.value.trim()) return;

  const userMessageText = userInput.value;
  messages.value.push({ from: 'user', text: userMessageText });
  userInput.value = '';
  loading.value = true;
  scrollToBottom();

  try {
    const response = await api.post(N8N_WEBHOOK_URL, {
      message: userMessageText
    });

    // دیباگ: خروجی رو چاپ کن
    console.log('📨 پاسخ n8n:', response.data);

    const botResponse = Array.isArray(response.data) ? response.data[0] : response.data;

    // دیباگ: ساختار داده رو چاپ کن
    console.log('🔍 ساختار داده:', {
      reply: botResponse.reply,
      results: botResponse.results,
      type: botResponse.type
    });

    messages.value.push({
      from: 'bot',
      text: botResponse.reply || botResponse.response || "پاسخی دریافت نشد.", // هر دو حالت رو چک کن
      results: botResponse.results || []
    });

  } catch (error) {
    console.error("❌ خطا در ارتباط با n8n:", error);
    messages.value.push({ from: 'bot', text: 'متاسفانه در ارتباط با دستیار مشکلی پیش آمده.' });
  } finally {
    loading.value = false;
    scrollToBottom();
  }
}

function goToBusiness(businessId) {
  router.push(`/business/${businessId}`);
}

function scrollToBottom() {
  nextTick(() => {
    const scrollArea = chatAreaRef.value;
    if (scrollArea) {
      scrollArea.setScrollPosition('vertical', scrollArea.getScrollTarget().scrollHeight, 300);
    }
  });
}
</script>

<style lang="scss" scoped>
@import 'quasar/src/css/variables.sass';

.chatbot-widget {
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.15);
}
.business-result-card {
  transition: background-color 0.3s;
  cursor: pointer;
  &:hover {
    background-color: $grey-2;
  }
}
</style>
