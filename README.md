import customtkinter as ctk
from tkinter import messagebox
import itertools
import re

# --- SOPORTE DE RESOLUCIÓN ---
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class LogicMasterPro(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Proyecto Final - Logica de Sistemas")
        self.geometry("1100x850")
        self.configure(fg_color="#FFFFFF")

        # Colores 
        self.blue, self.red, self.yellow, self.green = "#4285F4", "#EA4335", "#FBBC05", "#34A853"
        
        self.setup_ui()

    def traducir_a_python(self, exp):
        """ Lógica del grupo integrada y mejorada """
        # Bicondicional: (A and B) or (not A and not B)
        while "↔" in exp:
            exp = re.sub(r'(\w+|\))\s*↔\s*(\w+|\()', r'((\1 and \2) or (not \1 and not \2))', exp)
        # Condicional: not A or B
        while "→" in exp:
            exp = re.sub(r'(\w+|\))\s*→\s*(\w+|\()', r'(not \1 or \2)', exp)
        
        # Reemplazos directos
        exp = exp.replace("∧", " and ").replace("∨", " or ").replace("¬", " not ").replace("⊕", " ^ ")
        return exp

    def setup_ui(self):
        # Título
        ctk.CTkLabel(self, text="Calculadora Lógica", font=("Product Sans", 40, "bold"), text_color=self.blue).pack(pady=(20, 5))
        
        # Entrada de texto
        self.entry = ctk.CTkEntry(self, placeholder_text="Ejemplo: A ∧ B → C", width=600, height=50, font=("Product Sans", 18))
        self.entry.pack(pady=20)

        # Teclado de Símbolos (Para que el usuario no tenga que buscarlos)
        self.sym_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.sym_frame.pack(pady=10)

        simbolos = [("∧", self.blue), ("∨", self.green), ("¬", self.red), ("→", self.yellow), ("↔", "#5F6368"), ("⊕", "#5F6368")]
        for sym, col in simbolos:
            ctk.CTkButton(self.sym_frame, text=sym, width=60, fg_color="#FFFFFF", text_color=col, border_color=col, border_width=2,
                          font=("Consolas", 20, "bold"), command=lambda s=sym: self.entry.insert("insert", s)).pack(side="left", padx=5)

        # Botones Acción
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.pack(pady=20)
        
        ctk.CTkButton(self.action_frame, text="GENERAR TABLA", fg_color=self.blue, font=("Product Sans", 14, "bold"), height=45,
                      command=self.procesar).pack(side="left", padx=10)
        ctk.CTkButton(self.action_frame, text="LIMPIAR", fg_color="#F8F9FA", text_color="#5F6368", border_width=1, height=45,
                      command=lambda: [self.entry.delete(0, 'end'), self.txt.delete("1.0", "end")]).pack(side="left", padx=10)

        # Resultado
        self.txt = ctk.CTkTextbox(self, width=900, height=450, font=("Consolas", 18), corner_radius=15, border_width=2)
        self.txt.pack(pady=10, padx=50)

    def procesar(self):
        original_exp = self.entry.get()
        if not original_exp: return

        # Detectar variables (Letras Mayúsculas)
        vars_found = sorted(list(set(re.findall(r'[A-Z]', original_exp))))
        if not vars_found:
            messagebox.showerror("Error", "Usa letras mayúsculas para las variables (A, B, C...)")
            return

        try:
            exp_py = self.traducir_a_python(original_exp)
            
            # Encabezado
            self.txt.delete("1.0", "end")
            header = "  " + "  ".join(vars_found) + "  |  RESULTADO\n"
            self.txt.insert("end", header + "-"*len(header) + "\n")

            # Tabla
            combos = list(itertools.product([True, False], repeat=len(vars_found)))
            results = []
            
            for c in combos:
                d = dict(zip(vars_found, c))
                res = eval(exp_py, {"__builtins__": {}}, d)
                results.append(res)
                
                vals_str = "  ".join(["1" if v else "0" for v in c])
                res_str = "1" if res else "0"
                self.txt.insert("end", f"  {vals_str}  |      {res_str}\n")

            # Clasificación
            self.txt.insert("end", "\n" + "="*30 + "\n")
            if all(results): self.txt.insert("end", "TIPO: TAUTOLOGÍA 🟢")
            elif not any(results): self.txt.insert("end", "TIPO: CONTRADICCIÓN 🔴")
            else: self.txt.insert("end", "TIPO: CONTINGENCIA 🟡")

        except Exception as e:
            messagebox.showerror("Error de Sintaxis", "Revisa la expresión. Asegúrate de usar espacios o paréntesis si es compleja.")

if __name__ == "__main__":
    app = LogicMasterPro()
    app.mainloop()
