# Projet FinTech
"""
Nom du projet   : Financial Asset Profile
Auteur          : William Amani
Version         : 1.0
Date            : 2025-06-07
Description     : Extraction de données qualitatives et quantitatives d'un actif financier via Yahoo Finance
Licence         : Massachusetts Institute of Technology (MIT)
"""


# Packages
import yfinance as yf
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mlocat
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table



# Couleurs pour affichage
BLEU = "\033[94m"
BLEU_CIEL = "\033[96m"
GREEN = "\033[92m"
RED = "\033[91m"
ROSE = "\033[95m"
RESET = "\033[0m"

# Autres paramètres
delai = 0.5
console = Console()



# Accéder aux données de l'actif financier sur yahoo!finance via le ticker fourni
def get_ticker():
    while True:
        input_ticker = input("Ticker de l'actif financier ---> ").strip().upper()
        
        if input_ticker == "":
            print("Aucun ticker n'a été inscrit. Veuillez réessayer.")
            continue
        try:
            ticker = yf.Ticker(input_ticker)
            info = ticker.info
            time.sleep(delai)
            if 'shortName' in info:
                return input_ticker, ticker, info
            else:
                print(f"{RED}Le ticker n'a pas été reconnu. Veuillez vous assurer que {input_ticker} fait bien partie de yahoo!finance.{RESET}")
        except Exception as e:
            print(f"{RED}Veuillez vérifier le ticker puis réessayer.{RESET}")
            print(f"{RED}Erreur lors de la correspondance dans yahoo!finance : {e}{RESET}")


# Convertir la monnaie de l'actif financier en monnaie locale déterminée
def convert_currency(info):
    ticker_currency = info.get("currency")
    my_currency = input(f"Votre monnaie en ISO Code (ISO code du ticker : {info.get("currency")}) ---> ").upper()
    try:
        if ticker_currency != my_currency:
            currency_pair = f"{ticker_currency}{my_currency}=X"
            forex = yf.Ticker(currency_pair)
            exchange_rate = forex.history(period = "1d")["Close"].iloc[-1]
            time.sleep(delai)
        else:
            exchange_rate = 1
        return ticker_currency, my_currency, exchange_rate
    except Exception as e:
        print(f"{RED}Erreur lors de la conversion : {e}{RESET}")


# Récupérer sur yahoo!finance les données qualitatives de l'actif financier via son ticker
def get_qualitative_data(info):
    # Afficher les données qualitatives de l'actif financier via son ticker
    qualitative_data = {
        "Company name": info.get("longName")    if info.get("longName") 
                                                else "N/A",
        "Ticker": info.get("symbol")    if info.get("symbol") 
                                        else "N/A",
        "Type of Asset": info.get("quoteType").capitalize()     if info.get("quoteType") 
                                                                else "N/A",
        "Year of creation": "(Go to Description)",

        "Head of Office": f"{info.get("city")} ({info.get("state")}), {info.get("country")} ({info.get("address1")}, {info.get("zip")})"    if (((info.get("address1") and info.get("city")) and info.get("state")) and info.get("zip")) and info.get("country") 
                                                                                                                                            else "N/A",
        "Website": f"{BLEU_CIEL}{info.get('website')}{RESET}"   if info.get('website') 
                                                                else "N/A",
        "Sector": info.get("sector")    if info.get("sector") 
                                        else "N/A",
        "Industry": info.get("industry")    if info.get("industry") 
                                            else 'N/A',
        "Country": info.get("country")  if info.get("country") 
                                        else "N/A",
        "Exchange": f"{info.get('fullExchangeName')} ({info.get('exchange')}, {info.get('exchangeTimezoneName')})"  if (info.get('fullExchangeName') and info.get("exchange")) and info.get('exchangeTimezoneName') 
                                                                                                                    else "N/A",
        "ISO Currency Code": info.get("currency")   if info.get("currency") 
                                                    else "N/A",
        "Ex-Dividend Date": datetime.fromtimestamp(info["exDividendDate"]).strftime('%Y-%m-%d')     if info.get("exDividendDate") 
                                                                                                    else 'N/A',
        "Dividend Date": datetime.fromtimestamp(info["dividendDate"]).strftime('%Y-%m-%d')  if info.get("dividendDate") 
                                                                                            else 'N/A',
        "Next Fiscal Year End": datetime.fromtimestamp(info["nextFiscalYearEnd"]).strftime('%Y-%m-%d')  if info.get("nextFiscalYearEnd")
                                                                                                        else "N/A",
        "Next publication of results": info.get("earningsDate")     if info.get("earningsDate")
                                                                    else "N/A",
        "Description": f"{info.get('longBusinessSummary')[:500]}..."    if info.get("longBusinessSummary") 
                                                                        else "N/A"
    }

    return qualitative_data


