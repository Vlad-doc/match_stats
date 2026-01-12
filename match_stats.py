import os
import pandas as pd

folder = 'bundesliga'  # папка с файлами

files = [
    '18-19.csv',
    '19-20.csv',
    '20-21.csv',
    '21-22.csv',
    '22-23.csv',
    '23-24.csv',
    '24-25.csv',
    '25-26.csv'
]

# Добавляем путь к каждому файлу
files_with_path = [os.path.join(folder, filename) for filename in files]

# Проверяем, существуют ли файлы (опционально, но полезно)
for path in files_with_path:
    if not os.path.exists(path):
        print(f"Файл не найден: {path}")

# Читаем все CSV из папки
dfs = [pd.read_csv(f, on_bad_lines='skip') for f in files_with_path if os.path.exists(f)]

# Объединяем
combined = pd.concat(dfs, ignore_index=True, sort=False)

# Дальше ваш код: сортировка по дате и т.д.
combined['Date_parsed'] = pd.to_datetime(combined['Date'], dayfirst=True, errors='coerce')
combined = combined.sort_values(by=['Date_parsed', 'Time']).reset_index(drop=True)
combined = combined.drop(columns=['Date_parsed'])

# Сохраняем
combined.to_csv('bundesliga_combined_sorted.csv', index=False)

print(f"Готово! Объединено {len(combined)} матчей.")