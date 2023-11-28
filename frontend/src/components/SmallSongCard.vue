<template>
  <div class="bg-gray-800 shadow-lg rounded p-3 song-card">
    <div class="group relative">
      <img class="w-full md:w-72 block rounded" :src="track.image" alt="" />
      <div
        class="absolute bg-black rounded bg-opacity-0 group-hover:bg-opacity-60 w-full h-full top-0 flex items-center group-hover:opacity-100 transition justify-evenly">
        <button @click="toggleAudio"
          class="hover:scale-110 text-white opacity-0 transform translate-y-3 group-hover:translate-y-0 group-hover:opacity-100 transition">
          <svg v-if="!isPlaying" xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor"
            class="bi bi-play-circle-fill" viewBox="0 0 16 16">
            <path
              d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM6.79 5.093A.5.5 0 0 0 6 5.5v5a.5.5 0 0 0 .79.407l3.5-2.5a.5.5 0 0 0 0-.814l-3.5-2.5z" />
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor"
            class="bi bi-pause-circle-fill" viewBox="0 0 16 16">
            <path
              d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM6 5a1 1 0 0 0-1 1v4a1 1 0 0 0 2 0V6a1 1 0 0 0-1-1zm4 0a1 1 0 0 0-1 1v4a1 1 0 0 0 2 0V6a1 1 0 0 0-1-1z" />
          </svg>
        </button>
      </div>
    </div>
    <div class="p-5">
      <h3 ref="trackName" class="text-white text-lg truncate">{{ track.name }}</h3>
      <p class="text-gray-400">{{ track.artist }}</p>
      <p class="text-gray-500">Dist: {{ track.distance.toFixed(2) }}</p>
    </div>
  </div>
</template>
    
    
<script>
import { Howl } from 'howler';

export default {
  components: {
  },
  props: {
    track: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      isPlaying: false,
    };
  },
  methods: {
    toggleAudio() {
      const url = 'http://localhost:3000/audios/'+this.track.id+'.mp3'
      console.log(url);
      if (!this.sound) {
        this.sound = new Howl({
          src: [url],
          html5: true,
          format: ['mp3']
        });
      }
      if (this.sound.playing()) {
        this.sound.pause();
        this.isPlaying = false;
      } else {
        this.sound.play();
        this.isPlaying = true;
      }
    },
  }
};
</script>
    
<style scoped>
.song-card {
  max-height: 400px;
  max-width: 280px;
}

.truncate {
  white-space: nowrap;
  overflow: hidden;
}
</style>