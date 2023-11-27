<template>
  <div class="modal" v-if="show">
    <div class="modal-content">
      <span class="close-button" @click="close">&times;</span>
      <!-- header -->
      <div class="flex">
        <img class="mr-6" :src="track.image">
        <div class="flex flex-col justify-center">
          <!-- content -->
          <h4 class="mt-0 mb-2 uppercase text-gray-500 tracking-widest text-xs">{{ track.playlist_name }}</h4>
          <h1 class="mt-0 mb-2 text-white text-4xl">{{ track.name }}</h1>

          <p class="text-gray-600 mb-2 text-sm">{{ track.artist }}</p>
          <p class="text-gray-600 text-sm"><a>{{ track.album }}</a> - {{ track.minutes }} min {{ track.seconds }} sec</p>
        </div>
      </div>

      <!-- action buttons -->
      <div class="mt-6 flex justify-between">
        <div class="flex">
          <button @click="toggleAudio" class="mr-2 bg-green-500 text-green-100 block py-2 px-8 rounded-full">{{ isPlaying ? 'Pause' : 'Play' }}</button>
        </div>
      </div>

      <audio ref="audioRef" :src="track.preview_url"></audio>

      <!--audio ref="audioRef" controls :src="track.preview_url"></audio-->
      <h2 class="dark:text-white">Más similares</h2>
      <p v-if="execution_time" class="execution-time"> Tiempo de ejecución: {{ execution_time }} ms </p>
      <div class="similar-songs">
        <SmallSongCard v-for="song in similarSongs" :key="song.id" :track="song" />
      </div>
    </div>
  </div>
</template>
  
<script>
import SmallSongCard from './SmallSongCard.vue';

export default {
  components: {
    SmallSongCard
  },
  props: ['show', 'track'],
  data() {
    return {
      similarSongs: [],
      execution_time: null,
      isPlaying: false,
    };
  },
  mounted() {
    this.searchSimilars();
  },
  methods: {
    close() {
      this.$emit('close');
    },
    playAudio() {
      this.$refs.audioRef.play();
    },
    searchSimilars() {
      fetch(`http://localhost:8000/get_top_k?track_id=${this.track.id}&k=8`)
        .then(response => response.json())
        .then(data => {
          if (data.tracks && Array.isArray(data.tracks)) {
            this.similarSongs = data.tracks;
            this.execution_time = data.execution_time;
          } else {
            console.error('Data is not an array:', data);
          }
        })
        .catch(error => console.error('Error:', error));
    },
    toggleAudio() {
      const audio = this.$refs.audioRef;
      if (audio.paused) {
        audio.play();
        this.isPlaying = true;
      } else {
        audio.pause();
        this.isPlaying = false;
      }
    },
  }
};
</script>
  
<style scoped>
img {
  width: 200px;  /* Cambia esto al ancho que desees */
  height: 200px; /* Cambia esto a la altura que desees */
}

h2 {
  text-align: center;
  font-size: 40px;
  margin-top: 5px;
  margin-bottom: 10px;
}

.execution-time {
  text-align: center;
  font-weight: bold;
  color: white;
  margin-top: 15px;
  margin-bottom: 15px;
}

.modal {
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
  background-color: #141414;
  margin: 15% auto;
  padding: 20px;
  width: 80%;
}

.close-button {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close-button:hover,
.close-button:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

.similar-songs {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  justify-content: center;
}
</style>