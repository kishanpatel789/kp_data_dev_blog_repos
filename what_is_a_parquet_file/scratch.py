# %%
from datetime import datetime
import pyarrow as pa
import pyarrow.parquet as pq
import random

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

# du -h data/yellow_tripdata_2025-05*
# du -h data/*

# %%
numbers = [random.randint(1, 1000) for _ in range(1_000_000)]
numbers_table = pa.table({"numbers": numbers})

# %%
numbers_table

numbers_table.to_pandas()["numbers"].value_counts()

# %%
# plain encoding
pq.write_table(
    numbers_table,
    "data/numbers_plain.parquet",
    use_dictionary=False,
    column_encoding={
        "numbers": "PLAIN",
    },
)

# dictionary encoding
pq.write_table(numbers_table, "data/numbers_dict.parquet", use_dictionary=True)

# %%
# run length_encoding
sorted_table = pa.table({"numbers": sorted(numbers)})
sorted_table

pq.write_table(sorted_table, "data/numbers_sorted.parquet")

# %%
# check plain encoding, dictionary encoding
plain_file = pq.ParquetFile("data/numbers_plain.parquet")
dict_file = pq.ParquetFile("data/numbers_dict.parquet")
sorted_file = pq.ParquetFile("data/numbers_sorted.parquet")

# %%
plain_file.metadata.row_group(0).column(0)
dict_file.metadata.row_group(0).column(0)
sorted_file.metadata.row_group(0).column(0)


# %%
# delta encoding
timestamps = [datetime.now() for _ in range(1_000_000)]
ts_table = pa.table({"timestamps": timestamps})
ts_table

# %%
pq.write_table(
    ts_table,
    "data/timestamps_plain.parquet",
    compression=None,
    use_dictionary=False,
    column_encoding={
        "timestamps": "PLAIN",
    },
)

# %%
pq.write_table(
    ts_table,
    "data/timestamps_delta.parquet",
    compression=None,
    use_dictionary=False,
    column_encoding={
        "timestamps": "DELTA_BINARY_PACKED",
    },
)

# %%
### String Experiments
people_options = ["Harry", "Hermione", "Ron"]
people = [random.choice(people_options) for _ in range(100_000_000)]
people_table = pa.table({"people": people})

# %%
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
pq.write_table(people_table, "data/people_dict.parquet", use_dictionary=True)

# %%
# run length_encoding
sorted_people_table = pa.table({"people": sorted(people)})
sorted_people_table

pq.write_table(sorted_people_table, "data/people_sorted.parquet")
