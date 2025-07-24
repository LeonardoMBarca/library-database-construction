import os
from abc import ABC, abstractmethod
from datetime import datetime

class AbstractLogger(ABC):
    @abstractmethod
    def log_info(self, msg: str):
        pass

    @abstractmethod
    def log_error(self, msg: str):
        pass

class ConsoleLogger(AbstractLogger):
    def log_info(self, msg: str):
        print(f"[LOG] [INFO]: {msg}")
    
    def log_error(self, msg: str):
        print(f"[LOG] [ERROR]: {msg}")

class FileLogger(AbstractLogger):
    def __init__(self, file=f"{os.path.dirname(os.path.abspath(__file__))}/logs.txt"):
        self.file = file
    
    def log_info(self, msg: str):
        with open(self.file, "a") as f:
            f.write(f"[LOG] [INFO] - [{datetime.now()}]: {msg}")

    def log_error(self, msg: str):
        with open(self.file, "a") as f:
            f.write(f"[LOG] [ERROR] - [{datetime.now()}]: {msg}")

    def clear_logs(self):
        with open(self.file, "w") as f:
            f.write("")