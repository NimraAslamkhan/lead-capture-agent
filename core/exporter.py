import pandas as pd

def export_excel(leads):
    df = pd.DataFrame(leads)
    df.to_excel("leads.xlsx", index=False)
leads = []