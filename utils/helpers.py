import yaml
import json
import re
from typing import Any, Dict


class ConfigReader:
    
    @staticmethod
    def read_yaml(file_path: str) -> Dict[str, Any]:
        """קריאת YAML"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    
    @staticmethod
    def read_json(file_path: str) -> Dict[str, Any]:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)


class PriceParser:
    
    @staticmethod
    def extract_price(price_text: str) -> float:
        """
        מחלץ מחיר מטקסט
        דוגמאות: "$123.45" -> 123.45, "US $1,234.56" -> 1234.56
        """
        # הסרת כל התווים חוץ ממספרים ונקודה
        clean_text = re.sub(r'[^\d.]', '', price_text)
        
        try:
            return float(clean_text)
        except ValueError:
            return 0.0
    
    @staticmethod
    def is_price_valid(price: float, max_price: float) -> bool:
        """בדיקה אם מחיר תקין"""
        return 0 < price <= max_price


class Logger:
    """לוגר פשוט"""
    
    @staticmethod
    def info(message: str):
        print(f"[INFO] {message}")
    
    @staticmethod
    def error(message: str):
        print(f"[ERROR] {message}")
    
    @staticmethod
    def debug(message: str):
        print(f"[DEBUG] {message}")
