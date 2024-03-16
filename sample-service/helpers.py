import yaml

def importyaml(file="./sample-service/config.yaml"):
    with open(file, "r") as f:
        config = yaml.safe_load(f)
        f.close()
    return config

def writeyaml(category, key, value, file="./sample-service/config.yaml"):
    with open(file, "r") as f:
        config = yaml.safe_load(f)
        f.close()
    print(config)
    config[category][key] = value
    with open(file, 'w') as f:
        yaml.dump(config, f, sort_keys=False)