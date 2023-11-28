<template>
  <div class="song-card">
    <img :src="track.image" alt="Imagen de la canción" class="song-image" />
    <div class="song-info">
      <h2 class="song-name">{{ track.name }}</h2>
      <p class="song-artist">{{ track.artist }}</p>
      <p class="song-score">Score: {{ track.score }}</p>
    </div>
    <div>
      <button @click="openSimilarModal" type="button"
        class="inline-block rounded-full bg-neutral-50 px-6 pb-2 pt-2.5 text-xs font-medium uppercase leading-normal text-neutral-800 shadow-[0_4px_9px_-4px_#cbcbcb] transition duration-150 ease-in-out hover:bg-neutral-100 hover:shadow-[0_8px_9px_-4px_rgba(203,203,203,0.3),0_4px_18px_0_rgba(203,203,203,0.2)] focus:bg-neutral-100 focus:shadow-[0_8px_9px_-4px_rgba(203,203,203,0.3),0_4px_18px_0_rgba(203,203,203,0.2)] focus:outline-none focus:ring-0 active:bg-neutral-200 active:shadow-[0_8px_9px_-4px_rgba(203,203,203,0.3),0_4px_18px_0_rgba(203,203,203,0.2)] dark:shadow-[0_4px_9px_-4px_rgba(251,251,251,0.3)] dark:hover:shadow-[0_8px_9px_-4px_rgba(251,251,251,0.1),0_4px_18px_0_rgba(251,251,251,0.05)] dark:focus:shadow-[0_8px_9px_-4px_rgba(251,251,251,0.1),0_4px_18px_0_rgba(251,251,251,0.05)] dark:active:shadow-[0_8px_9px_-4px_rgba(251,251,251,0.1),0_4px_18px_0_rgba(251,251,251,0.05)]">
        Similares
      </button>
      <SimilarModal :show="showSimilar" :track="track" @close="showSimilar = false" />
      <button @click="openLyricsModal" type="button"
        class="inline-block mr-5 rounded-full bg-neutral-800 px-6 pb-2 pt-2.5 text-xs font-medium uppercase leading-normal text-neutral-50 shadow-[0_4px_9px_-4px_rgba(51,45,45,0.7)] transition duration-150 ease-in-out hover:bg-neutral-800 hover:shadow-[0_8px_9px_-4px_rgba(51,45,45,0.2),0_4px_18px_0_rgba(51,45,45,0.1)] focus:bg-neutral-800 focus:shadow-[0_8px_9px_-4px_rgba(51,45,45,0.2),0_4px_18px_0_rgba(51,45,45,0.1)] focus:outline-none focus:ring-0 active:bg-neutral-900 active:shadow-[0_8px_9px_-4px_rgba(51,45,45,0.2),0_4px_18px_0_rgba(51,45,45,0.1)] dark:bg-neutral-900 dark:shadow-[0_4px_9px_-4px_#030202] dark:hover:bg-neutral-900 dark:hover:shadow-[0_8px_9px_-4px_rgba(3,2,2,0.3),0_4px_18px_0_rgba(3,2,2,0.2)] dark:focus:bg-neutral-900 dark:focus:shadow-[0_8px_9px_-4px_rgba(3,2,2,0.3),0_4px_18px_0_rgba(3,2,2,0.2)] dark:active:bg-neutral-900 dark:active:shadow-[0_8px_9px_-4px_rgba(3,2,2,0.3),0_4px_18px_0_rgba(3,2,2,0.2)]">
        Letra
      </button>
      <LyricsModal :show="showLyrics" :lyrics="track.lyrics" :name="track.name" @close="showLyrics = false" />
    </div>
  </div>
</template>
  
  
<script>
import LyricsModal from './LyricsComponent.vue';
import SimilarModal from './TopKPageComponent.vue'

export default {
  components: {
    LyricsModal,
    SimilarModal
  },
  props: {
    track: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      showLyrics: false,
      showSimilar: false,
    };
  },
  methods: {
    openLyricsModal() {
      this.showLyrics = true;
    },
    openSimilarModal() {
      this.showSimilar = true;
    }
  }
};
</script>
  
<style scoped>
.bg-neutral-800 {
  background-color: rgb(76, 158, 83);
  margin-left: 5px;
  /* Resto de las propiedades CSS... */
}

.song-card {
  display: flex;
  /*border: 1px solid #ccc;*/
  justify-content: space-between;
  align-items: center;
  flex-direction: row;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
  background-color: #141414;
}

.song-image {
  width: 130px;
  height: 130px;
  margin-right: 10px;
}

.song-info {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  flex-grow: 1;
  margin-left: 10px;
}

.song-name {
  font-weight: bold;
  color: white;
  font-family: 'Circular', Circular, -apple-system, BlinkMacSystemFont, Roboto, 'Helvetica Neue', sans-serif;
  margin-bottom: 5px;
  margin-top: 3px;
  font-size: 1.5em;
  max-width: 780px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.song-artist {
  font-family: 'Circular', Circular, -apple-system, BlinkMacSystemFont, Roboto, 'Helvetica Neue', sans-serif;
  margin-bottom: 1px;
  margin-top: 1px;
  color: #A7A7A7;
}

.song-score {
  font-size: 1em;
  color: #666;
}
</style>
