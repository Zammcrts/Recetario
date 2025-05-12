--se crea la tabla usuarios
CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nombre_usuario VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    contraseña VARCHAR(100) NOT NULL
);
--se crea la tabla categorias
CREATE TABLE categorias (
    id_categoria SERIAL PRIMARY KEY,
    nombre_categoria VARCHAR(100) NOT NULL UNIQUE
);
--se crea la tabla recetar
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
--se crea la tabla ingredientes
CREATE TABLE ingredientes (
    id_ingrediente SERIAL PRIMARY KEY,
    nombre_ingrediente VARCHAR(100) NOT NULL UNIQUE
);
--tabla que relaciona receta e ingredientes
CREATE TABLE receta_ingredientes (
    id_receta INT NOT NULL,
    id_ingrediente INT NOT NULL,
    cantidad VARCHAR(50), -- ejemplo: "2", "1/2", etc.
    unidad VARCHAR(50),    -- ejemplo: "taza", "cucharadita", "gramos"
    PRIMARY KEY (id_receta, id_ingrediente),
    FOREIGN KEY (id_receta) REFERENCES recetas(id_receta),
    FOREIGN KEY (id_ingrediente) REFERENCES ingredientes(id_ingrediente)
);
--se crea la tabla comentarios
CREATE TABLE comentarios (
    id_comentario SERIAL PRIMARY KEY,
    id_receta INT NOT NULL,
    id_usuario INT NOT NULL,
    texto_comentario TEXT NOT NULL,
    fecha_comentario TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_receta) REFERENCES recetas(id_receta),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);
--se crear la tabla evaluaciones
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
--tabla de recetas guardadas
CREATE TABLE recetas_guardadas (
    id_usuario INT NOT NULL,
    id_receta INT NOT NULL,
    fecha_guardado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_usuario, id_receta),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_receta) REFERENCES recetas(id_receta)
);

--se insertan las categorias
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
('Vegana'),
-- arararara
('Comida Vampírica'),
('Comida Post-Apocalíptica'),
('Comida Futurista');
-- se insertan los usuarios
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
('FernandoCruz', 'fernando@example.com', 'ferpass654'),
-- aportacion epica de ara
('BellaSwanFan', 'bella@twilight.com', 'luna123'), -- 11
('DarylDixon01', 'daryl@twd.com', 'crossbow99'), -- 12
('ShinjiPilot', 'shinji@eva.com', 'nerv2025'); -- 13

--se insertan ingredientes
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
('Fresas'),
('Sangre artificial'),
('Harina de trigo'),
('Carne de conejo'),
('Zanahorias salvajes'),
('Gelatina roja'),
('Fruta en conserva');

--se insertan las recetas
INSERT INTO recetas (titulo, descripcion, tiempo_preparacion, imagen, id_categoria, id_usuario) VALUES
('Panqueques Saludables', 'Mezcla harina, azúcar, huevo y leche hasta obtener una masa uniforme. Cocina en una sartén antiadherente por ambos lados hasta dorar.', 20, 'C:\Users\samco\Documents\Recetario\imagenes\hotcakes.jpg', 1, 1),
('Pollo Teriyaki', 'Cocina el pollo en un sartén. Añade salsa de soya y arroz cocido. Deja reducir hasta que espese y sirve caliente.', 35, 'C:\Users\samco\Documents\Recetario\imagenes\teriyaky.jpg', 2, 2),
('Tarta de Limón', 'Prepara la base con harina y mantequilla, hornea. Mezcla limón, azúcar y huevos para el relleno. Hornea de nuevo y refrigera.', 45, 'C:\Users\samco\Documents\Recetario\imagenes\limon.jpg', 3, 3),
('Tacos de Pescado', 'Cocina el pescado con limón y aceite de oliva. Sirve en tortillas calientes con tus toppings favoritos.', 25, 'C:\Users\samco\Documents\Recetario\imagenes\pescado.jpg', 4, 4),
('Pizza Margarita', 'Extiende la masa, añade tomate en rodajas, albahaca y un toque de aceite de oliva. Hornea hasta que la masa esté crujiente.', 30, 'C:\Users\samco\Documents\Recetario\imagenes\pizza.jpg', 5, 5),
('Smoothie de Fresa', 'Licúa las fresas con leche y un poco de azúcar hasta obtener una mezcla cremosa. Sirve frío.', 10, 'C:\Users\samco\Documents\Recetario\imagenes\fresa.jpg', 9, 6),
('Hummus Clásico', 'Tritura los garbanzos cocidos con aceite de oliva y jugo de limón hasta lograr una crema suave.', 15, 'C:\Users\samco\Documents\Recetario\imagenes\hummus.jpeg', 7, 7),
('Ensalada Vegana', 'Corta el aguacate y pepino. Mezcla con espinacas frescas y aliña al gusto.', 12, 'C:\Users\samco\Documents\Recetario\imagenes\ensalada.jpg', 10, 8),
('Sushi de Salmón', 'Cocina el arroz, enfría y adereza. Enrolla con salmón y un poco de salsa de soya.', 50, 'C:\Users\samco\Documents\Recetario\imagenes\sushi.jpg', 2, 9),
('Café Dalgona', 'Bate café instantáneo, azúcar y agua caliente hasta que espese. Sirve sobre leche fría o caliente.', 5, 'C:\Users\samco\Documents\Recetario\imagenes\cafe.jpg', 9, 10),
('Pastel de Sangre de Twilight', 'Prepara una mezcla con harina y azúcar teñida con gelatina roja. Hornea en molde y decora con fruta en conserva y "sangre artificial".', 90, 'C:\Users\samco\Documents\Recetario\imagenes\Pastel-Twilight.jpeg', 11, 11),
('Estofado de Conejo Estilo TWD', 'Sella la carne de conejo, añade zanahorias y agua. Cocina a fuego lento hasta que la carne esté tierna. Ideal para sobrevivientes.', 120, 'C:\Users\samco\Documents\Recetario\imagenes\estofado.jpg', 12, 12),
('Pudín de Células Evangelion', 'Disuelve la gelatina roja en agua caliente y mezcla con fruta en conserva. Refrigera hasta que cuaje. No garantizamos efectos secundarios.', 45, 'C:\Users\samco\Documents\Recetario\imagenes\rei.jpeg', 13, 13);

