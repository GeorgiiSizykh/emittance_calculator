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
    # Создание фигуры с двумя подграфиками
    plt.figure(figsize=(12, 5))
    
    # График 1: Зависимость взвешенных стандартных отклонений расстояний для второй колонки от field
    plt.subplot(1, 2, 1)
    plt.plot(field_values, weighted_std_col2, 'bo-', linewidth=2, markersize=8)
    plt.xlabel('Field')
    plt.ylabel('Взвешенное стандартное отклонение\nрасстояний (для второй колонки)')
    plt.title('Зависимость взвешенного стандартного отклонения\nрасстояний от field (колонка 2)')
    plt.grid(True, alpha=0.3)
    
    # Добавление значений на точки
    for i, (x, y) in enumerate(zip(field_values, weighted_std_col2)):
        plt.annotate(f'{y:.6f}', (x, y), textcoords="offset points", 
                    xytext=(0,10), ha='center', fontsize=9)
    
    # График 2: Зависимость взвешенных стандартных отклонений расстояний для третьей колонки от field
    plt.subplot(1, 2, 2)
    plt.plot(field_values, weighted_std_col3, 'ro-', linewidth=2, markersize=8)
    plt.xlabel('Field')
    plt.ylabel('Взвешенное стандартное отклонение\nрасстояний (для третьей колонки)')
    plt.title('Зависимость взвешенного стандартного отклонения\nрасстояний от field (колонка 3)')
    plt.grid(True, alpha=0.3)
    
    # Добавление значений на точки
    for i, (x, y) in enumerate(zip(field_values, weighted_std_col3)):
        plt.annotate(f'{y:.6f}', (x, y), textcoords="offset points", 
                    xytext=(0,10), ha='center', fontsize=9)
    
    plt.tight_layout()
    
    # Сохранение графика, если указан путь
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"График сохранен в: {save_path}")
    
    # Показ графика
    if show_plot:
        plt.show()
    
    print("Графики построены и отображены!")


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
        weighted_std_col2 (list): Взвешенные стандартные отклонения для второй колонки
        weighted_std_col3 (list): Взвешенные стандартные отклонения для третьей колонки
    """
    print("\n" + "=" * 50)
    print("РЕЗУЛЬТАТЫ:")
    print(f"Значения field: {field_values}")
    print(f"Взвешенные стандартные отклонения расстояний для второй колонки: {[f'{x:.6f}' for x in weighted_std_col2]}")
    print(f"Взвешенные стандартные отклонения расстояний для третьей колонки: {[f'{x:.6f}' for x in weighted_std_col3]}")
    print("=" * 50) 