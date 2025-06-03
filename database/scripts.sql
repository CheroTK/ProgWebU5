-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS activelife_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE activelife_db;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'editor', 'cliente') NOT NULL DEFAULT 'cliente',
    edad INT DEFAULT NULL,
    altura DECIMAL(4,2) DEFAULT NULL,
    peso DECIMAL(5,2) DEFAULT NULL,
    objetivo VARCHAR(255) DEFAULT NULL,
    activo TINYINT(1) DEFAULT 1
);

-- Tabla de productos
CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(50) NOT NULL,   -- Agregado
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL
);

-- Tabla de ventas
CREATE TABLE IF NOT EXISTS ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Tabla de detalle_ventas
CREATE TABLE IF NOT EXISTS detalle_ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    venta_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (venta_id) REFERENCES ventas(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- Inserta usuarios (contraseñas ya hasheadas)
INSERT INTO usuarios (username, email, password, role)
VALUES
  ('admin', 'admin@correo.com', 'scrypt:32768:8:1$lDiShujSp5jhis1t$f0ae7b554669c2f5b521f946d8845262bcd3269b12b4c0688eebf0b6b4db63c2649eba864c0b49045e47a3743c457fa69ecceec0875819caa93a72ce2706cd7e', 'admin'),
  ('editor', 'editor@correo.com', 'scrypt:32768:8:1$leQ3Jm7aGRPLGFGp$f2a71b0ea227d3b7a6898d28cda227db47d35f6e7721c39c30b5a204239e66a464fc5e24367cc390014e96e2c7297b5f6e51f86f50bcf84b70bcb202841f36db', 'editor'),
  ('cliente', 'cliente@correo.com', 'scrypt:32768:8:1$ynpKs2n4YfAkrX9K$ba5396b0d3c2d4b7f4c3c50e12b6d6ebf045ca81c88a48cc9ef0ea652f258f32d6d4f51a6dc7794d1b929a5c13e65b34a265c8afcdebfce3c35c0dfac7e32a49', 'cliente');
  ('cherotk', 'cherotk@correo.com', 'cherotk123', 'admin');

-- Inserta productos con categoría (sin imágenes)
INSERT INTO productos (nombre, descripcion, categoria, precio, stock) VALUES
  -- Rutinas de Ejercicio
  ('30 days Muscle Building', 'Rutina intensa para ganar músculo en 30 días.', 'rutina', 20.00, 50),
  ('Insanity Deluxe Edition', 'Entrenamiento avanzado de alta intensidad.', 'rutina', 25.00, 40),
  ('Fast Hiking', 'Programa para mejorar tu resistencia en senderismo.', 'rutina', 15.00, 60),
  -- Recetas Saludables
  ('Meal Menu for Hiking', 'Menú nutricional pensado para largas caminatas.', 'receta', 10.00, 30),
  ('50 Recetas para una Vida Saludable', 'Recetario para mejorar tu alimentación diaria.', 'receta', 12.00, 35),
  ('Recetario Semanal para Volumen', 'Recetas para ganar masa muscular de forma saludable.', 'receta', 18.00, 25);
