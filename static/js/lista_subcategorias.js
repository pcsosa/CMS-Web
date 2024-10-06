function volver() {
  // Obtener la URL actual
  let currentUrl = window.location.href
  // Reemplazar '/lista/' con '/adminsub/lista/' y añadir el ID de la categoría

  let newUrl = currentUrl.replace(/\/adminsub\/lista\/\d+/, '/cat')

  // Redirigir a la nueva URL
  window.location.href = newUrl
}
function editSubcategoria(id) {
  document.getElementById('name-' + id).style.display = 'none'
  document.getElementById('input-name-' + id).style.display = 'inline'
  document.querySelector('#row-' + id + ' .btn-primary').style.display = 'none'
  document.querySelector('#row-' + id + ' .btn-success').style.display =
    'inline'
  document.querySelector('#row-' + id + ' .btn-danger').style.display = 'none'
}

function saveSubcategoria(id) {
  var newName = document.getElementById('input-name-' + id).value
  var row = document.getElementById('row-' + id)

  // Crear un formulario temporal para enviar los datos
  var form = document.createElement('form')
  form.method = 'POST'
  var url = window.location.href;
  var nuevoUrl = url.replace(/\/lista\/(\d+)\//, '/editar/');
  console.log(nuevoUrl);
  form.action = nuevoUrl // Asegúrate de tener una URL configurada para actualizar

  // Agregar campos ocultos para el ID de la subcategoría y el nuevo nombre
  var inputId = document.createElement('input')
  inputId.type = 'hidden'
  inputId.name = 'id'
  inputId.value = id
  form.appendChild(inputId)

  var inputNombre = document.createElement('input')
  inputNombre.type = 'hidden'
  inputNombre.name = 'nombre'
  inputNombre.value = newName
  form.appendChild(inputNombre)

  // Agregar CSRF token
  var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value
  var inputCsrfToken = document.createElement('input')
  inputCsrfToken.type = 'hidden'
  inputCsrfToken.name = 'csrfmiddlewaretoken'
  inputCsrfToken.value = csrfToken
  form.appendChild(inputCsrfToken)

  document.body.appendChild(form)
  form.submit()

  // Actualizar la vista para mostrar el nuevo nombre
  document.getElementById('name-' + id).textContent = newName
  document.getElementById('name-' + id).style.display = 'inline'
  document.getElementById('input-name-' + id).style.display = 'none'
  row.querySelector('.btn-primary').style.display = 'inline'
  row.querySelector('.btn-success').style.display = 'none'
  row.querySelector('.btn-danger').style.display = 'inline'
}

function crearSubcategoria(categoriaId) {
  // Mostrar un cuadro de entrada para solicitar el nombre de la nueva subcategoría
  var nombre = prompt('Ingrese el nombre de la nueva subcategoría:')

  // Verificar si el usuario ingresó un nombre
  if (nombre) {
    // Crear un formulario temporal para enviar el dato
    var form = document.createElement('form')
    form.method = 'POST'

    // Aquí debes usar comillas invertidas para interpolar variables
    let currentUrl = window.location.href
    let newUrl = currentUrl.replace(/\/lista\/\d+/, `/crear`)

    form.action = newUrl

    // Crear un campo oculto para el nombre de la subcategoría
    var inputNombre = document.createElement('input')
    inputNombre.type = 'hidden'
    inputNombre.name = 'nombre'
    inputNombre.value = nombre
    form.appendChild(inputNombre)

    // Crear un campo oculto para el ID de la categoría
    var inputCategoriaId = document.createElement('input')
    inputCategoriaId.type = 'hidden'
    inputCategoriaId.name = 'categoria_id'
    inputCategoriaId.value = categoriaId
    form.appendChild(inputCategoriaId)

    // Agregar CSRF token si estás usando Django
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value
    var inputCsrfToken = document.createElement('input')
    inputCsrfToken.type = 'hidden'
    inputCsrfToken.name = 'csrfmiddlewaretoken'
    inputCsrfToken.value = csrfToken
    form.appendChild(inputCsrfToken)

    // Añadir el formulario al cuerpo del documento y enviarlo
    document.body.appendChild(form)
    form.submit()
  }
}
