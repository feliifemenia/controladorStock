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

    //Primero verifico que todos los codigos que se envian en el array esten creados en la base de datos. 

    try {
        arrayDeCodigos.forEach(async codigo => {
            const insertQuery = `SELECT EXISTS (
                                    SELECT 1
                                    FROM productos
                                    WHERE codigoProducto = ?
                                );`

            const result = await connection.query(insertQuery, codigo);
        })
    } 
    catch (error) {
        console.log(error);
    }

    //Ahora actualizo la base de datos con el nuevo pedido. 

    try {
        arrayDeCodigos.forEach(async codigo => {
            const insertQuery = `SELECT codigoUnidadBase, cantidadUnidad FROM productos WHERE codigoProducto = ?`;
            const result = await connection.query(insertQuery, codigo);
    
            const {codigoUnidadBase, cantidadUnidad} = result[0];
            
            const insertQueryUnidad = `UPDATE productos SET cantidad = cantidad - ${cantidadUnidad} WHERE codigoProducto = ?`;
            const result_unidad = await connection.query(insertQueryUnidad, codigoUnidadBase);
    
            const insertQueryProducto = `UPDATE productos SET cantidad = cantidad - 1 WHERE codigoProducto = ?`;
            const result_producto = await connection.query(insertQueryProducto, codigo);
            
            res.status(200).json({ message: 'Consulta exitosa' });
        })
    } catch (error) {
        console.log(error);
    }
    
})

app.post("/cargar-nuevo-producto", async (req, res)=>{
    
    const formData = req.body;

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

app.post("/informacion-producto", async (req, res) =>{
    const {codigo} = req.body;

    try {
        const insertQuery = `SELECT nombre, descripcion FROM productos WHERE codigoProducto = ?`;

        const connection = await database.getConnection();

        const result = await connection.query(insertQuery, [codigo]);

        if(result.length === 0){
            return res.status(400).json({ message: "El código de unidad base no existe." });
        }

        const productData = {
            nombre : result[0].nombre,
            descripcion: result[0].descripcion 
        }
        console.log(productData);
        res.json(productData);
    } 
    catch (error) {
        console.log(error);
    }
})

app.post("/eliminar-producto", async (req, res)=>{
    const {codigoAEliminar} = req.body;

    try {
        const insertQuery = `DELETE FROM productos WHERE codigoProducto = ?`;
        
        const connection = await database.getConnection();

        const result = connection.query(insertQuery, [codigoAEliminar]);

        res.status(200).json({ message: "Producto Eliminado correctamente." });
    } 
    catch (error) {
        console.log(error);
    }
})
