<template>
  <div class="container py-4">
    <div class="alert alert-warning py-2 small" role="alert">
      Bu uygulama bilgi amaçlıdır; acil durumda 112’yi arayın.
    </div>
    <div class="mb-3" style="min-height: 50vh;">
      <MessageBubble v-for="(m, idx) in messages" :key="idx" :text="m.text" :from="m.from" :tags="m.tags" :sources="m.sources" />
    </div>
    <ChatBox @send="onSend" />
    <CompetitionTable class="mt-4" />
  </div>
</template>

<script lang="ts" setup>
import { onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import ChatBox from '../components/ChatBox.vue'
import MessageBubble from '../components/MessageBubble.vue'
import CompetitionTable from '../components/CompetitionTable.vue'

const store = useStore()
const messages = computed(() => store.state.messages)

function onSend(msg: string) {
  store.dispatch('sendMessage', msg)
}

onMounted(() => {
  store.dispatch('fetchHealth')
})
</script>

