#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MIGRACIÓN MYSQL → POSTGRESQL
Convierte y carga el dump MySQL en PostgreSQL.
"""

import psycopg2
import sys
import os

# ── Configuración de conexión ─────────────────────────────────────────────────
DB_HOST = "127.0.0.1"
DB_PORT = 5432
DB_NAME = "biblioteca"
DB_USER = "postgres"
DB_PASS = "K.evin2007"

def conectar():
    url = os.getenv('DATABASE_URL', '')
    if url:
        if url.startswith('postgres://'):
            url = 'postgresql://' + url[len('postgres://'):]
        return psycopg2.connect(url)
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASS
    )

# ── DDL en PostgreSQL ─────────────────────────────────────────────────────────
SCHEMA_SQL = """
DROP TABLE IF EXISTS detalle_permisos CASCADE;
DROP TABLE IF EXISTS prestamo CASCADE;
DROP TABLE IF EXISTS libro CASCADE;
DROP TABLE IF EXISTS autor CASCADE;
DROP TABLE IF EXISTS editorial CASCADE;
DROP TABLE IF EXISTS materia CASCADE;
DROP TABLE IF EXISTS permisos CASCADE;
DROP TABLE IF EXISTS estudiante CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;
DROP TABLE IF EXISTS configuracion CASCADE;

