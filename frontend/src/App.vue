<template>
  <div id="app">
    <img class="centered-image" :src="require('@/assets/capibara_2.jpg')" alt="Descripción de la imagen">
    <SongBrowser />
    <!--form @submit.prevent="handleSubmit">
      <input type="file" accept=".wav" @change="handleFileChange" />
      <input type="number" v-model.number="k" />
      <button type="submit">Buscar</button>
    </form>
    <audio controls v-if="previewUrl">
      <source :src="previewUrl" type="audio/wav">
      Tu navegador no soporta el elemento de audio.
    </audio>
    <p v-if="execution_time">Tiempo de ejecución: {{ execution_time }} segundos</p>
    <song-card v-for="track in tracks" :key="track.id" :track="track" /-->
  </div>
</template>

<script>
//import SongCard from './components/SongCard.vue';
import SongBrowser from './components/SongBrowser.vue';

export default {
  components: {
    //SongCard,
    SongBrowser
  },
  mounted() {
    document.body.style.backgroundColor = 'black';
  },
  data() {
    return {
      //tracks: [],
      //file: null,
      //k: 5,
      //previewUrl: null,
      //execution_time: null
    };
  },
  methods: {/*
    handleSubmit() {
      if (!this.file) {
        console.error('No file selected');
        return;
      }

      const formData = new FormData();
      formData.append('file', this.file);

      fetch(`http://localhost:8000/get_k?k=${this.k}`, {
        method: 'POST',
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        if (data.tracks && Array.isArray(data.tracks)) {
          this.tracks = data.tracks;
          this.execution_time = data.execution_time;
        } else {
          console.error('Data is not an array:', data);
        }
      })
      .catch(error => console.error('Error:', error));
    },
    handleFileChange(event) {
      const file = event.target.files[0];
      if (file && file.type === 'audio/wav') {
        if (this.previewUrl) {
          URL.revokeObjectURL(this.previewUrl);
        }
        this.file = file;
        this.previewUrl = URL.createObjectURL(file);
      } else {
        console.error('Invalid file type:', file.type);
      }
      event.target.value = null;
    }*/
  }
};
</script>

<style scoped>
.centered-image {
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 20%; /* Ajusta este valor para cambiar el tamaño de la imagen */
}
</style>