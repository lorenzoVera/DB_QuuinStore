CREATE TABLE hechos_ventas (
  id_venta int PRIMARY KEY,
  id_pedido_venta int,
  id_producto int,
  id_detalle_producto int,
  id_tiempo int,
  id_cliente int,
  id_canal int,
  id_metodo int,
  id_promo int,
  cantidad int,
  total decimal(10,2),
  fecha_venta date,
  hora_venta int
);

CREATE TABLE tiempo (
  id_tiempo int PRIMARY KEY,
  fecha date,
  mes int,
  año int,
  dia int
);

CREATE TABLE clientes (
  id_cliente int PRIMARY KEY,
  nombre varchar,
  apellido varchar,
  comuna varchar,
  region varchar,
  telefono varchar
);

CREATE TABLE productos (
  id_producto int PRIMARY KEY,
  nombre varchar,
  categoría varchar,
  precio_unitario decimal(10,2)
);

CREATE TABLE canal_ventas (
  id_canal int PRIMARY KEY,
  nombre_canal varchar
);

CREATE TABLE metodo_pagos (
  id_metodo int PRIMARY KEY,
  nombre_metodo varchar
);

CREATE TABLE promociones (
  id_promo int PRIMARY KEY,
  nombre_promo varchar,
  tipo varchar
);

CREATE TABLE detalle_productos (
  id_detalle_producto int PRIMARY KEY,
  talla varchar,
  color varchar,
  genero varchar,
  temporada varchar,
  material varchar,
  marca varchar,
  estilo varchar
);

CREATE TABLE hechos_compra (
  id_compra int PRIMARY KEY,
  id_pedido_compra int,
  id_tiempo int,
  id_proveedor int,
  id_producto int,
  total decimal(10,2),
  subtotal decimal(10,2),
  fecha_compra date,
  hora_compra int,
  fecha_llegada date,
  hora_llegada int
);

CREATE TABLE proveedores (
  id_proveedor int PRIMARY KEY,
  nombre varchar,
  telefono varchar,
  correo varchar
);

CREATE INDEX ON hechos_ventas (id_tiempo);
CREATE INDEX ON hechos_ventas (id_canal);
CREATE INDEX ON hechos_ventas (id_cliente);
CREATE INDEX ON hechos_ventas (id_producto);
CREATE INDEX ON hechos_ventas (id_detalle_producto);
CREATE INDEX ON hechos_ventas (id_pedido_venta);
CREATE INDEX ON hechos_ventas (id_promo);

CREATE INDEX ON hechos_compra (id_tiempo);
CREATE INDEX ON hechos_compra (id_proveedor);
CREATE INDEX ON hechos_compra (id_producto);

ALTER TABLE hechos_ventas ADD FOREIGN KEY (id_tiempo) REFERENCES tiempo (id_tiempo);
ALTER TABLE hechos_ventas ADD FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente);
ALTER TABLE hechos_ventas ADD FOREIGN KEY (id_producto) REFERENCES productos (id_producto);
ALTER TABLE hechos_ventas ADD FOREIGN KEY (id_canal) REFERENCES canal_ventas (id_canal);
ALTER TABLE hechos_ventas ADD FOREIGN KEY (id_metodo) REFERENCES metodo_pagos (id_metodo);
ALTER TABLE hechos_ventas ADD FOREIGN KEY (id_detalle_producto) REFERENCES detalle_productos (id_detalle_producto);
ALTER TABLE hechos_ventas ADD FOREIGN KEY (id_promo) REFERENCES promociones (id_promo);

ALTER TABLE hechos_compra ADD FOREIGN KEY (id_tiempo) REFERENCES tiempo (id_tiempo);
ALTER TABLE hechos_compra ADD FOREIGN KEY (id_proveedor) REFERENCES proveedores (id_proveedor);
ALTER TABLE hechos_compra ADD FOREIGN KEY (id_producto) REFERENCES productos (id_producto);
