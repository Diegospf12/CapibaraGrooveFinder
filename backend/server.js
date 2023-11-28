const express = require('express');
const app = express();

// Ruta para servir los archivos estáticamente
app.use('/audios', express.static('/Users/diegopachecoferrel/Desktop/audio'));

// Inicia el servidor
app.listen(3000, () => {
  console.log('Servidor corriendo en http://localhost:3000');
});