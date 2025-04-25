# 📊 Quuin_Store - OLAP para Tienda de Ropa Online

Este proyecto contiene la modelación e implementación de una base de datos OLAP para **Quuin_Store**, una tienda de ropa femenina que opera de forma online a través de distintos canales digitales. La base de datos está diseñada para facilitar consultas analíticas que apoyen la toma de decisiones en áreas como ventas, promociones, logística y comportamiento de clientes.

---

## 🛍️ Descripción del Negocio

**Quuin_Store** es una tienda online dedicada exclusivamente a la venta de ropa para mujeres. Utiliza **canales como Facebook, Instagram y WhatsApp** para realizar ventas y acepta métodos de pago como **transferencia, efectivo, tarjetas de débito o crédito**.

El catálogo de productos incluye:
- Beatles, faldas, abrigos, tops, vestidos, chaquetas, pantalones, shorts, cinturones, carteras, chalecos, enteritos, panties, entre otros.

Cada prenda puede tener promociones o descuentos asociados, y la tienda se abastece mediante pedidos a **proveedores externos**.

---

## 🧱 Estructura del Proyecto

- `create_schema.sql`: Script para crear todas las tablas necesarias con sus relaciones e índices.
- `insert_data.sql`: Datos de prueba insertados para simular la operación real de la tienda.
- `sample_queries.sql`: Consultas OLAP útiles para análisis estratégicos.
- `diagrams/`: Diagramas estrellas para ilustrar el modelo de datos.
- `README.md`: Este archivo 

---

## 🧩 Tablas Principales

- `Hechos_Ventas`: Ventas realizadas por producto y cliente.
- `Hechos_Compra`: Compras a proveedores.
- `Clientes`: Información de clientas.
- `Productos`: Catálogo de productos.
- `Detalle_Productos`: Atributos físicos (talla, color, marca, etc).
- `Tiempo`: Dimensión temporal para análisis por fechas y temporadas.
- `Promociones`, `Canal_Ventas`, `Metodo_pagos`, `Proveedores`.

---

## 📈 Consultas OLAP de Ejemplo

- ✅ Productos más vendidos en un mes  
- ✅ Promociones más utilizadas  
- ✅ Canal con mayor volumen de ventas  
- ✅ Colores más vendidos en Otoño  
- ✅ Talla más común por género (Mujer/Niña)  
- ✅ Regiones con mayor cantidad de ventas  
- ✅ Proveedor más eficiente por tiempo de entrega  
- ✅ Categorías de ropa que se compran juntas  

---

## 🛠️ Tecnologías

- **PostgreSQL** 15+
- SQL
- Dbeaver

---

## 🚀 Instrucciones

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tuusuario/QuuinStore-OLAP.git
   cd QuuinStore-OLAP
