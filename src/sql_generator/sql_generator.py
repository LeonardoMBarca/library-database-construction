import os
import pandas as pd
from logger import *
from deep_translator import GoogleTranslator

class SqlGenerator:
    def __init__(self, csv_path: str, api_key: str, logger_console, logger_file):
        self.csv_path = csv_path
        self.api_key = api_key
        self.logger_console = logger_console
        self.logger_file = logger_file
    
    def csv_processing(self):
        try:
            df_books = pd.read_csv(self.csv_path)
            self.logger_console.log_info(f"[CSV] Books DataFrame:\n{df_books.head(5)}\n")
            self.logger_file.log_info(f"[CSV] Books DataFrame:\n{df_books.head(5)}\n")

            df_books.rename(columns={
                    'Book': 'book',
                    'Author(s)': 'author',
                    'Original language': 'org_lang',
                    'First published': 'year_published',
                    'Approximate sales in millions': 'sales',
                    'Genre': 'genre'
            },
            inplace=True)

            df_books["genre"] = df_books["genre"].fillna("Unknown")

            sql_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "sql", "inserts")

            self.logger_console.log_info("[CSV] Authors step started\n")
            self.logger_file.log_info("[CSV] Authors step started\n")
            authors = pd.DataFrame(df_books["author"].unique(), columns=["author"])

            with open(os.path.join(sql_dir, "authors.sql"), "w", encoding="utf-8") as f:
                for _, row in authors.iterrows():
                    name = row["author"].replace("'", "''")
                    f.write(f"INSERT INTO authors (name) VALUES ('{name}');\n")
            self.logger_console.log_info("[CSV] Authors step ended\n")
            self.logger_file.log_info("[CSV] Authors step ended\n")

            self.logger_console.log_info("[CSV] Genre step started\n")
            self.logger_file.log_info("[CSV] Genre step started\n")
            genres = pd.DataFrame(df_books["genre"].unique(), columns=["genre"])
            genres["genre_pt"] = genres["genre"].apply(
                lambda x: GoogleTranslator(source="auto", target="pt").translate(x)
            )

            # Store original genre values before lowercasing
            genres["original_genre"] = genres["genre"]
            
            genres["genre_pt"] = genres["genre_pt"].replace("Novella", "Novela")
            genres["genre_pt"] = genres["genre_pt"].str.lower()

            with open(os.path.join(sql_dir, "genres.sql"), "w", encoding="utf-8") as f:
                for _, row in genres.iterrows():
                    genre = row["genre"].replace("'", "''")
                    genre_pt = row["genre_pt"].replace("'", "''")
                    f.write(f"INSERT INTO genres (name, name_pt) VALUES ('{genre}', '{genre_pt}');\n")
            self.logger_console.log_info("[CSV] Genre step ended\n")
            self.logger_file.log_info("[CSV] Genre step ended\n")

            self.logger_console.log_info("[CSV] Books step started\n")
            self.logger_file.log_info("[CSV] Books step started\n")
            authors["author_id"] = authors.index + 1
            genres["genre_id"] = genres.index + 1
            df_books["book_id"] = df_books.index + 1

            df_books = df_books.merge(authors, on="author", how="left")

            df_books = df_books.merge(genres[["original_genre", "genre_id"]], 
                                     left_on="genre", 
                                     right_on="original_genre", 
                                     how="left")

            df_books.drop("original_genre", axis=1, inplace=True, errors="ignore")
            
            with open(os.path.join(sql_dir, "books.sql"), "w", encoding="utf-8") as f:
                for _, row in df_books.iterrows():
                    book_name = row["book"].replace("'", "''")
                    org_lang = row["org_lang"].replace("'", "''")
                    year_published = int(row["year_published"])
                    sales = float(row["sales"])
                    author_id = int(row["author_id"])
                    genre_id = int(row["genre_id"])
                    sql = (f"INSERT INTO books (book_name, org_lang, year_published, sales, author_id, genre_id) "
                            f"VALUES ('{book_name}', '{org_lang}', '{year_published}', '{sales:.2f}', '{author_id}', '{genre_id}');\n")
                    f.write(sql)
            self.logger_console.log_info("[CSV] Books step ended\n")
            self.logger_file.log_info("[CSV] Books step ended\n")

            self.logger_console.log_error("[CSV] CSV Books successfully saved\n")
            self.logger_file.log_error("[CSV] CSV Books successfully saved\n")

            return df_books

        except Exception as e:
            self.logger_console.log_error(f"[CSV] {e}\n")
            self.logger_file.log_error(f"[CSV] {e}\n")
        
    def api_data_processing(self, df_books):
        def format_value(value):
            if pd.isna(value):
                return "NULL"
            elif isinstance(value, str):
                value = value.replace("'", "''")
                return f"'{value}'"
            else:
                return str(value)
            
        try:
            df_coments = pd.read_json(self.api_key)
            self.logger_console.log_info(f"[API] Coments DataFrame:\n{df_coments.head(5)}\n")
            self.logger_file.log_info(f"[API] Coments DataFrame:\n{df_coments.head(5)}\n")

            df_coments.rename(columns={
                'livro': 'book',
                'nome': 'name', 
                'sobrenome': 'last_name', 
                'comentario': 'coment'
                },
                inplace=True)

            sql_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "sql", "inserts")

            df_coments = df_coments.merge(df_books[["book"]].reset_index().rename(columns={"index": "book_id"}), on="book", how="left")

            df_coments["book_id"] += 1

            self.logger_console.log_info("[API] Coments step started\n")
            self.logger_file.log_info("[API] Coments step started\n")
            with open(os.path.join(sql_dir, "coments.sql"), "w", encoding="utf-8") as f:
                for _, row in df_coments.iterrows():
                    values = (
                        format_value(row["book_id"]),
                        format_value(row["name"]),
                        format_value(row["last_name"]),
                        format_value(row["coment"])
                    )
                    sql = f"INSERT INTO coments (book_id, name, last_name, coment) VALUES ({', '.join(values)});\n"
                    f.write(sql)
            self.logger_console.log_info("[API] Coments step ended\n")
            self.logger_file.log_info("[API] Coments step ended\n")

            self.logger_console.log_info("API Coments successfully saved\n")
            self.logger_file.log_info("API Coments successfully saved\n")

        except Exception as e:
            step1 = self.logger_console.log_error(f"[API] {e}\n")
            if step1:
                self.logger_file.log_error(f"[API] {e}\n")

    def execute(self):
        books = self.csv_processing()
        coments = self.api_data_processing(books)