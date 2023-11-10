import pandas as pd
import fastparquet as fp

def text_to_parquet(filename:str, text:str):
    df = pd.DataFrame([text], columns=['text'])
    try:
        fp.write(filename, df, append=True)
    except FileNotFoundError:
        fp.write(filename, df)