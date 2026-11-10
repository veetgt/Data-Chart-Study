"""
XLSX: https://www.kaggle.com/datasets/jakubkrasuski/league-of-legends-match-dataset-2025?resource=download

Passei para CSV através do https://convertio.co/pt/ previamente para facilitar.
"""
#   ----- Extração -----
import numpy             as np
import pandas            as pd
import matplotlib.pyplot as plt

df = pd.read_csv('league_data.csv')

# Limpeza simples
df = df.dropna()

#   ----- Os 20 campeões mais selecionados -----

most_played_champ = df['champion_name'].value_counts(ascending= True)
plt.barh(most_played_champ.index[-20:], 
         most_played_champ.values[-20:], 
         color="#a103fc", 
         edgecolor="black")

plt.title('Frequência de escolha de cada campeão de League of Legends')

plt.show()

#   ----- Elo dos jogadores da amostra -----
plt.close()

#Limpeza específica dos dados e classificação
df = df.drop_duplicates(subset="puuid")
elo_rank = {
    "IRON": "Low elo",
    "BRONZE": "Low elo",
    "SILVER": "Low elo",
    "GOLD": "Mid elo",
    "PLATINUM": "Mid elo",
    "EMERALD": "Mid elo",
    "DIAMOND": "High elo",
    "MASTER": "High elo",
    "GRANDMASTER": "High elo",
    "CHALLENGER": "Challenger",
}
df["elo_rank"] = df["solo_tier"].map(elo_rank)
all_elo = ["Low elo", "Mid elo", "High elo", "Challenger"]
n_players = df["elo_rank"].value_counts().reindex(all_elo)

# Gráfico
colors = plt.cm.Purples(np.linspace(0.3, 0.9, 4))
plt.pie(n_players, labels=all_elo, 
        autopct="%1.1f%%", 
        colors=colors,
        explode=[0,0,0,0.3])
plt.title("Distribuição de elo da amostra")
plt.show()

#   ----- Quantia de partidas por dia -----
plt.close()

# Convertendo para data
df["game_start_utc"] = pd.to_datetime(df["game_start_utc"])
df["game_date"] = df["game_start_utc"].dt.date

matches_per_day = df.groupby('game_date')['game_id'].nunique()

plt.plot(matches_per_day.index, matches_per_day.values,
         marker='.',
         markersize=5,
         markerfacecolor='#ff8800',
         markeredgecolor='#ff8800',
         linestyle='linear',
         color="#dd7600")

plt.gcf().autofmt_xdate()
plt.show()
