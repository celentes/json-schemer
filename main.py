import json

f = open("example.json", "r")
table = json.load(f)

schemas = {}

def newSchema(name):
    schemas[name] = {}
    return schemas[name]

id_gen_type = "id"

def schema_generator(json_dict, schema, prefix=""):
    for k, v in json_dict.items():
        # handle nested dict
        if isinstance(v, dict):
            newprefix = prefix + k + "_"
            schema_generator(v, schema, newprefix)
        # handle nested list
        elif isinstance(v, list):
            newschema = newSchema(k)
            schema[k] = id_gen_type
            newschema[id_gen_type] = int
            if isinstance(v[0], dict):
                schema_generator(v[0], newschema, "")
            else:
                newschema[k] = type(v)
        else:
            schema[prefix + k] = type(v)

schema_generator(table, newSchema("default"), "")

for name, schema in schemas.items():
    print("Printing schema", name)
    for k, v in schema.items():
        print("\t", k, v)
