#%%
import json
import yaml
# %%
with open("./config.json", "r") as f:
    config_json = json.load(f)

with open("./config.yaml", "r") as f:
    config_yaml = yaml.safe_load(f)
# %%
with open("./config2.yaml", "r") as f:
    config2_yaml = yaml.safe_load(f)
# %%
with open("./config3.yaml", "r") as f:
    config3_yaml = yaml.safe_load(f)
