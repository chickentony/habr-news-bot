import yaml


def parse_config(path_to_config_file: str):
    """
    Parse yaml config.

    :raise ValueError if not string path provided
    :param path_to_config_file: filepath to config.yaml
    :return: parsed config
    """
    if not isinstance(path_to_config_file, str):
        raise ValueError
    with open(path_to_config_file, 'r', encoding='utf 8') as file:
        config_data = yaml.safe_load(file)
    return config_data
