# Калькулятор эмиттанса

Проект для анализа данных эмиттанса с вычислением взвешенного стандартного отклонения расстояний и построением графиков зависимостей.

## Структура проекта

```
emittance_calculator/
├── data/                    # Данные для анализа
│   ├── data_1.xlsx
│   ├── test_data_1.xlsx
│   ├── test_data_2.xlsx
│   └── test_data_3.xlsx
├── src/                     # Исходный код
│   ├── __init__.py
│   ├── data_processor.py    # Обработка данных из Excel файлов
│   ├── visualization.py     # Построение графиков
│   ├── approximation.py     # Квадратичная аппроксимация и расчёт эмиттанса
│   └── physics_parameters.py # Физические константы и расчёты
├── results/                 # Результаты анализа
│   └── plots/              # Сохраненные графики
├── main.py                 # Главный скрипт для запуска анализа
├── config.yaml             # Конфигурационный файл с параметрами эксперимента
├── requirements.txt        # Зависимости проекта
└── README.md              # Документация
```

## Установка и запуск

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Запуск анализа

```bash
python main.py
```

## Конфигурация

Все параметры эксперимента (энергия, длины, список файлов, значения field и др.) задаются в файле `config.yaml`. Это позволяет легко менять условия расчёта без правки кода.

### Основные параметры конфигурации:
- `data_type`: Тип обрабатываемых данных ("experiment" или "modelling")
- `data_path`: Путь к директории с данными
- Другие физические параметры (энергия, длины и т.д.)

## Функциональность

### Обработка данных (`src/data_processor.py`)
- Чтение данных из Excel файлов
- Поддержка двух типов данных:
  - `experiment`: файлы с данными реальных экспериментов (расстояния и веса)
  - `modelling`: файлы с результатами моделирования (x, y координаты)
- Для expreiment: Вычисление взвешенного стандартного отклонения расстояний
- Обработка множественных файлов с разными значениями field
- Поддержка параметра `verbose` для подробного вывода

### Визуализация (`src/visualization.py`)
- Построение и сохранение графиков зависимостей

### Аппроксимация (`src/approximation.py`)
- Квадратичная аппроксимация зависимости стандартного отклонения от параметра w
- Расчёт эмиттанса

### Физические параметры (`src/physics_parameters.py`)
- Класс с физическими константами
- Расчёт релятивистских параметров и вспомогательных величин

## Формат данных

Программа поддерживает два формата Excel файлов:

### Экспериментальные данные (data_type: "experiment")
- **Колонка 1**: Расстояния (мм)
- **Колонка 2**: Количество измерений для каждого расстояния (эксперимент 1)
- **Колонка 3**: Количество измерений для каждого расстояния (эксперимент 2)

### Данные моделирования (data_type: "modelling")
- **Колонка 1**: x-координаты (мм)
- **Колонка 2**: y-координаты (мм)

## Результаты

Программа выводит:
- Взвешенные стандартные отклонения расстояний для каждого эксперимента
- Графики зависимостей от значений field и параметра w
- Сохранённые изображения графиков в папке `results/plots/`

## Зависимости

- pandas==2.1.4
- openpyxl==3.1.2
- matplotlib==3.8.2
- scipy==1.11.4
- pyyaml==6.0.2
