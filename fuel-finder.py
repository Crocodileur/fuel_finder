from lxml import etree
from geopy.geocoders import Nominatim
import os
import time
import wget
from os import path
import zipfile
from datetime import datetime
import traceback

URL = 'https://donnees.roulez-eco.fr/opendata/instantane'
date = str(datetime.today().strftime('%Y-%m-%d'))

# Téléchargement du fichier contenant les données des prix
while True:
    try:
        if path.exists('prix-carburant.xml')==True:
            os.remove('prix-carburant.xml')
        # print(path.exists('prix-carburant.xml'))
        response = wget.download(URL, 'data.zip')
        with zipfile.ZipFile('data.zip', 'r') as zip_ref:
            zip_ref.extractall()
        os.remove('data.zip')
        os.rename('PrixCarburants_instantane.xml', 'prix-carburant.xml')
        os.system('cls')
        break
    except:
        print('Erreur')
        time.sleep(1)


tree = etree.parse("prix-carburant.xml")
geolocator = Nominatim(user_agent="geoapiExercises")

while True:
    try:
        ville = str(input('Entrez votre ville: '))
        liste_long_ville = []
        liste_lat_ville = []
        for user in tree.xpath(f"/pdv_liste/pdv[ville='{ville.upper()}']"):
            id_long = user.get('longitude')
            liste_long_ville.append(id_long)
            id_lat = user.get('latitude')
            liste_lat_ville.append(id_lat)

        print('Il y a ', len(liste_lat_ville), 'stations disponibles.')
        lat_0 = tuple(liste_lat_ville)
        long_0 = str(liste_long_ville[0])

        lat_10 = str(float(liste_lat_ville[0]) / 100000)
        long_10 = str(float(liste_long_ville[0]) / 100000)

        location = geolocator.reverse(lat_10 + ',' + long_10, exactly_one=False)
        adresse = location[0][0]
        addv2 = adresse.split(', ')

        print('Voici l\'adresse de la station recommandée:\n', adresse,'\n')
        autres = str(input('Souhaitez vous chercher d\'autres stations? O/N : '))
        
        if autres == 'O' or autres == 'o':
            while True:
                try:
                    nb_autres = int(input(f'Combien de stations voulez vous afficher? ({len(liste_lat_ville)} disponibles) : '))
                    if nb_autres>len(liste_lat_ville):
                        print('Il n\'y à pas autant de stations disponibles.')
                        break
                    elif nb_autres==0:
                        break
                    else:
                        for clm in range (nb_autres):
                            lat_0 = tuple(liste_lat_ville)
                            long_0 = str(liste_long_ville[clm])

                            lat_10 = str(float(liste_lat_ville[clm]) / 100000)
                            long_10 = str(float(liste_long_ville[clm]) / 100000)

                            location = geolocator.reverse(lat_10 + ',' + long_10, exactly_one=False)
                            adresse = location[0][0]
                            print(clm,' : ',adresse, '\n\n')
                            break
                    break
                except:
                    traceback.print_exc()
                    time.sleep(1)

    except:
        print('Aucune station disponible dans cette ville.')
    recommencer = input('Souhaitez-vous effectuer une nouvelle recherche ? O/N : ')
    os.system('cls')
    if recommencer == 'n' or recommencer == 'N':
        break
print('Fin du programme...')