from . import lexer
 
def parse(tokens):
    pos = 0
    def peek(): return tokens[pos]
    def consume():
        nonlocal pos
        t = tokens[pos]
        pos += 1
        return t
    def tagNameOf(tagValue):
        return tagValue.split(" ", 1)[0]
    def parseDocument():
        seenNonImport = False
        children = []
        while peek()["type"] != lexer.TOKENTYPE["EOF"]:
            while peek()["type"] == lexer.TOKENTYPE["NEWLINE"]: consume()
            if peek()["type"] == lexer.TOKENTYPE["EOF"]: break
            elif peek()["type"] == lexer.TOKENTYPE["TAG"]:
                if peek()["value"].startswith("Import"):
                    if seenNonImport:
                        raise Exception("P001 - Import statements must be at the top of the tml file, before any other tags")
                    children.append(parseImport())
                else:
                    seenNonImport = True
                    children.append(parseTag())
            elif peek()["type"] == lexer.TOKENTYPE["TAGOPEN"]:
                seenNonImport = True
                name = tagNameOf(peek()["value"])
                if name == "Body":
                    children.append(parseBody())
                elif name == "Prefabs":
                    children.append(parsePrefabs())
                elif name == "OptionContainer":
                    children.append(parseOptionContainer())
                else:
                    children.append(parseContainer())
            else:
                raise Exception(f"P002 - Unexpected token {peek()['type']}")
        return {"type": "Document", "children": children}
    def parseTag():
        t = consume()
        name, attributes = parseText(t["value"])
        attributes, arguments = parseAttributes(attributes)
        return {"type": "Tag", "name": name, "arguments": arguments, "attributes": attributes, "children": []}
    def parseBody():
        t = consume()
        name, attributes = parseText(t["value"])
        attributes, _ = parseAttributes(attributes)
        return {"type": "Body", "attributes": attributes, "children": parseUntil(lexer.TOKENTYPE["TAGCLOSE"], name)}
    def parsePrefabs():
        t = consume()
        name, _ = parseText(t["value"])
        return {"type": "Prefabs", "children": parseUntil(lexer.TOKENTYPE["TAGCLOSE"], name)}
    def parseContainer():
        t = consume()
        name, attributes = parseText(t["value"])
        attributes, _ = parseAttributes(attributes)
        return {"type": "Container", "name": name, "attributes": attributes, "children": parseUntil(lexer.TOKENTYPE["TAGCLOSE"], name)}
    def parseOptionContainer():
        t = consume()
        name, attributes = parseText(t["value"])
        attributes, _ = parseAttributes(attributes)
        return {"type": "OptionContainer", "attributes": attributes, "children": parseUntil(lexer.TOKENTYPE["TAGCLOSE"], name)}
    def parseUntil(closeType, expectedName=None):
        children = []
        while peek()["type"] != lexer.TOKENTYPE["EOF"] and peek()["type"] != closeType:
            if peek()["type"] == lexer.TOKENTYPE["NEWLINE"]:
                consume()
                continue
            elif peek()["type"] == lexer.TOKENTYPE["TAG"]:
                children.append(parseTag())
            elif peek()["type"] == lexer.TOKENTYPE["TAGOPEN"]:
                name = tagNameOf(peek()["value"])
                if name == "Body":
                    children.append(parseBody())
                elif name == "OptionContainer":
                    children.append(parseOptionContainer())
                else:
                    children.append(parseContainer())
            else:
                raise Exception(f"P002 - Unexpected token {peek()['type']}")
        if peek()["type"] != closeType:
            raise Exception(f"P004 - Unclosed tag, expected {closeType} but got end of file")
        closeTag = consume()
        if expectedName is not None and closeTag["value"] != expectedName:
            raise Exception(
                f"P005 - Mismatched closing tag: expected </{expectedName}> but found </{closeTag['value']}>"
            )
        return children
    def parseText(input):
        if " " in input:
            name, attributes = input.split(" ", 1)
        else:
            name, attributes = input, ""
        return name, attributes
    def parseAttributes(input):
        arguments = []
        attributes = {}
        i = 0
        while i < len(input):
            if input[i] == "=":
                if input[i+1] == "\"":
                    j = i + 2
                    while j < len(input) and not (input[j] == "\"" and input[j-1] != "\\"):
                        j += 1
                    key = input[:i].strip()
                    value = input[i+2:j]
                    attributes[key] = {"kind": "string", "value": value}
                    input = input[j+1:]
                    i = 0
                elif input[i+1] == "(":
                    j = i + 2
                    while j < len(input) and input[j] != ")":
                        j += 1
                    key = input[:i].strip()
                    value = input[i+1:j+1]
                    attributes[key] = {"kind": "raw", "value": value}
                    input = input[j+1:]
                    i = 0
                else:
                    k = i + 1
                    while k < len(input) and input[k] != " " and input[k] != "(":
                        k += 1
                    if k < len(input) and input[k] == "(":
                        depth = 1
                        j = k + 1
                        while j < len(input) and depth > 0:
                            if input[j] == "(":
                                depth += 1
                            elif input[j] == ")":
                                depth -= 1
                            j += 1
                        key = input[:i].strip()
                        value = input[i+1:j]
                        attributes[key] = {"kind": "raw", "value": value}
                        input = input[j:]
                        i = 0
                    else:
                        key = input[:i].strip()
                        value = input[i+1:k].strip()
                        attributes[key] = {"kind": "raw", "value": value}
                        input = input[k:]
                        i = 0
            elif input[i] == "\"":
                j = i + 1
                while j < len(input) and not (input[j] == "\"" and input[j-1] != "\\"):
                    j += 1
                value = input[i+1:j]
                arguments.append(value)
                input = input[j+1:]
                i = 0
            else:
                i += 1
        return attributes, arguments
    def parseImport():
        t = consume()
        _, attributes = parseText(t["value"])
        attributes, _ = parseAttributes(attributes)
        return {"type": "Import", "attributes": attributes}
    print("Parsed")
    return parseDocument()