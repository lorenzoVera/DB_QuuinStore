CREATE TABLE "Hechos_Ventas" (
  "ID_venta" int PRIMARY KEY,
  "ID_pedido_venta" int,
  "ID_producto" int,
  "ID_detalle_producto" int,
  "ID_tiempo" int,
  "ID_cliente" int,
  "ID_canal" int,
  "ID_metodo" int,
  "ID_promo" int,
  "Cantidad" int,
  "Subtotal" decimal(10,2),
  "Fecha_venta" date,
  "Hora_venta" int
);

CREATE TABLE "Tiempo" (
  "ID_tiempo" int PRIMARY KEY,
  "Dia" int,
  "Mes" int,
  "Año" int,
  "Temporada" varchar
);

CREATE TABLE "Clientes" (
  "ID_cliente" int PRIMARY KEY,
  "Nombre" varchar,
  "Apellido" varchar,
  "Comuna" varchar,
  "Region" varchar,
  "Telefono" varchar
);

CREATE TABLE "Productos" (
  "ID_producto" int PRIMARY KEY,
  "Nombre" varchar,
  "Categoría" varchar
);

CREATE TABLE "Canal_Ventas" (
  "ID_canal" int PRIMARY KEY,
  "Nombre_canal" varchar
);

CREATE TABLE "Metodo_pagos" (
  "ID_metodo" int PRIMARY KEY,
  "Nombre_metodo" varchar
);

CREATE TABLE "Promociones" (
  "ID_promo" int PRIMARY KEY,
  "Nombre_promo" varchar,
  "Tipo" varchar
);

CREATE TABLE "Detalle_Productos" (
  "ID_detalle_producto" int PRIMARY KEY,
  "Talla" varchar,
  "Color" varchar,
  "Genero" varchar,
  "Temporada" varchar,
  "Material" varchar,
  "Marca" varchar,
  "Estilo" varchar,
  "Precio_unitario" decimal(10,2)
);

CREATE TABLE "Hechos_Compra" (
  "ID_compra" int PRIMARY KEY,
  "ID_pedido_proveedor" int,
  "ID_tiempo" int,
  "ID_proveedor" int,
  "ID_producto" int,
  "Cantidad" int,
  "Precio_unitario" decimal(10,2),
  "Subtotal" decimal(10,2),
  "Fecha_compra" date,
  "Hora_compra" int,
  "Fecha_llegada" date,
  "Hora_llegada" int
);

CREATE TABLE "Proveedores" (
  "ID_proveedor" int PRIMARY KEY,
  "Nombre" varchar,
  "Telefono" varchar,
  "Correo" varchar
);

CREATE INDEX ON "Hechos_Ventas" ("ID_tiempo");

CREATE INDEX ON "Hechos_Ventas" ("ID_canal");

CREATE INDEX ON "Hechos_Ventas" ("ID_cliente");

CREATE INDEX ON "Hechos_Ventas" ("ID_producto");

CREATE INDEX ON "Hechos_Ventas" ("ID_detalle_producto");

CREATE INDEX ON "Hechos_Ventas" ("ID_pedido_venta");

CREATE INDEX ON "Hechos_Ventas" ("ID_promo");

CREATE INDEX ON "Hechos_Compra" ("ID_tiempo");

CREATE INDEX ON "Hechos_Compra" ("ID_proveedor");

CREATE INDEX ON "Hechos_Compra" ("ID_producto");

ALTER TABLE "Hechos_Ventas" ADD FOREIGN KEY ("ID_tiempo") REFERENCES "Tiempo" ("ID_tiempo");

ALTER TABLE "Hechos_Ventas" ADD FOREIGN KEY ("ID_cliente") REFERENCES "Clientes" ("ID_cliente");

ALTER TABLE "Hechos_Ventas" ADD FOREIGN KEY ("ID_producto") REFERENCES "Productos" ("ID_producto");

ALTER TABLE "Hechos_Ventas" ADD FOREIGN KEY ("ID_canal") REFERENCES "Canal_Ventas" ("ID_canal");

ALTER TABLE "Hechos_Ventas" ADD FOREIGN KEY ("ID_metodo") REFERENCES "Metodo_pagos" ("ID_metodo");

ALTER TABLE "Hechos_Ventas" ADD FOREIGN KEY ("ID_detalle_producto") REFERENCES "Detalle_Productos" ("ID_detalle_producto");

ALTER TABLE "Hechos_Ventas" ADD FOREIGN KEY ("ID_promo") REFERENCES "Promociones" ("ID_promo");

ALTER TABLE "Hechos_Compra" ADD FOREIGN KEY ("ID_tiempo") REFERENCES "Tiempo" ("ID_tiempo");

ALTER TABLE "Hechos_Compra" ADD FOREIGN KEY ("ID_proveedor") REFERENCES "Proveedores" ("ID_proveedor");

ALTER TABLE "Hechos_Compra" ADD FOREIGN KEY ("ID_producto") REFERENCES "Productos" ("ID_producto");
