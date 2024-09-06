let dataTable;
let dataTableIsInitialized = false;

const listar_categorias = async () => {
  try {
    const response = await fetch("http://127.0.0.1:8000/list_cat/");
    const data = await response.json();
    console.log(data);
   /*let content = ``;
    data.categorias.forEach((categoria, index) => {

      content += `
          <tr>
              <td>${index + 1} </td>
              <td>${categoria.nombre}</td>
              <td>${categoria.descripcion}</td>
          </tr> 
          `;
    });
    tableBody_categorias.innerHTML = content;*/
  } catch (ex) {
    alert(ex)
  }
};
window.addEventListener("load", async () => {
  await listar_categorias();
});


/*SOLUCION DEL BUG
const express = require('express');
const app = express();
app.use('/static', express.static('static'));
app.listen(8000, () => console.log('Servidor corriendo en el puerto 8000'));*/
