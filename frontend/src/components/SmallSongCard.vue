<template>
    <div class="song-card">
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
  </div>
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
  
  .song-distance {
    font-size: 1em;
    color: #666;
  }
  </style>