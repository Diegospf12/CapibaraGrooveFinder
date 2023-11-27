<template>
  <form class="flex w-1/6 mt-4 mb-4 items-center mx-auto">
    <span class="ms-3 text-sm font-medium mr-4 text-gray-900 dark:text-white">MyIndex</span>
    <label class="relative inline-flex items-center me-5 cursor-pointer">
    <input type="checkbox" v-model="option" class="sr-only peer" checked>
    <div class="w-11 h-6 bg-gray-200 rounded-full peer dark:bg-gray-700 peer-focus:ring-4 peer-focus:ring-green-300 dark:peer-focus:ring-green-800 peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-green-600"></div>
    <span class="ms-3 text-sm font-medium text-gray-900 dark:text-white">Postgres</span>
  </label>
  </form>
  <form class="flex w-1/2 items-center mx-auto">
    <div class="relative w-3/6">
      <div class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
        <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
          fill="none" viewBox="0 0 21 21">
          <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M11.15 5.6h.01m3.337 1.913h.01m-6.979 0h.01M5.541 11h.01M15 15h2.706a1.957 1.957 0 0 0 1.883-1.325A9 9 0 1 0 2.043 11.89 9.1 9.1 0 0 0 7.2 19.1a8.62 8.62 0 0 0 3.769.9A2.013 2.013 0 0 0 13 18v-.857A2.034 2.034 0 0 1 15 15Z" />
        </svg>
      </div>
      <input v-model="query" type="text" id="voice-search"
        class="bg-gray-50 border-2 border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full ps-10 p-2.5 dark:bg-white dark:border-2 dark:border-gray-800 dark:placeholder-black dark:text-black dark:focus:ring-blue-500 dark:focus:border-blue-500"
        placeholder="Ingresa tu búsqueda" required>
      <button type="button" class="absolute inset-y-0 end-0 flex items-center pe-3">
        <svg class="w-4 h-4 text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white" aria-hidden="true"
          xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 16 20">
          <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M15 7v3a5.006 5.006 0 0 1-5 5H6a5.006 5.006 0 0 1-5-5V7m7 9v3m-3 0h6M7 1h2a3 3 0 0 1 3 3v5a3 3 0 0 1-3 3H7a3 3 0 0 1-3-3V4a3 3 0 0 1 3-3Z" />
        </svg>
      </button>
    </div>
    <input v-model="k" type="number" id="k-input"
      class="bg-gray-50 border-2 border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-1/4 p-2.5 dark:bg-white dark:border-2 dark:border-gray-800 dark:placeholder-black dark:text-black dark:focus:ring-blue-500 dark:focus:border-blue-500"
      placeholder="Ingresa el k" required>
    <button @click.prevent="search"
      class="bg-white hover:bg-gray-100 text-gray-800 font-semibold py-2 px-4 border border-gray-400 rounded shadow">
      Buscar
    </button>
  </form>

  <p v-if="time" class="execution-time"> Tiempo de ejecución: {{ time }} ms </p>

  <transition-group name="fade" tag="div">
    <div v-for="(track, index) in tracks" :key="track.id" class="song-card-container" :style="{ animationDelay: index * 0.5 + 's' }">
      <SongCard :track="track" />
    </div>
  </transition-group>
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
      tracks: [],
      time: null,
      option: false,
    }
  },
  methods: {
    async search() {
      this.tracks = []; 
      const optionText = this.option ? 'postgres' : 'myindex';
      const response = await fetch(`http://localhost:8000/search?query=${this.query}&k=${this.k}&option=${optionText}`)
      const data = await response.json()
      this.tracks = data.tracks
      this.time = data.execution_time
    }
  }
}
</script>

<style scoped>
.execution-time {
  text-align: center;
  font-weight: bold;
  color: white;
  margin-top: 15px;
  margin-bottom: 15px;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}

.song-card-container {
  max-width: 80%; /* Ajusta este valor para cambiar el ancho máximo de las tarjetas */
  margin: auto;
  margin-top: 10px;
  margin-bottom: 10px;
  animation: fadeIn 1s ease-in-out;
}

@keyframes fadeIn {
  0% { opacity: 0; transform: translateY(-30px); }
  100% { opacity: 1; transform: translateY(0); }
}
</style>