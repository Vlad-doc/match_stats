import os
import pandas as pd
from datetime import datetime

# --------------------- НАСТРОЙКИ ---------------------
FOLDER_PATH = 'Seria A'
FILE_NAME = 'seria_a_combined_sorted.csv'
FILE_PATH = os.path.join(FOLDER_PATH, FILE_NAME)
ODDS_COLUMN = 'PSH'                             # Колонка с коэффициентом (например, 'PSH', 'B365H', 'AvgH' и т.д.)
MIN_ODDS = 3.3                                  # Нижняя граница
MAX_ODDS = 3.7                                  # Верхняя граница
# ----------------------------------------------------

# Функция для определения сезона (август → начало нового сезона)
def get_season(date_str):
    try:
        date = datetime.strptime(date_str, '%d/%m/%Y')
    except:
        return 'Unknown'
    year = date.year
    if date.month >= 8:
        return f"{year}/{year + 1}"
    else:
        return f"{year - 1}/{year}"

# Загрузка данных
df = pd.read_csv(FILE_PATH)

# Добавляем колонку сезона
df['Season'] = df['Date'].apply(get_season)

# Фильтрация по диапазону коэффициентов (игнорируем NaN)
df_filtered = df[
    (df[ODDS_COLUMN].notna()) &
    (df[ODDS_COLUMN] >= MIN_ODDS) & 
    (df[ODDS_COLUMN] <= MAX_ODDS)
].copy()

if df_filtered.empty:
    print(f"Нет матчей с коэффициентом {ODDS_COLUMN} в диапазоне [{MIN_ODDS}, {MAX_ODDS}]")
else:
    # Подсчёт результатов по сезонам
    result_counts = df_filtered.groupby('Season')['FTR'].value_counts().unstack(fill_value=0)
    
    # Добавляем недостающие колонки H/D/A
    for col in ['H', 'D', 'A']:
        if col not in result_counts.columns:
            result_counts[col] = 0
    
    # Общее количество матчей по сезонам
    result_counts['Total'] = result_counts[['H', 'D', 'A']].sum(axis=1)
    
    # Проценты
    result_counts['Home %'] = (result_counts['H'] / result_counts['Total'] * 100).round(2)
    result_counts['Draw %'] = (result_counts['D'] / result_counts['Total'] * 100).round(2)
    result_counts['Away %'] = (result_counts['A'] / result_counts['Total'] * 100).round(2)
    
    # Порядок колонок
    result_counts = result_counts[['H', 'D', 'A', 'Total', 'Home %', 'Draw %', 'Away %']]
    
    # Сортировка по сезонам
    result_counts = result_counts.sort_index()
    
    # ИТОГО
    total_matches = result_counts['Total'].sum()
    total_h = result_counts['H'].sum()
    total_d = result_counts['D'].sum()
    total_a = result_counts['A'].sum()
    
    total_row = pd.DataFrame([{
        'H': total_h,
        'D': total_d,
        'A': total_a,
        'Total': total_matches,
        'Home %': round(total_h / total_matches * 100, 2),
        'Draw %': round(total_d / total_matches * 100, 2),
        'Away %': round(total_a / total_matches * 100, 2)
    }], index=['ИТОГО'])
    
    # Объединяем таблицу с итоговой строкой
    full_table = pd.concat([result_counts, total_row])
    
    # Вывод
    print(f"\nМатчи с {ODDS_COLUMN} в диапазоне [{MIN_ODDS} – {MAX_ODDS}]")
    print(f"Всего матчей: {total_matches}\n")
    print(full_table.to_string())
    
    # Опционально: сохранить в CSV
    # full_table.to_csv('result_psh_3.2-3.5.csv')
    # print("\nРезультаты сохранены в 'result_psh_3.2-3.5.csv'")