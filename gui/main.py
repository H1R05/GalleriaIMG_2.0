import tkinter as tk
import ttkbootstrap as ttk
from login import PannelloLogin

class ApplicazionePrincipale(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Galleria Immagini Samu - V2.0")
        self.style = ttk.Style()
        self.style.theme_use("darkly")
        self.geometry("1100x800")
        self.minsize(1100, 800)
        self.token_acquisito = None

        # Passo 'self' come argomento, dicendogli: "Io sono il tuo master (genitore)"
        self.panello_login = PannelloLogin(self)
        self.panello_login.pack(expand=True, fill="both")

    def login_completato(self, token_ricevuto):
        """Viene innescato da login.py quando l'accesso ha successo."""
        # Carico i moduli pesanti solo qui, non all'avvio
        from vista_galleria import PannelloGalleria
        
        # Salvo il token per le future richieste al server
        self.token_jwt = token_ricevuto
        print(f"Login effettuato! Token salvato in memoria: {self.token_jwt}")

        # Tolgo di mezzo il login e carico la galleria
        if hasattr(self, "panello_login"):
            self.panello_login.pack_forget()

        self.pannello_galleria = PannelloGalleria(self)
        self.pannello_galleria.pack(fill=tk.BOTH, expand=True)
        self.pannello_galleria.aggiorna_stato_auth()

if __name__ == "__main__":
    app = ApplicazionePrincipale()
    app.mainloop()