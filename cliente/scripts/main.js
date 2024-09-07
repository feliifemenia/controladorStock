//Codigo para el archivo "index.html"

const inputCodigo = document.getElementById("input-codigo");
const contenedorCodigos = document.getElementById("div-lista-productos");
const listaProductos = document.getElementById("lista-productos");

let codigos = [];
let timeout;


inputCodigo.addEventListener('input', ()=>{

    clearTimeout(timeout);

    timeout = setTimeout(()=>{
        const codigo = inputCodigo.value;

        codigos.push(codigo);

        inputCodigo.value = '';

        const html = codigos.map((codigoArray)=> `<li>Codigo: ${codigoArray}</li>`).join('<br>');
        
        listaProductos.innerHTML = html;
    }, 500)
})

document.addEventListener('keydown', (event)=>{

    if (event.code === 'Enter'){

        descontar_pedido();
    }
})

async function descontar_pedido(){

    let timeout;

    try{

        const jsonData = JSON.stringify(codigos);

        console.log(jsonData);

        const response = await fetch("http://localhost:4000/consultar-producto", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: jsonData});

        if(!response.ok){
            throw new Error("Error al cargar el pedido");
        }

        clearTimeout(timeout);
        
        // Mostrar el mensaje
        mensaje.style.display = 'block';
        
        // Ocultar el mensaje después de 2 segundos (2000 milisegundos)
        timeout = setTimeout(() => {
            mensaje.style.display = 'none';
        }, 1000); // Ajusta el tiempo según sea necesario
        
        codigos = [];
    
        listaProductos.innerHTML = '';
    }
    catch (error) {
        console.log(error);
    }
}

