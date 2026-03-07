import threading
from ultralytics import YOLO

def esegui_rilevamento_yolo_locale(image_path, callback_aggiornamento_ui):
    """
    Esegue YOLO in locale (Edge Computing) senza chiamate di rete.
    """
    def worker():
        try:
            # Carica il modello localmente (lo scarica la prima volta se non c'è)
            model = YOLO("yolov8n.pt") 
            
            # Esegue l'analisi locale
            risultati = model(image_path)
            
            oggetti_trovati = []
            for risultato in risultati:
                for box in risultato.boxes:
                    class_id = int(box.cls[0])
                    oggetti_trovati.append(model.names[class_id])
            
            if not oggetti_trovati:
                esito = "Nessun oggetto riconosciuto dall'IA."
                colore_stato = "inverse-warning"
                etichetta_dominante = None
            else:
                # Estraiamo la prima etichetta trovata (es. "car" o "person")
                etichetta_dominante = oggetti_trovati[0] 
                esito = f"✅ Trovati: {', '.join(oggetti_trovati)}"
                colore_stato = "inverse-success"
                
            # Restituiamo l'esito alla GUI, passando anche l'etichetta dominante
            # che ci servirà per il Punto 3 del tuo schema!
            callback_aggiornamento_ui(esito, colore_stato, etichetta_dominante)
            
        except Exception as e:
            esito = f"❌ Errore IA locale: {str(e)}"
            callback_aggiornamento_ui(esito, "inverse-danger", None)

    # YOLO è pesante per la CPU, usiamo un thread per non bloccare Tkinter
    thread_ia = threading.Thread(target=worker)
    thread_ia.daemon = True
    thread_ia.start()