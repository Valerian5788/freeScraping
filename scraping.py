import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

# URL de la page des annonces
url = 'https://www.free-work.com/fr/tech-it/jobs?query='

# Initialiser la base de données SQLite
conn = sqlite3.connect('annonces.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS annonces (date TEXT, mot_cle TEXT, nombre INTEGER)''')
conn.commit()

def scrape_annonces(cible: str, result_label: ttk.Label):
    # Envoyer une requête GET à la page des annonces
    response = requests.get(url + cible)
    if response.status_code != 200:
        result_label.config(text=f"Échec de la requête: {response.status_code}")
        return

    # Parser le contenu de la page avec BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Trouver toutes les annonces
    annonces = soup.find_all('div', class_='mb-4 relative rounded-lg max-full bg-white flex flex-col cursor-pointer shadow hover:shadow-md')

    # Compter le nombre d'annonces contenant le mot-clé
    compteur = 0
    for annonce in annonces:
        texte_annonce = annonce.text.lower()
        if cible.lower() in texte_annonce:
            compteur += 1

    # Enregistrer les données dans la base de données
    date_scraping = datetime.now().strftime('%Y-%m-%d')
    c.execute('INSERT INTO annonces (date, mot_cle, nombre) VALUES (?, ?, ?)', (date_scraping, cible, compteur))
    conn.commit()

    # Afficher le nombre d'annonces trouvées
    result_label.config(text=f"Nombre d'annonces '{cible}' cette semaine: {compteur}")

# Fonction pour démarrer le scraping lorsqu'on clique sur le bouton
def start_scraping():
    mot_cle = entry.get()
    scrape_annonces(mot_cle, result_label)

# Fonction pour afficher le graphique
def afficher_graphique():
    df = pd.read_sql_query('SELECT date, mot_cle, SUM(nombre) as nombre FROM annonces WHERE mot_cle = "python" GROUP BY date ORDER BY date', conn)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df = df.resample('W').sum()

    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df['nombre'], marker='o')
    plt.title("Nombre d'annonces 'Python' par semaine")
    plt.xlabel("Date")
    plt.ylabel("Nombre d'annonces")
    plt.grid(True)
    plt.show()

# Création de la fenêtre principale
root = tk.Tk()
root.title("Scraping d'annonces")

# Création d'un cadre pour le champ d'entrée et le bouton
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Champ d'entrée pour le mot-clé
ttk.Label(frame, text="Mot-clé:").grid(row=0, column=0, sticky=tk.W)
entry = ttk.Entry(frame, width=30)
entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

# Bouton pour lancer le scraping
button = ttk.Button(frame, text="Lancer le scraping", command=start_scraping)
button.grid(row=0, column=2, sticky=tk.W)

# Étiquette pour afficher les résultats
result_label = ttk.Label(root, text="", padding="10")
result_label.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Bouton pour afficher le graphique
graph_button = ttk.Button(root, text="Afficher le graphique", command=afficher_graphique)
graph_button.grid(row=2, column=0, sticky=tk.W)

# Configuration de la grille pour redimensionner correctement
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# Lancer la boucle principale de l'interface graphique
root.mainloop()

# Fermer la connexion à la base de données lors de la fermeture du programme
conn.close()


# # Planifier l'exécution du script chaque semaine
# schedule.every().week.do(scrape_annonces)

# # Lancer une boucle pour exécuter les tâches planifiées
# while True:
#     schedule.run_pending()
#     time.sleep(1)
    
    