import tkinter as tk
from tkinter import ttk, scrolledtext
import requests
from bs4 import BeautifulSoup

# URL de la page des annonces
url = 'https://www.free-work.com/fr/tech-it/jobs?query='

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

    # Afficher le nombre d'annonces trouvées
    result_label.config(text=f"Nombre d'annonces '{cible}' cette semaine: {compteur}")

# Fonction pour démarrer le scraping lorsqu'on clique sur le bouton
def start_scraping():
    mot_cle = entry.get()
    scrape_annonces(mot_cle, result_label)

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

# Configuration de la grille pour redimensionner correctement
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# Lancer la boucle principale de l'interface graphique
root.mainloop()

# # Planifier l'exécution du script chaque semaine
# schedule.every().week.do(scrape_annonces)

# # Lancer une boucle pour exécuter les tâches planifiées
# while True:
#     schedule.run_pending()
#     time.sleep(1)
    
    