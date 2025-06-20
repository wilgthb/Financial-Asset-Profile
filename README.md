

# GUIDE DE FINANCIAL ASSET PROFILE (FinAP, by WA)
"Outil d'extraction des données qualitatives et quantitatives d'un actif financier via Yahoo Finance"


## 1 Packages - Installation et/ou Mises à jour
- S'assurer d'avoir installé tous les packages nécessaires : yfinance, matplotlib, datetime, time et rich
- Régler le délai d'attente pour limiter le nombre de requêtes sur une courte durée. Par défaut, il est de 0.50 seconde
- Si l'erreur yfinance "Too Many Requests. Rate limited. Try after a while." se répète, procéder tout simplement à la mise à jour de ce package via le terminal avec "pip install yfinance --upgrade --no-cache-dir".


## 2 Yahoo Finance - Initialisation et récupération des données
- Récupérer le ticker de l'actif financier visé (ex. : CNR.TO pour Canadian National Railway Company)
- Connaître le code ISO de sa monnaie dite "monnaie locale" (ex. : CAD pour Dollar canadien)
- Lancer le code via le fichier "wa_fap.py"
- Inscrire le ticker de l'actif financier, puis cliquer sur Enter
- Inscrire le code ISO de la monnaie locale, puis cliquer sur Enter
La première partie du code récupèrera les données qualitatives et quantitatives de l'actif visé sur Yahoo Finance et effectuera la conversion de certaines données en monnnaie locale.


## 3 Graphique - Construction
- Inscrire le chiffre du choix, selon la légende, de la période d'évolution de prix de l'actif financier
- Cliquer sur Enter
Le code restant convertira les prix en monnaie locale avant d'émettre le graphique d'évolution de valeur de l'actif financier.


## 4 Restart
- Relancer le FinAP pour un autre actif financier



### Note : Ce code représente le début d'une analyse financière.
