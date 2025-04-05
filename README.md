
# Focus - Plataforma Educativa Interactiva

Focus es una plataforma educativa diseñada para proporcionar juegos interactivos y atractivos, especialmente orientada a niños con déficit de atención. Nuestro objetivo es crear un ambiente de aprendizaje divertido y estimulante que ayude a desarrollar habilidades cognitivas y de resolución de problemas.

## Características Principales

- **Interfaz Intuitiva**: Diseño atractivo y fácil de navegar
- **Juegos por Edad**: Contenido adaptado para grupos de 7-8, 9-10 y 11-12 años
- **Enfoque en Atención**: Juegos diseñados para mejorar la concentración
- **Sistema de Roles**: Gestión de usuarios estudiantes y administradores
- **Panel Administrativo**: Control total sobre usuarios y juegos

## Requisitos

- Python 3.8+
- pip

## Instalación

1. Clonar el repositorio
2. Crear un entorno virtual:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Crear archivo .env en la raíz del proyecto:
   ```
   SECRET_KEY=tu_clave_secreta
   FLASK_ENV=development
   ```

## Ejecución

```bash
python run.py
```

## Estructura del Proyecto

```
Focus/
├── app/
│   ├── models/       # Modelos de la base de datos
│   ├── routes/       # Rutas de la aplicación
│   ├── services/     # Lógica de negocio
│   └── utils/        # Utilidades y helpers
├── config/          # Configuraciones
├── static/          # Archivos estáticos
├── templates/       # Plantillas HTML
├── tests/           # Tests unitarios
├── .env             # Variables de entorno
├── requirements.txt # Dependencias
└── run.py          # Punto de entrada
```

## Tecnologías

- Backend: Python, Flask, SQLAlchemy
- Frontend: HTML5, CSS3, JavaScript
- Base de Datos: SQLite (desarrollo), PostgreSQL (producción)
- Autenticación: Flask-Login

## Diseño Responsivo

La plataforma está optimizada para funcionar en diferentes dispositivos y tamaños de pantalla.