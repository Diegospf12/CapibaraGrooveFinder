<template>
  <div class="modal" v-if="show">
    <div class="modal-content">
      <span class="close-button" @click="close">&times;</span>
      <h2>{{ name }}</h2>
      <p>{{ lyrics }}</p>
    </div>
  </div>
</template>
  
<script>
export default {
  props: ['show', 'lyrics', 'name'],
  methods: {
    close() {
      this.$emit('close');
    }
  }
}
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

h2 {
  text-align: center;
  font-family: 'Circular', Circular, -apple-system, BlinkMacSystemFont, Roboto, 'Helvetica Neue', sans-serif;
  font-size: 50px;
  margin-bottom: 5px;
  margin-top: 30px;
  color: white;
}

p {
  font-family: 'Arial', sans-serif;
  font-size: 18px;
  line-height: 1.6;
  color: #A7A7A7;
  text-align: justify;
  padding: 20px;
  margin-top: 5px;
}
</style>