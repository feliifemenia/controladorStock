const express = require("express");
const database = require("./routes/database");
const cors = require("cors");

//Configuracion inicial
const app = express();
app.set("port", 4000);
app.set('view engine', 'ejs')
app.listen(app.get("port"));
console.log("Esuchando comunicaciones al puerto " + app.get("port"));

//Middlewares
app.use(cors({
    origin: ["http://127.0.0.1:5501", "http://localhost:5173", "http://127.0.0.1:5500"]
}));
app.use(express.json());

app.get("/", (req, res) => {
    console.log("Hola Mundo");
})

app.post("/consultar-producto", async (req, res) =>{
    const arrayDeCodigos = req.body;

    const connection = await database.getConnection();

    const id = 1;

    const result = await connection.query(`SELECT * FROM productos WHERE id = ?` , [id]);

    const {id2, nombre, descripcion, codigoProducto, cantidad, codigoUnidadBase, cantidadUnidad} = result[0];

    connection.release();

    res.status(200).json({ message: 'Consulta exitosa' });
})

app.post("/cargar-nuevo-producto", async (req, res)=>{
    
    const formData = req.body;

    console.log(formData);

    const {nombre_producto, descripcion_producto, codigo_producto, cantidad_producto, codigo_unidad_producto, cantidad_unidad_producto} = formData;

    const connection = await database.getConnection();

    if(codigo_producto == codigo_unidad_producto){//Se verifica que justo no se trate de un producto base.
        // Logica para agregar un producto base.
        try {

            const insertQuery = `
                INSERT INTO productos 
                    (nombre, descripcion, codigoProducto, cantidad, codigoUnidadBase, cantidadUnidad)
                VALUES (?, ?, ?, ?, ?, ?)`;

            const insertResult = await connection.query(insertQuery, [nombre_producto, descripcion_producto, codigo_producto, cantidad_producto, codigo_unidad_producto, cantidad_unidad_producto]);

            res.status(200).json({ message: "Producto cargado correctamente." });
        } 
        catch (error) {
            console.log(error);

            res.status(500).json({ message: "Error al procesar la consulta." });
        }
    }
    else{
        try{

            const [result] = await connection.query(`SELECT codigoProducto FROM productos WHERE codigoUnidadBase = ? AND codigoProducto = ?`, [codigo_unidad_producto, codigo_unidad_producto]); // Se busca en la BD el producto base para ver si ya esta creado, ya que no se puede crear un producto asociado a un codigo unidad de producto base inexistente.
        
            if(result.length === 0){
                // No se encontró el producto con el código de unidad base, lanzar un error
                return res.status(400).json({ message: "El código de unidad base no existe." });
            }
    
            //Logica en caso de que el producto base si exista

            const insertQuery = `
                INSERT INTO productos 
                    (nombre, descripcion, codigoProducto, cantidad, codigoUnidadBase, cantidadUnidad)
                VALUES (?, ?, ?, ?, ?, ?)`;

            const insertResult = await connection.query(insertQuery, [nombre_producto, descripcion_producto, codigo_producto, cantidad_producto, codigo_unidad_producto, cantidad_unidad_producto]);

            connection.release();

            res.status(200).json({ message: "Producto cargado correctamente." });
        }
        catch(error){

            console.log(error);

            res.status(500).json({ message: "Error al procesar la consulta." });
        }
    }
})

