"""
Модуль для аппроксимации зависимостей в данных эмиттанса.
Содержит функции для подгонки различных математических функций к данным.
"""

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def linear_function(x, a, b):
    """
    Линейная функция: y = ax + b
    
    Args:
        x (array): Значения x
        a (float): Коэффициент наклона
        b (float): Свободный член
        
    Returns:
        array: Значения функции
    """
    return a * x + b


def quadratic_function(x, a, b, c):
    """
    Квадратичная функция: y = ax² + bx + c
    
    Args:
        x (array): Значения x
        a (float): Коэффициент при x²
        b (float): Коэффициент при x
        c (float): Свободный член
        
    Returns:
        array: Значения функции
    """
    return a * x**2 + b * x + c


def exponential_function(x, a, b, c):
    """
    Экспоненциальная функция: y = a * exp(bx) + c
    
    Args:
        x (array): Значения x
        a (float): Амплитуда
        b (float): Показатель экспоненты
        c (float): Смещение по y
        
    Returns:
        array: Значения функции
    """
    return a * np.exp(b * x) + c


def power_function(x, a, b, c):
    """
    Степенная функция: y = a * x^b + c
    
    Args:
        x (array): Значения x
        a (float): Коэффициент
        b (float): Показатель степени
        c (float): Смещение по y
        
    Returns:
        array: Значения функции
    """
    return a * x**b + c


def fit_function(x_data, y_data, function, initial_guess=None, bounds=None):
    """
    Подгоняет функцию к данным
    
    Args:
        x_data (array): Данные по оси X
        y_data (array): Данные по оси Y
        function (callable): Функция для подгонки
        initial_guess (tuple, optional): Начальное приближение параметров
        bounds (tuple, optional): Границы для параметров
        
    Returns:
        tuple: (оптимальные параметры, ковариационная матрица)
    """
    try:
        if bounds is not None:
            popt, pcov = curve_fit(function, x_data, y_data, 
                                  p0=initial_guess, bounds=bounds)
        else:
            popt, pcov = curve_fit(function, x_data, y_data, p0=initial_guess)
        return popt, pcov
    except Exception as e:
        print(f"Ошибка при подгонке функции: {e}")
        return None, None


