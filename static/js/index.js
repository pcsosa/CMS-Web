const listar_categorias = async () => {
  try {
      const response = await fetch("http://127.0.0.1:8000/listar/");
      const data = await response.json();

      let content = ``;
      data.categorias.forEach((categorias,index) => {

          content += `
          <tr>
              <><td>${index} </td><td>${categoria.nombre}</td></>
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