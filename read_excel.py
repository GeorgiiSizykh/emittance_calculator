import pandas as pd
import warnings

warnings.filterwarnings('ignore')

# Чтение данных из Excel файла
df = pd.read_excel('data_1.xlsx')

# Вывод первых нескольких строк для проверки
print("Первые 5 строк данных:")
print(df.head())

# Вывод информации о структуре данных
print("\nИнформация о данных:")
print(df.info())

# Вывод статистической информации
print("\nСтатистическая информация:")
print(df.describe()) 