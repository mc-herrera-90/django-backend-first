## Configuración del Proyecto

1. Crear entorno virtual:

```bash
# Linux / macOS
python3 -m venv .venv

# Windows
python -m venv .venv
```

2. Activar entorno virtual:

```
# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

3. Instalar dependencias:

```
pip install -r requirements.txt
```

Para `mysqlclient`, las dependencias dependen del sistema operativo.

> [!NOTE]
> En macOS, instalar previamente `mysql-client` y `pkg-config`:
>
> ```bash
> brew install mysql-client pkg-config
> ```
>
> En Ubuntu/Debian:
>
> ```bash
> sudo apt install build-essential pkg-config python3-dev default-libmysqlclient-dev
> ```

4. Instalar los hooks de pre-commit:

```
pre-commit install
```

5. Ejecutar migraciones:

```
python manage.py migrate
```

6. Lanzar servidor:

```
python manage.py runserver
```

Servidor disponible en `http://127.0.0.1:8000/`.

7. Lanzar documentación:

```
mkdocs serve -a 127.0.0.1:8001
```

Documentación disponible en `http://127.0.0.1:8001/`.

## Comandos útiles

```
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Aplicar migraciones a otra base de datos definida
python manage.py migrate --database=sqlite

# Crear superusuario
python manage.py createsuperuser

# Lanzar servidor
python manage.py runserver

# Formatear un template específico con djLint
djlint core/templates/core/dashboard.html --reformat 

# Formatear todos los templates de una aplicación
djlint core/templates --reformat

# Formatear los templates de todas las aplicaciones
djlint . --reformat # Usar con precaución

# Verificar el formato de un template
djlint core/templates/core/dashboard.html --check

# Verificar el formato de todos los templates
djlint . --check

# Automatiza la actualización de dependencias, la recolección de estáticos, la aplicación de migraciones y la carga de datos
chmod +x build.sh
./build.sh
```