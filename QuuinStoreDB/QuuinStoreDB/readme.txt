1. Preparación de la Base de Datos e Inserción de Datos

Esta sección detalla los pasos necesarios para configurar la base de datos e insertar los datos.

1.1. Crear base de datos:

Asegúrate de que tu sistema de gestión de bases de datos esté en funcionamiento.

Crea una nueva base de datos.

1.2. Navega al directorio creadorDb.

1.3. Insertar tablas:

Puedes insertar las tablas de dos maneras:

Ejecuta el script creador.py.

Importante: Modifica la variable #DATABASE_URL en creador.py con la cadena de conexión de tu base de datos. Por ejemplo:

# DATABASE_URL = "postgres://usuario:contraseña@host:puerto/nombre_db"
DATABASE_URL = "tu_cadena_de_conexión"  # Reemplaza con tus datos

Ejecuta el archivo SQL que contiene la definición de las tablas.

1.4. Insertar datos:

Ejecuta main.py para insertar los datos en las tablas.

1.5. (Opcional) Visualizar datos:

Ejecuta dataview.py para ver los datos en la base de datos.

Importante: Si ejecutas  dataview.py, también debes modificar la variable #DATABASE_URL en este archivo:

# DATABASE_URL = "postgres://usuario:contraseña@host:puerto/nombre_db"
DATABASE_URL = "tu_cadena_de_conexión"  # Reemplaza con tus datos

2. Creación de Gráficos

Esta sección explica cómo generar los gráficos.

2.1. Navega al directorio graficosDb.

2.2. Ejecutar main.py:

Ejecuta el script main.py.

El script te pedirá los datos necesarios.

Las imágenes se guardarán en la carpeta graficosImagenes.