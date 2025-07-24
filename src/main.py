from sql_generator import SqlGenerator
from sql_executor import SqlExecutor
from logger import *

logger_console = ConsoleLogger()
logger_file = FileLogger()
logger_file.clear_logs()

teste = SqlGenerator("/home/leona/workspace/personal-github/library-database-construction/data/livros.csv", "https://raw.githubusercontent.com/guilhermeonrails/datas-csv/refs/heads/main/comentarios.json", logger_console, logger_file)
test = teste.execute()

teste_1 = SqlExecutor(logger_console, logger_file)
test_1 = teste_1.execute()