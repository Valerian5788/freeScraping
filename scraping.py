import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import mplcursors


# URL de la page des annonces
url = 'https://www.free-work.com/fr/tech-it/jobs?query='

# List to store scraped data
data = []
counts_by_week = {}

compteur = 0  # Initialize compteur outside of the function
name =""

def scrape_annonces(cible: str, result_label: ttk.Label, page=1):
    global compteur  # Declare compteur as global
    global counts_by_week  # Declare counts_by_week as global
    global name
    name = cible
    while True:
        # Envoyer une requête GET à la page des annonces
        response = requests.get(url + cible + f'&page={page}')
        if response.status_code != 200:
            result_label.config(text=f"Échec de la requête: {response.status_code}")
            return compteur

        # Parser le contenu de la page avec BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Trouver toutes les annonces
        annonces = soup.find_all('div', class_='mb-4 relative rounded-lg max-full bg-white flex flex-col cursor-pointer shadow hover:shadow-md')

        # Compter le nombre d'annonces contenant le mot-clé
        for annonce in annonces:
            texte_annonce = annonce.text.lower()
            if cible.lower() in texte_annonce:
                print(texte_annonce)
                compteur += 1
                
                # Extract the date
                date_div = annonce.find('div', {'class': 'text-sm whitespace-nowrap'})
                date = date_div.find('time').text
                date = datetime.strptime(date, "%d/%m/%Y")

                # Find the start of the week for this date
                start_of_week = date - timedelta(days=date.weekday())
                # Increment the count for this week
                if start_of_week in counts_by_week:
                    counts_by_week[start_of_week] += 1
                else:
                    counts_by_week[start_of_week] = 1

        # Check if there is a next page
        # Find all buttons with the class
        buttons = soup.find_all('button', class_='flex items-center gap-2 h-8 min-w-[2rem] px-3 inline-flex items-center justify-center rounded-md font-semibold text-sm border border-transparent outline-none focus:outline-none transition-all duration-200 text-primary bg-gray-100 hover:bg-gray-200')

        # Identify the next page button by its text
        next_page_button = None
        for button in buttons:
            if button.text.strip() == "Suivant":
                next_page_button = button
                break

        # Now you can use next_page_button as before
        if next_page_button is not None and not next_page_button.has_attr('disabled'):
        # There is a next page
            print(f"Scraping page {page + 1}")
            page += 1
        else:
            # There is no next page
            print("No more pages")
            break

    # Store the data in a global list
    date_scraping = datetime.now().strftime('%Y-%m-%d')
    data.append({'date': date_scraping, 'mot_cle': cible, 'nombre': compteur})

    # Afficher le nombre d'annonces trouvées
    result_label.config(text=f"Nombre d'annonces '{cible}' trouvées: {compteur}")
    return compteur

# Fonction pour démarrer le scraping lorsqu'on clique sur le bouton
def start_scraping():
    mot_cle = entry.get()
    if not mot_cle:
        result_label.config(text="Veuillez entrer un mot-clé.")
        return
    scrape_annonces(mot_cle, result_label)

# Fonction pour afficher le graphique
def afficher_graphique():
    if not counts_by_week:
        result_label.config(text="Pas de données disponibles pour afficher le graphique.")
        return

    # Convert the dictionary to a DataFrame
    df = pd.DataFrame(list(counts_by_week.items()), columns=['date', 'nombre'])
    df.set_index('date', inplace=True)
    df = df.resample('W').sum()  # Resample by week

    plt.figure(figsize=(10, 5))
    line, = plt.plot(df.index, df['nombre'], marker='o')  # Save the line object
    plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator())  # Set major ticks to weekly
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format date
    plt.title(f"Nombre d'annonces {name} par semaine")
    plt.xlabel("Date")
    plt.ylabel("Nombre d'annonces")
    plt.grid(True)

    # Add interactivity
    cursor = mplcursors.cursor(line, hover=True)
    cursor.connect(
        "add", lambda sel: sel.annotation.set_text(f"Date: {mdates.num2date(sel.target[0]).strftime('%Y-%m-%d')}\nNombre d'annonces: {sel.target[1]}")
    )

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
