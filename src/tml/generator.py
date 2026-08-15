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
            pairs = [f'{key}="{value}"' for key, value in node["attributes"].items()]
            arguments = ", ".join(pairs)
            counter += 1
            var = f"tag{counter}"
            statement = f"{var} = toga.{node["name"]}({arguments})"
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
            var = "body"
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