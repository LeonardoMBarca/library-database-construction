CREATE TABLE authors(
	author_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE genres(
	genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
    genre TEXT NOT NULL,
    genre_pt TEXT NOT NULL
);

CREATE TABLE books(
	book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_name TEXT NOT NULL, 
    org_lang TEXT NOT NULL,
    year_published INTEGER NOT NULL,
    sales REAL NOT NULL,
    author_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
	FOREIGN KEY (author_id) REFERENCES authors(author_id),
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
);

CREATE TABLE comments(
	coment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    coment TEXT NOT NULL,
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);