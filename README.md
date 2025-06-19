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

- `creadorDb/`: Scripts para crear e insertar datos en la base de datos.
- `graficosDb/`: Scripts para generar gráficos a partir de los datos.
- `graficosImagenes/`: Carpeta donde se guardan las imágenes generadas.
- `diagrams/`: Diagramas estrella para ilustrar el modelo de datos.
- `CRUD/`: **Programa para la gestión de datos de ventas (Crear, Leer, Actualizar, Eliminar).**
- `README.md`: Este archivo.

---

## 🛠️ Instrucciones de Uso

### 1. Preparación de la Base de Datos e Inserción de Datos

1. Asegúrate de que tu sistema de gestión de bases de datos esté en funcionamiento.
2. Crea una nueva base de datos.
3. Navega al directorio `creadorDb`.
4. Inserta las tablas de una de estas dos maneras:
   - Ejecuta el script `creador.py`.  
     > **Importante:** Modifica la variable `DATABASE_URL` en `creador.py` con la cadena de conexión de tu base de datos.  
     > Ejemplo:  
     > `DATABASE_URL = "postgres://usuario:contraseña@host:puerto/nombre_db"`
   - O ejecuta el archivo SQL que contiene la definición de las tablas.
5. Inserta los datos ejecutando `main.py` en el mismo directorio.
6. (Opcional) Visualiza los datos ejecutando `dataview.py`.  
   > **Importante:** También debes modificar la variable `DATABASE_URL` en este archivo.

### 2. Creación de Gráficos

1. Navega al directorio `graficosDb`.
2. Ejecuta el script `main.py`.
   - El script te pedirá los datos necesarios.
   - Las imágenes se guardarán en la carpeta `graficosImagenes`.

---
Gestión de Datos (CRUD de Ventas)

1. Navega al directorio `CRUD/`.
2. **Asegúrate de configurar los detalles de conexión a la base de datos** en `db_config` del archivo `main_app.py`.
3. Ejecuta el script principal de la interfaz de usuario: `main_app.py`.
4. Este programa te permitirá **crear nuevas ventas, visualizar las existentes, modificarlas y eliminarlas** directamente en la base de datos.

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
- Python (para scripts de carga y gráficos)
-`customtkinter` (para la interfaz gráfica del programa CRUD)

---

## 🚀 Clonar el Repositorio

```bash
git clone https://github.com/tuusuario/QuuinStore-OLAP.git
cd QuuinStore-OLAP
```
