<template>
    <div class="modal" v-if="show">
      <div class="modal-content">
        <span class="close-button" @click="close">&times;</span>
        <audio ref="audioRef" controls :src="track.preview_url" @loadedmetadata="playAudio"></audio>
        <h2>Más similares</h2>
        <button @click="searchSimilars">Buscar</button>
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
      execution_time: null
    };
  },
  methods: {
    close() {
      this.$emit('close');
    },
    playAudio() {
      this.$refs.audioRef.play();
    },
    searchSimilars() {
      fetch(`http://localhost:8000/get_top_k?track_id=${this.track.id}&k=5`)
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
    }
  }
};
</script>
  
  <style scoped>
  .modal {
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0,0,0,0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
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
  display: flex;
  flex-direction: column;
  align-items: center;
}
    </style>