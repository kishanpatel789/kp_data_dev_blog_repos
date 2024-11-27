# %%
from datetime import datetime 
import sys
sys.path.insert(1, '..')

from api.models import User, Recipe, Tag, recipe_tag, Unit, Ingredient, Direction, complementary_dish, metadata_obj
from api.database import engine, SessionLocal

import csv

# %%
seed_map = [
    {
        'name': 'user',
        'cls': User,
        'file': 'data_user.csv',
        'dt_cols': [],
        'float_cols': [],
    },
    {
        'name': 'recipe',
        'cls': Recipe,
        'file': 'data_recipe.csv',
        'dt_cols': ['date_created', 'date_modified'],
        'float_cols': [],
    },
    {
        'name': 'tag',
        'cls': Tag,
        'file': 'data_tag.csv',
        'dt_cols': [],
        'float_cols': [],
    },
    {
        'name': 'unit',
        'cls': Unit,
        'file': 'data_unit.csv',
        'dt_cols': [],
        'float_cols': [],
    },
    {
        'name': 'ingredient',
        'cls': Ingredient,
        'file': 'data_ingredient.csv',
        'dt_cols': [],
        'float_cols': ['quantity'],
    },
    {
        'name': 'direction',
        'cls': Direction,
        'file': 'data_direction.csv',
        'dt_cols': [],
        'float_cols': [],
    },
]

seed_map_assoc = [
    {
        'name': 'recipe_tag',
        'tbl': recipe_tag,
        'file': 'data_recipetag.csv',
    },
    {
        'name': 'complementary_dish',
        'tbl': complementary_dish,
        'file': 'data_complementarydish.csv',
    },
]
# %%
with SessionLocal() as db:
    metadata_obj.drop_all(bind=engine)
    metadata_obj.create_all(bind=engine)

    # models
    for mapper in seed_map:
        print(mapper['name'])
        mod_inst_items = []

        with open(f'../seed_data/{mapper["file"]}', newline='\n') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row)
                mod_inst = mapper['cls']()
                for key, value in row.items():
                    if key == 'id':  # let postgres handle the id creation
                        continue
                    if value == '':  # overwrite empty value with None (null)
                        value = None
                    if key in mapper['dt_cols'] and value != None:
                        value = datetime.strptime(value, '%Y-%m-%d')
                    setattr(mod_inst, key, value)
                mod_inst_items.append(mod_inst)

        for mod_inst in mod_inst_items:
            db.add(mod_inst)
    
    db.commit()

    # association tables
    for mapper in seed_map_assoc:
        print(mapper['name'])
        records = []
        with open(f'../seed_data/{mapper["file"]}', newline='\n') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row)
                records.append(row)
        multiple_insert = mapper['tbl'].insert().values(records)
        db.execute(multiple_insert)

    db.commit()


# %%