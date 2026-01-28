import json
import os
from pathlib import Path

class ScoreManager:
    """Управление сохранением рекордов."""
    
    def __init__(self, filepath: str = "data/scores.json"):
        self.filepath = filepath
        self.high_score: int = 0
        self._ensure_data_dir()
        
    def _ensure_data_dir(self) -> None:
        """Создание папки data при необходимости."""
        Path("data").mkdir(exist_ok=True)
        
    def load_high_score(self) -> int:
        """Загрузка рекорда из файла."""
        try:
            if os.path.exists(self.filepath):
                with open(self.filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.high_score = data.get("high_score", 0)
        except (json.JSONDecodeError, IOError):
            self.high_score = 0
        return self.high_score
    
    def save_high_score(self) -> None:
        """Сохранение рекорда в файл."""
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump({"high_score": self.high_score}, f)
        except IOError:
            pass  # Игнорируем ошибки сохранения для учебного проекта
