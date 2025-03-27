# %%
import json
import yaml

def read_config_files(suffix: str) -> tuple[dict, dict]:
    """
    Read JSON and YAML configuration files.
    Args:
        suffix (str): Suffix of file names.
    Returns:    
        tuple[dict, dict]: Tuple containing the JSON and YAML configurations as dictionaries.
    """

    with open(f"./config_{suffix}.json", "r") as f:
        config_json = json.load(f)
    with open(f"./config_{suffix}.yaml", "r") as f:
        config_yaml = yaml.safe_load(f)
    return config_json, config_yaml

# %%
intro_json, intro_yaml = read_config_files("intro")
repeated_json, repeated_yaml = read_config_files("repeated")
# long_string_json, long_string_yaml = read_config_files("long_string")