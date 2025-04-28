CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nombre_usuario VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    contraseña VARCHAR(100) NOT NULL
);

CREATE TABLE categorias (
    id_categoria SERIAL PRIMARY KEY,
    nombre_categoria VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE recetas (
    id_receta SERIAL PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    descripcion TEXT NOT NULL,
    tiempo_preparacion INT NOT NULL, -- en minutos
    imagen TEXT, -- ruta al archivo o base64
    id_categoria INT NOT NULL,
    id_usuario INT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

CREATE TABLE ingredientes (
    id_ingrediente SERIAL PRIMARY KEY,
    nombre_ingrediente VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE receta_ingredientes (
    id_receta INT NOT NULL,
    id_ingrediente INT NOT NULL,
    cantidad VARCHAR(50), -- ejemplo: "2", "1/2", etc.
    unidad VARCHAR(50),    -- ejemplo: "taza", "cucharadita", "gramos"
    PRIMARY KEY (id_receta, id_ingrediente),
    FOREIGN KEY (id_receta) REFERENCES recetas(id_receta),
    FOREIGN KEY (id_ingrediente) REFERENCES ingredientes(id_ingrediente)
);

CREATE TABLE comentarios (
    id_comentario SERIAL PRIMARY KEY,
    id_receta INT NOT NULL,
    id_usuario INT NOT NULL,
    texto_comentario TEXT NOT NULL,
    fecha_comentario TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_receta) REFERENCES recetas(id_receta),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

CREATE TABLE evaluaciones (
    id_evaluacion SERIAL PRIMARY KEY,
    id_receta INT NOT NULL,
    id_usuario INT NOT NULL,
    estrellas INT CHECK (estrellas BETWEEN 0 AND 5),
    fecha_evaluacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_receta) REFERENCES recetas(id_receta),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    UNIQUE (id_receta, id_usuario) -- cada usuario solo puede evaluar una vez cada receta
);

CREATE TABLE recetas_guardadas (
    id_usuario INT NOT NULL,
    id_receta INT NOT NULL,
    fecha_guardado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_usuario, id_receta),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_receta) REFERENCES recetas(id_receta)
);

INSERT INTO categorias (nombre_categoria) VALUES
('Saludable'),
('Asiáticas'),
('Postres'),
('Mexicana'),
('Italiana'),
('Desayunos'),
('Árabes'),
('Pescados y Mariscos'),
('Bebidas'),
('Vegana');

INSERT INTO usuarios (nombre_usuario, email, contraseña) VALUES
('AnaGomez', 'ana@example.com', 'contrasena123'),
('LuisPerez', 'luis@example.com', 'miclave456'),
('SofiaLopez', 'sofia@example.com', 'seguro789'),
('CarlosMendez', 'carlos@example.com', 'pass321'),
('MarianaSoto', 'mariana@example.com', 'clave987'),
('JuanRamirez', 'juan@example.com', 'password123'),
('ElenaDiaz', 'elena@example.com', 'mypassword456'),
('DanielSantos', 'daniel@example.com', 'pass789'),
('ValeriaTorres', 'valeria@example.com', 'valepass321'),
('FernandoCruz', 'fernando@example.com', 'ferpass654');

INSERT INTO ingredientes (nombre_ingrediente) VALUES
('Harina'),
('Azúcar'),
('Huevo'),
('Leche'),
('Mantequilla'),
('Pollo'),
('Arroz'),
('Salsa de soya'),
('Tomate'),
('Albahaca'),
('Pescado'),
('Limón'),
('Aceite de oliva'),
('Aguacate'),
('Garbanzos'),
('Pepino'),
('Espinacas'),
('Café'),
('Chocolate'),
('Fresas');

INSERT INTO recetas (titulo, descripcion, tiempo_preparacion, imagen, id_categoria, id_usuario) VALUES
('Panqueques Saludables', 'Panqueques integrales bajos en azúcar.', 20, 'imagenes/panqueques.jpg', 1, 1),
('Pollo Teriyaki', 'Pollo estilo japonés con salsa teriyaki.', 35, 'imagenes/teriyaki.jpg', 2, 2),
('Tarta de Limón', 'Tarta dulce y refrescante para postres.', 45, 'imagenes/tartalimon.jpg', 3, 3),
('Tacos de Pescado', 'Tacos mexicanos de pescado con limón.', 25, 'imagenes/tacospescado.jpg', 4, 4),
('Pizza Margarita', 'Pizza italiana con tomate y albahaca.', 30, 'imagenes/pizza.jpg', 5, 5),
('Smoothie de Fresa', 'Bebida saludable a base de fresas.', 10, 'imagenes/smoothiefresa.jpg', 9, 6),
('Hummus Clásico', 'Crema árabe de garbanzos y aceite de oliva.', 15, 'imagenes/hummus.jpg', 7, 7),
('Ensalada Vegana', 'Ensalada fresca con aguacate y espinacas.', 12, 'imagenes/ensaladavegana.jpg', 10, 8),
('Sushi de Salmón', 'Sushi japonés clásico.', 50, 'imagenes/sushi.jpg', 2, 9),
('Café Dalgona', 'Bebida coreana de café batido.', 5, 'imagenes/dalgona.jpg', 9, 10);

