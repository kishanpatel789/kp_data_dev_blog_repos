# %%
# explore parquet file
import pyarrow.parquet as pq

file_path = "data/yellow_tripdata_2025-05.parquet"
table = pq.read_table(file_path)

table.shape

table.schema

table.slice(0, 5)


# %%
# save as csv
df = table.to_pandas()

df.shape

df.to_csv("data/yellow_tripdata_2025-05.csv", index=False)







# %%
# explore parquet file some more
parquet_file = pq.ParquetFile(file_path)

metadata = parquet_file.metadata
metadata

for i in range(metadata.num_row_groups):
    print(f"{i}: {metadata.row_group(i).num_rows}")

metadata.row_group(0)

metadata.row_group(0).column(0)


# %%
# plain encoding vs dictionary encoding
import pyarrow as pa
import random
people_options = ["Harry", "Hermione", "Ron"]
people = [random.choice(people_options) for _ in range(10_000_000)]
people_table = pa.table({"people": people})

people_table.to_pandas().value_counts()

# plain encoding
pq.write_table(
    people_table,
    "data/people_plain.parquet",
    use_dictionary=False,
    column_encoding={
        "people": "PLAIN",
    },
)

# dictionary encoding
pq.write_table(
    people_table, 
    "data/people_dict.parquet", 
    use_dictionary=True,
)




# %%
# run length_encoding
sorted_people_table = pa.table({"people": sorted(people)})

sorted_people_table

pq.write_table(sorted_people_table, "data/people_sorted.parquet")







# %%
# plain encoding vs delta encoding
from datetime import datetime
timestamps = [datetime.now() for _ in range(1_000_000)]
ts_table = pa.table({"timestamps": timestamps})
ts_table

# plain encoding
pq.write_table(
    ts_table,
    "data/timestamps_plain.parquet",
    compression=None,
    use_dictionary=False,
    column_encoding={
        "timestamps": "PLAIN",
    },
)

# delta encoding
pq.write_table(
    ts_table,
    "data/timestamps_delta.parquet",
    compression=None,
    use_dictionary=False,
    column_encoding={
        "timestamps": "DELTA_BINARY_PACKED",
    },
)

