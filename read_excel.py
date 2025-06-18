import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# Константа для вычисления количества электронов по интенсивности излучения: const = N / I
const = 1

# Список значений field, соответствующих каждому файлу
field = [1, 2, 3]

# Список файлов для обработки (исключаем data_1.xlsx, так как у нас есть test_data_1.xlsx)
data_files = ['test_data_1.xlsx', 'test_data_2.xlsx', 'test_data_3.xlsx']

# Списки для хранения взвешенных стандартных отклонений расстояний
weighted_std_distances_col2 = []  # Взвешенные стандартные отклонения расстояний для второй колонки
weighted_std_distances_col3 = []  # Взвешенные стандартные отклонения расстояний для третьей колонки

def weighted_std(values, weights):
    """
    Вычисляет взвешенное стандартное отклонение
    """
    if len(values) == 0 or sum(weights) == 0:
        return 0
    
    # Взвешенное среднее
    weighted_mean = np.average(values, weights=weights)
    
    # Взвешенная дисперсия
    weighted_variance = np.average((values - weighted_mean)**2, weights=weights)
    
    # Взвешенное стандартное отклонение
    weighted_std = np.sqrt(weighted_variance)
    
    return weighted_std

print("Обработка файлов из папки data:")
print("-" * 40)

# Обработка каждого файла
for i, filename in enumerate(data_files):
    file_path = os.path.join('data', filename)
    
    if os.path.exists(file_path):
        print(f"\nОбработка файла: {filename}")
        print(f"Соответствующее значение field: {field[i]}")
        
        # Чтение данных из Excel файла без использования первой строки как заголовков
        df = pd.read_excel(file_path, header=None)
        
        # Вывод информации о данных
        print(f"Размер данных: {df.shape}")
        print("Первые 5 строк данных:")
        print(df.head())
        
        # Умножение всех колонок, кроме первой, на константу
        columns_to_multiply = df.columns[1:]  # Все колонки кроме первой
        df[columns_to_multiply] = df[columns_to_multiply] * const
        
        # Подготовка данных для взвешенного стандартного отклонения
        # Для второй колонки
        valid_col2_mask = df.iloc[:, 1].notna() & (df.iloc[:, 1] != 0) & df.iloc[:, 0].notna()
        distances_col2 = df.loc[valid_col2_mask, 0].values  # Расстояния
        weights_col2 = df.loc[valid_col2_mask, 1].values   # Количество измерений
        
        # Для третьей колонки
        valid_col3_mask = df.iloc[:, 2].notna() & (df.iloc[:, 2] != 0) & df.iloc[:, 0].notna()
        distances_col3 = df.loc[valid_col3_mask, 0].values  # Расстояния
        weights_col3 = df.loc[valid_col3_mask, 2].values   # Количество измерений
        
        print(f"\nОтладочная информация:")
        print(f"Количество строк с данными во второй колонке: {valid_col2_mask.sum()}")
        print(f"Количество строк с данными в третьей колонке: {valid_col3_mask.sum()}")
        
        # Вычисляем взвешенные стандартные отклонения расстояний
        weighted_std_col2 = weighted_std(distances_col2, weights_col2)
        weighted_std_col3 = weighted_std(distances_col3, weights_col3)
        
        weighted_std_distances_col2.append(weighted_std_col2)
        weighted_std_distances_col3.append(weighted_std_col3)
        
        print(f"Взвешенное стандартное отклонение расстояний для второй колонки: {weighted_std_col2:.6f}")
        print(f"Взвешенное стандартное отклонение расстояний для третьей колонки: {weighted_std_col3:.6f}")
        
        # Дополнительная отладочная информация
        if len(distances_col2) > 0:
            print(f"Пример для второй колонки:")
            print(f"  Расстояния: {distances_col2[:5]}...")
            print(f"  Веса (количество измерений): {weights_col2[:5]}...")
            print(f"  Взвешенное среднее: {np.average(distances_col2, weights=weights_col2):.6f}")
        
    else:
        print(f"Файл {filename} не найден!")

print("\n" + "=" * 50)
print("РЕЗУЛЬТАТЫ:")
print(f"Значения field: {field}")
print(f"Взвешенные стандартные отклонения расстояний для второй колонки: {[f'{x:.6f}' for x in weighted_std_distances_col2]}")
print(f"Взвешенные стандартные отклонения расстояний для третьей колонки: {[f'{x:.6f}' for x in weighted_std_distances_col3]}")

# Построение графиков
plt.figure(figsize=(12, 5))

# График 1: Зависимость взвешенных стандартных отклонений расстояний для второй колонки от field
plt.subplot(1, 2, 1)
plt.plot(field, weighted_std_distances_col2, 'bo-', linewidth=2, markersize=8)
plt.xlabel('Field')
plt.ylabel('Взвешенное стандартное отклонение\nрасстояний (для второй колонки)')
plt.title('Зависимость взвешенного стандартного отклонения\nрасстояний от field (колонка 2)')
plt.grid(True, alpha=0.3)

# Добавление значений на точки
for i, (x, y) in enumerate(zip(field, weighted_std_distances_col2)):
    plt.annotate(f'{y:.6f}', (x, y), textcoords="offset points", 
                xytext=(0,10), ha='center', fontsize=9)

# График 2: Зависимость взвешенных стандартных отклонений расстояний для третьей колонки от field
plt.subplot(1, 2, 2)
plt.plot(field, weighted_std_distances_col3, 'ro-', linewidth=2, markersize=8)
plt.xlabel('Field')
plt.ylabel('Взвешенное стандартное отклонение\nрасстояний (для третьей колонки)')
plt.title('Зависимость взвешенного стандартного отклонения\nрасстояний от field (колонка 3)')
plt.grid(True, alpha=0.3)

# Добавление значений на точки
for i, (x, y) in enumerate(zip(field, weighted_std_distances_col3)):
    plt.annotate(f'{y:.6f}', (x, y), textcoords="offset points", 
                xytext=(0,10), ha='center', fontsize=9)

plt.tight_layout()
plt.show()

print("\nГрафики построены и отображены!")

