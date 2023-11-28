<template>
  <div class="modal" v-if="show">
    <div class="modal-content">
      <span class="close-button" @click="close">&times;</span>
      <div class="flex">
        <img class="mr-6" :src="track.image">
        <div class="flex flex-col justify-center">
          <h4 class="mt-0 mb-2 uppercase text-gray-500 tracking-widest text-xs">{{ track.playlist_name }}</h4>
          <h1 class="mt-0 mb-2 text-white text-4xl">{{ track.name }}</h1>
          <p class="text-gray-600 mb-2 text-sm">{{ track.artist }}</p>
          <p class="text-gray-600 text-sm"><a>{{ track.album }}</a> - {{ track.minutes }} min {{ track.seconds }} sec</p>
        </div>
      </div>
      <div class="mt-6 flex justify-between">
        <div class="flex">
          <button @click="toggleAudio"
            class="animate-play-button mr-2 bg-green-500 text-green-100 block py-2 px-8 rounded-full">{{ isPlaying
              ? 'Pause' : 'Play' }}</button>
        </div>
      </div>
      <h2 class="dark:text-white">Más similares</h2>
      <button @click="searchSimilars"
        class="animate-arrow flex justify-center items-center mr-2 bg-grey-200 text-align-center text-green-100 block py-2 px-8 rounded-full w-full">
        <svg v-if="!isLoadingSimilars" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
          stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 13.5L12 21m0 0l-7.5-7.5M12 21V3" />
        </svg>
        <svg v-else aria-hidden="true"
          class="inline w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-gray-600 dark:fill-gray-300"
          viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path
            d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
            fill="currentColor" />
          <path
            d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
            fill="currentFill" />
        </svg>
      </button>
      <p v-if="execution_time" class="execution-time"> Tiempo de ejecución: {{ execution_time }} ms </p>
      <div class="similar-songs">
        <SmallSongCard v-for="song in similarSongs" :key="song.id" :track="song" />
      </div>
    </div>
  </div>
</template>
  
<script>
import SmallSongCard from './SmallSongCard.vue';
import { Howl } from 'howler';

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
      isLoadingSimilars: false,
    };
  },
  methods: {
    close() {
      this.$emit('close');
    },
    searchSimilars() {
      this.isLoadingSimilars = true;
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
        .catch(error => console.error('Error:', error)
        ).finally(() => {
          this.isLoadingSimilars = false;
        });
    },
    toggleAudio() {
      const url = 'http://localhost:3000/audios/' + this.track.id + '.mp3'
      if (!this.sound) {
        this.sound = new Howl({
          src: [url],
          html5: true,
          format: ['mp3'],
          onplay: () => {
            this.isPlaying = true;
          },
          onpause: () => {
            this.isPlaying = false;
          },
          onstop: () => {
            this.isPlaying = false;
          }
        });
      }
      if (this.sound.playing()) {
        this.sound.pause();
      } else {
        this.sound.play();
      }
    },
  }
};
</script>
  
<style scoped>
img {
  width: 200px;
  height: 200px;
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

.animate-arrow {
  transition: transform 0.3s ease;
}

.animate-arrow:hover {
  transform: scale(2.2);
}

.animate-play-button {
  transition: transform 0.3s ease;
}

.animate-play-button:hover {
  transform: scale(1.1);
}</style>
