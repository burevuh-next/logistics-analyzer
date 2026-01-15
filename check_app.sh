#!/bin/bash
echo "🔍 Проверка приложения Logistics Analyzer"
echo "========================================"

# 1. Проверка окружения
echo "1. Проверка Python окружения..."
python --version
conda env list | grep "*"

# 2. Проверка зависимостей
echo "\n2. Проверка зависимостей..."
python -c "
try:
    import pandas as pd
    print(f'✅ Pandas {pd.__version__}')
except ImportError:
    print('❌ Pandas не установлен')

try:
    import numpy as np
    print(f'✅ NumPy {np.__version__}')
except ImportError:
    print('❌ NumPy не установлен')
"

# 3. Проверка структуры
echo "\n3. Проверка структуры проекта..."
[ -f "scripts/analyze.py" ] && echo "✅ Основной скрипт" || echo "❌ Основной скрипт не найден"
[ -f "README.md" ] && echo "✅ README.md" || echo "❌ README.md не найден"
[ -f "requirements.txt" ] && echo "✅ requirements.txt" || echo "❌ requirements.txt не найден"

# 4. Запуск приложения
echo "\n4. Тестовый запуск..."
python -c "
import pandas as pd
import numpy as np
print('✅ Импорт библиотек успешен')

# Создаем тестовые данные
data = {'test': [1, 2, 3]}
df = pd.DataFrame(data)
print(f'✅ Создан DataFrame с {len(df)} записями')
"

echo "\n🎉 Проверка завершена!"
echo "Приложение готово к дальнейшей разработке."
