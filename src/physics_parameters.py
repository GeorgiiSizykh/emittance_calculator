"""
Модуль для физических параметров и расчетов эмиттанса.
Содержит константы и функции для расчета вспомогательных величин.
"""

import numpy as np


# Физические константы
class PhysicsConstants:
    """Класс для хранения физических констант"""
    
    # Скорость света (м/с)
    c = 299792458.0
    
    # Масса электрона (кг)
    m = 9.1093837015e-31
    
    # Заряд электрона (Кл)
    e = 1.602176634e-19
    
    # Энергия покоя электрона (Дж)
    m_c2 = m * c**2


def calculate_relativistic_parameters(epsilon):
    """
    Вычисляет релятивистские параметры gamma и beta
    
    Args:
        epsilon (float): Энергия электрона (Дж)
        
    Returns:
        tuple: (gamma, beta)
    """
    gamma = epsilon / PhysicsConstants.m_c2
    beta = np.sqrt(1 - 1 / gamma**2)
    return gamma, beta


def calculate_w_parameter(field_values, d, l, Z, epsilon):
    """
    Вычисляет вспомогательную величину w для каждого значения поля
    
    Args:
        field_values (list): Значения магнитного поля B
        d (float): Длина дрейфа (м)
        l (float): Эффективная длина соленоида (м)
        Z (float): Величина заряда
        epsilon (float): Энергия электрона (Дж)
        
    Returns:
        list: Значения параметра w
    """
    gamma, beta = calculate_relativistic_parameters(epsilon)
    
    w_values = []
    for B in field_values:
        # w = 1 - d * l * (e * Z * B)**2 / (2 * m * c * gamma * beta)**2
        numerator = d * l * (PhysicsConstants.e * Z * B)**2
        denominator = (2 * PhysicsConstants.m * PhysicsConstants.c * gamma * beta)**2
        w = 1 - numerator / denominator
        w_values.append(w)
    
    return w_values


def print_physics_parameters(d, l, epsilon, Z, field_values):
    """
    Выводит физические параметры и вспомогательные величины
    
    Args:
        d (float): Длина дрейфа
        l (float): Эффективная длина соленоида
        epsilon (float): Энергия электрона
        Z (float): Величина заряда
        field_values (list): Значения поля
    """
    gamma, beta = calculate_relativistic_parameters(epsilon)
    w_values = calculate_w_parameter(field_values, d, l, Z, epsilon)
    
    print("=" * 60)
    print("ФИЗИЧЕСКИЕ ПАРАМЕТРЫ")
    print("=" * 60)
    print(f"Длина дрейфа d = {d:.6e} м")
    print(f"Эффективная длина соленоида l = {l:.6e} м")
    print(f"Энергия электрона ε = {epsilon:.6e} Дж")
    print(f"Величина заряда Z = {Z}")
    print(f"Релятивистский параметр γ = {gamma:.6f}")
    print(f"Параметр β = {beta:.6f}")
    print()
    
    print("ЗНАЧЕНИЯ ПОЛЯ И ПАРАМЕТРА w:")
    print("-" * 40)
    for i, (B, w) in enumerate(zip(field_values, w_values)):
        print(f"Field[{i}] = {B}: w = {w:.6f}")
    print("=" * 60)
    
    return w_values 