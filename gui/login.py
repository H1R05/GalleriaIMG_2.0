import ttkbootstrap as ttk
import requests as req
import tkinter as tk
from tkinter import messagebox
from ttkbootstrap.constants import *


class PannelloLogin(ttk.Frame):
    def __init__(self, master_app):
        super().__init__(master_app, padding=20)
        
        self.app_principale = master_app

        self._crea_widget_login()

    def chiusura_forzata(self):
        """Utente preme x termina programma"""
        self.master.destroy()

    def _crea_widget_login(self):
        self.card_login = ttk.Frame(self, padding=40)
        self.card_login.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        ttk.Label(self.card_login, text="Accesso di Sicurezza", font=("Segoe UI", 18, "bold")).pack(pady=(0, 5))
        ttk.Label(self.card_login, text="Inserisci le tue credenziali per continuare", font=("Segoe UI", 10), foreground="gray").pack(pady=(0, 25))

        # Area per mostrare gli errori
        self.lbl_errore = ttk.Label(self.card_login, text="", font=("Segoe UI", 9), foreground="red")
        self.lbl_errore.pack(anchor=tk.W, pady=(0, 15), fill=tk.X)

        ttk.Label(self.card_login, text="username", font=("Segoe UI", 9, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.ent_username = ttk.Entry(self.card_login, width=35)
        self.ent_username.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(self.card_login, text="password", font=("Segoe UI", 9, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.ent_password = ttk.Entry(self.card_login, width=35, show="*")
        self.ent_password.pack(fill=tk.X, pady=(0, 25))

        self.ent_password.bind("<Return>", lambda e: self._tenta_connessione())

        self.btn_login = ttk.Button(self.card_login, text="Accedi al Sistema", bootstyle="primary", command=self._tenta_connessione)
        self.btn_login.pack(fill=tk.X, pady=(0, 10))

        ttk.Separator(self.card_login).pack(fill=tk.X, pady=15)

        self.btn_ospite = ttk.Button(self.card_login, text="Accedi come ospite", bootstyle="secondary", command=self._accesso_ospite)
        self.btn_ospite.pack(fill=tk.X)
        
        self._timer_errore = None
    
    def _accesso_ospite(self):
        """Salta il login e va diretto nella galleria - utile per lavorare offline."""
        self.app_principale.login_completato(None)

    def _tenta_connessione(self):
        """La funzione che scatta quando l'utente preme 'Accedi' o il tasto Invio."""
        user = self.ent_username.get()
        pwd = self.ent_password.get()

        if not user or not pwd:
            self._mostra_errore("Inserisci username e password")
            return
            
        url_server = "http://localhost:5000/login"
        dati_da_inviare = {"username": user, "password": pwd}

        self.btn_login.config(text="Connessione in corso...", state=tk.DISABLED)
        self.update_idletasks()
        
        try:
            # Timeout di 3 secondi - altrimenti se il server non c'è l'interfaccia si blocca
            risposta = req.post(url_server, json=dati_da_inviare, timeout=3)

            if risposta.status_code == 200:
                dati_json = risposta.json()
                token_acquisito = dati_json.get("token")
                
                if token_acquisito:
                    self.app_principale.login_completato(token_acquisito)
            else:
                self._mostra_errore("Username o password errati")
                
        except req.exceptions.ConnectionError:
             self._mostra_errore("Server non raggiungibile - Docker acceso?")
        finally:
            if self.winfo_exists():
                self.btn_login.config(text="Accedi al Sistema", state=tk.NORMAL)
    
    def _mostra_errore(self, messaggio):
        """Mostra un messaggio di errore nel label e lo nasconde dopo 4 secondi."""
        if self._timer_errore:
            self.after_cancel(self._timer_errore)
        
        self.lbl_errore.config(text=messaggio)
        self._timer_errore = self.after(4000, lambda: self.lbl_errore.config(text=""))