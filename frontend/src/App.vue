<template>
  <div id="app">
    <img class="centered-image" :src="require('@/assets/capibara_2.jpg')" alt="Descripción de la imagen">
    <SongBrowser />
  </div>
</template>

<script>
import SongBrowser from './components/SongBrowser.vue';

export default {
  components: {
    SongBrowser
  },
  mounted() {
    document.body.style.backgroundColor = 'black';
  }
};
</script>

<style scoped>
.centered-image {
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 20%;
}
</style>