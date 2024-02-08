document.addEventListener("DOMContentLoaded", function() {
    var botonInformacion = document.getElementById("informacion");
    var infoBox = document.getElementById("infoBox");

    // Función para mostrar o ocultar la información según su estado actual
    function toggleInfoBox() {
        if (infoBox.style.display === "block") {
            infoBox.style.display = "none";
        } else {
            infoBox.style.display = "block";
        }
    }

    // Mostrar u ocultar la información cuando se hace clic en el botón
    botonInformacion.addEventListener("click", function(event) {
        event.stopPropagation(); // Evita que el evento se propague hacia arriba
        toggleInfoBox();
    });

    // Ocultar la información cuando se hace clic en cualquier otro lugar de la pantalla
    document.addEventListener("click", function() {
        infoBox.style.display = "none";
    });

    // Evitar que hacer clic en la información la oculte
    infoBox.addEventListener("click", function(event) {
        event.stopPropagation(); // Evita que el evento se propague hacia arriba
    });
});