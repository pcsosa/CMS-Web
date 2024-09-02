let dataTable;
let dataTableIsInitialized = false;

const listar_categorias = async () => {
  try {
      const response = await fetch("http://127.0.0.1:8000/listar/");
      const data = await response.json();

      let content = ``;
      data.categorias.forEach((categoria,index) => {

          content += `
          <tr>
              <td>${index + 1} </td>
              <td>${categoria.nombre}</td>
              <td>${categoria.descripcion}</td>
          </tr> 
          `;
      });
      tableBody_categorias.innerHTML = content;   
  } catch (ex) {
      alert(ex)
  }
};
window.addEventListener("load", async () => {
  await listar_categorias();
});