-- 1. Panqueques Saludables
INSERT INTO receta_ingredientes (id_receta, id_ingrediente, cantidad, unidad) VALUES
(1, 1, '1', 'taza'), -- Harina
(1, 2, '2', 'cucharadas'), -- Azúcar
(1, 3, '1', 'unidad'), -- Huevo
(1, 4, '1', 'taza'); -- Leche

-- 2. Pollo Teriyaki
INSERT INTO receta_ingredientes (id_receta, id_ingrediente, cantidad, unidad) VALUES
(2, 6, '300', 'gramos'), -- Pollo
(2, 8, '3', 'cucharadas'), -- Salsa de soya
(2, 7, '1', 'taza'); -- Arroz

-- 3. Tarta de Limón
INSERT INTO receta_ingredientes (id_receta, id_ingrediente, cantidad, unidad) VALUES
(3, 1, '1.5', 'tazas'), -- Harina
(3, 2, '3/4', 'taza'), -- Azúcar
(3, 12, '2', 'unidades'), -- Limón
(3, 5, '100', 'gramos'); -- Mantequilla

-- 4. Tacos de Pescado
INSERT INTO receta_ingredientes (id_receta, id_ingrediente, cantidad, unidad) VALUES
(4, 11, '200', 'gramos'), -- Pescado
(4, 12, '1', 'unidad'), -- Limón
(4, 13, '2', 'cucharadas'); -- Aceite de oliva

-- 5. Pizza Margarita
INSERT INTO receta_ingredientes (id_receta, id_ingrediente, cantidad, unidad) VALUES
(5, 9, '3', 'unidades'), -- Tomate
(5, 10, '0.5', 'taza'), -- Albahaca
(5, 13, '1', 'cucharada'); -- Aceite de oliva

-- 6. Smoothie de Fresa
INSERT INTO receta_ingredientes (id_receta, id_ingrediente, cantidad, unidad) VALUES
(6, 20, '1', 'taza'), -- Fresas
(6, 4, '1', 'taza'), -- Leche
(6, 2, '1', 'cucharada'); -- Azúcar

-- 7. Hummus Clásico
INSERT INTO receta_ingredientes (id_receta, id_ingrediente, cantidad, unidad) VALUES
(7, 15, '1', 'taza'), -- Garbanzos
(7, 13, '2', 'cucharadas'), -- Aceite de oliva
(7, 12, '1', 'unidad'); -- Limón

-- 8. Ensalada Vegana
INSERT INTO receta_ingredientes (id_receta, id_ingrediente, cantidad, unidad) VALUES
(8, 14, '1', 'unidad'), -- Aguacate
(8, 16, '0.5', 'unidad'), -- Pepino
(8, 17, '1', 'taza'); -- Espinacas

-- 9. Sushi de Salmón
INSERT INTO receta_ingredientes (id_receta, id_ingrediente, cantidad, unidad) VALUES
(9, 7, '2', 'tazas'), -- Arroz
(9, 11, '200', 'gramos'), -- Pescado (salmón)
(9, 8, '2', 'cucharadas'); -- Salsa de soya

-- 10. Café Dalgona
INSERT INTO receta_ingredientes (id_receta, id_ingrediente, cantidad, unidad) VALUES
(10, 18, '2', 'cucharadas'), -- Café
(10, 2, '2', 'cucharadas'), -- Azúcar
(10, 4, '1', 'taza'); -- Leche

-- 11. Pastel de Sangre de Twilight
INSERT INTO receta_ingredientes (id_receta, id_ingrediente, cantidad, unidad) VALUES
(11, 1, '1', 'taza'), -- Harina
(11, 2, '2', 'tazas'), -- Azúcar
(11, 25, '1', 'sobre'), -- Gelatina roja
(11, 26, '1', 'lata'), -- Fruta en conserva
(11, 21, '2', 'cucharadas'); -- Sangre artificial

-- 12. Estofado de Conejo Estilo TWD
INSERT INTO receta_ingredientes (id_receta, id_ingrediente, cantidad, unidad) VALUES
(12, 23, '500', 'gramos'), -- Carne de conejo
(12, 24, '3', 'unidades'); -- Zanahorias salvajes

-- 13. Pudín de Células Evangelion
INSERT INTO receta_ingredientes (id_receta, id_ingrediente, cantidad, unidad) VALUES
(13, 25, '1', 'sobre'), -- Gelatina roja
(13, 26, '1', 'lata'); -- Fruta en conserva

--se insertan comentarios
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
(10, 1, 'Muy fácil de preparar, y delicioso.'),
(11, 12, '¡Tenebrosamente delicioso! Me sentí como un verdadero Cullen.'),
(12, 13, 'Perfecto para una cena al estilo supervivencia, como en Alexandria.'),
(13, 11, 'Una textura misteriosa, digno de un experimento de NERV.');

--se insertan las evaluaciones
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
(10, 1, 5),
(11, 12, 5), -- Daryl evaluando receta Twilight
(12, 13, 4), -- Shinji evaluando receta TWD
(13, 11, 5); -- Bella evaluando receta Evangelion
