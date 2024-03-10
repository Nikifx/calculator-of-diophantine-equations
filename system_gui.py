import tkinter as tk
from tkinter import scrolledtext
from artificial_immune_system import artificial_immune_system

class DiophantineSolverApp:
    def __init__(self, master):
        self.master = master
        master.title("Решатель диофантовых уравнений")

        self.equation_label = tk.Label(master, text="Диофантово уравнение:")
        self.equation_label.pack()

        self.equation_entry = tk.Entry(master)
        self.equation_entry.pack()

        self.cells_count_label = tk.Label(master, text="Число клеток в популяции:")
        self.cells_count_label.pack()

        self.cells_count_entry = tk.Entry(master)
        self.cells_count_entry.pack()

        self.max_populations_label = tk.Label(master, text="Максимальное число популяций:")
        self.max_populations_label.pack()

        self.max_populations_entry = tk.Entry(master)
        self.max_populations_entry.pack()

        self.solve_button = tk.Button(master, text="Готово", command=self.solve)
        self.solve_button.pack()

        self.solutions_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=40, height=10)
        self.solutions_text.config(state=tk.DISABLED)
        self.solutions_text.pack()

    def solve(self):
        try:
            equation = self.equation_entry.get()
            
            # Попытка преобразовать входные данные в целые числа
            cells_count = int(self.cells_count_entry.get())
            max_populations = int(self.max_populations_entry.get())
        except ValueError:
            # Обработка случая, когда ввод не может быть преобразован в целое число
            self.solutions_text.config(state=tk.NORMAL)
            self.solutions_text.delete('1.0', tk.END)
            self.solutions_text.insert(tk.END, "Ошибка: Неверный формат ввода. Пожалуйста, введите корректные числа.\n")
            self.solutions_text.config(state=tk.DISABLED)
            return

        # Если мы здесь, значит преобразование прошло успешно и можно продолжить
        # Здесь должен быть вызов функции решения диофантова уравнения
        result, execution_time = artificial_immune_system(equation, cells_count, max_populations)

        if result:
            solutions_str = ";\n".join(result)
            output = f"Найденные решения:\n{solutions_str}."
        else:
            output = "Решение не найдено."

        output += f"\nВремя выполнения искусственной иммунной сети: {execution_time:.2f} секунды."

        self.solutions_text.config(state=tk.NORMAL)
        self.solutions_text.delete('1.0', tk.END)
        self.solutions_text.insert(tk.END, output)
        self.solutions_text.config(state=tk.DISABLED)


def main():
    root = tk.Tk()
    app = DiophantineSolverApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
