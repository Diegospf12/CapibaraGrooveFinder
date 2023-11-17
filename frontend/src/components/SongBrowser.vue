<template>
  <div class="container">
    <div>
      <input v-model="query" type="text" placeholder="Ingresa tu búsqueda">
      <input v-model="k" type="number" placeholder="Ingresa el k">
      <button @click="search">Buscar</button>
    </div>
  </div>
  <div v-for="track in tracks" :key="track.id">
      <SongCard :track="track" />
    </div>
</template>

<script>
import SongCard from './SongCard.vue'

export default {
  components: {
    SongCard
  },
  data() {
    return {
      query: '',
      k: null,
      tracks: []
    }
  },
  methods: {
    async search() {
      const response = await fetch(`http://localhost:8000/search?query=${this.query}&k=${this.k}`)
      const data = await response.json()
      this.tracks = data.tracks
    }
  }
}
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 25px;
  margin-bottom: 15px;
}

.container input[type="text"] {
  width: 350px; /* Ajusta este valor según tus necesidades */
  height: 25px; /* Ajusta este valor según tus necesidades */
  padding: 5px;
}

.container input[type="number"] {
  width: 100px; /* Ajusta este valor según tus necesidades */
  height: 25px; /* Ajusta este valor según tus necesidades */
  padding: 5px;
}

.container button {
  width: 70px; /* Ajusta este valor según tus necesidades */
  height: 35px; /* Ajusta este valor según tus necesidades */
  padding: 5px;
  font-size: 1em; /* Ajusta este valor según tus necesidades */
  margin-left: 10px;
}
</style>