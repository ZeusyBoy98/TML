def generate(node):
    match node["type"]:
        case "Document":
            return "\n".join([generate(child) for child in node["children"]])
        case "Tag":
            return f"toga.{node["name"]}()"