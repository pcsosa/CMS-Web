const mobileScreen = window.matchMedia('(max-width: 990px)')

document.addEventListener('DOMContentLoaded', function () {
  const dropdownToggles = document.querySelectorAll(
    '.dashboard-nav-dropdown-toggle'
  )
  const menuToggle = document.querySelector('.menu-toggle')
  const dashboardNav = document.querySelector('.dashboard-nav')
  const dashboard = document.querySelector('.dashboard')

  // Función para manejar el clic en los elementos con clase .dashboard-nav-dropdown-toggle
  dropdownToggles.forEach(function (toggle) {
    toggle.addEventListener('click', function () {
      const closestDropdown = toggle.closest('.dashboard-nav-dropdown')
      const otherDropdowns = document.querySelectorAll(
        '.dashboard-nav-dropdown.show'
      )

      // Mostrar o esconder el dropdown seleccionado
      if (closestDropdown) {
        closestDropdown.classList.toggle('show')
      }

      // Asegurarse de cerrar cualquier dropdown anidado o abierto anteriormente
      otherDropdowns.forEach(function (dropdown) {
        if (dropdown !== closestDropdown) {
          dropdown.classList.remove('show')
        }
      })
    })
  })

  // Función para manejar el clic en el botón de menú
  menuToggle.addEventListener('click', function () {
    if (mobileScreen.matches) {
      dashboardNav.classList.toggle('mobile-show')
    } else {
      dashboard.classList.toggle('dashboard-compact')
    }
  })
})
