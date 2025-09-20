<template>
  <div :class="['d-flex mb-2', from === 'user' ? 'justify-content-end' : 'justify-content-start']">
    <div :class="['card', from === 'user' ? 'bg-primary text-white' : 'bg-light']" style="max-width: 75%">
      <div class="card-body">
        <p class="card-text mb-2" style="white-space: pre-wrap;">{{ text }}</p>
        <SdgTags v-if="tags && tags.length" :tags="tags" />
        <SourceCard v-if="sources && sources.length" :sources="sources" class="mt-2" />
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import SdgTags from './SdgTags.vue'
import SourceCard from './SourceCard.vue'

defineProps<{ text: string; from: 'user' | 'bot'; tags?: string[]; sources?: { title: string; url: string }[] }>()
</script>
