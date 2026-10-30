import operaciones as op
import tkinter as tk
from tkinter import ttk, messagebox


class CalculadoraMatriz(ttk.Frame):
    def __init__(self, ventana):
        super().__init__(ventana, padding=15)
        self.pack(fill="both", expand=True)

        self.expresion = ""
        self.pantalla_var = tk.StringVar(value="0")

        self.crear_widgets()

    def crear_widgets(self):
        pantalla = tk.Entry(
            self,
            textvariable=self.pantalla_var,
            font=("Consolas", 20, "bold"),
            justify="right",
            state="readonly",
        )
        pantalla.grid(row=0, column=0, columnspan=4, sticky="ew", ipady=10, pady=(0, 15))

        botones = [
            ('C', 1, 0), ('CE', 1, 1), ('±', 1, 2), ('÷', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('×', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('0', 5, 0), ('.', 5, 1), ('=', 5, 2),
        ]

        for i in range(4):
            self.columnconfigure(i, weight=1)
        for i in range(1, 6):
            self.rowconfigure(i, weight=1)

        for texto, fila, col in botones:
            btn = tk.Button(self, text=texto, command=lambda t=texto: self.al_presionar(t))
            span = 2 if texto == '=' else 1
            btn.grid(row=fila, column=col, columnspan=span, sticky="nsew", padx=2, pady=2)

    def al_presionar(self, tecla):
        if tecla in '0123456789.' and len(tecla) == 1:
            if self.expresion == "0" and tecla != '.':
                self.expresion = tecla
            else:
                self.expresion += tecla
            self.pantalla_var.set(self.expresion)

        elif tecla in ('+', '-', '×', '÷'):
            actual = self.expresion.strip()
            if actual and actual[-1] not in '+-×÷':
                self.evaluar_expresion()
                if self.expresion != "":
                    self.expresion = self.expresion.strip() + f" {tecla} "
                    self.pantalla_var.set(self.expresion)

        elif tecla == '=':
            self.evaluar_expresion()

        elif tecla == 'C':
            self.expresion = ""
            self.pantalla_var.set("0")

        elif tecla == 'CE':
            self.expresion = self.expresion.strip()[:-1].strip()
            self.pantalla_var.set(self.expresion if self.expresion else "0")

        elif tecla == '±':
            self.cambiar_signo()

    def cambiar_signo(self):
        if not self.expresion.strip() or self.expresion == "0":
            return
        partes = self.expresion.split(" ")
        # Cambia el signo del último número escrito
        ultimo = partes[-1]
        if ultimo == "":
            return
        if ultimo.startswith('-'):
            partes[-1] = ultimo[1:]
        else:
            partes[-1] = '-' + ultimo
        self.expresion = " ".join(partes)
        self.pantalla_var.set(self.expresion)

    def evaluar_expresion(self):
        partes = self.expresion.strip().split()
        if len(partes) != 3:
            return

        try:
            num1 = float(partes[0])
            operador = partes[1]
            num2 = float(partes[2])

            if operador == '+':
                res = op.sumar(num1, num2)
            elif operador == '-':
                res = op.restar(num1, num2)
            elif operador == '×':
                res = op.multiplicar(num1, num2)
            elif operador == '÷':
                res = op.dividir(num1, num2)
            else:
                return

            if res.is_integer():
                res = int(res)
            else:
                res = round(res, 4)

            self.expresion = str(res)
            self.pantalla_var.set(self.expresion)

        except ZeroDivisionError as err:
            messagebox.showerror("Error", str(err))
            self.expresion = ""
            self.pantalla_var.set("Error")
        except ValueError:
            messagebox.showerror("Error", "Entrada inválida.")
            self.expresion = ""
            self.pantalla_var.set("Error")


if __name__ == "__main__":
    ventana = tk.Tk()
    ventana.title("Calculadora Matriz")
    ventana.geometry("320x400")
    ventana.minsize(280, 350)
    app = CalculadoraMatriz(ventana)
    ventana.mainloop()
