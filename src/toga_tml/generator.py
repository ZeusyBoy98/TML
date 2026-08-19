counter = 0
prefabs = {}

def generate(node):
    global counter
    global prefabs
    match node["type"]:
        case "Document":
            allStatements = []
            for child in node["children"]:
                childStatements, childVar = generate(child)
                allStatements.append(childStatements)
            print("Generated")
            return "\n".join(allStatements)
        case "Tag":
            if node["name"] in prefabs:
                prefab = prefabs[node["name"]]
                if "name" not in node["attributes"]:
                    raise Exception(f"G001 - Prefab {node['name']} requires a 'name' attribute")
                node["attributes"].pop("type", None)
                usageAttributes = node["attributes"]
                node = {
                    "type": "Tag",
                    "name": prefab["type"],
                    "attributes": {**prefab["attributes"], **usageAttributes},
                    "arguments": node["arguments"] or prefab["arguments"],
                    "children": [],
                }

            pairs = []
            counter += 1
            var = f"tag{counter}"
            name_attributes = node["attributes"].pop("name", None)
            name = name_attributes["value"] if name_attributes else var
            for key, attribute in node["attributes"].items():
                if attribute["kind"] == "string":
                    pairs.append(f'{key}="{attribute["value"]}"')
                elif attribute["kind"] == "raw":
                    pairs.append(f'{key}={attribute["value"]}')
            attributes = ", ".join(pairs)
            argumentParts = [f'"{argument}"' for argument in node["arguments"]]
            argumentString = ", ".join(argumentParts)
            allArguments = ", ".join(filter(None, [argumentString, attributes]))
            statement = f"{var} = toga.{node['name']}({allArguments})\nself.{name} = {var}"
            return statement, var
        case "Box":
            childStatementsList = []
            childVars = []
            counter += 1
            var = f"box{counter}"
            name_attributes = node["attributes"].pop("name", None)
            name = name_attributes["value"] if name_attributes else var
            for child in node["children"]:
                child_statements, child_var = generate(child)
                childStatementsList.append(child_statements)
                childVars.append(child_var)
            pairs = []
            for key, attribute in node["attributes"].items():
                if attribute["kind"] == "string":
                    pairs.append(f'{key}="{attribute["value"]}"')
                elif attribute["kind"] == "raw":
                    pairs.append(f'{key}={attribute["value"]}')
            attributes = ", ".join(pairs)
            box_statement = f"{var} = toga.Box({attributes})\nself.{name} = {var}"
            add_statement = f"{var}.add({', '.join(childVars)})"

            all_statements = "\n".join(childStatementsList + [box_statement, add_statement])
            return all_statements, var
        case "Body":
            childStatementsList = []
            childVars = []
            for child in node["children"]:
                childStatements, childVar = generate(child)
                childStatementsList.append(childStatements)
                childVars.append(childVar)
            pairs = []
            for key, attribute in node["attributes"].items():
                if attribute["kind"] == "string":
                    pairs.append(f'{key}="{attribute["value"]}"')
                elif attribute["kind"] == "raw":
                    pairs.append(f'{key}={attribute["value"]}')
            attributes = ", ".join(pairs)
            box_statement = f"body = toga.Box({attributes})\nself.body = body"
            add_statement = f"body.add({', '.join(childVars)})"
            all_statements = "\n".join(childStatementsList + [box_statement, add_statement])
            return all_statements, "body"
        case "Prefabs":
            for child in node["children"]:
                attributes = child["attributes"]
                tag_type = attributes.pop("type")["value"]
                prefabs[child["name"]] = {"type": tag_type, "arguments": child["arguments"], "attributes": attributes}
            return "", None
        case "Import":
            fromAttribute = None
            importAttribute = None
            moduleAttribute = None
            for key, attribute in node["attributes"].items():
                if key == "from":
                    fromAttribute = attribute["value"]
                elif key == "import":
                    importAttribute = attribute["value"]
                elif key == "module":
                    moduleAttribute = attribute["value"]
            if fromAttribute:
                return f"from {fromAttribute} import {importAttribute}", None
            else:
                return f"import {moduleAttribute}", None