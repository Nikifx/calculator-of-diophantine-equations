from sympy import sympify, Eq
from random import randint
from math import sqrt
from time import time
from json import dump, load
import matplotlib.pyplot as plt

# Функция для преобразования строки в список объектов Eq и извлечения переменных
def parse_equations(equations):
    equations = equations.split(',')
    eqs = []
    variables = set()
    for equation in equations:
        lhs, rhs = map(lambda x: sympify(x.replace('^', '**')), equation.split('='))
        eq = Eq(lhs, rhs)
        eqs.append(eq)
        variables.update(eq.free_symbols)
    variables = sorted(variables, key=lambda x: str(x))
    return eqs, variables

# Целевая функция
def D(*args):
    substitutions = dict(zip(variables, args))
    total_difference = sum(abs(eq.lhs.subs(substitutions) - eq.rhs.subs(substitutions)) for eq in eqs)
    return total_difference

# Генерация начальной популяции
def generate_population(pop_size):
    return [[randint(-10, 10) for _ in range(comp_count)] for _ in range(pop_size)]

# Клонирование
def clone(cell):
    return cell.copy()

# Мутация 1
def mutate1(cell):
    new_cell = cell.copy()
    idx = randint(0, len(new_cell)-1)
    new_cell[idx] = randint(-1000, 1000)
    return new_cell

# Вычисляет медиану списка чисел
def calculate_median(data):
    if not data:
        return None
    sorted_data = sorted(data)
    n = len(sorted_data)
    midpoint = n // 2
    
    if n % 2 == 1:
        return sorted_data[midpoint]
    else:
        return (sorted_data[midpoint - 1] + sorted_data[midpoint]) / 2

# Вычисляет среднее арифметическое списка чисел
def calculate_mean(data):
    if not data:
        return None
    return sum(data) / len(data)

# Мутация 2
def mutate2(cell):
    new_cell = cell.copy()
    med = calculate_median(new_cell)
    avg = calculate_mean(new_cell)
    idx = randint(0, len(new_cell)-1)
    if med < avg:
        new_cell[idx] = randint(int(med), int(avg))
    else:
        new_cell[idx] = randint(int(avg), int(med))
    return new_cell

# Мутация 3
def mutate3(cell):
    new_cell = cell.copy()
    idx = randint(0, len(new_cell)-1)
    new_cell[idx] = randint(-5, 5)
    return new_cell

# Оценка одной клетки
def evaluate(cell):
    return abs(D(*cell))

# Оценка популяции
def evaluate_population(population):
    return [abs(D(*cell)) for cell in population]

# Клональный отбор
def clonal_selection(population, scores, pop_size):
    sorted_population = [x for _, x in sorted(zip(scores, population), key=lambda pair: pair[0])]
    return sorted_population[:pop_size]

# Функция для вычисления Евклидова расстояния между двумя точками
def euclidean_distance(point1, point2):
    return sqrt(sum((p1 - p2) ** 2 for p1, p2 in zip(point1, point2)))

# Процедура сжатия
def compression(population, threshold):
    to_remove = set()
    
    # Соберем все расстояния и их индексы
    distances = []
    for i in range(len(population)):
        for j in range(i + 1, len(population)):
            distance = euclidean_distance(population[i], population[j])
            distances.append((distance, i, j))
    
    # Проверим, есть ли расстояния для нормализации
    if not distances:
        return population
    
    # Найдем минимальное и максимальное расстояния
    min_dist = min(distances, key=lambda x: x[0])[0]
    max_dist = max(distances, key=lambda x: x[0])[0]

    # Если минимальное и максимальное расстояние равны, возвращаем исходную популяцию
    if min_dist == max_dist:
        return population
    
    # Нормализуем расстояния
    normalized_distances = [(i, j, (d - min_dist) / (max_dist - min_dist)) for d, i, j in distances]
    
    # Применим пороговое значение
    for i, j, normalized_distance in normalized_distances:
        if normalized_distance < threshold:
            if evaluate(population[i]) < evaluate(population[j]):
                to_remove.add(j)
            else:
                to_remove.add(i)
                    
    # Возвращаем обновленный список, исключая элементы, индексы которых содержатся в to_remove
    return [cell for i, cell in enumerate(population) if i not in to_remove]

# Основная функция
def artificial_immune_system(equations, pop_size, max_pop, n_c=10, threshold=0.2):
    # Запускаем таймер для измерения времени выполнения
    start_time = time()
    
    global eqs, variables, comp_count
    # Разбор уравнения на составляющие и сохранение в глобальные переменные
    eqs, variables = parse_equations(equations)
    # Определение количества компонент (переменных в уравнении)
    comp_count = len(variables)
    # Генерация начальной популяции
    population = generate_population(pop_size)
    # Инициализация клеток памяти
    memory_cells = []

    # Основной цикл алгоритма, повторяется заданное max_pop раз
    for _ in range(max_pop):
        # Клонирование клеток
        cloned_population = []
        for cell in population:
            cloned_population.extend([clone(cell) for _ in range(n_c)])
        population = cloned_population.copy()

        # Мутации
        for i in range(len(population)):
            cell = population[i]
            cell = mutate1(cell)
            if evaluate(cell) != 0:
                cell = mutate2(cell)
                if evaluate(cell) != 0:
                    cell = mutate3(cell)
            population[i] = cell

        # Добавление в память клеток с нулевым значением целевой функции
        scores = evaluate_population(population)
        for i, score in enumerate(scores):
            if score == 0:
                solution = dict(zip(variables, population[i]))
                solution_str = ", ".join(f"{var}={solution[var]}" for var in variables)
                if solution_str not in memory_cells:
                    memory_cells.append(solution_str)

        # Клональный отбор
        population = clonal_selection(population, scores, pop_size)

        # Процедура сжатия
        population = compression(population, threshold)
        pop_size = len(population)

    execution_time = time() - start_time

    return memory_cells, execution_time

if __name__ == "__main__":
    # Запуск системы
    result, execution_time = artificial_immune_system(
        equations="a = b, (1 - 9*a^3)^3 + (3*b - 9*b^4)^3 + 205891132094648 = 0", 
        pop_size=50, 
        max_pop=200
    )

    if result:
        solutions_str = ";\n".join(result)
        output = f"Найденные решения:\n{solutions_str}."
    else:
        output = "Решение не найдено."

    output += f"\nВремя выполнения искусственной иммунной сети: {execution_time:.2f} с."
    
    print(output)
