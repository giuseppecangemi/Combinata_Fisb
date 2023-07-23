from flask import Flask, render_template
import pandas as pd
import os
import matplotlib.pyplot as plt

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))


# Definizione della funzione calcola_posizione()
# Inserire qui il codice per la funzione calcola_posizione()
def calcola_posizione(punteggi_singolo, punteggi_coppia, punteggi_piccola,
                      punteggi_grande, punteggi_musici, lista_gruppi=None, parametri=None):
    if lista_gruppi is None:
        lista_gruppi = ["Contrada della Corte", "Artena", "Torri Metelliane", "Pozzo Seravezza", "Piazzarola", "Borgo Veneto",
                        "Borgo Don Bosco", "Tempesta Noale", "Arquatesi", "Terre Sabaude", "Rione Cento", "Borgo San Pietro",
                        "Porta Tufilla", "Rione Santa Caterina", "ASTA", "Citta Regia", "Rocca di Monselice",
                        "Torre Dei Germani", "Contesa Estense", "Rione San Paolo"]

    if parametri is None:
        parametri = {"Singolo": 1, "Coppia": 1.2, "Piccola": 1.4, "Grande": 1.6, "Musici": 1.6}

    df = pd.DataFrame({"Posizione": [], "Gruppo": [], "Singolo": int, "Coppia": int,
                       "Piccola": int, "Grande": int, "Musici": int, "Combinata": []})

    for i, gruppo in enumerate(lista_gruppi):
        df.at[i, 'Gruppo'] = gruppo

    for i, j in df.iterrows():
        df.at[i, 'Singolo'] = punteggi_singolo[i]
        df.at[i, 'Coppia'] = punteggi_coppia[i]
        df.at[i, 'Piccola'] = punteggi_piccola[i]
        df.at[i, 'Grande'] = punteggi_grande[i]
        df.at[i, 'Musici'] = punteggi_musici[i]

    df = df.where(pd.notna(df), 0)

    for h, k in df.iterrows():
        df.at[h, 'Combinata'] = ((k.Singolo * parametri["Singolo"])
                                 + (k.Coppia * parametri["Coppia"])
                                 + (k.Piccola * parametri["Piccola"])
                                 + (k.Grande * parametri["Grande"])
                                 + (k.Musici * parametri["Musici"]))
    df["Combinata"] = round(df.Combinata,3)
    df = df.sort_values(by='Combinata', ascending=True)
    df['Posizione'] = range(1, len(df) + 1)

    return df

lista_gruppi = ["Contrada della Corte", "Artena", "Torri Metelliane", "Pozzo Seravezza", "Piazzarola", "Borgo Veneto",
                        "Borgo Don Bosco", "Tempesta Noale", "Arquatesi", "Terre Sabaude", "Rione Cento", "Borgo San Pietro",
                        "Porta Tufilla", "Rione Santa Caterina", "ASTA", "Citta Regia", "Rocca di Monselice",
                        "Torre Dei Germani", "Contesa Estense", "Rione San Paolo"]

punteggi_piccola = [0 for _ in range(20)]
punteggi_grande= [0 for _ in range(20)]
punteggi_musici = [0 for _ in range(20)]

punteggi_singolo = [1, 3, 8, 5, 6, 9, 2, 12, 11, 10, 7, 5, 13, 19, 14, 18, 16, 15, 17, 20]
punteggi_coppia = [1, 4, 2, 6, 7, 5, 11, 3, 9, 10, 13, 16, 12, 8, 14, 15, 17, 19, 18, 20]

valori_punteggi_grande = {
    "Contrada della Corte": 2,
    "Artena": 13,
    "Torri Metelliane": 9,
    "Pozzo Seravezza": 4,
    "Piazzarola": 6,
    "Borgo Veneto": 1,
    "Borgo Don Bosco": 15,
    "Tempesta Noale": 19,
    "Arquatesi": 12,
    "Terre Sabaude": 16,
    "Rione Cento": 17,
    "Borgo San Pietro": 7,
    "Porta Tufilla": 3,
    "Rione Santa Caterina": 8,
    "ASTA": 5,
    "Citta Regia": 10,
    "Rocca di Monselice": 20,
    "Torre Dei Germani": 18,
    "Contesa Estense": 14,
    "Rione San Paolo": 11
}


punteggi_grande = [valori_punteggi_grande.get(gruppo, 0) for gruppo in lista_gruppi]


valori_punteggi_musici = {
    "Contrada della Corte": 8,
    "Artena": 19,
    "Torri Metelliane": 5,
    "Pozzo Seravezza": 1,
    "Piazzarola": 4,
    "Borgo Veneto": 11,
    "Borgo Don Bosco": 16,
    "Tempesta Noale": 13,
    "Arquatesi": 2,
    "Terre Sabaude": 15,
    "Rione Cento": 17,
    "Borgo San Pietro": 9,
    "Porta Tufilla": 6,
    "Rione Santa Caterina": 3,
    "ASTA": 18,
    "Citta Regia": 14,
    "Rocca di Monselice": 20,
    "Torre Dei Germani": 10,
    "Contesa Estense": 7,
    "Rione San Paolo": 12
}


punteggi_musici = [valori_punteggi_musici.get(gruppo, 0) for gruppo in lista_gruppi]


valori_punteggi_piccola = {
    "Contrada della Corte": 1,
    "Artena": 10,
    "Torri Metelliane": 7,
    "Pozzo Seravezza": 2,
    "Piazzarola": 13,
    "Borgo Veneto": 3,
    "Borgo Don Bosco": 12,
    "Tempesta Noale": 15,
    "Arquatesi": 5,
    "Terre Sabaude": 6,
    "Rione Cento": 16,
    "Borgo San Pietro": 8,
    "Porta Tufilla": 17,
    "Rione Santa Caterina": 9,
    "ASTA": 4,
    "Citta Regia": 11,
    "Rocca di Monselice": 20,
    "Torre Dei Germani": 19,
    "Contesa Estense": 14,
    "Rione San Paolo": 18
}


punteggi_piccola = [valori_punteggi_piccola.get(gruppo, 0) for gruppo in lista_gruppi]


@app.route('/')
def show_dataframe():
    # Inserire qui il codice per calcolare il DataFrame
    df = calcola_posizione(punteggi_singolo, punteggi_coppia, punteggi_piccola,
                           punteggi_grande, punteggi_musici)
    # Imposta l'indice del DataFrame
    df.set_index('Posizione', inplace=True)
    # Controlla se la prima riga corrisponde alla posizione 1
    first_row_gold = df.index[0] == 1
    # Renderizza il template HTML con il DataFrame come parametro
    # Rinomina la variabile dataframe_html in dataframe
    return render_template('index.html', dataframe=df, first_row_gold=first_row_gold)


if __name__ == '__main__':
    app.run(debug=True)