def calculate_r_squared(y_actual, y_predicted):
    """
    Вычисляет коэффициент детерминации R²
    
    Args:
        y_actual (array): Фактические значения
        y_predicted (array): Предсказанные значения
        
    Returns:
        float: Коэффициент детерминации R²
    """
    ss_res = np.sum((y_actual - y_predicted) ** 2)
    ss_tot = np.sum((y_actual - np.mean(y_actual)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)
    return r_squared


def compare_approximations(x_data, y_data, functions_dict):
    """
    Сравнивает качество аппроксимации различными функциями
    
    Args:
        x_data (array): Данные по оси X
        y_data (array): Данные по оси Y
        functions_dict (dict): Словарь с функциями для сравнения
        
    Returns:
        dict: Результаты сравнения для каждой функции
    """
    results = {}
    
    for func_name, func_info in functions_dict.items():
        function = func_info['function']
        initial_guess = func_info.get('initial_guess')
        bounds = func_info.get('bounds')
        
        # Подгонка функции
        popt, pcov = fit_function(x_data, y_data, function, initial_guess, bounds)
        
        if popt is not None:
            # Вычисление предсказанных значений
            y_predicted = function(x_data, *popt)
            
            # Вычисление R²
            r_squared = calculate_r_squared(y_data, y_predicted)
            
            # Вычисление среднеквадратичной ошибки
            mse = np.mean((y_data - y_predicted) ** 2)
            
            results[func_name] = {
                'parameters': popt,
                'covariance': pcov,
                'r_squared': r_squared,
                'mse': mse,
                'y_predicted': y_predicted
            }
            
            print(f"{func_name}: R² = {r_squared:.6f}, MSE = {mse:.6f}")
        else:
            print(f"{func_name}: Ошибка при подгонке")
    
    return results


def find_best_approximation(x_data, y_data, functions_dict):
    """
    Находит лучшую аппроксимацию среди заданных функций
    
    Args:
        x_data (array): Данные по оси X
        y_data (array): Данные по оси Y
        functions_dict (dict): Словарь с функциями для сравнения
        
    Returns:
        tuple: (название лучшей функции, её параметры, предсказанные значения)
    """
    results = compare_approximations(x_data, y_data, functions_dict)
    
    if not results:
        return None, None, None
    
    # Находим функцию с максимальным R²
    best_func = max(results.keys(), key=lambda k: results[k]['r_squared'])
    best_result = results[best_func]
    
    print(f"\nЛучшая аппроксимация: {best_func}")
    print(f"R² = {best_result['r_squared']:.6f}")
    print(f"MSE = {best_result['mse']:.6f}")
    print(f"Параметры: {best_result['parameters']}")
    
    return best_func, best_result['parameters'], best_result['y_predicted']


def print_approximation_equation(func_name, parameters):
    """
    Выводит уравнение аппроксимирующей функции
    
    Args:
        func_name (str): Название функции
        parameters (array): Параметры функции
    """
    if func_name == "Линейная":
        a, b = parameters
        print(f"Уравнение: y = {a:.6f} * x + {b:.6f}")
    elif func_name == "Квадратичная":
        a, b, c = parameters
        print(f"Уравнение: y = {a:.6f} * x² + {b:.6f} * x + {c:.6f}")
    elif func_name == "Экспоненциальная":
        a, b, c = parameters
        print(f"Уравнение: y = {a:.6f} * exp({b:.6f} * x) + {c:.6f}")
    elif func_name == "Степенная":
        a, b, c = parameters
        print(f"Уравнение: y = {a:.6f} * x^{b:.6f} + {c:.6f}")


def fit_parabola_and_calculate_emittance(w_values, std_values, d, gamma, beta, axis_name="x"):
    """
    Аппроксимирует зависимость стандартного отклонения от w параболой
    и вычисляет параметры эмиттанса
    
    Args:
        w_values (list): Значения параметра w
        std_values (list): Значения стандартного отклонения
        d (float): Длина дрейфа
        gamma (float): Релятивистский фактор
        beta (float): Относительная скорость
        axis_name (str): Название оси (x или y)
        
    Returns:
        dict: Параметры эмиттанса
    """
    print(f"\nАППРОКСИМАЦИЯ ДЛЯ ОСИ {axis_name.upper()}")
    print("-" * 50)
    
    # Преобразуем в numpy arrays для корректной работы
    w_array = np.array(w_values)
    std_array = np.array(std_values)
    
    # Подгонка параболы: std² = a * w² + b * w + c
    # Но мы аппроксимируем std = sqrt(a * w² + b * w + c)
    # Для этого используем квадратичную функцию
    popt, pcov = fit_function(w_array, std_array, quadratic_function)
    
    if popt is None:
        print(f"Ошибка при аппроксимации для оси {axis_name}")
        return None
    
    a, b, c = popt
    
    # Вычисляем предсказанные значения
    std_predicted = quadratic_function(w_array, a, b, c)
    
    # Вычисляем R²
    r_squared = calculate_r_squared(std_array, std_predicted)
    
    print(f"Параболическая аппроксимация: std = {a:.6f} * w² + {b:.6f} * w + {c:.6f}")
    print(f"R² = {r_squared:.6f}")
    
    # Вычисляем параметры эмиттанса
    # sigma2_x0 = a (коэффициент при w²)
    # sigma2_xxp0 = b / (2 * d) (коэффициент при w, деленный на 2d)
    # sigma2_xpxp0 = c / d² (свободный член, деленный на d²)
    
    sigma2_0 = a
    sigma2_1 = b / (2 * d)
    sigma2_2 = c / (d**2)
    
    # Вычисляем эмиттанс
    emittance = np.sqrt(sigma2_0 * sigma2_2 - sigma2_1**2)
    
    # Вычисляем нормированный эмиттанс
    norm_emittance = beta * gamma * emittance
    
    # Формируем названия параметров в зависимости от оси
    if axis_name == "x":
        param_names = ["sigma2_x0", "sigma2_xxp0", "sigma2_xpxp0", "emittance_x", "norm_emittance_x"]
    else:
        param_names = ["sigma2_y0", "sigma2_yyp0", "sigma2_ypyp0", "emittance_y", "norm_emittance_y"]
    
    print(f"\nПАРАМЕТРЫ ЭМИТТАНСА ДЛЯ ОСИ {axis_name.upper()}:")
    print(f"{param_names[0]} = {sigma2_0:.6e}")
    print(f"{param_names[1]} = {sigma2_1:.6e}")
    print(f"{param_names[2]} = {sigma2_2:.6e}")
    print(f"{param_names[3]} = {emittance:.6e} м·рад")
    print(f"{param_names[4]} = {norm_emittance:.6e} м·рад")
    
    return {
        'sigma2_0': sigma2_0,
        'sigma2_1': sigma2_1,
        'sigma2_2': sigma2_2,
        'emittance': emittance,
        'norm_emittance': norm_emittance,
        'r_squared': r_squared,
        'parameters': popt,
        'predicted_values': std_predicted,
        'param_names': param_names
    }


def calculate_total_emittance(emittance_x, emittance_y):
    """
    Вычисляет общий эмиттанс пучка
    
    Args:
        emittance_x (float): Эмиттанс по оси x
        emittance_y (float): Эмиттанс по оси y
        
    Returns:
        float: Общий эмиттанс
    """
    # Общий эмиттанс как среднее геометрическое
    total_emittance = np.sqrt(emittance_x * emittance_y)
    return total_emittance 