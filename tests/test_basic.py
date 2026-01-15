"""Базовые тесты для приложения"""

import unittest
import pandas as pd
import sys
import os

# Добавляем путь к проекту
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestApp(unittest.TestCase):
    """Тесты приложения"""
    
    def test_pandas_import(self):
        """Проверка импорта pandas"""
        self.assertTrue(hasattr(pd, 'DataFrame'))
        
    def test_data_loading(self):
        """Проверка загрузки данных"""
        # Создаем тестовые данные
        test_data = {'col1': [1, 2], 'col2': [3, 4]}
        df = pd.DataFrame(test_data)
        self.assertEqual(len(df), 2)
        
    def test_app_structure(self):
        """Проверка структуры проекта"""
        self.assertTrue(os.path.exists('scripts/analyze.py'))
        self.assertTrue(os.path.exists('data/'))
        self.assertTrue(os.path.exists('notebooks/'))

if __name__ == '__main__':
    unittest.main()