# Récupérer sur yahoo!finance les données quantitatives de l'actif financier via son ticker
def get_quantitative_data(ticker, info, ticker_currency, my_currency, exchange_rate):
    # Accéder à l'historique de prix et y déterminer ce qui suit
    time.sleep(delai)
    price_data = ticker.history(period="1d")
    if not price_data.empty:
        last_price_date = price_data.index[-1].strftime('%Y-%m-%d')                                                         # Dernier prix last de l'actif financier
        if 'Adj Close' in price_data.columns:                                                                               # Prix de fermeture ajusté comme
            current_price = price_data["Adj Close"].iloc[-1]                                                                # prix courant de l'actif financier, sinon
        else:                                                                                                               # Prix de fermeture comme
            current_price = price_data["Close"].iloc[-1]                                                                    # prix courant de l'actif financier
        previous_close = info.get("previousClose")                                                                          # Précédent prix de fermeture
        price_change_value = current_price - previous_close if previous_close else None                                     # Variation de prix (en monnaie)
        price_change_percent = (price_change_value / previous_close) if previous_close else None                            # Variation de prix (en pourcentage)
    else:
        last_price_date = None
        current_price = None
        price_change_value = None
        price_change_percent = None

    # Afficher les données quantitatives de l'actif financier via son ticker
    quantitative_data = {
        "Price Date": last_price_date   if last_price_date 
                                        else "N/A",
        "ISO Currency Code": info.get("currency")   if info.get("currency") 
                                                    else "N/A",
        "My ISO Currency Code": my_currency     if my_currency 
                                                else "N/A",
        "Exchange Rate": f"{round(exchange_rate, 4)} {my_currency}/{ticker_currency}",
        
        "Current Price": f"{round(current_price * exchange_rate, 2)} {my_currency} <-- {round(current_price, 2)} {info.get('currency')}"    if current_price 
                                                                                                                                            else "N/A",
        "Price Change (currency)":  f"{RED}{round(price_change_value * exchange_rate, 2)} {my_currency}{RESET} <-- {RED}{round(price_change_value, 2)} {info.get('currency')}{RESET}"   if price_change_value <= 0 
                                                                                                                                                                                        else f"{GREEN}+{round(price_change_value * exchange_rate, 2)} {my_currency}{RESET} <-- {GREEN}+{round(price_change_value, 2)} {info.get("currency")}{RESET}",
        "Price Change (percent)":   f"{RED}{round(price_change_percent * 100, 2)}%{RESET}"  if price_change_percent <= 0 
                                                                                            else f"{GREEN}+{round(price_change_percent * 100, 2)}%{RESET}",
        "Forward Earning": f"{round(info.get("epsForward") * exchange_rate, 2)} {my_currency} <-- {round(info.get("lastDividendValue"), 2)} {info.get('currency')}"     if info.get("epsForward") 
                                                                                                                                                                        else "N/A",
        "Last Dividend": f"{round(info.get("lastDividendValue") * exchange_rate, 2)} {my_currency} <-- {round(info.get("lastDividendValue"), 2)} {info.get('currency')}"    if info.get("lastDividendValue") 
                                                                                                                                                                            else "N/A",
        "Enterprise Value": f"{round(info.get("enterpriseValue") * exchange_rate, 0)} {my_currency} <-- {round(info.get("enterpriseValue"), 0)} {info.get('currency')}"     if info.get("enterpriseValue") 
                                                                                                                                                                            else "N/A",
        "Total Cash": f"{round(info.get("totalCash") * exchange_rate, 0)} {my_currency} <-- {round(info.get("totalCash"), 0)} {info.get('currency')}"   if info.get("totalCash") 
                                                                                                                                                        else "N/A",
        "Total Debt": f"{round(info.get("totalDebt") * exchange_rate, 0)} {my_currency} <-- {round(info.get("totalDebt"), 0)} {info.get('currency')}"   if info.get("totalDebt") 
                                                                                                                                                        else "N/A",
        "Market Capitalization": f"{round(info.get("marketCap") * exchange_rate, 0)} {my_currency} <-- {round(info.get("marketCap"), 0)} {info.get('currency')}"    if info.get("marketCap") 
                                                                                                                                                                    else "N/A",
        "Shares outstanding": f"{info.get("sharesOutstanding")} shares"     if info.get("sharesOutstanding") 
                                                                            else "N/A", 
        "Number of Employees": f"{info.get("fullTimeEmployees")} employees" if info.get("fullTimeEmployees") 
                                                                            else "N/A", 
        "52 Week High": f"{round(info.get('fiftyTwoWeekHigh') * exchange_rate, 2)} {my_currency} <-- {round(info.get('fiftyTwoWeekHigh'), 2)} {info.get('currency')}"   if info.get("fiftyTwoWeekHigh") 
                                                                                                                                                                        else "N/A", 
        "52 Week Low": f"{round(info.get('fiftyTwoWeekLow') * exchange_rate, 2)} {my_currency} <-- {round(info.get('fiftyTwoWeekLow'), 2)} {info.get('currency')}"  if info.get("fiftyTwoWeekLow") 
                                                                                                                                                                    else "N/A", 
        "Beta": round(info.get("beta"), 5)  if info.get("beta") 
                                            else "N/A", 
        "Return on Equity": f"{round(info.get('returnOnEquity') * 100, 2)}%"    if info.get("returnOnEquity") 
                                                                                else "N/A", 
        "Dividend Payout Ratio": f"{round(info.get('payoutRatio') * 100, 2)}%"  if info.get("payoutRatio") 
                                                                                else "N/A", 
        "Sustainable Growth Rate": f"{round((info.get('returnOnEquity') * (1 - info.get('payoutRatio'))) * 100,2)}%"    if info.get("returnOnEquity") and info.get("payoutRatio") 
                                                                                                                        else "N/A",
        "Trailing P/E": round(info.get("trailingPE"), 2)    if info.get("trailingPE") 
                                                            else "N/A",
        "Forward P/E": round(info.get("forwardPE"), 2)  if info.get("forwardPE") 
                                                        else "N/A",
        "PEG Ratio": round(info.get("pegRatio"), 2)     if info.get("pegRatio") 
                                                        else "N/A",
        "EV/EBITDA": round(info.get("enterpriseToEbitda"), 2)   if info.get("enterpriseToEbitda") 
                                                                else "N/A",
        "EV/Revenue": round(info.get("enterpriseToRevenue"), 2)     if info.get("enterpriseToRevenue") 
                                                                    else "N/A",
    }

    return quantitative_data


