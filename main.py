import json

f = open("example.json", "r")
table = json.load(f)

schemas = {}

def newSchema(name):
    schemas[name] = {}
    return schemas[name]

id_type = "id"

def schema_generator(schema, json_key, json_value):
    if isinstance(json_value, dict):
        for k, v in json_value.items():
            # handle nested dict
            if isinstance(v, dict):
                # flatten nested dictionary into schema
                newprefix = json_key + k + "_"
                schema_generator(schema, newprefix, v)
            else:
                newprefix = json_key + k
                schema_generator(schema, newprefix, v)
    elif isinstance(json_value, list):
        # create new schema
        newschema = newSchema(json_key)
        # set up references from current schema
        # and we look up the correct schema by k
        schema[json_key] = id_type
        newschema[id_type] = int
        # recursively go into the first element
        # NOTE: the assumption here is that the list is made of
        # self-similar items, and they are not lists of lists
        schema_generator(newschema, "", json_value[0])
    else:
        schema[json_key] = type(json_value)

schema_generator(newSchema("default"), "", table)

def createTableFromSchema(name, schema):
    # atm just report what we've found
    print("Printing schema", name)
    for k, v in schema.items():
        print("\t", k, v)

for name, schema in schemas.items():
    createTableFromSchema(name, schema)

def parseData(tables, schemas, current_schema, json):
    # should also be recursive
    pass
