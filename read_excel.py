import pandas as pd

# Константа для вычисления количества электронов по интенсивности излучения: const = N / I
const = 1

# Чтение данных из Excel файла без использования первой строки как заголовков
df = pd.read_excel('data_1.xlsx', header=None)

# Вывод первых нескольких строк для проверки
print("Первые 5 строк данных:")
print(df.head())

# Умножение всех колонок, кроме первой, на константу
columns_to_multiply = df.columns[1:]  # Все колонки кроме первой
df[columns_to_multiply] = df[columns_to_multiply] * const

# Вычисление стандартных отклонений для всех колонок, кроме первой
std_deviations = df[columns_to_multiply].std()
print("\nСтандартные отклонения:")
for column, std in std_deviations.items():
    print(f"Колонка {column}: {std:.6f}")

