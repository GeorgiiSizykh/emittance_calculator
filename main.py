"""
Главный скрипт для анализа данных эмиттанса.
Использует модули для обработки данных, визуализации и аппроксимации.
"""

import os
import sys

# Добавляем папку src в путь для импорта модулей
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data_processor import process_data_files
from src.visualization import plot_weighted_std_dependencies, print_results_summary


def main():
    """
    Главная функция для выполнения анализа данных эмиттанса
    """
    print("=" * 60)
    print("АНАЛИЗ ДАННЫХ ЭМИТТАНСА")
    print("=" * 60)
    
    # Параметры анализа
    const = 1  # Константа для вычисления количества электронов по интенсивности излучения
    field_values = [1, 2, 3]  # Значения field
    data_files = ['test_data_1.xlsx', 'test_data_2.xlsx', 'test_data_3.xlsx']  # Файлы для обработки
    
    print(f"Константа: {const}")
    print(f"Значения field: {field_values}")
    print(f"Файлы для обработки: {data_files}")
    print()
    
    # Обработка данных
    print("ШАГ 1: Обработка данных из Excel файлов")
    print("-" * 50)
    
    weighted_std_col2, weighted_std_col3, field_values = process_data_files(
        data_files=data_files,
        field_values=field_values,
        data_folder='data',
        const=const
    )
    
    # Вывод сводки результатов
    print_results_summary(field_values, weighted_std_col2, weighted_std_col3)
    
    # Построение графиков
    print("\nШАГ 2: Построение графиков зависимостей")
    print("-" * 50)
    
    # Создаем папку для результатов, если её нет
    os.makedirs('results/plots', exist_ok=True)
    
    # Строим и сохраняем графики
    plot_weighted_std_dependencies(
        field_values=field_values,
        weighted_std_col2=weighted_std_col2,
        weighted_std_col3=weighted_std_col3,
        save_path='results/plots/weighted_std_dependencies.png',
        show_plot=True
    )
    
    print("\n" + "=" * 60)
    print("АНАЛИЗ ЗАВЕРШЕН")
    print("=" * 60)
    print("Результаты сохранены в папке results/")
    print("Графики сохранены в папке results/plots/")


if __name__ == "__main__":
    main() 