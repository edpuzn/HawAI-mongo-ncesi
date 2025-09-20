<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/">HawAI</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarsExampleDefault" aria-controls="navbarsExampleDefault" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarsExampleDefault">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item"><router-link class="nav-link" to="/">Home</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/about">About</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/competition">Competition</router-link></li>
          </ul>
          <div class="d-flex align-items-center">
            <span v-if="health === true" class="badge bg-success">Online</span>
            <span v-else-if="health === false" class="badge bg-danger">Offline</span>
            <span v-else class="badge bg-secondary">Unknown</span>
          </div>
        </div>
      </div>
    </nav>

    <router-view />

    <div class="position-fixed bottom-0 end-0 p-3" style="z-index: 1080">
      <div ref="toastEl" class="toast align-items-center text-white bg-danger border-0" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="d-flex">
          <div class="toast-body">
            Çok fazla istek gönderdiniz. Lütfen kısa bir süre sonra tekrar deneyin.
          </div>
          <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, watch, computed, onMounted } from 'vue'
import { useStore } from 'vuex'

const store = useStore()
const health = computed(() => store.state.health.reachable)
const rateLimited = computed(() => store.state.rateLimited)
const toastEl = ref<HTMLDivElement | null>(null)
let toastInstance: any = null

onMounted(() => {
  // @ts-ignore
  const bootstrap = (window as any).bootstrap
  if (toastEl.value && bootstrap && bootstrap.Toast) {
    toastInstance = new bootstrap.Toast(toastEl.value, { autohide: true, delay: 3000 })
  }
})

watch(rateLimited, (val) => {
  if (val && toastInstance) {
    toastInstance.show()
  }
})
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