CREATE TABLE autor (
    id SERIAL PRIMARY KEY,
    autor VARCHAR(150) NOT NULL,
    imagen VARCHAR(100) NOT NULL DEFAULT '',
    estado INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE configuracion (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    direccion TEXT NOT NULL,
    correo VARCHAR(100) NOT NULL,
    foto VARCHAR(50) NOT NULL
);

CREATE TABLE editorial (
    id SERIAL PRIMARY KEY,
    editorial VARCHAR(150) NOT NULL,
    estado INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE materia (
    id SERIAL PRIMARY KEY,
    materia TEXT NOT NULL,
    estado INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE permisos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    tipo INTEGER NOT NULL
);

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    clave VARCHAR(255) NOT NULL,
    rol VARCHAR(50) NOT NULL DEFAULT 'usuario',
    estado INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE estudiante (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(20) NOT NULL,
    dni VARCHAR(20) NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    carrera VARCHAR(255) NOT NULL,
    direccion TEXT NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    estado INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE libro (
    id SERIAL PRIMARY KEY,
    titulo TEXT NOT NULL,
    cantidad INTEGER NOT NULL,
    id_autor INTEGER NOT NULL REFERENCES autor(id),
    id_editorial INTEGER NOT NULL REFERENCES editorial(id),
    anio_edicion DATE NOT NULL,
    id_materia INTEGER NOT NULL REFERENCES materia(id),
    num_pagina INTEGER NOT NULL,
    descripcion TEXT NOT NULL DEFAULT '',
    imagen VARCHAR(100) NOT NULL DEFAULT '',
    estado INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE detalle_permisos (
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id),
    id_permiso INTEGER NOT NULL REFERENCES permisos(id)
);

CREATE TABLE prestamo (
    id SERIAL PRIMARY KEY,
    id_estudiante INTEGER NOT NULL REFERENCES estudiante(id),
    id_libro INTEGER NOT NULL REFERENCES libro(id),
    fecha_prestamo DATE NOT NULL,
    fecha_devolucion DATE NOT NULL,
    cantidad INTEGER NOT NULL,
    observacion TEXT NOT NULL DEFAULT '',
    estado INTEGER NOT NULL DEFAULT 1
);
"""

# ── DATOS ─────────────────────────────────────────────────────────────────────

AUTORES = [
    (1,'111111','autor_20260413231501731249.jpg',1),
    (2,'cambiar el nombre llll','autor_20260413231507757357.png',1),
    (3,'popoiipippi','logo.png',1),
    (4,'Gabriel García Márquez','autor_20260413231514646557.jpg',1),
    (5,'Miguel de Cervantes','autor_20260413231518181142.jpg',1),
    (6,'George Orwell','autor_20260413231521497143.jpg',1),
    (7,'Antoine de Saint-Exupéry','autor_20260413231524965119.jpg',1),
    (8,'J.K. Rowling','autor_20260413231528984611.jpg',1),
    (9,'J.R.R. Tolkien','autor_20260413231533131335.jpg',1),
    (10,'Jane Austen','autor_20260413231538050074.jpg',1),
    (11,'Fiódor Dostoyevski','autor_20260413231541737661.jpg',1),
    (12,'F. Scott Fitzgerald','autor_20260413231545330653.jpg',1),
    (13,'Harper Lee','autor_20260413231548968333.jpg',1),
    (14,'Paulo Coelho','autor_20260413231552251805.jpg',1),
    (15,'León Tolstói','autor_20260413231555497125.jpg',1),
    (16,'Aldous Huxley','autor_20260413231559255727.png',1),
    (17,'Victor Hugo','autor_20260413231603519555.jpg',1),
    (18,'Ray Bradbury','autor_20260413231607470909.jpg',1),
    (19,'Umberto Eco','autor_20260413231611108215.jpg',1),
    (20,'Yuval Noah Harari','autor_20260413231614868085.jpg',1),
    (21,'Jorge Luis Borges','autor_20260413231618689140.jpg',1),
    (22,'Carlos Ruiz Zafón','autor_20260413231622231291.jpg',1),
    (23,'Juan Rulfo','autor_20260413231625397946.jpg',1),
    (24,'Ernesto Sabato','autor_20260413231630788567.jpg',1),
    (25,'Julio Cortázar','autor_20260413231635985751.jpg',1),
    (26,'Isabel Allende','autor_20260413231640452296.jpg',1),
    (27,'José Saramago','autor_20260413231644689518.jpg',1),
    (28,'Franz Kafka','autor_20260413231650094858.jpg',1),
    (29,'Oscar Wilde','autor_20260413231655156307.jpg',1),
    (30,'Mary Shelley','autor_20260413231659860565.jpg',1),
    (31,'Bram Stoker','autor_20260413231703454221.jpg',1),
    (32,'Dan Brown','autor_20260413231707445262.jpg',1),
    (33,'Elizabeth Gilbert','autor_20260413231714222686.jpg',1),
    (34,'Jostein Gaarder','autor_20260413231718244927.jpg',1),
    (35,'Arthur Golden','logo.png',1),
    (36,'Patrick Süskind','logo.png',1),
    (37,'Rubén Darío','autor_20260413231729869710.jpg',1),
    (38,'José Eustasio Rivera','autor_20260413231734813558.png',1),
    (39,'George R.R. Martin','autor_20260413231738157675.jpg',1),
    (40,'Orson Scott Card','autor_20260413231742086596.jpg',1),
    (41,'Frank Herbert','autor_20260413231745834893.jpg',1),
    (42,'William Gibson','autor_20260413231752202385.jpg',1),
    (43,'William Golding','autor_20260413231758549135.jpg',1),
    (44,'Jonathan Franzen','autor_20260413231802582803.jpg',1),
    (45,'Toni Morrison','autor_20260413231808884926.jpg',1),
    (46,'Joseph Conrad','autor_20260413231815123677.png',1),
    (47,'Roberto Bolaño','autor_20260413231819945793.jpg',1),
    (48,'Mario Vargas Llosa','autor_20260413231825018923.png',1),
    (49,'Horacio Quiroga','autor_20260414145255607301.jpg',1),
    (50,'Herman Melville','autor_20260414145258899811.jpg',1),
    (51,'William Shakespeare','autor_20260414145302139335.jpg',1),
    (52,'Alexandre Dumas','autor_20260414145306147192.jpg',1),
    (53,'Ana Franck','20260414143917_url.jpg',1),
    (54,'Dante Alighieri','autor_20260414145310483940.jpg',1),
    (55,'Vladimir Nabokov','autor_20260414145314231305.jpg',1),
    (56,'Albert Camus','autor_20260414145318163294.jpg',1),
    (57,'James Joyce','autor_20260414145322823573.jpg',1),
    (58,'Emily Brontë','autor_20260414145327403936.jpg',1),
    (59,'Jean-Paul Sartre','autor_20260414145332228425.jpg',1),
    (60,'Ralph Ellison','autor_20260414145336668342.jpg',1),
    (61,'Milan Kundera','autor_20260414153433256059.jpg',1),
    (62,'Gustave Flaubert','autor_20260414160807209563.jpg',1),
    (63,'Hermann Hesse','autor_20260414160810699373.jpg',1),
    (64,'Mario Benedetti','autor_20260414160813921473.jpg',1),
    (65,'Federico García Lorca','autor_20260414160817042736.jpg',1),
    (66,'Pablo Neruda','autor_20260414160820254124.jpg',1),
    (67,'Alejo Carpentier','autor_20260414160823507279.jpg',1),
    (68,'Manuel Puig','autor_20260414160826863299.jpg',1),
    (69,'Carlos Fuentes','autor_20260414160830278910.jpg',1),
    (70,'Juan Carlos Onetti','autor_20260414160834243402.jpg',1),
    (71,'José María Arguedas','autor_20260414162541797752.jpg',1),
    (72,'José Donoso','autor_20260414162547651455.jpg',1),
    (73,'José Lezama Lima','autor_20260414162550921281.jpg',1),
    (74,'Ricardo Piglia','autor_20260414162554020977.jpg',1),
    (75,'Guillermo Cabrera Infante','autor_20260414162557314982.png',1),
    (76,'Han Kang','autor_20260414163154327592.jpg',1),
    (77,'Jean Giono','autor_20260414163157570215.png',1),
    (78,'Muriel Barbery','autor_20260414163200868949.jpg',1),
    (79,'Michel Houellebecq','autor_20260414163204031556.jpg',1),
    (80,'Mark Z. Danielewski','autor_20260414163207156843.jpg',1),
    (81,'Eduardo Galeano','autor_20260414163210344005.jpg',1),
    (82,'Mijaíl Bulgákov','autor_20260414164010845505.jpg',1),
    (83,'Georges Perec','autor_20260414164014187668.jpg',1),
    (84,'Iain McGilchrist','autor_20260414164017518580.png',1),
    (85,'Douglas Hofstadter','autor_20260414164022212861.jpg',1),
    (86,'Ursula K. Le Guin','autor_20260414164025520592.jpg',1),
    (87,'Samuel Beckett','autor_20260414175356098303.jpg',1),
    (88,'Italo Calvino','autor_20260414175359340075.jpg',1),
    (89,'Orhan Pamuk','autor_20260414175402503050.jpg',1),
    (90,'Thomas Mann','autor_20260414175405796025.jpg',1),
    (91,'Samuel Huntington','autor_20260414175409138527.jpg',1),
    (92,'888888','default.png',1),
]

CONFIGURACION = [
    (1,'Vida Informático','925491523','Lima - Perú','angelsifuentes@gmail.com','logo.png'),
]

EDITORIALES = [
    (1,'editorial',1),(2,'Toribio anyarin',0),(3,'Sudamericana',1),(4,'Alfaguara',1),
    (5,'Destino',1),(6,'Salamandra',1),(7,'Minotauro',1),(8,'Alba Editorial',1),
    (9,'Cátedra',1),(10,'Anagrama',1),(11,'Oveja Negra',1),(12,'Ediciones B',1),
    (13,'Planeta',1),(14,'Penguin Clásicos',1),(15,'Lumen',1),(16,'Debate',1),
    (17,'Alianza Editorial',1),(18,'RM Editorial',1),(19,'Seix Barral',1),
    (20,'Plaza & Janés',1),(21,'Anaya',1),(22,'Valdemar',1),(23,'Umbriel',1),
    (24,'Aguilar',1),(25,'Siruela',1),(26,'Punto de Lectura',1),(27,'Panamericana',1),
    (28,'Gigamesh',1),(29,'Debolsillo',1),(30,'Peisa',1),(31,'Losada',1),
    (32,'Espasa',1),(33,'Penguin',1),(34,'Tusquets',1),(35,'Emecé',1),
    (36,'FCE',1),(37,'Ayacucho',1),(38,'Era',1),(39,'Siglo XXI',1),(40,'Pomaire',1),
    (41,'Random House',1),(42,'Duomo',1),(43,'Alpha Decay',1),(44,'YMCA Press',1),
    (45,'Sur',1),(46,'Hachette',1),(47,'S. Fischer Verlag',1),(48,'Putnam',1),
    (49,'Yale University Press',1),(50,'Basic Books',1),(51,'Lindon',1),
    (52,'Einaudi',1),(53,'Suhrkamp',1),(54,'Ceskoslovensky spisovatel',1),
    (55,'Iletisim',1),(56,'Kier',1),(57,'Simon & Schuster',1),
]

MATERIAS = [
    (1,'Base de Datos',1),(2,'Ingenieria de Software',1),(3,'77777',1),
    (4,'Matematica',1),(5,'Geometria Analitica',1),(6,'Literatura',1),
    (7,'Literatura Clásica',1),(8,'Ciencia Ficción',1),(9,'Literatura Infantil',1),
    (10,'Fantasía',1),(11,'Romance Clásico',1),(12,'Literatura Moderna',1),
    (13,'Drama Social',1),(14,'Autoayuda/Novela',1),(15,'Misterio Histórico',1),
    (16,'Historia',1),(17,'Misterio',1),(18,'Ciencia Ficción/Terror',1),
    (19,'Terror',1),(20,'Thriller',1),(21,'Autobiografía',1),(22,'Filosofía/Novela',1),
    (23,'Ficción Histórica',1),(24,'Poesía/Cuentos',1),(25,'Literatura Colombiana',1),
    (26,'Literatura Contemporánea',1),(27,'Teatro',1),(28,'Filosofía / Literatura',1),
    (29,'Modernismo',1),(30,'Romántico',1),(31,'Cuentos',1),(32,'Literatura Mexicana',1),
    (33,'Poesía',1),(34,'Literatura Peruana',1),(35,'Literatura Chilena',1),
    (36,'Literatura Cubana',1),(37,'Literatura Argentina',1),(38,'Novela',1),
    (39,'Cuento',1),(40,'Ensayo',1),(41,'Literatura Experimental',1),(42,'Filosofia',1),
    (43,'Neurociencia',1),(44,'Matematicas',1),(45,'Espiritualidad',1),
    (46,'Literatura Absurda',1),(47,'Literatura Fantastica',1),(48,'Politica',1),
    (49,'Mitologia',1),(50,'Geopolitica',1),
]

PERMISOS = [
    (1,'Libros',1),(2,'Autor',2),(3,'Editorial',3),(4,'Usuarios',4),
    (5,'Configuracion',5),(6,'Estudiantes',6),(7,'Materias',7),
    (8,'Reportes',8),(9,'Prestamos',9),
]

USUARIOS = [
    (1,'admin','Administrador','pbkdf2:sha256:600000$iYcPBwYaBoLbZUNb$b72d0246374d5d5af7304d2da0e7f421d17078c4272a82da5ad50387c0512cf6',1),
    (2,'angel','Vida Informatico','pbkdf2:sha256:600000$iYcPBwYaBoLbZUNb$b72d0246374d5d5af7304d2da0e7f421d17078c4272a82da5ad50387c0512cf6',1),
    (3,'kevin','Kevin Forero','pbkdf2:sha256:600000$gj9lTCmwHiDsbJeh$e800ae3404bddf69229229b28636f15e496fbe3f460709cdbdd72b75c1d9bc97',1),
    (4,'kevin','Kevin Forero','pbkdf2:sha256:600000$0HWmSv3J4ecDr437$eb0a38b0a7692a34003b3f2fcf110725b56ef34243ee20ebfa891946fc26f51d',1),
    (5,'camilo','camilo puentes','pbkdf2:sha256:600000$dYga6iGiBAL5YEQV$0c89fe054c3afe1c83de452c5e75bf5894eda8f10cee6f0d85941195c9954c8c',1),
    (6,'Martin','Martin Lopez','pbkdf2:sha256:600000$u0PxV3OxJ6NfBL3d$ab02563ba261106d28c551c9efb3202d0b1962ef360e0e0514c7161932b0e4a9',1),
    (7,'edward','Edward Infante','pbkdf2:sha256:600000$kFQsr6YeW62IbY9a$a2e09a0b9c3f9009bb7c3713e6cd812c2c6ac180a0a880126d07fbaccfffda8a',1),
    (8,'myuser123','Mi Usuario','pbkdf2:sha256:600000$NcCuCgv60THDkkb7$09122386ec904e5901cd1e9019a0180b8be20d22eb40dc3af24aa1f7ab5a676a',1),
    (9,'tester123','Tester User','pbkdf2:sha256:600000$6sYP5xdZm1TaCuor$6729822085dcb926793284bfd57b0ffb40d81dbd51d9db0a4233b7e69e97f137',1),
    (10,'tester999','Tester User','pbkdf2:sha256:600000$HzPmesGvH0vM2T95$47509dab3b46791caf87e11392b9e49b775205553fc1b89f94031feec475b588',1),
    (11,'Jaime123','Jaime Moreno','pbkdf2:sha256:600000$FiriclpWLLGtuo4I$40d386cb66014b689596b7b7688af7e048ab9ae2d754fbe12d31b3670b3739c5',1),
    (12,'jose','Jose Moreno','pbkdf2:sha256:600000$e5wIH5PlflxG8BTo$a8a91f9ad0ece7c6d3fd901397218bd6431cfd9a8e963fd0b0d4a23e031a9081',1),
    (13,'admin2','Administrador2','pbkdf2:sha256:600000$aaa$bbb',1),
    (14,'test_user_pub2','Test User','pbkdf2:sha256:600000$eJJculCY9sP7PRNq$83cc5c8b97dd03ee48b8d26311c4ed111a6f6260d2494687ec3eeb7abc771c34',1),
    (15,'test_http_3','Test HTTP 3','pbkdf2:sha256:600000$64iBT59DtqUsG4yf$b27132bb3c30c076ff80fd2abae1698366dec90442873ec6b63762ddc5b73586',1),
    (16,'test_http_4','Test HTTP 4','pbkdf2:sha256:600000$gG0AqSVVXFEAhAjD$e3ad9620a8de00760da12b3af91b5eeaf54bc692bd1cd6af71941fd9c2891a8c',1),
    (17,'test_ex_0','Test HTTP 0','pbkdf2:sha256:600000$dv1Q6vKnOfG5O40R$ef479364fab6d9536aa0eed6b19618f638d030e877b181339c4f19bf45ebd7d5',1),
    (18,'test_ex_1','Test HTTP 1','pbkdf2:sha256:600000$cYRM0xTZZkso9o9p$ab855fef138c416212c288ee90e5393ba4eba9a1c2d3fd2aa1de1d794483c30f',1),
    (19,'test_ex_2','Test HTTP 2','pbkdf2:sha256:600000$JanzY1PL62UrGWA1$2a3b6b52d00c2c487d5716588f932f68000a58d176b51b5c83ad12b0f54884d5',1),
    (20,'test_ex_3','Test HTTP 3','pbkdf2:sha256:600000$OwQPWRrDHvjFkzON$6821e7d41b4fde11cdaa143e508aa407900f238c6466aad77bc3768addf96e56',1),
    (21,'test_ex_4','Test HTTP 4','pbkdf2:sha256:600000$VrIpgUut6HhcXWiy$878343edac089434661d0abfeea5a09125ed01a36bd6cc08b1a8d04c98f517c8',1),
    (22,'test_ex_5','Test HTTP 5','pbkdf2:sha256:600000$K0y0jVjfl5pSPtbk$2ddbc66da8c7937df862fa756c92b05624c3e8ce7dab7bbb29fd9ec3d2d56c8f',1),
    (23,'test_ex_6','Test HTTP 6','pbkdf2:sha256:600000$AlaLOMd9Ipc89z74$3101b9fcc9429a5bffbb0ee482453515909942848f1b31f727ad371589c5334a',1),
    (24,'test_ex_7','Test HTTP 7','pbkdf2:sha256:600000$NjcOWJdi63fFLPZ0$fcca647d2a3288ddc8bf02d9f739b895a2012e4990c5a40eceb53438324ef7e9',1),
    (25,'test_ex_8','Test HTTP 8','pbkdf2:sha256:600000$aV5V18M4buklwSfr$8a02329f982ce123c7031ad9fcdf6f872183704eab055ec9f02a7dcc2de927d6',1),
    (26,'test_ex_9','Test HTTP 9','pbkdf2:sha256:600000$1OxcZQmaLcLY3YsU$379297b9a534f6b73b050a41ae25a6cc8852c22e9b2d0d212f0fc82c98114602',1),
    (27,'fonseca','camilo fonseca','pbkdf2:sha256:600000$WoNp56yEBhhI7TeX$f0066b77c1a08b172e25499091bb875c31fc9b0cef77328a2444c84761d04e9f',1),
    (28,'memleak_0','Test HTTP 0','pbkdf2:sha256:600000$Fh50bOaS5YDGCJ4p$92794d9d825bcd596ab44c78d6c7c4f1e72645c275980bc7adedd1519bd33865',1),
    (29,'memleak_1','Test HTTP 1','pbkdf2:sha256:600000$GZYyDAvya3PfyAsn$bc1a3f8648cf0a7677766de0609f96677dd3e6baae5d366a36b3db606372e9db',1),
    (30,'memleak_2','Test HTTP 2','pbkdf2:sha256:600000$KXJ9kb2pzfCgk92T$827576991eee053cdea78b485a40959f922d087740d3f4f7e02c442eb24fd989',1),
    (31,'memleak_3','Test HTTP 3','pbkdf2:sha256:600000$IoI3iv0LVcgu9Npc$14e9bdb27b1e3ae3888c59e67ce48d5c289fad7d4bdfa577861e6eb498688136',1),
    (32,'memleak_4','Test HTTP 4','pbkdf2:sha256:600000$x8RVYlk0IiUzWmal$4680f0ce2e04958e00006ccd04a50529d6d475309dde696350012482fa317a51',1),
    (33,'memleak_5','Test HTTP 5','pbkdf2:sha256:600000$ZZaA38qCzEbtzlag$fe5673c3344caef7615cb816fb8a25c6f5bd4c0a37c92a46b651932c83da130b',1),
    (34,'memleak_6','Test HTTP 6','pbkdf2:sha256:600000$OxdWbrCae30OpYsx$45b9cd72c02a07aee12769c54f024bc57b7520bd5c93451d4eb07b67e767e1cd',1),
    (35,'memleak_7','Test HTTP 7','pbkdf2:sha256:600000$oi90Fwpi4wkYd3NI$a9167923943835697d8f7d9d7313d7c0faebdee127066c48663cccf5374e9332',1),
    (36,'memleak_8','Test HTTP 8','pbkdf2:sha256:600000$4OBDP9nimHnc11Pf$40b44c7a87da45ba662d34494e857ba44cb9e01c322abd37c2c3a569d35cd9d4',1),
    (37,'memleak_9','Test HTTP 9','pbkdf2:sha256:600000$XtnLtLLzSWtYlyu8$c1371b81573fa96a8760fb7eafa39b56319c0ec7710e1ba7f65ff70eaa534ac7',1),
    (38,'memleak_10','Test HTTP 10','pbkdf2:sha256:600000$cxtmkSaDc0mNgRzR$006f6648a8539282af295974218c6c030eafc86660a1aa593130dbf86ddbca86',1),
    (39,'memleak_11','Test HTTP 11','pbkdf2:sha256:600000$p73IJjTAmDTQ2ipf$f27acff8c11198b5ff5c3bcfe782384995c1269762a02729cfc404803c899cfc',1),
    (40,'memleak_12','Test HTTP 12','pbkdf2:sha256:600000$WxhE9ej7WBEKQeTU$53230bd341fdf047c9a183ccfaeb3bf0c02fcfae728352e4e6292ee22fc283e9',1),
    (41,'memleak_13','Test HTTP 13','pbkdf2:sha256:600000$l7zMrLMQUJGFa4xl$41806a605962887f3ebf530ddd3703ec316b390713f15add5de4a33ff3161797',1),
    (42,'memleak_14','Test HTTP 14','pbkdf2:sha256:600000$CyC0cuLf3sgHhG7k$ac2168c0ad49662aa55de3fac6046c5e28230bebfa183532100fb64658fa7375',1),
    (43,'Gongora','Gongora Martinez','pbkdf2:sha256:600000$222L5GCZanQ2iaSR$4caca28e198381ce1093c2fbc642875676ea5dfa2d3f2c851578bba55352520b',1),
    (44,'Juanito','Juan Andres','pbkdf2:sha256:600000$6oy8sNzx3xVfLR0J$56ca45d573224c0d888e30adeae3bf13f904c907bf3f20221ec554684260d5ab',1),
    (45,'luz123','luz ramirez','pbkdf2:sha256:600000$qZUokttzyQh8SO2o$2becd0050a928739c880c48a903a6aadd5bdd01aad3d99f13d4235b4762441f5',1),
    (46,'luis','luis carlos','pbkdf2:sha256:600000$zip5KGR9ytK40kxU$b265af8ec73f550b0fe437d7bd9b78fe6f1ccfcebee2f87f5daf56f05797405d',1),
    (47,'user2222','22222','pbkdf2:sha256:600000$Awmb6GHVdDRvUz2a$5427bf080389ba6c06dab7955dde21f3dcc6c06403ef0073d7591d674c62eb40',1),
    (48,'hgh','sdfs','pbkdf2:sha256:600000$2PPKzH6JjwtGuIYo$b6a16dfbc1388275ad43a9580be3c211e5d1738a4d4d759cc3f8fa0fc18df15d',1),
    (49,'liz','liz diaz','pbkdf2:sha256:600000$7tSBDPrkyCzxKx3Q$2c8ce9281078968b692930a66a2be09c449c6080e223cd81ce4fb38a1db86564',1),
    (50,'luna','luna','pbkdf2:sha256:1000000$dofWfMlYqynG7XqL$9bc73ccdf88d1e6d3f8f673ff331561a1b03406524dc7bc51496c4a03255bf93',1),
]

ESTUDIANTES = [
    (1,'123455','74589745','Angel sifuentes','Ingenieria de sistemas','','925491523',1),
    (2,'465','9779879','Prueba','Ingenieria','Lima','987978456',1),
    (3,'USR12','00000000','Jose Moreno','Usuario Web','-','-',1),
    (4,'USR44','00000000','Juan Andres','Usuario Web','-','-',1),
    (5,'1234567','1029280551','Martin','Sistemas','cra 18','000000000',1),
    (6,'USR46','00000000','luis carlos','Usuario Web','-','-',1),
    (7,'USR49','00000000','liz diaz','Usuario Web','-','-',1),
]

LIBROS = [
    (1,'libro 1',50,4,4,'1000-01-01',2,1335,'si','logo.png',1),
    (2,'Javascript',69,1,1,'2021-05-08',2,1478,'Domina javascript','libro_20260413230926185491.jpg',1),
    (3,'python para todos',23,1,1,'2021-05-08',1,258,'anaconda','libro_20260413230932138176.jpg',1),
    (4,'ultima prueba',23,1,1,'2021-05-14',1,569,'','libro_20260413230938672184.jpg',1),
    (5,'cien años de soledad',16,1,1,'1968-01-01',2,100,'','libro_20260413230944240411.jpg',1),
    (6,'Don Quijote de la Mancha',14,5,4,'1605-01-01',7,863,'La obra cumbre de la literatura en español','libro_20260413230949017239.jpg',1),
    (7,'1984',8,6,5,'1949-01-01',8,328,'Novela distópica sobre un estado totalitario','libro_20260413230957400247.jpg',1),
    (8,'El Principito',18,7,6,'1943-01-01',9,96,'Cuento filosófico universal sobre la amistad y la vida','libro_20260413231012198263.jpg',1),
    (9,'Harry Potter y la Piedra Filosofal',10,8,6,'1997-01-01',10,309,'Inicio de la saga sobre el joven mago Harry Potter','libro_20260413231015830275.jpg',1),
    (10,'El Señor de los Anillos',6,9,7,'1954-01-01',10,1200,'Épica novela de fantasía sobre la lucha contra el mal','libro_20260413231018305492.jpg',1),
    (11,'Orgullo y Prejuicio',12,10,8,'1813-01-01',11,432,'Novela romántica sobre las costumbres de la Inglaterra del siglo XIX','libro_20260413231022121186.jpg',1),
    (12,'Crimen y Castigo',7,11,9,'1866-01-01',7,551,'Exploración psicológica de un joven criminal ruso','libro_20260413231026628408.jpg',1),
    (13,'El Gran Gatsby',6,12,10,'1925-01-01',12,208,'Crítica al sueño americano en los años 20','libro_20260413231030435629.jpg',1),
    (14,'Crónica de una Muerte Anunciada',8,4,11,'1981-01-01',6,152,'Relato sobre un asesinato anunciado en un pueblo colombiano','libro_20260413231033956741.jpg',1),
    (15,'Matar a un Ruiseñor',6,13,12,'1960-01-01',13,281,'Historia sobre la justicia racial en el sur de EE.UU.','libro_20260413231037243862.jpg',1),
    (16,'El Alquimista',12,14,13,'1988-01-01',14,197,'Novela filosófica sobre seguir los sueños','libro_20260413231040744550.jpg',1),
    (17,'Anna Karenina',4,15,8,'1878-01-01',7,964,'Trágica historia de amor en la Rusia imperial','libro_20260413231042939951.jpg',1),
    (18,'Brave New World',6,16,5,'1932-01-01',8,311,'Novela distópica sobre una sociedad futurista controlada','libro_20260413231046450817.jpg',1),
    (19,'Los Miserables',8,17,14,'1862-01-01',7,1232,'Epopeya social sobre la redención en la Francia del siglo XIX','libro_20260413231050072806.jpg',1),
    (20,'Fahrenheit 451',8,18,7,'1953-01-01',8,256,'Novela sobre una sociedad donde los libros son prohibidos','libro_20260413231054060996.jpg',1),
    (21,'El Nombre de la Rosa',6,19,15,'1980-01-01',15,544,'Novela de misterio ambientada en un monasterio medieval','libro_20260413231057548956.jpg',1),
    (22,'Sapiens',10,20,16,'2011-01-01',16,496,'Historia breve de la humanidad desde los orígenes','libro_20260413231106655397.jpg',1),
    (23,'El Hobbit',8,9,7,'1937-01-01',10,310,'Aventura de Bilbo Bolsón antes de El Señor de los Anillos','libro_20260413231120400172.jpg',1),
    (24,'Ficciones',6,21,17,'1944-01-01',6,224,'Cuentos fantásticos e intelectuales del maestro argentino','libro_20260413231126442525.jpg',1),
    (25,'La Sombra del Viento',8,22,13,'2001-01-01',17,565,'Misterio literario en la Barcelona de posguerra','libro_20260413231130536096.jpg',1),
    (26,'Pedro Páramo',6,23,18,'1955-01-01',6,124,'Novela fundamental del boom latinoamericano','logo.png',1),
    (27,'El Túnel',4,24,19,'1948-01-01',6,152,'Relato de obsesión y crimen de un pintor argentino','logo.png',1),
    (28,'Rayuela',6,25,4,'1963-01-01',6,635,'Novela experimental del boom latinoamericano','libro_20260413231144809207.jpg',1),
    (29,'La Casa de los Espíritus',8,26,20,'1982-01-01',6,433,'Saga familiar chilena con elementos de realismo mágico','libro_20260413231147962615.jpg',1),
    (30,'Ensayo sobre la Ceguera',6,27,4,'1995-01-01',6,342,'Novela sobre una epidemia de ceguera y sus consecuencias','libro_20260413231151596341.jpg',1),
    (31,'La Metamorfosis',8,28,17,'1915-01-01',7,112,'Relato absurdista sobre un hombre que se convierte en insecto','libro_20260413231156387828.jpg',1),
    (32,'El Retrato de Dorian Gray',6,29,14,'1890-01-01',7,272,'Novela sobre la belleza eterna y la corrupción moral','libro_20260413231208552829.jpg',1),
    (33,'Frankenstein',6,30,21,'1818-01-01',18,320,'La primera novela de ciencia ficción sobre un científico y su creación','libro_20260413231221479699.jpg',1),
    (34,'Drácula',4,31,22,'1897-01-01',19,448,'Novela gótica sobre el famoso vampiro del conde Drácula','libro_20260413231226770405.jpg',1),
    (35,'El Código Da Vinci',10,32,23,'2003-01-01',20,543,'Thriller de misterio sobre secretos religiosos y conspiraciones','libro_20260413231230028441.jpg',1),
    (36,'Comer, Rezar, Amar',6,33,24,'2006-01-01',21,352,'Viaje de autodescubrimiento por Italia, India e Indonesia','libro_20260413231233385506.jpg',1),
    (37,'El Mundo de Sofía',8,34,25,'1991-01-01',22,638,'Novela introductoria a la historia de la filosofía occidental','libro_20260413231240035485.jpg',1),
    (38,'Memorias de una Geisha',6,35,26,'1997-01-01',23,480,'Historia de una geisha en el Japón del siglo XX','libro_20260413231243545722.jpg',1),
    (39,'El Perfume',8,36,19,'1985-01-01',23,320,'Historia de un asesino obsesionado con los olores en la Francia del siglo XVIII','libro_20260413231249980747.jpg',1),
    (40,'Azul',4,37,17,'1888-01-01',24,192,'Obra fundacional del modernismo hispanoamericano','libro_20260414153247513645.jpg',1),
    (41,'La Vorágine',6,38,27,'1924-01-01',25,320,'Novela sobre la selva amazónica colombiana','libro_20260413231257985607.jpg',1),
    (42,'Canción de Hielo y Fuego',6,39,28,'1996-01-01',10,694,'Épica saga de fantasía medieval llena de intrigas políticas','libro_20260413231308894145.jpg',1),
    (43,'El Juego de Ender',8,40,12,'1985-01-01',8,352,'Novela de ciencia ficción sobre un niño entrenado para la guerra','libro_20260413231313332475.jpg',1),
    (44,'Dune',6,41,29,'1965-01-01',8,736,'Épica novela de ciencia ficción sobre política, religión y ecología','libro_20260413231316806098.jpg',1),
    (45,'Neuromante',4,42,7,'1984-01-01',8,320,'Novela fundacional del cyberpunk','libro_20260413231321138908.jpg',1),
    (46,'El Señor de las Moscas',6,43,17,'1954-01-01',6,256,'Novela sobre niños náufragos que crean una sociedad violenta','libro_20260413231325175032.jpg',1),
    (47,'Las Correcciones',4,44,6,'2001-01-01',26,576,'Retrato de una familia americana en crisis','libro_20260413231328851759.jpg',1),
    (48,'Beloved',4,45,12,'1987-01-01',6,336,'Novela sobre el trauma de la esclavitud en EE.UU.','libro_20260413231333051249.jpg',1),
    (49,'El Corazón de las Tinieblas',6,46,22,'1899-01-01',7,112,'Relato sobre la colonización del Congo africano','libro_20260413231336953878.jpg',1),
    (50,'Los Detectives Salvajes',6,47,10,'1998-01-01',6,609,'Novela sobre poetas jóvenes en el México de los 70','logo.png',1),
    (51,'2666',4,47,10,'2004-01-01',6,1119,'Obra póstuma de Bolaño sobre la violencia en la frontera México-EE.UU.','logo.png',1),
    (52,'El Otoño del Patriarca',6,4,3,'1975-01-01',6,317,'Novela sobre la dictadura y el poder en Latinoamérica','libro_20260413231405321892.jpg',1),
    (53,'Conversación en la Catedral',4,48,4,'1969-01-01',6,701,'Novela sobre la corrupción política en el Perú','libro_20260414145008733509.jpg',1),
    (54,'Los Cachorros',6,48,30,'1967-01-01',6,112,'Relato sobre la juventud y la masculinidad en Lima','libro_20260413231452740075.jpg',1),
    (55,'Cien Anios de Soledad',3,4,3,'1967-01-01',6,471,'Novela clasica de la literatura latinoamericana','logo.png',1),
    (56,'Cuentos de la Selva',4,49,31,'1918-01-01',9,180,'Colección de cuentos protagonizados por animales de la selva misionera','libro_20260414145032825330.jpg',1),
    (57,'Moby Dick',2,50,14,'1851-01-01',6,720,'La épica persecución de la ballena blanca por el capitán Ahab','libro_20260414145036364470.jpg',1),
    (58,'Hamlet',5,51,32,'1603-01-01',27,342,'Tragedia del príncipe de Dinamarca que busca vengar la muerte de su padre','libro_20260414145047855377.jpg',1),
    (59,'El Conde de Montecristo',3,52,17,'1844-01-01',6,1276,'Historia de traición, prisión y venganza de Edmond Dantés','libro_20260414145055094535.jpg',1),
    (60,'El diario de ana franck',5,53,8,'1945-01-01',6,200,'','20260414144056_url.jpg',1),
    (61,'La Divina Comedia',9,54,17,'1320-01-01',7,798,'Poema épico medieval que narra el viaje del autor por el Infierno, el Purgatorio y el Paraíso','libro_20260414153301500096.jpg',1),
    (62,'Guerra y Paz',6,15,8,'1869-01-01',7,1225,'Monumental novela que retrata la sociedad rusa durante las guerras napoleónicas','libro_20260414145134693322.jpg',1),
    (63,'Lolita',9,55,10,'1955-01-01',6,384,'Polémica novela narrada por un hombre obsesionado con una niña de doce años','libro_20260414145139165649.jpg',1),
    (64,'El Extranjero',12,56,17,'1942-01-01',28,159,'Novela existencialista que explora la alienación y la absurdidad de la condición humana','libro_20260414145143614836.jpg',1),
    (65,'Los Hermanos Karamázov',6,11,9,'1880-01-01',7,1000,'Obra maestra que aborda el libre albedrío, la moralidad y la existencia de Dios','libro_20260414145147534532.jpg',1),
    (66,'Ulises',6,57,15,'1922-01-01',29,933,'Novela modernista que narra un día en la vida de Leopold Bloom en Dublín','libro_20260414145152398924.jpg',1),
    (67,'Cumbres Borrascosas',12,58,14,'1847-01-01',30,349,'Historia de pasión destructiva entre Heathcliff y Catherine en los páramos ingleses','libro_20260414145156515612.jpg',1),
    (68,'El Retrato de la Artista Adolescente',9,57,17,'1916-01-01',29,318,'Novela de formación autobiográfica sobre el despertar artístico de Stephen Dedalus','logo.png',1),
    (69,'Nausea',9,59,17,'1938-01-01',28,253,'Diario filosófico de un historiador que experimenta la revelación de la existencia absurda','libro_20260414153307820539.jpg',1),
    (70,'Invisible Man',6,60,33,'1952-01-01',6,581,'Novela sobre la invisibilidad social de un hombre afroamericano en Estados Unidos','libro_20260414145242044571.jpg',1),
    (71,'El Amor en los Tiempos del Cólera',4,4,3,'1985-01-01',6,406,'Historia de amor que se desarrolla a lo largo de más de cincuenta años en el Caribe','libro_20260414153312070246.jpg',1),
    (72,'La Insoportable Levedad del Ser',3,61,34,'1984-01-01',6,314,'Novela filosófica sobre el amor, la política y la identidad en la Praga de los años 60','libro_20260414153354671066.jpg',1),
    (73,'El Proceso',3,28,17,'1925-01-01',6,263,'Novela sobre un hombre arrestado y procesado por una causa que jamás le es revelada','libro_20260414153358384565.jpg',1),
    (74,'Madame Bovary',4,62,14,'1857-01-01',7,368,'Retrato de una mujer insatisfecha que busca escapar de su vida provincial a través de romances','libro_20260414153402074655.jpg',1),
    (75,'El Jugador',3,11,17,'1867-01-01',7,192,'Novela que narra la psicología obsesiva de un joven adicto al juego en Europa','libro_20260414153406295812.jpg',1),
    (76,'Siddhartha',5,63,17,'1922-01-01',28,152,'Viaje espiritual de un joven indio en busca de la iluminación y el sentido de la vida','libro_20260414153409540106.jpg',1),
    (77,'La Tregua',4,64,4,'1960-01-01',6,215,'Diario íntimo de un viudo uruguayo que encuentra el amor inesperado antes de jubilarse','libro_20260414153413104916.jpg',1),
    (78,'El Llano en Llamas',4,23,36,'1953-01-01',32,184,'Cuentos que retratan la vida campesina y la violencia en el México rural posrevolucionario','libro_20260414161329637990.jpg',1),
    (79,'Poeta en Nueva York',3,65,9,'1940-01-01',33,256,'Poemario surrealista inspirado en la estancia del autor en Nueva York a finales de los años 20','libro_20260414153420934993.jpg',1),
    (80,'La Ciudad y los Perros',4,48,4,'1963-01-01',6,412,'Novela sobre la violencia y la corrupción en un colegio militar de Lima','libro_20260414160722771714.jpg',1),
    (81,'Canto General',3,66,31,'1950-01-01',33,343,'Obra épica que recorre la historia y la naturaleza de América Latina en verso','libro_20260414160727430389.jpg',1),
    (82,'Los Pasos Perdidos',3,67,9,'1953-01-01',6,302,'Viaje de un músico hacia las profundidades de la selva latinoamericana en busca de sus raíces','libro_20260414160731093357.jpg',1),
    (83,'El Beso de la Mujer Araña',4,68,19,'1976-01-01',6,290,'Novela contada en diálogos entre dos presos argentinos de personalidades opuestas','logo.png',1),
    (84,'Sobre Héroes y Tumbas',2,24,19,'1961-01-01',6,542,'Novela que entrelaza el amor trágico con la historia y la decadencia de Argentina','libro_20260414160742271170.jpg',1),
    (85,'Terra Nostra',2,69,19,'1975-01-01',32,800,'Ambiciosa novela que recorre cinco siglos de historia hispanoamericana y europea','libro_20260414160747348182.jpg',1),
    (86,'El Astillero',3,70,4,'1961-01-01',6,198,'Novela sobre un hombre que dirige un astillero en ruinas como metáfora del fracaso existencial','libro_20260414160754398939.jpg',1),
    (87,'La Hojarasca',3,4,3,'1955-01-01',6,148,'Primera novela de García Márquez que introduce el mítico pueblo de Macondo','libro_20260414162419170582.jpg',1),
    (88,'El Coronel No Tiene Quien le Escriba',4,4,3,'1961-01-01',6,102,'Historia de un veterano que espera durante años una pensión que nunca llega','libro_20260414163100281418.jpg',1),
    (89,'Aura',5,69,38,'1962-01-01',32,63,'Novela corta gótica sobre un joven historiador atrapado en una casa misteriosa en Ciudad de México','libro_20260414163106774117.jpg',1),
    (90,'Los Ríos Profundos',3,71,31,'1958-01-01',34,235,'Novela de formación ambientada en los Andes que explora la identidad mestiza del Perú','libro_20260414162449062606.jpg',1),
    (91,'El Obsceno Pájaro de la Noche',2,72,19,'1970-01-01',35,543,'Novela barroca y perturbadora sobre la decadencia de la aristocracia chilena','libro_20260414162451553041.jpg',1),
    (92,'Paradiso',2,73,9,'1966-01-01',36,617,'Novela poética y autobiográfica considerada la obra cumbre de las letras cubanas','libro_20260414162455899494.jpg',1),
    (93,'El Recurso del Método',3,67,39,'1974-01-01',6,349,'Sátira sobre un dictador latinoamericano ilustrado que alterna entre Europa y su país','libro_20260414163116186198.jpg',1),
    (94,'Respiración Artificial',3,74,40,'1980-01-01',37,211,'Novela epistolar que reflexiona sobre la historia argentina y sus zonas oscuras','libro_20260414162520814273.jpg',1),
    (95,'La Región Más Transparente',2,69,36,'1958-01-01',32,465,'Fresco de la sociedad mexicana posrevolucionaria en la Ciudad de México de los años 50','libro_20260414162524568251.jpg',1),
    (96,'Tres Tristes Tigres',2,75,19,'1967-01-01',36,451,'Novela experimental que recrea la vida nocturna de La Habana antes de la Revolución','libro_20260414162528638150.jpg',1),
    (97,'La vegetariana',5,76,41,'2007-01-01',38,183,'Historia inquietante sobre identidad y rebeldía.','libro_20260414163125403699.jpg',1),
    (98,'El hombre que plantaba árboles',5,77,42,'1953-01-01',39,64,'Relato sobre la perseverancia y la naturaleza.','libro_20260414163127824905.jpg',1),
    (99,'La elegancia del erizo',5,78,19,'2006-01-01',38,368,'Reflexión filosófica sobre la vida cotidiana.','libro_20260414163130420493.jpg',1),
    (100,'El mapa y el territorio',5,79,10,'2010-01-01',38,368,'Crítica a la sociedad contemporánea.','libro_20260414163134275540.jpg',1),
    (101,'La casa de hojas',5,80,43,'2000-01-01',38,736,'Historia experimental de terror psicológico.','libro_20260414163138628156.jpg',1),
    (102,'El libro de los abrazos',5,81,39,'1989-01-01',40,272,'Textos breves sobre la vida y la sociedad.','libro_20260414163852347925.jpg',1),
    (103,'El Maestro y Margarita',2,82,44,'1967-01-01',6,480,'Satira sovietica con elementos fantasticos y filosoficos','libro_20260414163855914475.jpg',1),
    (104,"La Vie mode d'emploi",1,83,46,'1978-01-01',41,581,'Novela-puzzle sobre los habitantes de un edificio parisino','logo.png',1),
    (105,'El Aleph y Otros Cuentos',2,21,31,'1949-01-01',31,203,'Cuentos que exploran el infinito, el tiempo y la identidad','logo.png',1),
    (106,'Steppenwolf',2,63,47,'1927-01-01',42,237,'Novela de alienacion y dualidad del ser humano moderno','libro_20260414164250555801.jpg',1),
    (107,'Pale Fire',1,55,48,'1962-01-01',6,315,'Novela experimental estructurada como un poema con comentarios','libro_20260414163934815036.jpg',1),
    (108,'The Master and Emissary',1,84,49,'2009-01-01',43,534,'Estudio sobre los hemisferios cerebrales y la cultura occidental','libro_20260414163942569821.jpg',1),
    (109,'Godel, Escher, Bach',2,85,50,'1979-01-01',44,777,'Exploracion de la conciencia, la autorreferencia y los sistemas formales','libro_20260414163946044808.jpg',1),
    (110,'El Nombre del Mundo es Bosque',3,86,7,'1972-01-01',8,157,'Novela corta sobre colonialismo y resistencia en un mundo arboreo','libro_20260414163949593618.jpg',1),
    (111,'La Bruja de Portobello',2,14,13,'2006-01-01',45,288,'Historia de una mujer que busca su identidad a traves de rituales','libro_20260414163955649980.jpg',1),
    (112,'El Informe de Brodie',2,21,35,'1970-01-01',31,156,'Cuentos de tribus primitivas y destinos inexorables','libro_20260414175250639587.jpg',1),
    (113,'Malone Muere',1,87,51,'1951-01-01',46,148,'Monólogo de un anciano postrado que espera la muerte narrando historias','libro_20260414175256226696.jpg',1),
    (114,'Las Ciudades Invisibles',3,88,52,'1972-01-01',47,165,'Marco Polo describe ciudades imaginarias al emperador Kublai Kan','libro_20260414175259749778.jpg',1),
    (115,'El Juego de los Abalorios',1,63,53,'1943-01-01',42,558,'Utopia intelectual sobre un juego que sintetiza todas las artes y ciencias','logo.png',1),
    (116,'La Broma',2,61,54,'1967-01-01',6,335,'Novela sobre el absurdo del totalitarismo checoslovaco y la memoria','libro_20260414175306121650.jpg',1),
    (117,'Nieve',2,89,55,'2002-01-01',48,479,'Poeta turco atrapado en una ciudad nevada entre islam y modernidad','libro_20260414175309437829.jpg',1),
    (118,'La Montaña Magica',1,90,47,'1924-01-01',42,720,'Joven en sanatorio suizo dialoga sobre vida, muerte y Europa moderna','libro_20260414175313306496.jpg',1),
    (119,'El Libro de los Seres Imaginarios',3,21,56,'1969-01-01',49,256,'Bestiario de criaturas fantásticas de mitologias del mundo entero','libro_20260414175324610728.jpg',1),
    (120,'Choque de Civilizaciones',1,91,57,'1996-01-01',50,368,'Teoria sobre conflictos futuros basados en identidades culturales','libro_20260414175344196066.jpg',1),
]

PRESTAMOS = [
    (1,1,1,'2021-05-11','2021-05-11',5,'',0),
    (2,1,2,'2021-05-11','2021-05-11',15,'',0),
    (3,1,3,'2026-04-07','2026-04-08',2,'Tiene la pasta doblada',0),
    (4,3,6,'2026-04-01','2026-04-19',1,'',0),
    (5,3,8,'2026-04-01','2026-04-28',1,'',0),
    (6,3,2,'2026-04-09','2026-04-20',1,'',0),
    (7,3,36,'2026-04-09','2026-04-19',1,'',0),
    (8,3,9,'2026-04-09','2026-04-19',1,'',0),
    (9,3,17,'2026-04-11','2026-04-21',1,'',0),
    (10,3,47,'2026-04-11','2026-04-21',1,'',0),
    (11,3,6,'2026-04-11','2026-04-21',1,'',3),
    (12,3,7,'2026-04-11','2026-04-21',1,'',3),
    (13,3,1,'2026-04-14','2026-04-24',2,'',0),
    (14,4,6,'2026-04-14','2026-04-24',1,'',1),
    (15,6,1,'2026-04-18','2026-04-28',1,'',2),
    (16,7,1,'2026-04-18','2026-04-28',1,'',2),
]

DETALLE_PERMISOS = [
    (5,2,1),(6,2,2),(7,2,3),(8,2,5),(9,2,8),(30,2,9),
    (31,4,1),(32,4,2),(33,4,3),(34,4,4),(35,4,5),(36,4,6),(37,4,7),(38,4,8),(39,4,9),
    (40,3,1),(41,3,2),(42,3,3),(43,3,4),(44,3,5),(45,3,7),
    (46,5,1),(47,5,2),(48,5,3),(49,5,7),
    (54,6,1),(55,6,2),(56,6,3),(57,6,6),(58,6,9),
    (59,8,1),(60,8,2),(61,8,3),(62,8,7),(63,8,9),
    (64,9,1),(65,9,2),(66,9,3),(67,9,7),(68,9,9),
    (69,10,1),(70,10,2),(71,10,3),(72,10,7),(73,10,9),
    (74,11,1),(75,11,2),(76,11,3),(77,11,7),(78,11,9),
    (79,12,1),(80,12,2),(81,12,3),(82,12,7),(83,12,9),
    (84,14,1),(85,14,2),(86,14,3),(87,14,7),(88,14,9),
    (89,15,1),(90,15,2),(91,15,3),(92,15,7),(93,15,9),
    (94,16,1),(95,16,2),(96,16,3),(97,16,7),(98,16,9),
    (99,17,1),(100,17,2),(101,17,3),(102,17,7),(103,17,9),
    (104,18,1),(105,18,2),(106,18,3),(107,18,7),(108,18,9),
    (109,19,1),(110,19,2),(111,19,3),(112,19,7),(113,19,9),
    (114,20,1),(115,20,2),(116,20,3),(117,20,7),(118,20,9),
    (119,21,1),(120,21,2),(121,21,3),(122,21,7),(123,21,9),
    (124,22,1),(125,22,2),(126,22,3),(127,22,7),(128,22,9),
    (129,23,1),(130,23,2),(131,23,3),(132,23,7),(133,23,9),
    (134,24,1),(135,24,2),(136,24,3),(137,24,7),(138,24,9),
    (139,25,1),(140,25,2),(141,25,3),(142,25,7),(143,25,9),
    (144,26,1),(145,26,2),(146,26,3),(147,26,7),(148,26,9),
    (149,27,1),(150,27,2),(151,27,3),(152,27,7),(153,27,9),
    (154,28,1),(155,28,2),(156,28,3),(157,28,7),(158,28,9),
    (159,29,1),(160,29,2),(161,29,3),(162,29,7),(163,29,9),
    (164,30,1),(165,30,2),(166,30,3),(167,30,7),(168,30,9),
    (169,31,1),(170,31,2),(171,31,3),(172,31,7),(173,31,9),
    (174,32,1),(175,32,2),(176,32,3),(177,32,7),(178,32,9),
    (179,33,1),(180,33,2),(181,33,3),(182,33,7),(183,33,9),
    (184,34,1),(185,34,2),(186,34,3),(187,34,7),(188,34,9),
    (189,35,1),(190,35,2),(191,35,3),(192,35,7),(193,35,9),
    (194,36,1),(195,36,2),(196,36,3),(197,36,7),(198,36,9),
    (199,37,1),(200,37,2),(201,37,3),(202,37,7),(203,37,9),
    (204,38,1),(205,38,2),(206,38,3),(207,38,7),(208,38,9),
    (209,39,1),(210,39,2),(211,39,3),(212,39,7),(213,39,9),
    (214,40,1),(215,40,2),(216,40,3),(217,40,7),(218,40,9),
    (219,41,1),(220,41,2),(221,41,3),(222,41,7),(223,41,9),
    (224,42,1),(225,42,2),(226,42,3),(227,42,7),(228,42,9),
    (229,43,1),(230,43,2),(231,43,3),(232,43,7),(233,43,9),
    (234,44,1),(235,44,2),(236,44,3),(237,44,7),(238,44,9),
    (239,45,1),(240,45,2),(241,45,3),(242,45,7),(243,45,9),
    (244,46,1),(245,46,2),(246,46,3),(247,46,7),(248,46,9),
    (249,47,1),(250,47,2),(251,47,3),(252,47,7),(253,47,9),
    (254,48,1),(255,48,2),(256,48,3),(257,48,7),(258,48,9),
    (259,49,1),(260,49,2),(261,49,3),(262,49,7),(263,49,9),
    (264,50,1),(265,50,2),(266,50,3),(267,50,7),(268,50,9),
]


def insertar_con_id(cur, tabla, columnas, filas):
    """Inserta filas preservando los IDs originales y actualiza el SERIAL."""
    col_str = ", ".join(columnas)
    placeholders = ", ".join(["%s"] * len(columnas))
    sql = f"INSERT INTO {tabla} ({col_str}) VALUES ({placeholders})"
    cur.executemany(sql, filas)
    # Actualizar la secuencia al máximo ID insertado
    cur.execute(f"SELECT setval(pg_get_serial_sequence('{tabla}', 'id'), MAX(id)) FROM {tabla}")


def main():
    print("\n📚 CARGA DE BASE DE DATOS BIBLIOTECA → POSTGRESQL")
    print("=" * 55)

    try:
        conn = conectar()
        conn.autocommit = False
        cur = conn.cursor()
        print("✅ Conectado a PostgreSQL")

        # Crear esquema
        print("\n🔧 Creando tablas...")
        cur.execute(SCHEMA_SQL)
        conn.commit()
        print("✅ Tablas creadas")

        # Cargar datos en orden (respetando foreign keys)
        print("\n📥 Cargando datos...")

        insertar_con_id(cur, 'autor', ['id','autor','imagen','estado'], AUTORES)
        print(f"  ✅ Autores: {len(AUTORES)}")

        insertar_con_id(cur, 'configuracion', ['id','nombre','telefono','direccion','correo','foto'], CONFIGURACION)
        print(f"  ✅ Configuración: {len(CONFIGURACION)}")

        insertar_con_id(cur, 'editorial', ['id','editorial','estado'], EDITORIALES)
        print(f"  ✅ Editoriales: {len(EDITORIALES)}")

        insertar_con_id(cur, 'materia', ['id','materia','estado'], MATERIAS)
        print(f"  ✅ Materias: {len(MATERIAS)}")

        insertar_con_id(cur, 'permisos', ['id','nombre','tipo'], PERMISOS)
        print(f"  ✅ Permisos: {len(PERMISOS)}")

        insertar_con_id(cur, 'usuarios', ['id','usuario','nombre','clave','estado'], USUARIOS)
        cur.execute("UPDATE usuarios SET rol = 'administrador' WHERE id = 1")
        cur.execute("UPDATE usuarios SET rol = 'administrador' WHERE usuario = 'angel'")
        print(f"  ✅ Usuarios: {len(USUARIOS)}")

        insertar_con_id(cur, 'estudiante', ['id','codigo','dni','nombre','carrera','direccion','telefono','estado'], ESTUDIANTES)
        print(f"  ✅ Estudiantes: {len(ESTUDIANTES)}")

        insertar_con_id(cur, 'libro', ['id','titulo','cantidad','id_autor','id_editorial','anio_edicion','id_materia','num_pagina','descripcion','imagen','estado'], LIBROS)
        print(f"  ✅ Libros: {len(LIBROS)}")

        insertar_con_id(cur, 'detalle_permisos', ['id','id_usuario','id_permiso'], DETALLE_PERMISOS)
        print(f"  ✅ Detalle permisos: {len(DETALLE_PERMISOS)}")

        insertar_con_id(cur, 'prestamo', ['id','id_estudiante','id_libro','fecha_prestamo','fecha_devolucion','cantidad','observacion','estado'], PRESTAMOS)
        print(f"  ✅ Préstamos: {len(PRESTAMOS)}")

        conn.commit()
        print("\n✅ TODOS LOS DATOS CARGADOS EXITOSAMENTE")

        # Verificación final
        print("\n📊 Verificación:")
        for tabla in ['autor','editorial','materia','permisos','usuarios','estudiante','libro','prestamo','detalle_permisos','configuracion']:
            cur.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = cur.fetchone()[0]
            print(f"  • {tabla}: {count} registros")

        cur.close()
        conn.close()
        print("\n🎉 BASE DE DATOS LISTA PARA USAR")
        print("=" * 55)
        print("   Usuario admin  → admin / (contraseña original)")
        print("=" * 55)
        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    ok = main()
    sys.exit(0 if ok else 1)
