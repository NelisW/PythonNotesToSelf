import pandas as pd
df = pd.read_excel('oktal-pricing.xlsx')
df.to_latex('output.tex')

