import pandas as pd

movies_df = pd.read_json("./dataset/movies.json")
movies_df.to_csv("./dataset/movies.csv")
print(movies_df)
