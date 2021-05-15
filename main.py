import json

f = open("example.json", "r")
table = json.load(f)

schemas = {}

def newSchema(name):
    schemas[name] = {}
    return schemas[name]

id_type = "id"

def schema_generator(json_dict, schema, prefix=""):
    for k, v in json_dict.items():
        # handle nested dict
        if isinstance(v, dict):
            # flatten nested dictionary into schema
            newprefix = prefix + k + "_"
            schema_generator(v, schema, newprefix)
        # handle nested list
        elif isinstance(v, list):
            # create new schema
            newschema = newSchema(k)
            # set up references from current schema
            # and we look up the correct schema by k
            schema[k] = id_type
            newschema[id_type] = int
            # if our new schema is a dictionary, fill the schema
            if isinstance(v[0], dict):
                schema_generator(v[0], newschema, "")
            # if it is not a dictionary, it's a list of values
            else:
                newschema["value"] = type(v)
        else:
            schema[prefix + k] = type(v)

schema_generator(table, newSchema("default"), "")

for name, schema in schemas.items():
    print("Printing schema", name)
    for k, v in schema.items():
        print("\t", k, v)
