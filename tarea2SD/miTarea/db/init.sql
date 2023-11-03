CREATE TABLE formulario (
    id TEXT PRIMARY KEY,
    timestamp TIMESTAMP, 
    nombre TEXT, 
    email TEXT, 
    password TEXT, 
    tipo TEXT
);

CREATE TABLE ingredientes (
    id TEXT PRIMARY KEY, 
    timestamp TIMESTAMP,
    ingrediente TEXT, 
    estado TEXT,
    formulario_id TEXT REFERENCES formulario(id)
);

CREATE TABLE ventas (
    id_venta TEXT PRIMARY KEY,
    timestamp TIMESTAMP,
    cantidad INT, 
    valor FLOAT,
    formulario_id TEXT REFERENCES formulario(id)
);

