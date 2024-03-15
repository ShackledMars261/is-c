import yaml

def importyaml(file="config.yaml"):
    with open(file, "r") as f:
        config = yaml.safe_load(f)
        f.close()
    return config