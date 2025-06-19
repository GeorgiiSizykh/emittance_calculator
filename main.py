"""
Главный скрипт для расчета эмиттанса электронного пучка.
Обрабатывает данные из Excel файлов, вычисляет взвешенные стандартные отклонения,
выполняет аппроксимацию и рассчитывает эмиттанс.
"""

import os
import sys
from pathlib import Path
import yaml
import csv

# Добавляем папку src в путь для импорта модулей
sys.path.append(str(Path(__file__).parent / 'src'))

from src.data_processor import process_data_files
from src.visualization import plot_weighted_std_dependencies, plot_std_vs_w_with_approximation, print_results_summary
from src.physics_parameters import calculate_relativistic_parameters, calculate_w_parameter
from src.approximation import fit_parabola_and_calculate_emittance


def load_config(config_path="config.yaml"):
    """Загружает параметры из YAML-конфига"""
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config


def main():
    """Основная функция программы"""
    print("=" * 60)
    print("КАЛЬКУЛЯТОР ЭМИТТАНСА ЭЛЕКТРОННОГО ПУЧКА")
    print("=" * 60)
    
    # Загрузка параметров из config.yaml
    config = load_config()
    
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    # Параметры для обработки данных
    data_files = config["data_files"]
    field_values = config["field_values"]
    const = config["const"]
    
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
    
    print_results_summary(field_values, weighted_std_col2, weighted_std_col3)
    
    print("\n2. ПОСТРОЕНИЕ ГРАФИКОВ ЗАВИСИМОСТИ ОТ FIELD...")
    plot_weighted_std_dependencies(
        field_values, 
        weighted_std_col2, 
        weighted_std_col3,
        save_path=results_dir / "std_vs_field.png"
    )
    
    # Физические параметры теперь из конфига
    d = config["drift_length"]
    l = config["solenoid_length"]
    epsilon = config["energy"]
    Z = config["charge"]
    
    print(f"\n3. РАСЧЕТ ФИЗИЧЕСКИХ ПАРАМЕТРОВ...")
    print(f"Длина дрейфа d = {d} м")
    print(f"Эффективная длина соленоида l = {l} м")
    print(f"Энергия электрона ε = {epsilon:.2e} Дж")
    print(f"Величина заряда Z = {Z}")
    
    gamma, beta = calculate_relativistic_parameters(epsilon)
    w_values = calculate_w_parameter(field_values, d, l, Z, epsilon)
    print(f"Релятивистский фактор γ = {gamma:.6f}")
    print(f"Относительная скорость β = {beta:.6f}")
    print(f"Значения параметра w: {[f'{w:.6f}' for w in w_values]}")
    
    print(f"\n4. АППРОКСИМАЦИЯ И РАСЧЕТ ЭМИТТАНСА...")
    emittance_x_result = fit_parabola_and_calculate_emittance(w_values, weighted_std_col2, d, gamma, beta, axis_name="x")
    emittance_y_result = fit_parabola_and_calculate_emittance(w_values, weighted_std_col3, d, gamma, beta, axis_name="y")
    
    print(f"\n5. ПОСТРОЕНИЕ ГРАФИКОВ ЗАВИСИМОСТИ ОТ W С АППРОКСИМАЦИЕЙ...")
    plot_std_vs_w_with_approximation(
        w_values,
        weighted_std_col2,
        weighted_std_col3,
        emittance_x_result,
        emittance_y_result,
        save_path=results_dir / "std_vs_w_with_approximation.png"
    )
    
    print(f"\n6. ФИНАЛЬНЫЕ РЕЗУЛЬТАТЫ:")
    print("=" * 50)
    if emittance_x_result:
        print(f"Эмиттанс по оси X: {emittance_x_result['emittance']:.6e} м·рад")
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

    # Сохраняем эмиттансы в CSV
    emittance_csv_path = results_dir / "emittance_results.csv"
    with open(emittance_csv_path, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["axis", "emittance", "norm_emittance"])
        if emittance_x_result:
            writer.writerow([
                "x",
                f"{emittance_x_result['emittance']:.6e}",
                f"{emittance_x_result['norm_emittance']:.6e}"
            ])
        if emittance_y_result:
            writer.writerow([
                "y",
                f"{emittance_y_result['emittance']:.6e}",
                f"{emittance_y_result['norm_emittance']:.6e}"
            ])
    print(f"Результаты эмиттанса сохранены в {emittance_csv_path}")


if __name__ == "__main__":
    main() 