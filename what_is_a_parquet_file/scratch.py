# %%
import pyarrow as pa
import pyarrow.parquet as pq

# %%

file_path = "data/yellow_tripdata_2025-05.parquet"

# %%
table = pq.read_table(file_path)
table.schema
table.shape

# %%
parquet_file = pq.ParquetFile(file_path)
parquet_file.metadata
parquet_file.schema

parquet_file.num_row_groups

parquet_file.read_row_group(0)

parquet_file.read()



# %%
metadata = parquet_file.metadata
metadata.row_group(0)

for i in range(metadata.num_row_groups):
    print(f"{i}: {metadata.row_group(i).num_rows}")

metadata.row_group(0).column(0)

# %%
# save as csv
df = parquet_file.read().to_pandas()

df.shape

df.to_csv("data/yellow_tripdata_2025-05.csv", index=False)

# du -h data/yellow_tripdata_2025-05.csv
# du -h data/*
