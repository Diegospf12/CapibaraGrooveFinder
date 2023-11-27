<template>
  <!-- CARD 3 -->
  <div class="bg-gray-800 shadow-lg rounded p-3 song-card">
    <div class="group relative">
      <img class="w-full md:w-72 block rounded" :src="track.image" alt="" />
      <div
        class="absolute bg-black rounded bg-opacity-0 group-hover:bg-opacity-60 w-full h-full top-0 flex items-center group-hover:opacity-100 transition justify-evenly">
        <button @click="playPreview"
          class="hover:scale-110 text-white opacity-0 transform translate-y-3 group-hover:translate-y-0 group-hover:opacity-100 transition">
          <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor"
            class="bi bi-play-circle-fill" viewBox="0 0 16 16">
            <path
              d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM6.79 5.093A.5.5 0 0 0 6 5.5v5a.5.5 0 0 0 .79.407l3.5-2.5a.5.5 0 0 0 0-.814l-3.5-2.5z" />
          </svg>
        </button>
      </div>
    </div>
    <div class="p-5">
      <h3 ref="trackName" class="text-white text-lg truncate">{{ track.name }}</h3>
      <p class="text-gray-400">{{ track.artist }}</p>
      <p class="text-gray-500">Dist: {{ track.distance.toFixed(2) }}</p>
    </div>
    <audio ref="audioPreview" :src="track.preview_url" type="audio/mpeg"></audio>
  </div>
  <!-- END OF CARD 3 -->

  <!--div class="song-card">
    <img :src="track.image" alt="Imagen de la canción" class="song-image" />
    <div class="song-info">
      <h2 class="song-name">{{ track.name }}</h2>
      <p class="song-artist">{{ track.artist }}</p>
      <p class="song-distance">Distancia: {{ track.distance }}</p>
    </div>
    <div>
       <audio controls class="song-preview" @loadeddata="updatePreviewUrl">
        <source :src="previewUrl" type="audio/mpeg">
        Tu navegador no soporta el elemento de audio.
      </audio>
    </div>
  </div-->
</template>
    
    
<script>
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
      previewUrl: this.track.preview_url,
      isPlaying: false,
    };
  },
  mounted() {
    this.$nextTick(() => {
      if (this.$refs.trackName.scrollWidth > this.$refs.trackName.clientWidth) {
        this.$refs.trackName.classList.add('animate-marquee');
      }
    });
  },
  watch: {
    'track.preview_url': function (newUrl) {
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
    playPreview() {
      const audio = this.$refs.audioPreview;
      if (audio.paused) {
        audio.play();
        this.isPlaying = true;
        audio.onended = () => {
          this.isPlaying = false;
        };
      } else {
        audio.pause();
        this.isPlaying = false;
      }
    },
  }
};
</script>
    
<style scoped>
.song-card {
  /*display: flex;
    border: 1px solid #ccc;
    justify-content: space-between;
    align-items: center;
    flex-direction: row;
    padding: 10px;
    margin-bottom: 10px;
    border-radius: 5px;*/
  max-height: 400px;
  max-width: 280px;
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

.song-distance {
  font-size: 1em;
  color: #666;
}

.truncate {
  white-space: nowrap;
  overflow: hidden;
}

.animate-marquee {
  text-overflow: clip;
  animation: marquee 10s linear infinite;
}

@keyframes marquee {
  0% {
    text-indent: 0;
  }

  50% {
    text-indent: -100%;
  }

  100% {
    text-indent: 0;
  }
}
</style>