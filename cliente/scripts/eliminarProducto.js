const formulario = document.getElementById("codigo-form");

formulario.addEventListener("submit", function(event){

    // Prevenir la acción del botón si algún campo es inválido
    event.preventDefault();
    if (!this.checkValidity()) {
        alert("Por favor, completa todos los campos obligatorios.");
    }

    const codigoAEliminar = document.getElementById("codigo-a-eliminar").value;

    obtener_datos(codigoAEliminar);

})

async function obtener_datos(codigoAEliminar) { // Funcion para obtener los datos del producto a eliminar
    
    try {
        const jsonData = {codigo: codigoAEliminar};

        const response = await fetch("http://localhost:4000/informacion-producto", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(jsonData)
        })

        if (!response.ok) {
            throw new Error('Error en la solicitud');
        }

        const datosProducto = await response.json();

        //Hago que se muestren los datos.

        document.getElementById('nombreProducto').textContent = datosProducto.nombre;
        document.getElementById('descripcionProducto').textContent = datosProducto.descripcion;
        
        // Mostrar el contenedor con los datos y los botones
        document.getElementById('datosProducto').style.display = 'block';

        // Manejar el botón Confirmar
        document.getElementById('btnConfirmar').onclick = function() {
            confirmarAccion(codigoAEliminar);
        };

        // Manejar el botón Rechazar
        document.getElementById('btnRechazar').onclick = function() {
            rechazarAccion();
        };

    } 
    catch (error) {
        //Falta hacer el Manejo de error cuando no existe el codigo que se ingreso.
        console.log("El codigo ingresado no existe");
        console.log(error);
    }
}

async function confirmarAccion(codigo) {

    try {
        const jsonData = {codigoAEliminar: codigo};
        
        const response = await fetch("http://localhost:4000/eliminar-producto", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(jsonData)
        })

        if(!response.ok){
            throw new Error('Error en la solicitud');
        }

        const inputEliminar = document.getElementById("codigo-a-eliminar");

        inputEliminar.value = '';

        const mensajeEliminado = document.querySelector('.producto-eliminado');
        mensajeEliminado.style.display = 'block';

        document.getElementById('datosProducto').style.display = 'none';

        setTimeout(() => {
            mensajeEliminado.style.display = 'none';
        }, 3000);

    } 
    catch (error) {
        console.log(error);
    }
}

function rechazarAccion() {
    const inputEliminar = document.getElementById("codigo-a-eliminar");

    inputEliminar.value = '';

    document.getElementById('datosProducto').style.display = 'none';

}