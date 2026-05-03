import customtkinter as ctk
from tkinter import messagebox
import itertools
import re

# --- MEJORA DE RESOLUCIÓN ---
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# Configuración de tema
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class TruthTableApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Ventana principal
        self.title("Proyecto Final Logica De Sistemas")
        self.geometry("1050x850")
        self.configure(fg_color="#FFFFFF")

        # Paleta de Colores Oficiales de Google
        self.google_blue = "#4285F4"
        self.google_red = "#EA4335"
        self.google_yellow = "#FBBC05"
        self.google_green = "#34A853"
        self.google_gray = "#F8F9FA"
        self.text_dark = "#202124"

        self.setup_ui()

    def setup_ui(self):
        # Título Principal
        ctk.CTkLabel(self, text="Calculadora Lógica", font=("Product Sans", 40, "bold"), text_color=self.google_blue).pack(pady=(30, 5))
        ctk.CTkLabel(self, text="Generador de Tablas de Verdad ", font=("Product Sans", 18), text_color="#5F6368").pack(pady=(0, 25))

        # --- SECCIÓN DE ENTRADA ---
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(pady=10, fill="x", padx=60)

        self.entry_exp = ctk.CTkEntry(
            self.input_frame, placeholder_text="Escribe tu expresión",  #(ej: p and q or not r)
            width=500, height=55, border_width=2, border_color="#E0E0E0", 
            fg_color=self.google_gray, text_color=self.text_dark, font=("Product Sans", 18)
        )
        self.entry_exp.pack(side="left", padx=(0, 10), expand=True, fill="x")

        # Botón GENERAR
        self.btn_generate = ctk.CTkButton(
            self.input_frame, text="GENERAR", command=self.generate_table,
            fg_color=self.google_blue, hover_color="#3367D6",
            font=("Product Sans", 14, "bold"), height=55, width=140
        )
        self.btn_generate.pack(side="left", padx=5)

        # Botón LIMPIAR
        self.btn_clear = ctk.CTkButton(
            self.input_frame, text="LIMPIAR",
            command=self.clear_all,
            fg_color="#FFFFFF", hover_color="#F1F3F4", text_color="#5F6368",
            border_color="#E0E0E0", border_width=2,
            font=("Product Sans", 14, "bold"), height=55, width=110
        )
        self.btn_clear.pack(side="left", padx=5)

        # --- BOTONES DE ACCESO RÁPIDO---
        self.btns_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btns_frame.pack(pady=20)

        operators_config = [
            ("and", self.google_blue),
            ("or", self.google_green),
            ("not", self.google_red),
            ("xor", self.google_yellow),
            ("(", "#5F6368"),
            (")", "#5F6368")
        ]

        for op, color in operators_config:
            ctk.CTkButton(
                self.btns_frame, text=op.upper(), width=90, height=40,
                fg_color="#FFFFFF", text_color=color, border_color=color,
                border_width=2, hover_color="#F8F9FA",
                font=("Consolas", 14, "bold"),
                command=lambda o=op: self.entry_exp.insert("insert", f" {o} ")
            ).pack(side="left", padx=8)

        # --- ÁREA DE RESULTADO ---
        self.result_frame = ctk.CTkTextbox(
            self, width=900, height=450, font=("Consolas", 20), 
            border_width=2, border_color="#E0E0E0", fg_color="#FFFFFF",
            text_color=self.text_dark, corner_radius=15
        )
        self.result_frame.pack(pady=10, padx=60)

    def clear_all(self):
        self.entry_exp.delete(0, 'end')
        self.result_frame.delete("1.0", "end")

    def generate_table(self):
        exp_input = self.entry_exp.get().lower()
        if not exp_input:
            messagebox.showwarning("Atención", "Por favor, ingresa una expresión primero.")
            return

        self.result_frame.delete("1.0", "end")
        variables = sorted(list(set(re.findall(r'\b[a-z]\b', exp_input))))
        
        if not variables:
            messagebox.showerror("Error", "No se detectaron variables. Usa letras minúsculas (p, q, r...).")
            return

        try:
            header = "  " + "   ".join(variables).upper() + "   |   RESULTADO"
            self.result_frame.insert("end", header + "\n")
            self.result_frame.insert("end", "-" * (len(header) + 5) + "\n")

            combinations = list(itertools.product([True, False], repeat=len(variables)))
            results_list = []

            for combo in combinations:
                vals = dict(zip(variables, combo))
                res = eval(exp_input, {"__builtins__": None}, vals)
                results_list.append(res)
                
                row_vals = [(" V " if v else " F ") for v in combo]
                row_res = "VERDADERO" if res else "FALSO"
                self.result_frame.insert("end", "  " + "  ".join(row_vals) + f"  |   {row_res}\n")

            self.result_frame.insert("end", "\n" + "="*40 + "\n")
            if all(results_list):
                self.result_frame.insert("end", "CLASIFICACIÓN: TAUTOLOGÍA 🟢")
            elif not any(results_list):
                self.result_frame.insert("end", "CLASIFICACIÓN: CONTRADICCIÓN 🔴")
            else:
                self.result_frame.insert("end", "CLASIFICACIÓN: CONTINGENCIA 🟡")

        except Exception:
            messagebox.showerror("Error", "Expresión inválida. Revisa los paréntesis.")

if __name__ == "__main__":
    app = TruthTableApp()
    app.mainloop()