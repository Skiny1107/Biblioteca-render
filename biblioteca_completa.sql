-- ===============================================================
-- BASE DE DATOS BIBLIOTECA v2.1.0 - FUNCIONAL COMPLETA
-- ===============================================================
-- Autogenerado: 31/05/2026
-- Compatible con: MySQL 8.0+
-- Charset: UTF-8 MB4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

-- ===============================================================
-- CREAR BASE DE DATOS
-- ===============================================================

DROP DATABASE IF EXISTS `biblioteca_db`;
CREATE DATABASE `biblioteca_db`
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE `biblioteca_db`;

-- ===============================================================
-- TABLA: USUARIOS
-- ===============================================================

DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE `usuarios` (
  `id` INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `usuario` VARCHAR(50) UNIQUE NOT NULL,
  `clave` VARCHAR(255) NOT NULL,
  `nombre` VARCHAR(100) NOT NULL,
  `correo` VARCHAR(100) NOT NULL,
  `rol` VARCHAR(20) NOT NULL DEFAULT 'usuario',
  `estado` INT(1) NOT NULL DEFAULT 1,
  `fecha_creacion` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insertar usuarios de prueba
INSERT INTO `usuarios` (`id`, `usuario`, `clave`, `nombre`, `correo`, `rol`, `estado`) VALUES
(1, 'admin', '$2b$12$ZK.yKq.pCKPGQeVqEbVMmuWTjVzlAJJBpVyIJDLJLJYZtNV5OgDzy', 'Administrador', 'admin@biblioteca.com', 'administrador', 1),
(2, 'bibliotecario', '$2b$12$ZK.yKq.pCKPGQeVqEbVMmuWTjVzlAJJBpVyIJDLJLJYZtNV5OgDzy', 'Bibliotecario Principal', 'bibliotecario@biblioteca.com', 'bibliotecario', 1),
(3, 'usuario1', '$2b$12$ZK.yKq.pCKPGQeVqEbVMmuWTjVzlAJJBpVyIJDLJLJYZtNV5OgDzy', 'Usuario Prueba', 'usuario@biblioteca.com', 'usuario', 1),
(4, 'usuario_inactivo', '$2b$12$ZK.yKq.pCKPGQeVqEbVMmuWTjVzlAJJBpVyIJDLJLJYZtNV5OgDzy', 'Usuario Desactivado', 'inactivo@biblioteca.com', 'usuario', 0);

-- ===============================================================
-- TABLA: AUTOR
-- ===============================================================

DROP TABLE IF EXISTS `autor`;
CREATE TABLE `autor` (
  `id` INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `autor` VARCHAR(150) NOT NULL,
  `imagen` VARCHAR(100) DEFAULT 'default.png',
  `estado` INT(1) NOT NULL DEFAULT 1,
  `fecha_creacion` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `autor` (`id`, `autor`, `imagen`, `estado`) VALUES
(1, 'Jorge Luis Borges', 'borges.png', 1),
(2, 'Pablo Neruda', 'neruda.png', 1),
(3, 'Gabriel García Márquez', 'gabo.png', 1),
(4, 'Julio Cortázar', 'cortazar.png', 1),
(5, 'Isabel Allende', 'allende.png', 1),
(6, 'Juan Rulfo', 'rulfo.png', 1);

-- ===============================================================
-- TABLA: EDITORIAL
-- ===============================================================

DROP TABLE IF EXISTS `editorial`;
CREATE TABLE `editorial` (
  `id` INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `nombre` VARCHAR(150) NOT NULL,
  `pais` VARCHAR(50) DEFAULT NULL,
  `estado` INT(1) NOT NULL DEFAULT 1,
  `fecha_creacion` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `editorial` (`id`, `nombre`, `pais`, `estado`) VALUES
(1, 'Emecé Editores', 'Argentina', 1),
(2, 'Editorial Seix Barral', 'España', 1),
(3, 'Random House', 'USA', 1),
(4, 'Siglo XXI Editores', 'México', 1),
(5, 'Editorial Planeta', 'España', 1),
(6, 'Fondo de Cultura Económica', 'México', 1);

-- ===============================================================
-- TABLA: MATERIA
-- ===============================================================

DROP TABLE IF EXISTS `materia`;
CREATE TABLE `materia` (
  `id` INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `nombre` VARCHAR(100) NOT NULL,
  `descripcion` TEXT DEFAULT NULL,
  `estado` INT(1) NOT NULL DEFAULT 1,
  `fecha_creacion` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `materia` (`id`, `nombre`, `descripcion`, `estado`) VALUES
(1, 'Ficción Clásica', 'Obras maestras de la literatura clásica', 1),
(2, 'Poesía', 'Colección de poesías latinoamericanas', 1),
(3, 'Novela Latinoamericana', 'Novelas de autores latinoamericanos', 1),
(4, 'Cuento', 'Colección de cuentos', 1),
(5, 'Drama', 'Obras de teatro y dramas', 1),
(6, 'Ensayo', 'Colección de ensayos literarios', 1);

-- ===============================================================
-- TABLA: LIBROS
-- ===============================================================

DROP TABLE IF EXISTS `libros`;
CREATE TABLE `libros` (
  `id` INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `titulo` VARCHAR(200) NOT NULL,
  `isbn` VARCHAR(20) UNIQUE NOT NULL,
  `id_autor` INT(11) NOT NULL,
  `id_editorial` INT(11) NOT NULL,
  `id_materia` INT(11) NOT NULL,
  `cantidad_total` INT(11) NOT NULL DEFAULT 1,
  `cantidad_disponible` INT(11) NOT NULL DEFAULT 1,
  `anio_publicacion` INT(4) DEFAULT NULL,
  `descripcion` TEXT DEFAULT NULL,
  `imagen` VARCHAR(100) DEFAULT 'default_book.png',
  `estado` INT(1) NOT NULL DEFAULT 1,
  `fecha_creacion` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (`id_autor`) REFERENCES `autor`(`id`) ON DELETE RESTRICT,
  FOREIGN KEY (`id_editorial`) REFERENCES `editorial`(`id`) ON DELETE RESTRICT,
  FOREIGN KEY (`id_materia`) REFERENCES `materia`(`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `libros` (`id`, `titulo`, `isbn`, `id_autor`, `id_editorial`, `id_materia`, `cantidad_total`, `cantidad_disponible`, `anio_publicacion`, `descripcion`, `estado`) VALUES
(1, 'El Aleph', '978-8497403871', 1, 1, 1, 5, 3, 1945, 'Colección de cuentos magistrales de Jorge Luis Borges', 1),
(2, 'Veinte poemas de amor y una canción de desesperación', '978-8432074257', 2, 2, 2, 8, 5, 1924, 'Obra poética más famosa de Pablo Neruda', 1),
(3, 'Cien años de soledad', '978-8439702573', 3, 5, 3, 10, 6, 1967, 'Novela maestra de García Márquez', 1),
(4, 'Rayuela', '978-8439700242', 4, 2, 3, 4, 2, 1963, 'Novela experimental de Julio Cortázar', 1),
(5, 'La casa de los espíritus', '978-8422676843', 5, 5, 3, 6, 4, 1982, 'Novela multigeneracional de Isabel Allende', 1),
(6, 'Pedro Páramo', '978-8439701560', 6, 6, 1, 3, 1, 1955, 'Novela clásica mexicana de Juan Rulfo', 1),
(7, 'El Boom', '978-8432039089', 1, 3, 3, 7, 5, 1970, 'Análisis del movimiento literario latinoamericano', 1),
(8, 'Odas elementales', '978-8435063791', 2, 4, 2, 5, 2, 1954, 'Poesía dedicada a cosas simples de la vida', 1),
(9, 'Amor en tiempos de cólera', '978-8439701751', 3, 5, 1, 9, 7, 1985, 'Novela de amor de García Márquez', 1),
(10, 'La muerte de Artemio Cruz', '978-8432031076', 4, 6, 3, 4, 3, 1962, 'Novela de Carlos Fuentes', 1);

-- ===============================================================
-- TABLA: ESTUDIANTES
-- ===============================================================

DROP TABLE IF EXISTS `estudiantes`;
CREATE TABLE `estudiantes` (
  `id` INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `nombre` VARCHAR(100) NOT NULL,
  `apellido` VARCHAR(100) NOT NULL,
  `cedula` VARCHAR(20) UNIQUE NOT NULL,
  `correo` VARCHAR(100) DEFAULT NULL,
  `telefono` VARCHAR(20) DEFAULT NULL,
  `direccion` TEXT DEFAULT NULL,
  `estado` INT(1) NOT NULL DEFAULT 1,
  `fecha_creacion` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `estudiantes` (`id`, `nombre`, `apellido`, `cedula`, `correo`, `telefono`, `direccion`, `estado`) VALUES
(1, 'Juan', 'García', '1234567890', 'juan.garcia@correo.com', '5551234567', 'Calle Principal 123', 1),
(2, 'María', 'López', '1234567891', 'maria.lopez@correo.com', '5551234568', 'Avenida Secundaria 456', 1),
(3, 'Carlos', 'Rodríguez', '1234567892', 'carlos.rodriguez@correo.com', '5551234569', 'Calle Tertia 789', 1),
(4, 'Ana', 'Martínez', '1234567893', 'ana.martinez@correo.com', '5551234570', 'Avenida Principal 321', 1),
(5, 'Pedro', 'Sánchez', '1234567894', 'pedro.sanchez@correo.com', '5551234571', 'Calle Final 654', 0),
(6, 'Laura', 'Gómez', '1234567895', 'laura.gomez@correo.com', '5551234572', 'Avenida Central 987', 1),
(7, 'Diego', 'Torres', '1234567896', 'diego.torres@correo.com', '5551234573', 'Calle Nueva 111', 1);

-- ===============================================================
-- TABLA: PRESTAMOS
-- ===============================================================

DROP TABLE IF EXISTS `prestamos`;
CREATE TABLE `prestamos` (
  `id` INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `id_estudiante` INT(11) NOT NULL,
  `id_libro` INT(11) NOT NULL,
  `cantidad_prestada` INT(11) NOT NULL DEFAULT 1,
  `fecha_prestamo` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `fecha_vencimiento` DATE NOT NULL,
  `fecha_devolucion` DATE DEFAULT NULL,
  `estado_prestamo` VARCHAR(20) NOT NULL DEFAULT 'activo',
  `observaciones` TEXT DEFAULT NULL,
  `estado` INT(1) NOT NULL DEFAULT 1,
  FOREIGN KEY (`id_estudiante`) REFERENCES `estudiantes`(`id`) ON DELETE RESTRICT,
  FOREIGN KEY (`id_libro`) REFERENCES `libros`(`id`) ON DELETE RESTRICT,
  INDEX idx_estudiante (id_estudiante),
  INDEX idx_libro (id_libro),
  INDEX idx_estado (estado_prestamo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `prestamos` (`id`, `id_estudiante`, `id_libro`, `cantidad_prestada`, `fecha_prestamo`, `fecha_vencimiento`, `fecha_devolucion`, `estado_prestamo`, `observaciones`) VALUES
(1, 1, 1, 1, '2026-05-20', '2026-06-20', NULL, 'activo', 'Préstamo activo'),
(2, 2, 3, 2, '2026-05-25', '2026-06-25', NULL, 'activo', 'Préstamo activo'),
(3, 3, 2, 1, '2026-05-15', '2026-06-15', '2026-05-30', 'devuelto', 'Devuelto a tiempo'),
(4, 4, 5, 1, '2026-05-18', '2026-06-18', NULL, 'activo', 'Préstamo activo'),
(5, 6, 8, 3, '2026-05-22', '2026-06-22', NULL, 'activo', 'Préstamo activo'),
(6, 1, 9, 2, '2026-05-10', '2026-06-10', '2026-06-05', 'devuelto', 'Devuelto con retraso - 5 días');

-- ===============================================================
-- TABLA: CONFIGURACION
-- ===============================================================

DROP TABLE IF EXISTS `configuracion`;
CREATE TABLE `configuracion` (
  `id` INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `nombre` VARCHAR(200) NOT NULL,
  `telefono` VARCHAR(20) NOT NULL,
  `direccion` TEXT NOT NULL,
  `correo` VARCHAR(100) NOT NULL,
  `foto` VARCHAR(50) DEFAULT 'logo.png',
  `dias_prestamo` INT(3) DEFAULT 30,
  `multa_por_dia` DECIMAL(10, 2) DEFAULT 0.50,
  `fecha_actualizacion` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `configuracion` (`id`, `nombre`, `telefono`, `direccion`, `correo`, `foto`, `dias_prestamo`, `multa_por_dia`) VALUES
(1, 'Biblioteca Central - Institución Educativa', '925491523', 'Lima - Perú', 'info@biblioteca.com', 'logo.png', 30, 0.50);

-- ===============================================================
-- INDICES Y OPTIMIZACIONES
-- ===============================================================

ALTER TABLE `usuarios` ADD INDEX idx_usuario (usuario);
ALTER TABLE `usuarios` ADD INDEX idx_rol (rol);
ALTER TABLE `libros` ADD INDEX idx_titulo (titulo);
ALTER TABLE `libros` ADD INDEX idx_isbn (isbn);
ALTER TABLE `libros` ADD INDEX idx_estado (estado);
ALTER TABLE `estudiantes` ADD INDEX idx_cedula (cedula);
ALTER TABLE `estudiantes` ADD INDEX idx_estado (estado);

-- ===============================================================
-- CREAR VISTAS ÚTILES
-- ===============================================================

-- Vista: Libros disponibles
CREATE OR REPLACE VIEW vw_libros_disponibles AS
SELECT
  l.id,
  l.titulo,
  l.isbn,
  a.autor,
  e.nombre AS editorial,
  m.nombre AS materia,
  l.cantidad_disponible,
  l.cantidad_total,
  l.anio_publicacion
FROM libros l
JOIN autor a ON l.id_autor = a.id
JOIN editorial e ON l.id_editorial = e.id
JOIN materia m ON l.id_materia = m.id
WHERE l.estado = 1 AND l.cantidad_disponible > 0;

-- Vista: Préstamos activos
CREATE OR REPLACE VIEW vw_prestamos_activos AS
SELECT
  p.id,
  s.nombre,
  s.apellido,
  l.titulo AS libro,
  p.cantidad_prestada,
  p.fecha_prestamo,
  p.fecha_vencimiento,
  DATEDIFF(p.fecha_vencimiento, CURDATE()) AS dias_restantes
FROM prestamos p
JOIN estudiantes s ON p.id_estudiante = s.id
JOIN libros l ON p.id_libro = l.id
WHERE p.estado_prestamo = 'activo' AND p.estado = 1;

-- ===============================================================
-- CREAR PROCEDIMIENTOS ALMACENADOS
-- ===============================================================

-- Procedimiento: Registrar préstamo
DELIMITER $$
CREATE PROCEDURE proc_registrar_prestamo(
  IN p_id_estudiante INT,
  IN p_id_libro INT,
  IN p_cantidad INT,
  IN p_dias_prestamo INT
)
BEGIN
  DECLARE v_cantidad_disponible INT;

  -- Verificar cantidad disponible
  SELECT cantidad_disponible INTO v_cantidad_disponible
  FROM libros WHERE id = p_id_libro;

  IF v_cantidad_disponible >= p_cantidad THEN
    -- Registrar préstamo
    INSERT INTO prestamos (
      id_estudiante,
      id_libro,
      cantidad_prestada,
      fecha_vencimiento,
      estado_prestamo
    ) VALUES (
      p_id_estudiante,
      p_id_libro,
      p_cantidad,
      DATE_ADD(CURDATE(), INTERVAL p_dias_prestamo DAY),
      'activo'
    );

    -- Actualizar cantidad disponible
    UPDATE libros
    SET cantidad_disponible = cantidad_disponible - p_cantidad
    WHERE id = p_id_libro;
  END IF;
END$$
DELIMITER ;

-- Procedimiento: Registrar devolución
DELIMITER $$
CREATE PROCEDURE proc_registrar_devolucion(
  IN p_id_prestamo INT
)
BEGIN
  DECLARE v_id_libro INT;
  DECLARE v_cantidad INT;

  SELECT id_libro, cantidad_prestada INTO v_id_libro, v_cantidad
  FROM prestamos WHERE id = p_id_prestamo;

  -- Actualizar préstamo
  UPDATE prestamos
  SET fecha_devolucion = NOW(),
      estado_prestamo = 'devuelto'
  WHERE id = p_id_prestamo;

  -- Restaurar cantidad disponible
  UPDATE libros
  SET cantidad_disponible = cantidad_disponible + v_cantidad
  WHERE id = v_id_libro;
END$$
DELIMITER ;

-- ===============================================================
-- CREAR USUARIO DE APLICACIÓN
-- ===============================================================

-- Crear usuario para la aplicación (opcional - comentado)
-- CREATE USER 'biblioteca_user'@'localhost' IDENTIFIED BY 'biblioteca_pass_2026';
-- GRANT ALL PRIVILEGES ON biblioteca_db.* TO 'biblioteca_user'@'localhost';
-- FLUSH PRIVILEGES;

COMMIT;

-- ===============================================================
-- FIN DE SCRIPT
-- ===============================================================
-- Base de datos lista para usar
-- Usuarios de prueba:
--   - admin / password (admin)
--   - bibliotecario / password (bibliotecario)
--   - usuario1 / password (usuario)
--
-- Nota: Las contraseñas están hasheadas con bcrypt
-- Para cambiar: usar la función de seguridad del sistema
-- ===============================================================
