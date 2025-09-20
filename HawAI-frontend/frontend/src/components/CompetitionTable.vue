<template>
  <div class="container py-3">
    <h3>Competition Analysis</h3>
    <div v-if="loading" class="my-3">Loading…</div>
    <div v-else>
      <h5>HawAI — Focus</h5>
      <p>{{ hawai.focus }}</p>

      <h5 class="mt-4">Competitors</h5>
      <table class="table table-striped table-bordered">
        <thead class="thead-light">
          <tr>
            <th>Name</th>
            <th>Focus</th>
            <th>Strengths</th>
            <th>Weaknesses</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in competitors" :key="c.name">
            <td>{{ c.name }}</td>
            <td>{{ c.focus }}</td>
            <td>
              <ul>
                <li v-for="s in c.strengths" :key="s">{{ s }}</li>
              </ul>
            </td>
            <td>
              <ul>
                <li v-for="w in c.weaknesses" :key="w">{{ w }}</li>
              </ul>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  </template>

<script>
export default {
  name: "CompetitionTable",
  data() {
    return {
      loading: true,
      competitors: [],
      hawai: {}
    };
  },
  async mounted() {
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL || ''}/competition/`);
      if (!res.ok) throw new Error("Network response was not ok");
      const data = await res.json();
      this.competitors = data.competitors || [];
      this.hawai = data.hawai || {};
    } catch (e) {
      console.error("Failed to load competition:", e);
    } finally {
      this.loading = false;
    }
  }
};
</script>

<style scoped>
.container { max-width: 1000px; }
</style>


