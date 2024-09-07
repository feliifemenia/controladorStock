//Codigo para el archivo "cargarProducto.html
const buttonCargarProducto = document.getElementById("button-cargar-producto");

document.querySelector("form").addEventListener("submit", function(event) {
    // Validar todo el formulario
    if (!this.checkValidity()) {
        // Prevenir la acción del botón si algún campo es inválido
        event.preventDefault();
        alert("Por favor, completa todos los campos obligatorios.");
    }

    const nombreProducto = document.getElementById("nombre-producto").value;
    const descripcionProducto = document.getElementById("descripcion-producto").value;
    const codigoProducto = document.getElementById("codigo-producto").value;
    const cantidadProducto = document.getElementById("cantidad-producto").value;
    const codigoUnidadProducto = document.getElementById("codigo-unidad").value;
    const cantidadUnidadProducto = document.getElementById("cantidad-unidad").value;

    const formData = {
        nombre_producto: nombreProducto,
        descripcion_producto: descripcionProducto,
        codigo_producto: codigoProducto,
        cantidad_producto: cantidadProducto,
        codigo_unidad_producto: codigoUnidadProducto, 
        cantidad_unidad_producto: cantidadUnidadProducto,
    }

    cargar_nuevo_producto(formData);

});

async function cargar_nuevo_producto(formData) {    

    try{
        const jsonData = JSON.stringify(formData);

        console.log("hola")

        const response = await fetch("http://localhost:4000/cargar-nuevo-producto", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: jsonData});
        
        if(!response.ok){
            throw new Error("Error al Cargar el Nuevo Producto");
        }
    }
    catch(error){
        console.log(error);
    }

    //falta hacer la parte de manejar los errores.

}
