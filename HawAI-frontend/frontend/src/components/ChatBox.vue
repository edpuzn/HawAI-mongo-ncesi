<template>
  <form @submit.prevent="onSubmit" class="d-flex gap-2">
    <input v-model="text" type="text" class="form-control" placeholder="Mesajınızı yazın" :disabled="disabled" />
    <button class="btn btn-primary" type="submit" :disabled="disabled || !text.trim()">Gönder</button>
  </form>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'

const emit = defineEmits<{ (e: 'send', value: string): void }>()
const store = useStore()
const text = ref('')
const disabled = computed(() => store.state.isLoading)

function onSubmit() {
  if (!text.value.trim()) return
  emit('send', text.value)
  text.value = ''
}
</script>
