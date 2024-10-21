function redirigirUrl(categoriaId) {
  // Obtener la URL actual
  let currentUrl = window.location.href

  // Reemplazar '/lista/' con '/adminsub/lista/' y añadir el ID de la categoría
  let newUrl = currentUrl.replace('/cat/', `/adminsub/lista/${categoriaId}`)

  // Redirigir a la nueva URL
  window.location.href = newUrl
}

$('#crearModal').on('hidden.bs.modal', function () {
  $(this).find('form').trigger('reset')
})

$('#editModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Botón que abrió el modal
  var id = button.data('id') // Extrae el ID de los datos del botón
  var nombre = button.data('nombre') // Extrae el nombre de los datos del botón
  var descripcion = button.data('descripcion') // Extrae la descripción de los datos del botón

  var modal = $(this)
  modal.find('#categoriaId').val(id)
  modal.find('#nombre').val(nombre)
  modal.find('#descripcion').val(descripcion)

  let curr = window.location.href;

  // Actualiza la URL del formulario en el modal
  var actionUrl = curr.replace('/cat/',`/cat/editar/${id}/`)
  modal.find('form').attr('action', actionUrl)
})