-- Panqueques Saludables
INSERT INTO receta_ingredientes (id_receta, id_ingrediente, cantidad, unidad) VALUES
(1, 1, '1', 'taza'),
(1, 2, '2', 'cucharadas'),
(1, 3, '1', 'unidad'),
(1, 4, '1', 'taza');

-- Pollo Teriyaki
INSERT INTO receta_ingredientes (id_receta, id_ingrediente, cantidad, unidad) VALUES
(2, 6, '300', 'gramos'),
(2, 8, '3', 'cucharadas'),
(2, 7, '1', 'taza');

-- Tarta de Limón
INSERT INTO receta_ingredientes (id_receta, id_ingrediente, cantidad, unidad) VALUES
(3, 1, '1.5', 'tazas'),
(3, 2, '3/4', 'taza'),
(3, 12, '2', 'unidades'),
(3, 5, '100', 'gramos');

-- Tacos de Pescado
INSERT INTO receta_ingredientes (id_receta, id_ingrediente, cantidad, unidad) VALUES
(4, 11, '200', 'gramos'),
(4, 12, '1', 'unidad'),
(4, 13, '2', 'cucharadas');

-- Pizza Margarita
INSERT INTO receta_ingredientes (id_receta, id_ingrediente, cantidad, unidad) VALUES
(5, 9, '3', 'unidades'),
(5, 10, '0.5', 'taza'),
(5, 13, '1', 'cucharada');

-- Smoothie de Fresa
INSERT INTO receta_ingredientes (id_receta, id_ingrediente, cantidad, unidad) VALUES
(6, 20, '1', 'taza'),
(6, 4, '1', 'taza'),
(6, 2, '1', 'cucharada');

-- Hummus Clásico
INSERT INTO receta_ingredientes (id_receta, id_ingrediente, cantidad, unidad) VALUES
(7, 15, '1', 'taza'),
(7, 13, '2', 'cucharadas'),
(7, 12, '1', 'unidad');

-- Ensalada Vegana
INSERT INTO receta_ingredientes (id_receta, id_ingrediente, cantidad, unidad) VALUES
(8, 14, '1', 'unidad'),
(8, 16, '0.5', 'unidad'),
(8, 17, '1', 'taza');

-- Sushi de Salmón
INSERT INTO receta_ingredientes (id_receta, id_ingrediente, cantidad, unidad) VALUES
(9, 7, '2', 'tazas'),
(9, 11, '200', 'gramos'),
(9, 8, '2', 'cucharadas');

-- Café Dalgona
INSERT INTO receta_ingredientes (id_receta, id_ingrediente, cantidad, unidad) VALUES
(10, 18, '2', 'cucharadas'),
(10, 2, '2', 'cucharadas'),
(10, 4, '1', 'taza');

INSERT INTO comentarios (id_receta, id_usuario, texto_comentario) VALUES
(1, 2, 'Muy ricos para un desayuno rápido.'),
(2, 3, 'El pollo quedó jugoso y muy sabroso.'),
(3, 4, 'Perfecto balance de dulce y ácido.'),
(4, 5, 'Me encantó el sabor fresco del pescado.'),
(5, 6, 'Una pizza sencilla pero deliciosa.'),
(6, 7, 'Muy refrescante, ideal para el calor.'),
(7, 8, 'Súper fácil de hacer y muy rico.'),
(8, 9, 'Fresca y ligera, muy buena combinación.'),
(9, 10, '¡Me encanta el sushi, excelente receta!'),
(10, 1, 'Muy fácil de preparar, y delicioso.');

INSERT INTO evaluaciones (id_receta, id_usuario, estrellas) VALUES
(1, 2, 5),
(2, 3, 4),
(3, 4, 5),
(4, 5, 4),
(5, 6, 5),
(6, 7, 4),
(7, 8, 5),
(8, 9, 4),
(9, 10, 5),
(10, 1, 5);
