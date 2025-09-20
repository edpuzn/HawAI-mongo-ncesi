<template>
  <div class="d-flex flex-wrap gap-1">
    <span v-for="t in tags" :key="t" class="badge bg-success">SDG {{ t }}</span>
  </div>
</template>

<script lang="ts" setup>
defineProps<{ tags: string[] }>()
</script>
