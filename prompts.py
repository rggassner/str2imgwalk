from urllib.request import urlretrieve
import pandas as pd

# Download the parquet table
table_url = f'https://huggingface.co/datasets/poloclub/diffusiondb/resolve/main/metadata.parquet'
urlretrieve(table_url, 'metadata.parquet')

# Read the table using Pandas
metadata_df = pd.read_parquet('metadata.parquet')


# assuming the column you want to save is called "column_name"
column_to_save = metadata_df['prompt']

# specify the file path where you want to save the txt file
file_path = 'prompt.txt'

# save the column to a txt file
column_to_save.to_csv(file_path, sep='\t', index=False, quotechar='"', escapechar='\\')
