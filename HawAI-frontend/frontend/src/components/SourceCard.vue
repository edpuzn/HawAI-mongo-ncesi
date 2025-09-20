<template>
  <div>
    <div v-for="s in sources" :key="s.url" class="small">
      <a :href="s.url" target="_blank" rel="noopener" class="link-secondary">{{ s.title }}</a>
    </div>
  </div>
</template>

<script lang="ts" setup>
defineProps<{ sources: { title: string; url: string }[] }>()
</script>