# Emettre le graphique d'évolution de prix de l'actif financier via son ticker
def chart(input_ticker, info, ticker, exchange_rate, my_currency):
    # Indiquer les périodes et labels du grpahique
    periods = {
        "1": "3d", "2": "5d", "3": "1mo", "4": "3mo", 
        "5": "6mo", "6": "1y", "7":"5y", "8": "10y", "9": "max"
    }
    labels = {
        "1": "3 jours", "2": "5 jours", "3": "1 mois", "4": "1 trimestre", 
        "5": "1 semestre", "6": "1 an", "7": "5 ans", "8": "10 ans", "9": "Depuis le début"
    }

    # Boucle de la composition du graphique d'évolution de prix de l'actif financier
    while True:
        # Afficher d'une légende pour faciliter le choix de la période
        print("Période du graphique :", 
              "\n   1: 3 jours      ‖ 2: 5 jours    ‖ 3: 1 mois     ‖ 4: 1 trimestre", 
              "\n   5: 1 semestre   ‖ 6: 1 an       ‖ 7: 5 ans      ‖ 8: 10 ans         ‖ 9: Depuis le début")
        
        # Choisir la période et paramétrer le label
        period_choice = input(f"{ROSE}---> Votre choix est un graphique de {input_ticker} sur une période{RESET} #").strip()
        period = periods.get(period_choice)
        label = labels.get(period_choice)
        if not period:
            print(f"{RED}Choix invalide. Veuillez réessayer.{RESET}")
            continue

        # Vérifier la période choisie et Convertir les prix en monnaie locale
        period_data = ticker.history(period = period)
        time.sleep(delai)
        if period_data.empty:
            print(f"{RED}Aucune donnée n'est disponible pour cette période. Veuillez réessayez.{RESET}")
            continue
        period_data["Converted_Close"] = period_data["Close"] * exchange_rate

        # Indiquer les paramètres du graphique de l'évolution de prix de l'actif financier
        plt.figure(figsize=(16, 5))
        plt.plot(period_data.index, period_data["Converted_Close"], label="Prix (converti)", color="blue")
        plt.title(f"Évolution du prix de {info.get('longName')} (sur {label}, {datetime.now().date()})", fontweight='bold')
        plt.xlabel("Date", fontweight='bold')
        plt.ylabel(f"Prix (en {my_currency})", fontweight='bold')
        plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')
        plt.minorticks_on()

        ax = plt.gca()
        if period == "3d":
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %Hh'))
            ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))
        elif period == "5d":
            ax.xaxis.set_major_locator(mdates.DayLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %Hh'))
        elif period in ["1mo", "3mo", "6mo"]:
            ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        elif period in ["1y", "5y", "10y"]:
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        else:
            ax.xaxis.set_major_locator(mdates.YearLocator(base=1))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        ax.xaxis.set_minor_locator(mlocat.NullLocator())

        plt.legend()
        plt.margins(x=0)
        plt.autoscale(enable=True, axis='x', tight=True)
        plt.tight_layout()
        plt.show()

        break
    

# Afficher les données qualitatives et quantitatives extraites sur l'actif financier via son ticker
def results_display(input_ticker, ticker, info, ticker_currency, my_currency, exchange_rate):
    console.print(Panel(f"[bold yellow]--- INFORMATIONS QUALITATITVES POUR {input_ticker} ({datetime.now().date()}) ---[bold yellow]"))
    qualitative_data = get_qualitative_data(info)
    table_qual = Table(title=None, show_header=False)
    for key, value in qualitative_data.items():
        table_qual.add_row(key, str(value), end_section=True)
    console.print(table_qual)
    
    console.print(Panel(f"[bold yellow]--- INFORMATIONS QUANTITATIVES POUR {input_ticker} ({datetime.now().date()}) ---[bold yellow]"))
    quantitative_data = get_quantitative_data(ticker, info, ticker_currency, my_currency, exchange_rate)
    table_quant = Table(title=None, show_header=False)
    for key, value in quantitative_data.items():
        table_quant.add_row(key, str(value), end_section=True)
    console.print(table_quant)


# Préparer l'affichage final des résultats sur l'actif financier
def final_display():
    console.print(Panel(f"[bold cyan]---> Lancement de Financial Asset Profile ({datetime.now().date()}) - conçu par William Amani[/bold cyan]", border_style="cyan"))
    # Lancer une boucle de l'affiche desdits résultats
    while True:
        input_ticker, ticker, info = get_ticker()
        ticker_currency, my_currency, exchange_rate = convert_currency(info)
        
        results_display(input_ticker, ticker, info, ticker_currency, my_currency, exchange_rate)

        console.print(Panel(f"[bold yellow]--- GRAPHIQUE POUR {input_ticker} ({datetime.now().date()}) ---[bold yellow]"))
        chart(input_ticker, info, ticker, exchange_rate, my_currency)
        
        # Rélancer, ou pas, le code FAP pour un autre actif financier
        while True:
            restart = input("\nSouhaitez-vous analyser un autre actif financier ? (O-Oui, N-Non) ---> ").strip().upper()
            if restart in ["O", "N"]:
                break
            print(f"{RED}Veuillez répondre par 'O' pour Oui ou 'N' pour Non.{RESET}")
        if restart == "O":
            console.print(Panel("[bold cyan]---> Lancement de FAP pour un autre actif financier[/bold cyan]", border_style="cyan"))
            continue
        else:   # restart == "N"
            console.print(Panel("[bold green]Informations fournies. Merci d'avoir utilisé notre outil, le FAP ! <---[/bold green]", border_style="green"))
            break
            
        
# Restreindre l'exécution de ce code au lancement de ce fichier uniquement
if __name__ == "__main__":
    final_display()





# Licence Massachusetts Institute of Technology (MIT)
"""
MIT License

Copyright (c) 2025 William Amani

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""


"""
Licence MIT

Une licence permissive courte et simple avec des conditions exigeant uniquement la 
préservation des droits d'auteur et des avis de licence. Les œuvres sous licence, 
les modifications et les œuvres plus importantes peuvent être distribuées sous des 
conditions différentes et sans code source.

Autorisations                   Conditions                      Limitations
 Utilisation commerciale         Licence et avis de              Responsabilité
 Distribution                    droit d'auteur                  Garantie
 Modification
 Usage privé
"""
