
-- ==========================================
-- SMARTRECIPE AI - MYSQL
-- ==========================================

CREATE DATABASE IF NOT EXISTS smartrecipe_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE smartrecipe_db;


-- ==========================================
-- USUARIOS
-- ==========================================

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;


-- ==========================================
-- INGREDIENTES
-- ==========================================

CREATE TABLE IF NOT EXISTS ingredientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    cantidad DECIMAL(10,2) NOT NULL,
    unidad VARCHAR(30) NOT NULL,

    CONSTRAINT fk_ingredientes_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE CASCADE
) ENGINE=InnoDB;


-- ==========================================
-- RECETAS
-- ==========================================

CREATE TABLE IF NOT EXISTS recetas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    ingredientes_json JSON NOT NULL,
    pasos_json JSON NOT NULL,
    tiempo_estimado INT NOT NULL,
    dificultad VARCHAR(20) NOT NULL,
    favorita BOOLEAN NOT NULL DEFAULT FALSE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_recetas_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE CASCADE
) ENGINE=InnoDB;


-- ==========================================
-- CALIFICACIONES
-- ==========================================

CREATE TABLE IF NOT EXISTS calificaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    receta_id INT NOT NULL,
    puntuacion INT NOT NULL,
    fecha_calificacion DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_calificaciones_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_calificaciones_receta
        FOREIGN KEY (receta_id)
        REFERENCES recetas(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_usuario_receta
        UNIQUE (usuario_id, receta_id),

    CONSTRAINT chk_calificacion_valida
        CHECK (puntuacion BETWEEN 1 AND 5)
) ENGINE=InnoDB;
