"""
Модуль для визуализации результатов анализа данных эмиттанса.
Содержит функции для построения графиков зависимостей.
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_weighted_std_dependencies(field_values, weighted_std_col2, weighted_std_col3, 
                                  save_path=None, show_plot=True):
    """
    Строит графики зависимости взвешенного стандартного отклонения от field
    
    Args:
        field_values (list): Значения field
        weighted_std_col2 (list): Взвешенные стандартные отклонения для второй колонки
        weighted_std_col3 (list): Взвешенные стандартные отклонения для третьей колонки
        save_path (str, optional): Путь для сохранения графика
        show_plot (bool): Показывать ли график на экране (по умолчанию True)
    """
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(field_values, weighted_std_col2, 'bo-', linewidth=2, markersize=8)
    plt.xlabel('Field')
    plt.ylabel('Взвешенное стандартное отклонение\nрасстояний (м) (для второй колонки)')
    plt.title('Зависимость взвешенного стандартного отклонения\nрасстояний от field (колонка 2)')
    plt.grid(True, alpha=0.3)
    for x, y in zip(field_values, weighted_std_col2):
        plt.annotate(f'{y:.6f}', (x, y), textcoords="offset points", xytext=(0,10), ha='center', fontsize=9)
    plt.subplot(1, 2, 2)
    plt.plot(field_values, weighted_std_col3, 'ro-', linewidth=2, markersize=8)
    plt.xlabel('Field')
    plt.ylabel('Взвешенное стандартное отклонение\nрасстояний (м) (для третьей колонки)')
    plt.title('Зависимость взвешенного стандартного отклонения\nрасстояний от field (колонка 3)')
    plt.grid(True, alpha=0.3)
    for x, y in zip(field_values, weighted_std_col3):
        plt.annotate(f'{y:.6f}', (x, y), textcoords="offset points", xytext=(0,10), ha='center', fontsize=9)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"График сохранен в: {save_path}")
    if show_plot:
        plt.show()
    print("Графики построены и отображены!")


def plot_std_vs_w_with_approximation(w_values, weighted_std_col2, weighted_std_col3, 
                                    emittance_x_result, emittance_y_result,
                                    save_path=None, show_plot=True):
    """
    Строит графики зависимости стандартного отклонения от параметра w с аппроксимирующими параболами
    
    Args:
        w_values (list): Значения параметра w
        weighted_std_col2 (list): Взвешенные стандартные отклонения для второй колонки
        weighted_std_col3 (list): Взвешенные стандартные отклонения для третьей колонки
        emittance_x_result (dict): Результаты аппроксимации для оси x
        emittance_y_result (dict): Результаты аппроксимации для оси y
        save_path (str, optional): Путь для сохранения графика
        show_plot (bool): Показывать ли график на экране (по умолчанию True)
    """
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(w_values, weighted_std_col2, 'bo-', linewidth=2, markersize=8, label='Фактические значения')
    if emittance_x_result:
        a, b, c = emittance_x_result['parameters']
        w_smooth = np.linspace(min(w_values), max(w_values), 100)
        std_predicted_smooth = a * w_smooth**2 + b * w_smooth + c
        plt.plot(w_smooth, std_predicted_smooth, 'r--', linewidth=2, label=f'Аппроксимация: {a:.2f}w² + {b:.2f}w + {c:.2f}')
    plt.xlabel('Параметр w')
    plt.ylabel('Взвешенное стандартное отклонение\nрасстояний (м) (ось X)')
    plt.title('Зависимость стандартного отклонения от w\nс параболической аппроксимацией (ось X)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    for x, y in zip(w_values, weighted_std_col2):
        plt.annotate(f'{y:.6f}', (x, y), textcoords="offset points", xytext=(0,10), ha='center', fontsize=9)
    plt.subplot(1, 2, 2)
    plt.plot(w_values, weighted_std_col3, 'go-', linewidth=2, markersize=8, label='Фактические значения')
    if emittance_y_result:
        a, b, c = emittance_y_result['parameters']
        w_smooth = np.linspace(min(w_values), max(w_values), 100)
        std_predicted_smooth = a * w_smooth**2 + b * w_smooth + c
        plt.plot(w_smooth, std_predicted_smooth, 'm--', linewidth=2, label=f'Аппроксимация: {a:.2f}w² + {b:.2f}w + {c:.2f}')
    plt.xlabel('Параметр w')
    plt.ylabel('Взвешенное стандартное отклонение\nрасстояний (м) (ось Y)')
    plt.title('Зависимость стандартного отклонения от w\nс параболической аппроксимацией (ось Y)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    for x, y in zip(w_values, weighted_std_col3):
        plt.annotate(f'{y:.6f}', (x, y), textcoords="offset points", xytext=(0,10), ha='center', fontsize=9)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"График сохранен в: {save_path}")
    if show_plot:
        plt.show()
    print("Графики зависимости от w построены и отображены!")


def plot_approximation_comparison(field_values, actual_values, approximated_values, 
                                title, save_path=None, show_plot=True):
    """
    Строит график сравнения фактических и аппроксимированных значений
    
    Args:
        field_values (list): Значения field (ось X)
        actual_values (list): Фактические значения
        approximated_values (list): Аппроксимированные значения
        title (str): Заголовок графика
        save_path (str, optional): Путь для сохранения графика
        show_plot (bool): Показывать ли график на экране (по умолчанию True)
    """
    plt.figure(figsize=(10, 6))
    
    # Построение фактических значений
    plt.plot(field_values, actual_values, 'bo-', linewidth=2, markersize=8, 
             label='Фактические значения')
    
    # Построение аппроксимированных значений
    plt.plot(field_values, approximated_values, 'r--', linewidth=2, 
             label='Аппроксимация')
    
    plt.xlabel('Field')
    plt.ylabel('Взвешенное стандартное отклонение расстояний')
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Добавление значений на точки
    for i, (x, y) in enumerate(zip(field_values, actual_values)):
        plt.annotate(f'{y:.6f}', (x, y), textcoords="offset points", 
                    xytext=(0,10), ha='center', fontsize=9)
    
    # Сохранение графика, если указан путь
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"График сохранен в: {save_path}")
    
    # Показ графика
    if show_plot:
        plt.show()


def print_results_summary(field_values, weighted_std_col2, weighted_std_col3):
    """
    Выводит сводку результатов в консоль
    
    Args:
        field_values (list): Значения field
        weighted_std_col2 (list): Взвешенные стандартные отклонения для второй колонки (в метрах)
        weighted_std_col3 (list): Взвешенные стандартные отклонения для третьей колонки (в метрах)
    """
    print("\n" + "=" * 50)
    print("РЕЗУЛЬТАТЫ:")
    print(f"Значения field: {field_values}")
    print(f"Взвешенные стандартные отклонения расстояний для второй колонки (м): {[f'{x:.6f}' for x in weighted_std_col2]}")
    print(f"Взвешенные стандартные отклонения расстояний для третьей колонки (м): {[f'{x:.6f}' for x in weighted_std_col3]}")
    print("\n" + "=" * 50) 