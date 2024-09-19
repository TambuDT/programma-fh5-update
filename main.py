import tkinter as tk
from tkinter import messagebox, font
import requests
import webbrowser

# Funzione per controllare la versione
def check_version():
    try:
        # Leggi la versione attuale dal file
        with open('version.txt', 'r') as file:
            current_version = file.read().strip()
        
        # Ottieni la versione dal servizio web
        response = requests.get('https://fh5-update-scraper-api.onrender.com/scrape')
        data = response.json()
        latest_version = data['data']['version'].strip()
        magnet_link = data['data']['link'].strip()  # Recupera il magnet link
        
        # Aggiorna l'interfaccia utente
        latest_version_label.config(text=f"Versione disponibile: {latest_version}")

        # Mostra messaggio appropriato
        if current_version != latest_version:
            current_version_label.config(text=f"Versione installata: {current_version}")
            download_button.config(command=lambda: open_magnet_link(magnet_link, latest_version))
            download_button.grid(row=2, column=0, pady=20, sticky='n')
        else:
            current_version_label.config(text=f"Versione installata: {current_version}")
            latest_version_label.config(text="Non ci sono aggiornamenti")
            download_button.grid_forget()
    except Exception as e:
        messagebox.showerror("Errore", f"Si è verificato un errore: {e}")

# Funzione per aprire il magnet link e aggiornare la versione
def open_magnet_link(magnet_link, latest_version):
    try:
        # Apri il link magnetico
        webbrowser.open(magnet_link)
        # Aggiorna il file con la nuova versione
        with open('version.txt', 'w') as file:
            file.write(latest_version)
        messagebox.showinfo("Link Magnet Aperto", "Il link magnetico è stato aperto nel tuo browser e la versione è stata aggiornata.")
    except Exception as e:
        messagebox.showerror("Errore", f"Si è verificato un errore durante l'apertura del link magnetico: {e}")

# Funzione per cambiare lo stile del pulsante su hover
def on_enter(event):
    download_button.config(bg="#4CAF50", fg="#ffffff", borderwidth=2, relief='solid')  # Tutto verde, senza bordo

def on_leave(event):
    download_button.config(bg="#202225", fg="#f9f9f7", borderwidth=2, relief='solid')  # Bordo verde

# Creazione della finestra principale
root = tk.Tk()
root.title("FH5 Update")
root.geometry("400x400")  # Imposta la dimensione della finestra
root.configure(bg="#202225")  # Colore di sfondo della finestra

# Creazione di un frame centrale per il layout
frame = tk.Frame(root, bg="#202225", padx=20, pady=20)
frame.place(relx=0.5, rely=0.5, anchor='center')

# Configura font
header_font = font.Font(family="Helvetica", size=12, weight="bold")  # Font più piccolo
text_font = font.Font(family="Helvetica", size=12)  # Font più piccolo

# Etichette per le versioni
current_version_label = tk.Label(frame, text="Versione attuale: ...", font=text_font, bg="#202225", fg="#f9f9f7")
current_version_label.grid(row=0, column=0, pady=10)

latest_version_label = tk.Label(frame, text="Versione disponibile: ...", font=text_font, bg="#202225", fg="#f9f9f7")
latest_version_label.grid(row=1, column=0, pady=10)

# Pulsante di download
download_button = tk.Button(frame, text="Download", font=header_font, bg="#202225", fg="#f9f9f7", height=1, width=12, relief='solid', borderwidth=2, highlightbackground="#4CAF50", highlightcolor="#4CAF50")
download_button.grid(row=2, column=0, pady=20, sticky='n')

# Bind dell'evento di hover
download_button.bind("<Enter>", on_enter)
download_button.bind("<Leave>", on_leave)

# Controlla la versione all'avvio
check_version()

# Avvia l'interfaccia utente
root.mainloop()
