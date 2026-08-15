counter = 0

def generate(node):
    global counter
    match node["type"]:
        case "Document":
            allStatements = []
            for child in node["children"]:
                childStatements, childVar = generate(child)
                allStatements.append(childStatements)
            print("Generated")
            return "\n".join(allStatements)
        case "Tag":
            pairs = []
            for key, attribute in node["attributes"].items():
                if attribute["kind"] == "string":
                    pairs.append(f'{key}="{attribute["value"]}"')
                elif attribute["kind"] == "raw":
                    pairs.append(f'{key}={attribute["value"]}')
            attributes = ", ".join(pairs)
            counter += 1
            var = f"tag{counter}"
            argumentParts = [f'"{argument}"' for argument in node["arguments"]]
            argumentString = ", ".join(argumentParts)
            allArguments = ", ".join(filter(None, [argumentString, attributes]))
            statement = f"{var} = toga.{node["name"]}({allArguments})"
            return statement, var
        case "Box":
            childStatementsList = []
            childVars = []
            for child in node["children"]:
                child_statements, child_var = generate(child)
                childStatementsList.append(child_statements)
                childVars.append(child_var)

            counter += 1
            var = f"box{counter}"
            box_statement = f"{var} = toga.Box()"
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
            counter += 1
            var = "main_box"
            box_statement = f"{var} = toga.Box()"
            add_statement = f"{var}.add({', '.join(childVars)})"
            all_statements = "\n".join(childStatementsList + [box_statement, add_statement])
            return all_statements, var
        case "Prefabs":
            allStatements = []
            for child in node["children"]:
                childStatements, childVar = generate(child)
                allStatements.append(childStatements)
            return "\n".join(allStatements), None