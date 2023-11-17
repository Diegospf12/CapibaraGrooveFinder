<template>
  <div class="song-card">
  <img :src="track.image" alt="Imagen de la canción" class="song-image" />
  <div class="song-info">
    <h2 class="song-name">{{ track.name }}</h2>
    <p class="song-artist">{{ track.artist }}</p>
    <p class="song-score">Score: {{ track.score }}</p>
  </div>
  <div>
     <!--audio controls class="song-preview" @loadeddata="updatePreviewUrl">
      <source :src="previewUrl" type="audio/mpeg">
      Tu navegador no soporta el elemento de audio.
    </audio-->
    <button @click="openSimilarModal" class="lyrics-button">Similares</button>
    <SimilarModal :show="showSimilar" :track="track" @close="showSimilar = false" />
    <button @click="openLyricsModal" class="lyrics-button">Mostrar letra</button>
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
      previewUrl: this.track.preview_url,
      showLyrics: false,
      showSimilar: false,
    };
  },
  watch: {
    'track.preview_url': function(newUrl) {
      this.previewUrl = '';
      this.$nextTick(() => {
        this.previewUrl = newUrl;
      });
    }
  },
  methods: {
    updatePreviewUrl() {
      this.previewUrl = this.track.preview_url;
    },
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
.song-card {
  display: flex;
  border: 1px solid #ccc;
  justify-content: space-between;
  align-items: center;
  flex-direction: row;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
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
  color: black;
  font-family: 'Circular', Circular, -apple-system, BlinkMacSystemFont, Roboto, 'Helvetica Neue', sans-serif;
  margin-bottom: 5px;
  margin-top: 3px;
}

.song-lyrics {
  margin: 10px 0;
}

.song-artist {
  font-family: 'Circular', Circular, -apple-system, BlinkMacSystemFont, Roboto, 'Helvetica Neue', sans-serif;
  margin-bottom: 1px;
  margin-top: 1px;
}

.song-score {
  font-size: 1em;
  color: #666;
}
</style>