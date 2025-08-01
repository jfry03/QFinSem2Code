import pandas as pd
import os

names = {"SC": "Stefan", "BW": "Brandon", "LE": "Luke", "David": "David", "CK": "Cameron", "CH": "Cooper", "CO": "Chelsea", "DM": "Devdhar", "BM": "Ben", "BK": "Baxter", "AV": "Adriaan", "GB": "Grace", "JY": "Jayden", "LC": "Lewis", "MV": "Matthew", "NC": "Nick", "RC": "Rahul", "SA": "Stanley", "TB": "Theo", "WW": "Wesley"}

def analyse_xlsx(file_name, liquidity_providers=None):
    sheets = pd.read_excel(file_name, sheet_name=None)

    pnls = {}
    for sheet_name, df in sheets.items():
        df.columns = df.columns.str.strip()
        new_pnl = analyse_csv(df)
        new_pnl = normalise_pnls(new_pnl, liquidity_providers)
        pnls = merge_pnls(pnls, new_pnl)


    return pnls

def analyse_csv(df):
    settlement = df["Solution"].iloc[0]
    df = df.drop(columns=["Solution"])
    print(df.columns)
    df["Buyer_Pnl"] = settlement - df["Price"]
    df["Seller_Pnl"] = df["Price"] - settlement

    buyer_pnl = df.groupby("Buy")["Buyer_Pnl"].sum().to_dict()
    seller_pnl = df.groupby("Sell")["Seller_Pnl"].sum().to_dict()

    game_pnl = merge_pnls(buyer_pnl, seller_pnl)

    return game_pnl

def merge_pnls(initial_pnl, new_pnl):
    
    for key, value in new_pnl.items():
        if key in initial_pnl:
            initial_pnl[key] += value
        else:
            initial_pnl[key] = value
    
    return initial_pnl

def normalise_pnls(pnls, liqudity_providers):
    winners = {k: v for k, v in pnls.items() if v > 0 and k not in liquidity_providers}
    losers = {k: v for k, v in pnls.items() if v < 0 and k not in liquidity_providers}

    winners_sum = sum(winners.values())
    winners_factor = 100 / winners_sum

    losers_sum = sum(losers.values())
    losers_factor = 100 / losers_sum 

    winners_adj = {k: v * winners_factor for k, v in winners.items()}
    losers_adj = {k: -v * losers_factor for k, v in losers.items()}


    return {**winners_adj, **losers_adj}

def analyse_txt(path):
    with open(path, 'r') as file:
        lines = file.readlines()

    pnls = {}
    for line in lines:
        if line.strip():
            name, pnl = line.split(':')
            name = name.strip()
            pnl = int(pnl.strip())
            pnls[name] = pnl

    return pnls

def update_readme(df):
    md = "# PnL Summary\n\n"
    md += "| Player | Total PnL |\n|--------|-----------|\n"
    
    for player, row in df.iterrows():
        pnl = row["PnL"]
        md += f"| {player} | {pnl:.2f} |\n"
    
    with open("../README.md", "w") as f:
        f.write(md)




path = "TradingGameResults/"
csvs = os.listdir(path)

liquidity_providers = ["JF", "KM"]

pnls = {}
for file in csvs:
    if file.endswith(".xlsx"):   
        new_pnls = analyse_xlsx(path + file)
        print(new_pnls)
        pnls = merge_pnls(pnls, new_pnls)
    if file.endswith("txt"):
        new_pnls = analyse_txt(path + file)
        print(new_pnls)
        pnls = merge_pnls(pnls, new_pnls)

df = pd.DataFrame.from_dict(pnls, orient='index', columns=['PnL']).sort_values(by='PnL', ascending=False)
df.index = df.index.map(names)

update_readme(df)


