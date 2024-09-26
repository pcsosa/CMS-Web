function initTinyMCE() {
  tinymce.init({
    selector: '#content',
    plugins: 'link lists code',
    toolbar:
      'undo redo | styleselect | bold italic underline | copy cut paste | alignleft aligncenter alignright | bullist numlist outdent indent | link',
    menubar: 'file edit view insert format tools table',
    branding: false,
    height: 400,
    setup: function (editor) {
      editor.on('change', function () {
        editor.save() // Sincroniza el contenido del editor con el textarea
      })
    }
  })
}

document.addEventListener('DOMContentLoaded', function () {
  initTinyMCE()
})

function selectTemplate(templateType) {
  const formTitle = document.getElementById('form-title')
  const contentImageInput = document.getElementById('content-image')
  const contentImageLabel = document.getElementById('content-image-label')

  formTitle.textContent =
    templateType === 'blog' ? 'Crear Blog' : 'Crear Contenido Multimedia'

  // Mostrar u ocultar el input de la imagen según la plantilla seleccionada
  if (templateType === 'multimedia') {
    contentImageInput.style.display = 'block'
    contentImageLabel.style.display = 'block'
  } else {
    contentImageInput.style.display = 'none'
    contentImageLabel.style.display = 'none'
  }
}

// Cargar subcategorías basadas en la categoría seleccionada
function cargarSubcategorias() {
  const categoriaId = parseInt(document.getElementById('categoria').value)
  const subcategoriasSelect = document.getElementById('subcategoria')
  const subcategorias = JSON.parse(
    document.getElementById('subcategorias-data').textContent || '[]'
  )

  // Limpiar el select de subcategorías y agregar opción predeterminada
  subcategoriasSelect.innerHTML =
    '<option value="">Selecciona una subcategoría</option>'

  if (isNaN(categoriaId)) return

  const subcategoriasFiltradas = subcategorias.filter(
    (subcat) => subcat.fields.categoria === categoriaId
  )

  if (subcategoriasFiltradas.length === 0) {
    subcategoriasSelect.innerHTML +=
      '<option value="">Sin subcategorías</option>'
    return
  }

  subcategoriasFiltradas.forEach((subcat) => {
    const option = document.createElement('option')
    option.value = subcat.pk
    option.textContent = subcat.fields.nombre
    subcategoriasSelect.appendChild(option)
  })
}
