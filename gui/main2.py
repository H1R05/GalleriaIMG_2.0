import tkinter as tk
from tkinter import ttk
from ttkbootstrap.constants import *

# IMPORTANTE: Importiamo il mattoncino che abbiamo creato nell'altro file!
from login import FinestraLogin

class FinestraPrincipale(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Architettura Modulare DevOps")
        self.geometry("460x350")
        self.token_acquisito = None

        # 1. Istanziamo (creiamo) il nostro mattoncino Login.
        # Passiamo 'self' come argomento, dicendogli: "Io sono il tuo master (genitore)"
        self.vista_login = FinestraLogin(self)
        self.vista_login.pack(expand=True, fill="both")

    def login_completato(self):
        self.vista_login.pack_forget()

        print("Login effettuato!")

        label_temporanera = ttk.Label(self, text="Benvenuto", font=("Arial", 16), justify=tk.CENTER)
        label_temporanera.pack(expand=True)

# Il blocco di esecuzione standard
if __name__ == "__main__":
    app = FinestraPrincipale()
    app.mainloop()