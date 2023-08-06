# MS Core

Ms Core


# Instalar / Crear un proyecto

```bash
mkdir nombre_proyecto
cd nombre_proyecto
pip install --upgrade bws
python3 -m bws.cmd.create_project --name_app=main

```


# Crear un aplicación

```bash
cd nombre_proyecto;
python3 -m bws.cmd.create_project --name=app/nombre_app

```

# Activar app


Agregar dentro de app.config.INSTALLED_APPS el path del modulo
```python
INSTALLED_APPS = [
    "...",
    "app.nombre_app"
]
```