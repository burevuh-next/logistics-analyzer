# Makefile
.PHONY: help setup run clean

help:
	@echo "Доступные команды:"
	@echo "  make setup    - Настройка окружения"
	@echo "  make run      - Запуск анализатора"
	@echo "  make notebook - Запуск Jupyter notebook"
	@echo "  make clean    - Очистка временных файлов"

setup:
	conda env create -f environment.yml
	conda activate logistics

run:
	python scripts/analyze.py

notebook:
	jupyter notebook notebooks/01_exploration.ipynb

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -f data/kpi_report.txt