
function limpiarCampos() {
    // Limpiar el campo de búsqueda
    document.querySelector('input[name="busqueda"]').value = "";

    // Restablecer las opciones seleccionadas a las predeterminadas (opción vacía)
    document.querySelector('select[name="categoria"]').selectedIndex = 0;
    document.querySelector('select[name="autor"]').selectedIndex = 0;
    document.querySelector('select[name="orden"]').selectedIndex = 0;
}
