# 🍳 Generador de Recetas con Inteligencia Artificial

## 📖 Descripción del proyecto

Generador de Recetas con IA es una aplicación web diseñada para ayudar a los usuarios a aprovechar los ingredientes que tienen disponibles en casa.

El sistema permite administrar un inventario personal de ingredientes y utilizar inteligencia artificial para generar recetas personalizadas a partir de los alimentos registrados.

Además, permite consultar recetas generadas anteriormente, calificarlas y eliminarlas del historial.

## 🚀 Funcionalidades del software

### 👤 Gestión de usuarios
- Registro de nuevos usuarios.
- Inicio de sesión mediante autenticación.
- Gestión individual de la información de cada usuario.

### 🥕 Inventario de ingredientes
- Registrar ingredientes disponibles.
- Consultar los ingredientes almacenados.
- Actualizar la información de los ingredientes.
- Eliminar ingredientes del inventario.

### 🤖 Generación de recetas con IA
- Analizar los ingredientes disponibles en el inventario.
- Generar recetas personalizadas mediante inteligencia artificial.
- Obtener el nombre del plato.
- Mostrar los ingredientes y sus cantidades.
- Presentar instrucciones de preparación paso a paso.
- Indicar el tiempo estimado de preparación.
- Mostrar el nivel de dificultad de la receta.

### 📚 Historial de recetas
- Almacenar las recetas generadas.
- Consultar recetas anteriores.
- Eliminar recetas del historial.

### ⭐ Calificación de recetas
- Calificar recetas mediante una escala de 1 a 5 estrellas.
- Guardar las calificaciones asociadas a las recetas.

## 🏗️ Organización del software

La aplicación se organiza en diferentes componentes para separar las responsabilidades del sistema.

### Frontend
Es la interfaz visual mediante la cual los usuarios interactúan con el software, administran sus ingredientes y consultan las recetas.

### Backend
Gestiona la lógica del sistema, procesa las solicitudes de los usuarios, administra la autenticación y conecta los diferentes servicios.

### Base de datos
Almacena la información necesaria para el funcionamiento de la aplicación.

Su estructura principal contempla:

- **Usuarios:** información de las cuentas registradas.
- **Ingredientes:** inventario personal de alimentos.
- **Recetas:** información de las recetas generadas.
- **Calificaciones:** valoraciones realizadas por los usuarios.

### Servicio de inteligencia artificial
Se encarga de recibir los ingredientes disponibles, procesar la solicitud mediante un modelo de lenguaje y devolver una receta estructurada.

## 📂 Estructura del proyecto

```text
proyecto-recetas/
│
├── app/
│   ├── main.py
│   ├── models/
│   ├── routers/
│   ├── services/
│   │   └── llm_service.py
│   └── schemas/
│
├── tests/
│   └── test_*.py
│
├── static/
│   └── favicon.ico
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## 🔄 Funcionamiento general

1. El usuario se registra o inicia sesión.
2. Ingresa los ingredientes que tiene disponibles.
3. El sistema almacena y organiza su inventario.
4. El usuario solicita generar una receta.
5. La inteligencia artificial procesa los ingredientes registrados.
6. El sistema presenta una receta con cantidades, instrucciones, tiempo y dificultad.
7. La receta generada se almacena en el historial.
8. El usuario puede consultar, calificar o eliminar sus recetas.

## 🎯 Objetivo del software

Facilitar la preparación de comidas mediante el uso de inteligencia artificial, aprovechando los ingredientes disponibles en el hogar y ofreciendo una herramienta digital para organizar alimentos y descubrir nuevas recetas.

## Despliegue en Railway

1. En Railway, crea un proyecto con un servicio MySQL con volumen persistente y un servicio vacío para SmartRecipe AI. Usa el nombre `MySQL` para el servicio de base de datos si vas a copiar estas referencias.
2. En el servicio de la app, define las variables de conexión usando la red privada de Railway.

   | Variable de la app | Valor en Railway |
   | --- | --- |
   | `DB_HOST` | `${{MySQL.RAILWAY_PRIVATE_DOMAIN}}` |
   | `DB_PORT` | `3306` |
   | `DB_NAME` | `${{MySQL.MYSQLDATABASE}}` |
   | `DB_USER` | `${{MySQL.MYSQLUSER}}` |
   | `DB_PASSWORD` | `${{MySQL.MYSQLPASSWORD}}` |
   | `JWT_SECRET_KEY` | Secreto aleatorio exclusivo del despliegue |
   | `OPENROUTER_API_KEY` | Clave de OpenRouter guardada como secreto |

3. Crea un token de proyecto en Railway para el entorno de producción. En GitHub, guárdalo como secreto de Actions `RAILWAY_TOKEN` y añade la variable de Actions `RAILWAY_SERVICE` con el nombre del servicio de la app.
4. Ejecuta **Desplegar en Railway** desde GitHub Actions. El workflow también se ejecuta al actualizar `main`. Usa el comando de inicio del Dockerfile en Railway para que el contenedor cree las tablas que falten antes de iniciar FastAPI.
5. Genera un dominio público para el servicio de la app en Railway. Abre ese dominio y verifica que puedes registrarte, iniciar sesión, añadir un ingrediente y generar una receta.
