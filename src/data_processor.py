"""
Модуль для обработки данных эмиттанса из Excel файлов.
Содержит функции для чтения данных и вычисления взвешенного стандартного отклонения.
"""

import pandas as pd
import numpy as np
import os


def weighted_std(values, weights):
    """
    Вычисляет взвешенное стандартное отклонение
    
    Args:
        values (array): Значения для которых вычисляется стандартное отклонение
        weights (array): Веса для каждого значения
        
    Returns:
        float: Взвешенное стандартное отклонение
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


def read_excel_data(file_path):
    """
    Читает данные из Excel файла и подготавливает их для анализа
    Args:
        file_path (str): Путь к Excel файлу
    Returns:
        tuple: (df, distances_col2, weights_col2, distances_col3, weights_col3)
    """
    # Чтение данных из Excel файла без использования первой строки как заголовков
    df = pd.read_excel(file_path, header=None)
    # Перевод расстояний из миллиметров в метры (первая колонка)
    df.iloc[:, 0] = df.iloc[:, 0] * 0.001
    # Подготовка данных для взвешенного стандартного отклонения
    # Для второй колонки
    valid_col2_mask = df.iloc[:, 1].notna() & (df.iloc[:, 1] != 0) & df.iloc[:, 0].notna()
    distances_col2 = df.loc[valid_col2_mask, 0].values  # Расстояния (в метрах)
    weights_col2 = df.loc[valid_col2_mask, 1].values   # Количество измерений
    # Для третьей колонки
    valid_col3_mask = df.iloc[:, 2].notna() & (df.iloc[:, 2] != 0) & df.iloc[:, 0].notna()
    distances_col3 = df.loc[valid_col3_mask, 0].values  # Расстояния (в метрах)
    weights_col3 = df.loc[valid_col3_mask, 2].values   # Количество измерений
    return df, distances_col2, weights_col2, distances_col3, weights_col3


def process_data_files(data_files, field_values, data_folder='data', verbose=False):
    """
    Обрабатывает список файлов и вычисляет взвешенные стандартные отклонения
    Args:
        data_files (list): Список имен файлов для обработки
        field_values (list): Список значений field, соответствующих каждому файлу
        data_folder (str): Папка с данными (по умолчанию 'data')
        verbose (bool): Флаг для вывода отладочной информации (по умолчанию False)
    Returns:
        tuple: (weighted_std_col2, weighted_std_col3, field_values)
    """
    weighted_std_distances_col2 = []
    weighted_std_distances_col3 = []
    if verbose:
        print("Обработка файлов из папки data:")
        print("-" * 40)
    for i, filename in enumerate(data_files):
        file_path = os.path.join(data_folder, filename)
        if os.path.exists(file_path):
            if verbose:
                print(f"\nОбработка файла: {filename}")
                print(f"Соответствующее значение field: {field_values[i]}")
            # Чтение и обработка данных
            df, distances_col2, weights_col2, distances_col3, weights_col3 = read_excel_data(file_path)
            # Вывод информации о данных
            if verbose:
                print(f"Размер данных: {df.shape}")
                print("Первые 5 строк данных:")
                print(df.head())
            if verbose:
                print(f"Количество строк с данными во второй колонке: {len(distances_col2)}")
                print(f"Количество строк с данными в третьей колонке: {len(distances_col3)}")
            # Вычисляем взвешенные стандартные отклонения расстояний
            weighted_std_col2 = weighted_std(distances_col2, weights_col2)
            weighted_std_col3 = weighted_std(distances_col3, weights_col3)
            weighted_std_distances_col2.append(weighted_std_col2)
            weighted_std_distances_col3.append(weighted_std_col3)
            if verbose and len(distances_col2) > 0:
                print(f"Пример для второй колонки:")
                print(f"  Расстояния (м): {distances_col2[:5]}...")
                print(f"  Веса (количество измерений): {weights_col2[:5]}...")
                print(f"  Взвешенное среднее (м): {np.average(distances_col2, weights=weights_col2):.6f}")
        else:
            if verbose:
                print(f"Файл {filename} не найден!")
    return weighted_std_distances_col2, weighted_std_distances_col3, field_values


def check_excel_structure(file_path, expected_cols, data_type):
    """
    Проверяет структуру Excel-файла. Если количество столбцов не совпадает с ожидаемым для выбранного типа обработки, вызывает ошибку.
    """
    df = pd.read_excel(file_path, header=None)
    if df.shape[1] != expected_cols:
        if data_type == 'modelling' and df.shape[1] != 2:
            raise ValueError(f"Ошибка: выбран тип обработки 'modelling', но в файле {file_path} не 2 столбца!")
        elif data_type == 'experiment' and df.shape[1] == 2:
            raise ValueError(f"Ошибка: выбран тип обработки 'experiment', но в файле {file_path} только 2 столбца! Проверьте тип данных и конфиг.")
    return df


def read_excel_data_modelling(file_path):
    """
    Читает данные формата modelling: 2 столбца (x, y), веса = 1
    Возвращает массивы x, y, веса (все веса = 1)
    """
    df = pd.read_excel(file_path, header=None)
    if df.shape[1] != 2:
        raise ValueError(f"Файл {file_path} не соответствует формату modelling (2 столбца)")
    x = df.iloc[:, 0].values * 0.001  # Переводим из мм в метры
    y = df.iloc[:, 1].values * 0.001
    weights = np.ones_like(x)
    return x, y, weights


def process_data_files_modelling(data_files, field_values, data_folder='data', verbose=False, data_type='modelling'):
    """
    Обрабатывает список файлов формата modelling (2 столбца, веса = 1)
    Возвращает стандартные отклонения по x и y для каждого файла
    """
    std_x = []
    std_y = []
    for i, filename in enumerate(data_files):
        file_path = os.path.join(data_folder, filename)
        if os.path.exists(file_path):
            # Проверка структуры файла
            df = check_excel_structure(file_path, 2, data_type)
            x, y, weights = read_excel_data_modelling(file_path)
            std_x.append(np.std(x))
            std_y.append(np.std(y))
            if verbose:
                print(f"Файл {filename}: std_x = {std_x[-1]:.6e}, std_y = {std_y[-1]:.6e}")
        else:
            if verbose:
                print(f"Файл {filename} не найден!")
    return std_x, std_y, field_values 