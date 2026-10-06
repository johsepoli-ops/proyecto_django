# Sistema de Gestión de Mantenimiento

Proyecto desarrollado en Django para la gestión de mantenimiento, equipos, empresas, órdenes de trabajo y evidencias.

## Tecnologías utilizadas

- Python 3.12
- Django 4.2
- MariaDB / MySQL
- Pillow
- OpenPyXL
- HTML
- JavaScript
- SweetAlert2

## Funcionalidades principales

El sistema incluye:

- Autenticación de usuarios.
- Cierre de sesión.
- Recuperación de contraseña mediante código numérico.
- Roles y permisos diferenciados.
- Scoping de información por usuario.
- Gestión de órdenes de trabajo.
- Gestión de equipos.
- Gestión de empresas.
- Gestión de evidencias de mantenimiento.
- Carga y validación de imágenes.
- Borrado lógico.
- Confirmaciones con SweetAlert2.
- Paginación configurable de 5, 15 y 30 registros.
- Persistencia de la paginación mediante sesión.
- Exportación de órdenes de trabajo a Excel.
- Generación reproducible de más de 1000 registros de prueba.

---

# Requisitos previos

Antes de ejecutar el proyecto se debe tener instalado:

- Python 3.12 o compatible.
- MariaDB o MySQL.
- Git.

---

# Clonar el repositorio

```bash
git clone https://github.com/johsepoli-ops/proyecto_django.git