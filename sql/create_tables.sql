CREATE DATABASE digital_library;
use digital_library;

CREATE TABLE authors(
	author_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL
);

CREATE TABLE genres(
	genre_id INT PRIMARY KEY AUTO_INCREMENT,
    genre VARCHAR(100) NOT NULL,
    genre_pt VARCHAR(100) NOT NULL
);

CREATE TABLE books(
	book_id INT PRIMARY KEY AUTO_INCREMENT,
    book_name VARCHAR(200) NOT NULL, 
    org_lang VARCHAR(30) NOT NULL,
    year_published INT NOT NULL,
    sales DECIMAL(10, 2) NOT NULL,
    author_id INT NOT NULL,
    genre_id INT NOT NULL,
	FOREIGN KEY (author_id) REFERENCES authors(author_id),
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
);

CREATE TABLE coments(
	coment_id INT PRIMARY KEY AUTO_INCREMENT,
    book_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    coment TEXT NOT NULL,
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);