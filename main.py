"""
Главный скрипт для расчета эмиттанса электронного пучка.
Обрабатывает данные из Excel файлов, вычисляет взвешенные стандартные отклонения,
выполняет аппроксимацию и рассчитывает эмиттанс.
"""

import os
import sys
from pathlib import Path

# Добавляем папку src в путь для импорта модулей
sys.path.append(str(Path(__file__).parent / 'src'))

from data_processor import process_data_files
from visualization import plot_weighted_std_dependencies, plot_std_vs_w_with_approximation, print_results_summary
from physics_parameters import calculate_relativistic_parameters, calculate_w_parameter
from approximation import fit_parabola_and_calculate_emittance


def main():
    """Основная функция программы"""
    print("=" * 60)
    print("КАЛЬКУЛЯТОР ЭМИТТАНСА ЭЛЕКТРОННОГО ПУЧКА")
    print("=" * 60)
    
    # Создание папки для результатов, если её нет
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    # Параметры для обработки данных
    data_files = ['test_data_1.xlsx', 'test_data_2.xlsx', 'test_data_3.xlsx']
    field_values = [1, 2, 3]
    const = 1
    
    # Обработка данных
    print("\n1. ОБРАБОТКА ДАННЫХ...")
    weighted_std_col2, weighted_std_col3, field_values = process_data_files(
        data_files=data_files,
        field_values=field_values,
        data_folder='data',
        const=const
    )
    
    if not field_values:
        print("Ошибка: Не удалось обработать данные!")
        return
    
    # Вывод результатов обработки
    print_results_summary(field_values, weighted_std_col2, weighted_std_col3)
    
    # Построение графиков зависимости от field
    print("\n2. ПОСТРОЕНИЕ ГРАФИКОВ ЗАВИСИМОСТИ ОТ FIELD...")
    plot_weighted_std_dependencies(
        field_values, 
        weighted_std_col2, 
        weighted_std_col3,
        save_path=results_dir / "std_vs_field.png"
    )
    
    # Физические параметры (захардкожены, как просили)
    d = 0.5  # Длина дрейфа (м)
    l = 0.01  # Эффективная длина соленоида (м)
    epsilon = 1.6e-13  # Энергия электрона (Дж) - примерно 1 МэВ
    Z = 1.0  # Величина заряда
    
    print(f"\n3. РАСЧЕТ ФИЗИЧЕСКИХ ПАРАМЕТРОВ...")
    print(f"Длина дрейфа d = {d} м")
    print(f"Эффективная длина соленоида l = {l} м")
    print(f"Энергия электрона ε = {epsilon:.2e} Дж")
    print(f"Величина заряда Z = {Z}")
    
    # Расчет физических параметров
    gamma, beta = calculate_relativistic_parameters(epsilon)
    w_values = calculate_w_parameter(field_values, d, l, Z, epsilon)
    print(f"Релятивистский фактор γ = {gamma:.6f}")
    print(f"Относительная скорость β = {beta:.6f}")
    print(f"Значения параметра w: {[f'{w:.6f}' for w in w_values]}")
    
    # Аппроксимация и расчет эмиттанса
    print(f"\n4. АППРОКСИМАЦИЯ И РАСЧЕТ ЭМИТТАНСА...")
    
    # Аппроксимация для оси X (вторая колонка)
    emittance_x_result = fit_parabola_and_calculate_emittance(w_values, weighted_std_col2, d, gamma, beta, axis_name="x")
    
    # Аппроксимация для оси Y (третья колонка)
    emittance_y_result = fit_parabola_and_calculate_emittance(w_values, weighted_std_col3, d, gamma, beta, axis_name="y")
    
    # Построение графиков зависимости от w с аппроксимацией
    print(f"\n5. ПОСТРОЕНИЕ ГРАФИКОВ ЗАВИСИМОСТИ ОТ W С АППРОКСИМАЦИЕЙ...")
    plot_std_vs_w_with_approximation(
        w_values,
        weighted_std_col2,
        weighted_std_col3,
        emittance_x_result,
        emittance_y_result,
        save_path=results_dir / "std_vs_w_with_approximation.png"
    )
    
    # Вывод финальных результатов
    print(f"\n6. ФИНАЛЬНЫЕ РЕЗУЛЬТАТЫ:")
    print("=" * 50)
    
    if emittance_x_result:
        print(f"Эмиттанс по оси X: {10 * emittance_x_result['emittance']:.6e} мм·мрад")
        print(f"Нормированный эмиттанс по оси X: {emittance_x_result['norm_emittance']:.6e} м·рад")
        print(f"Параметры аппроксимации (a, b, c): {emittance_x_result['parameters']}")
        print(f"Коэффициент детерминации R²: {emittance_x_result['r_squared']:.6f}")
    
    if emittance_y_result:
        print(f"Эмиттанс по оси Y: {emittance_y_result['emittance']:.6e} м·рад")
        print(f"Нормированный эмиттанс по оси Y: {emittance_y_result['norm_emittance']:.6e} м·рад")
        print(f"Параметры аппроксимации (a, b, c): {emittance_y_result['parameters']}")
        print(f"Коэффициент детерминации R²: {emittance_y_result['r_squared']:.6f}")
    
    print("=" * 50)
    print("РАСЧЕТ ЗАВЕРШЕН!")


if __name__ == "__main__":
    main() 