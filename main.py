from flask import Flask, render_template, request
import pandas as pd
import numpy as np

app = Flask(__name__, template_folder='templates')

def calcola_posizione(lista_gruppi=None, parametri=None, updates=None):
    if lista_gruppi is None:
        lista_gruppi = ["Associazione Culturale Sestiere Porta Bonomini", "Associazione Giovani Maestri – Motta Sant’Anastasia (CT)",
        "Borgo S. Nicolò – Le Cinque Contrade – Cava dei Tirreni", "Casa Normanna – Rione Vecchia Matrice (CT)", "GRUPPO SBANDIERATORI E MUSICI DEL NIBALLO",
        "Musici e Sbandieratori Castelfranco di Sotto APS", "Rione Cento", "Rione Madonna delle Stuoie", "San Paolo – Ferrara"]

    if parametri is None:
        parametri = {"Singolo": 1, "Coppia": 1.2, "Piccola": 1.4, "Grande": 1.6, "Musici": 1.6}

    df = pd.DataFrame({"Posizione": [], "Gruppo": [], "Singolo": int, "Coppia": int,
                       "Piccola": int, "Grande": int, "Musici": int, "Combinata": []})

    for i, gruppo in enumerate(lista_gruppi):
        df.at[i, 'Gruppo'] = gruppo

    punteggi_singolo = np.zeros((len(lista_gruppi)+1,), dtype=int)
    punteggi_coppia = np.zeros((len(lista_gruppi)+1,), dtype=int)
    punteggi_piccola = np.zeros((len(lista_gruppi)+1,), dtype=int)
    punteggi_grande = np.zeros((len(lista_gruppi)+1,), dtype=int)
    punteggi_musici = np.zeros((len(lista_gruppi)+1,), dtype=int)

    

    for i, j in df.iterrows():
        df.at[i, 'Singolo'] = punteggi_singolo[i]
        df.at[i, 'Coppia'] = punteggi_coppia[i]
        df.at[i, 'Piccola'] = punteggi_piccola[i]
        df.at[i, 'Grande'] = punteggi_grande[i]
        df.at[i, 'Musici'] = punteggi_musici[i]

    df = df.where(pd.notna(df), 0)

    if updates:
        for index, row in df.iterrows():
            df.at[index, 'Singolo'] = int(updates.get(f'singolo_{index}', row['Singolo']))
            df.at[index, 'Coppia'] = int(updates.get(f'coppia_{index}', row['Coppia']))
            df.at[index, 'Piccola'] = int(updates.get(f'piccola_{index}', row['Piccola']))
            df.at[index, 'Grande'] = int(updates.get(f'grande_{index}', row['Grande']))
            df.at[index, 'Musici'] = int(updates.get(f'musici_{index}', row['Musici']))

    for h, k in df.iterrows():
        df.at[h, 'Combinata'] = ((k.Singolo * parametri["Singolo"])
                                 + (k.Coppia * parametri["Coppia"])
                                 + (k.Piccola * parametri["Piccola"])
                                 + (k.Grande * parametri["Grande"])
                                 + (k.Musici * parametri["Musici"]))
    df["Combinata"] = round(df.Combinata, 3)
    df = df.sort_values(by='Combinata', ascending=True)
    df['Posizione'] = range(1, len(df) + 1)

    return df

@app.route('/')
def show_dataframe():
    df = calcola_posizione()
    df.set_index('Posizione', inplace=True)
    first_row_gold = df.index[0] == 1
    return render_template('index.html', dataframe=df, first_row_gold=first_row_gold)

@app.route('/update', methods=['POST'])
def update_scores():
    updates = request.form.to_dict()
    df = calcola_posizione(updates=updates)
    df.set_index('Posizione', inplace=True)
    first_row_gold = df.index[0] == 1
    return render_template('index.html', dataframe=df, first_row_gold=first_row_gold)

if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.11')
