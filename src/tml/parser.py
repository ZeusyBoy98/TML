import lexer

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
            if peek()["type"] == lexer.TOKENTYPE["TAG"]:
                children.append(parseTag())
            if peek()["type"] == lexer.TOKENTYPE["TAGOPEN"]:
                if peek()["value"].startswith("Box"):
                    children.append(parseBox())
                elif peek()["value"].startswith("Body"):
                    children.append(parseBody())
                elif peek()["value"].startswith("Prefabs"):
                    children.append(parsePrefabs())
                else:
                    raise Exception(f"Unknown tag {peek()["value"]}")
        return {"type": "Document", "children": children}
    def parseTag():
        t = consume()
        name, attributes = parseText(t["value"])
        attributes = parseAttributes(attributes)
        return {"type": "Tag", "name": name, "attributes": attributes, "children": []}
    def parseBody():
        consume()
        return {"type": "Body", "children": parseUntil(lexer.TOKENTYPE["TAGCLOSE"])}
    def parsePrefabs():
        consume()
        return {"type": "Prefabs", "children": parseUntil(lexer.TOKENTYPE["TAGCLOSE"])}
    def parseBox():
        consume()
        return {"type": "Box", "children": parseUntil(lexer.TOKENTYPE["TAGCLOSE"])}
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
                elif peek()["value"].startswith("Prefabs"):
                    children.append(parsePrefabs())
                else:
                    raise Exception(f"Unknown tag {peek()["value"]}")
        if peek()["type"] != closeType:
            raise Exception(f"Unclosed tag, expected {closeType} but hit EOF")
        #if peek()["type"] == lexer.TOKENTYPE["TAGCLOSE"]:
        consume()
        return children
    def parseText(input):
        if " " in input:
            name, attributes = input.split(" ", 1)
        else:
            name, attributes = input, ""
        return name, attributes
    def parseAttributes(input):
        attributes = {}
        i = 0
        while i < len(input):
            if input[i] == "=":
                if input[i+1] == "\"":
                    j = i + 2
                    while j < len(input) and input[j] != "\"":
                        j += 1
                    key = input[:i].strip()
                    value = input[i+2:j]
                    attributes[key] = value
                    input = input[j+1:]
                    i = 0
                else:
                    key = input[:i].strip()
                    value = input[i+1:].strip()
                    attributes[key] = value
                    input = input[i+1:]
                    i = 0
            else:
                i += 1
        return attributes
    print("Parsed")
    return parseDocument()