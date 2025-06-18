CREATE TABLE "Pedidos_Venta" (
  "ID_pedido_venta" int PRIMARY KEY,
  "ID_cliente" int,
  "Fecha_pedido" date,
  "Hora_pedido" time,
  "Estado_pedido" varchar,
  "ID_canal" int,
  "ID_metodo_pago" int,
  "Subtotal" decimal(10,2),
  "Total" decimal(10,2)
);

CREATE TABLE "Detalle_Pedidos_Venta" (
  "ID_detalle_pedido_venta" int PRIMARY KEY,
  "ID_pedido_venta" int,
  "ID_detalle_producto" int,
  "Cantidad" int,
  "Precio_unitario_venta" decimal(10,2),
  "Subtotal_linea" decimal(10,2),
  "ID_promo" int
);

CREATE TABLE "Clientes" (
  "ID_cliente" int PRIMARY KEY,
  "Nombre" varchar,
  "Apellido" varchar,
  "Direccion" varchar,
  "Comuna" varchar,
  "Region" varchar,
  "Telefono" varchar
);

CREATE TABLE "Productos" (
  "ID_producto" int PRIMARY KEY,
  "Nombre_producto" varchar,
  "Categoria" varchar,
  "Descripcion" text,
  "Activo" boolean
);

CREATE TABLE "Detalle_Productos" (
  "ID_detalle_producto" int PRIMARY KEY,
  "ID_producto" int,
  "Talla" varchar,
  "Color" varchar,
  "Genero" varchar,
  "Temporada" varchar,
  "Material" varchar,
  "Marca" varchar,
  "Estilo" varchar,
  "Precio_unitario_actual" decimal(10,2),
  "Stock_disponible" int
);

CREATE TABLE "Canales_Venta" (
  "ID_canal" int PRIMARY KEY,
  "Nombre_canal" varchar,
  "Descripcion" varchar
);

CREATE TABLE "Metodos_Pago" (
  "ID_metodo_pago" int PRIMARY KEY,
  "Nombre_metodo" varchar,
  "Tipo_metodo" varchar
);

CREATE TABLE "Promociones" (
  "ID_promo" int PRIMARY KEY,
  "Nombre_promo" varchar,
  "Tipo_promo" varchar,
  "Valor_descuento" decimal(10,2),
  "Fecha_inicio" date,
  "Fecha_fin" date,
  "Activa" boolean,
  "ID_detalle_productos" int
);

CREATE TABLE "Pedidos_Compra_Proveedor" (
  "ID_pedido_proveedor" int PRIMARY KEY,
  "ID_proveedor" int,
  "Fecha_pedido" date,
  "Hora_pedido" time,
  "Total_compra" decimal(10,2)
);

CREATE TABLE "Detalle_Pedidos_Compra" (
  "ID_detalle_pedido_compra" int PRIMARY KEY,
  "ID_pedido_proveedor" int,
  "ID_producto" int,
  "Cantidad" int,
  "Precio_unitario_compra" decimal(10,2),
  "Subtotal_linea" decimal(10,2)
);

CREATE TABLE "Proveedores" (
  "ID_proveedor" int PRIMARY KEY,
  "Nombre_proveedor" varchar,
  "Contacto" varchar,
  "Telefono" varchar,
  "Correo_electronico" varchar,
  "Direccion" varchar,
  "Activo" boolean
);

ALTER TABLE "Pedidos_Venta" ADD FOREIGN KEY ("ID_cliente") REFERENCES "Clientes" ("ID_cliente");

ALTER TABLE "Pedidos_Venta" ADD FOREIGN KEY ("ID_canal") REFERENCES "Canales_Venta" ("ID_canal");

ALTER TABLE "Pedidos_Venta" ADD FOREIGN KEY ("ID_metodo_pago") REFERENCES "Metodos_Pago" ("ID_metodo_pago");

ALTER TABLE "Detalle_Pedidos_Venta" ADD FOREIGN KEY ("ID_pedido_venta") REFERENCES "Pedidos_Venta" ("ID_pedido_venta");

ALTER TABLE "Detalle_Pedidos_Venta" ADD FOREIGN KEY ("ID_detalle_producto") REFERENCES "Detalle_Productos" ("ID_detalle_producto");

ALTER TABLE "Detalle_Pedidos_Venta" ADD FOREIGN KEY ("ID_promo") REFERENCES "Promociones" ("ID_promo");

ALTER TABLE "Detalle_Productos" ADD FOREIGN KEY ("ID_producto") REFERENCES "Productos" ("ID_producto");

ALTER TABLE "Promociones" ADD FOREIGN KEY ("ID_detalle_productos") REFERENCES "Detalle_Productos" ("ID_detalle_producto");

ALTER TABLE "Pedidos_Compra_Proveedor" ADD FOREIGN KEY ("ID_proveedor") REFERENCES "Proveedores" ("ID_proveedor");

ALTER TABLE "Detalle_Pedidos_Compra" ADD FOREIGN KEY ("ID_pedido_proveedor") REFERENCES "Pedidos_Compra_Proveedor" ("ID_pedido_proveedor");

ALTER TABLE "Detalle_Pedidos_Compra" ADD FOREIGN KEY ("ID_producto") REFERENCES "Productos" ("ID_producto");
