const express = require('express');
const app = express();

// Configuración para servir archivos estáticos
app.use('/static', express.static('static'));

// Iniciar el servidor
app.listen(8000, () => {
    console.log('Servidor corriendo en el puerto 8000');
});
