import ttkbootstrap as ttk
import requests as req
import tkinter as tk
from tkinter import messagebox
from ttkbootstrap.constants import *


class FinestraLogin(ttk.Frame):
    def __init__(self, master_app):
        super().__init__(master_app)
        # Chiamiamo la funzione che "arreda" la stanza
        self._crea_widget_login()

    def chiusura_forzata(self):
        """Utente preme x termina programma"""
        self.master.destroy()

    def _crea_widget_login(self):
        """Crea fisicamente le etichette, le caselle di testo e il bottone."""
        # Un frame con un po' di margine (padding) per non avere tutto appiccicato ai bordi
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # Titolo
        ttk.Label(frame, text="Inserisci le credenziali", font=("Arial", 12, "bold")).pack(pady=(0, 15))

        # --- Campo Username ---
        ttk.Label(frame, text="Username:").pack(anchor=tk.W)
        # ttk.Entry è la casella in cui l'utente può digitare
        self.entry_username = ttk.Entry(frame)
        self.entry_username.pack(fill=tk.X, pady=(0, 10))

        # --- Campo Password ---
        ttk.Label(frame, text="Password:").pack(anchor=tk.W)
        # show="*" è il trucco di sicurezza per coprire i caratteri digitati
        self.entry_password = ttk.Entry(frame, show="*")
        self.entry_password.pack(fill=tk.X, pady=(0, 20))

        # --- Bottone di Invio ---
        # Il parametro command=self._tenta_connessione dice al bottone quale funzione eseguire al click
        self.btn_accedi = ttk.Button(frame, text="Accedi", command=self._tenta_connessione, bootstyle=PRIMARY)
        self.btn_accedi.pack(fill=tk.X)

    def _tenta_connessione(self):
        """La funzione che scatta quando l'utente preme 'Accedi'."""
        # 1. Aspiriamo il testo che l'utente ha digitato nelle caselle
        user = self.entry_username.get()
        pwd = self.entry_password.get()

        # Se l'utente ha lasciato i campi vuoti, lo blocchiamo subito (risparmiamo una chiamata di rete inutile)
        if not user or not pwd:
            messagebox.showwarning("Attenzione", "Devi inserire sia username che password.")
            return

        # 2. Prepariamo la busta da spedire al nostro container Docker
        url_server = "http://localhost:5000/login"
        dati_da_inviare = {"username": user, "password": pwd}

        # Cambiamo il testo del bottone per far capire all'utente che stiamo caricando
        self.btn_accedi.config(text="Connessione in corso...", state=tk.DISABLED)
        self.update() # Forza Tkinter ad aggiornare la grafica immediatamente

        # 3. La telefonata vera e propria (dentro un try/except per sicurezza)
        try:
            # Ricordi? Il professore ha usato methods=['GET'], quindi usiamo requests.get
            # Il parametro 'timeout=3' è vitale per un DevOps: se il server non risponde in 3 secondi, annulla tutto.
            risposta = req.post(url_server, json=dati_da_inviare, timeout=3)

            # 4. Leggiamo la risposta
            if risposta.status_code == 200:
                # Login corretto!
                dati_json = risposta.json()
                self.master.token_acquisito = dati_json.get("token")
                
                if hasattr(self.master, "mostra_galleria"):
                    self.master.mostra_galleria()
            else:
                # Se il server ha risposto con Errore di autenticazione
                messagebox.showerror("Accesso Negato", "Username o password errati.")
                
        except req.exceptions.ConnectionError:
             messagebox.showerror("Errore di Rete", "Impossibile contattare il server.\nHai acceso il container Docker?")
        except req.exceptions.Timeout:
             messagebox.showerror("Errore di Rete", "Il server ci sta mettendo troppo tempo a rispondere.")
        finally:
            # Qualsiasi cosa succeda (successo o errore), se la finestra esiste ancora, riattiviamo il bottoneccendere il servizio)
            if self.winfo_exists():
                self.btn_accedi.config(text="Accedi", state=tk.NORMAL)