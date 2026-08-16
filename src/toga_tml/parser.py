from . import lexer

def parse(tokens):
    pos = 0
    def peek(): return tokens[pos]
    def consume(): 
        nonlocal pos
        t = tokens[pos]
        pos += 1
        return t
    def expect(type):
        t = consume()
        if t["type"] != type:
            raise Exception(f"Expected {type}, got {t["type"]}")
            return t
    def parseDocument():
        children = []
        while peek()["type"] != lexer.TOKENTYPE["EOF"]:
            while peek()["type"] == lexer.TOKENTYPE["NEWLINE"]: consume()
            if peek()["type"] == lexer.TOKENTYPE["EOF"]: break
            elif peek()["type"] == lexer.TOKENTYPE["TAG"]:
                children.append(parseTag())
            elif peek()["type"] == lexer.TOKENTYPE["TAGOPEN"]:
                if peek()["value"].startswith("Box"):
                    children.append(parseBox())
                elif peek()["value"].startswith("Body"):
                    children.append(parseBody())
                # elif peek()["value"].startswith("Prefabs"):
                    # children.append(parsePrefabs())
                else:
                    raise Exception(f"Unknown tag {peek()}")
            else:
                raise Exception(f"Unexpected token {peek()["type"]}")
        return {"type": "Document", "children": children}
    def parseTag():
        t = consume()
        name, attributes = parseText(t["value"])
        attributes, arguments = parseAttributes(attributes)
        return {"type": "Tag", "name": name, "arguments": arguments, "attributes": attributes, "children": []}
    def parseBody():
        t = consume()
        _, attributes = parseText(t["value"])
        attributes, _ = parseAttributes(attributes)
        return {"type": "Body", "attributes": attributes, "children": parseUntil(lexer.TOKENTYPE["TAGCLOSE"])}
    # def parsePrefabs():
        # consume()
        # return {"type": "Prefabs", "children": parseUntil(lexer.TOKENTYPE["TAGCLOSE"])}
    def parseBox():
        t = consume()
        _, attributes = parseText(t["value"])
        attributes, _ = parseAttributes(attributes)
        return {"type": "Box", "attributes": attributes, "children": parseUntil(lexer.TOKENTYPE["TAGCLOSE"])}
    def parseUntil(closeType):
        children = []
        while peek()["type"] != lexer.TOKENTYPE["EOF"] and peek()["type"] != closeType:
            if peek()["type"] == lexer.TOKENTYPE["NEWLINE"]:
                consume()
                continue
            elif peek()["type"] == lexer.TOKENTYPE["TAG"]:
                children.append(parseTag())
            elif peek()["type"] == lexer.TOKENTYPE["TAGOPEN"]:
                if peek()["value"].startswith("Box"):
                    children.append(parseBox())
                elif peek()["value"].startswith("Body"):
                    children.append(parseBody())
                # elif peek()["value"].startswith("Prefabs"):
                #     children.append(parsePrefabs())
                else:
                    raise Exception(f"Unknown tag {peek()["value"]}")
        if peek()["type"] != closeType:
            raise Exception(f"Unclosed tag, expected {closeType} but hit EOF")
        consume()
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
                        attributes[key] = {"kind": "string", "value": value}
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
    print("Parsed")
    return parseDocument()