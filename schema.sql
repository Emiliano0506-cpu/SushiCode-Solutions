CREATE DATABASE IF NOT EXISTS bd_sushicode CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE bd_sushicode;

CREATE TABLE IF NOT EXISTS Clientes (
 id_cliente INT AUTO_INCREMENT PRIMARY KEY,
 nombre VARCHAR(100) NOT NULL,
 apellido_paterno VARCHAR(50) NOT NULL,
 apellido_materno VARCHAR(50),
 telefono VARCHAR(15),
 correo VARCHAR(100),
 RFC VARCHAR(13),
 calle VARCHAR(100),
 numero_exterior VARCHAR(10),
 numero_interior VARCHAR(10),
 colonia VARCHAR(80),
 codigo_postal CHAR(5),
 ciudad VARCHAR(60) NOT NULL,
 estado VARCHAR(60) NOT NULL
);

CREATE TABLE IF NOT EXISTS Menu (
 id_menu INT AUTO_INCREMENT PRIMARY KEY,
 nombre VARCHAR(80) NOT NULL,
 descripcion VARCHAR(200),
 disponibilidad BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS Platillos (
 id_platillo INT AUTO_INCREMENT PRIMARY KEY,
 id_menu INT NOT NULL,
 nombre VARCHAR(100) NOT NULL,
 descripcion VARCHAR(200),
 categoria VARCHAR(50),
 precio DECIMAL(10,2) NOT NULL,
 disponibilidad BOOLEAN NOT NULL DEFAULT TRUE,
 CONSTRAINT fk_platillo_menu FOREIGN KEY (id_menu) REFERENCES Menu(id_menu)
);

-- Tabla de asociación mostrada en el diagrama relacional.
-- Evita duplicar una misma asociación Menu-Platillo.
CREATE TABLE IF NOT EXISTS Platillos_Menu (
 id_platillo INT NOT NULL,
 id_menu INT NOT NULL,
 PRIMARY KEY (id_platillo, id_menu),
 CONSTRAINT fk_pm_platillo FOREIGN KEY (id_platillo) REFERENCES Platillos(id_platillo) ON DELETE CASCADE,
 CONSTRAINT fk_pm_menu FOREIGN KEY (id_menu) REFERENCES Menu(id_menu) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Pedidos (
 id_pedido INT AUTO_INCREMENT PRIMARY KEY,
 id_cliente INT NOT NULL,
 fecha_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
 estado VARCHAR(20) NOT NULL DEFAULT 'En preparación',
 total DECIMAL(10,2) NOT NULL DEFAULT 0,
 CONSTRAINT fk_pedido_cliente FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente)
);

CREATE TABLE IF NOT EXISTS DetallePedido (
 id_detalle INT AUTO_INCREMENT PRIMARY KEY,
 id_pedido INT NOT NULL,
 id_platillo INT NOT NULL,
 cantidad INT NOT NULL,
 costo_unitario DECIMAL(10,2) NOT NULL,
 subtotal DECIMAL(10,2) NOT NULL,
 CONSTRAINT fk_detalle_pedido FOREIGN KEY (id_pedido) REFERENCES Pedidos(id_pedido) ON DELETE CASCADE,
 CONSTRAINT fk_detalle_platillo FOREIGN KEY (id_platillo) REFERENCES Platillos(id_platillo)
);
