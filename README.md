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
