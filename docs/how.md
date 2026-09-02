# How It Works
Toga Markup Language goes through three stages to go from XML-style code to valid Toga. These three stages are pretty standard within markup languages. 

## Lexing
`lexer.py` goes through the code character by character, and turns it into tokens - important individual parts of code. In TML, the different tokens are:
```python
TOKENTYPE = {
    "TAG": "TAG",
    "TAGOPEN": "TAGOPEN",
    "TAGCLOSE": "TAGCLOSE",
    "NEWLINE": "NEWLINE",
    "EOF": "EOF",
}
```
The `TAG` token is used for self closing tags, so it takes everything in the `</>` and marks it as a token. `TAGOPEN` and `TAGCLOSE` are for tags that do not self-close and instead contain content. Once the input code has been tokenised, it moves onto the next stage.

## Parsing
`parser.py` takes the tokens and turns the into an AST - Abstract Syntax Tree. It does this by `peek()`ing and `consume()`ing tokens. It checks for and skips `NEWLINE`s, and it stops when it hits the `EOF`. For `TAG`s and `TAGOPEN`s it runs through different processes. Normal `TAG`s go through a `parseTag()` function, which splits apart the tag name, attributes, and arguments, and then puts them into valid syntax tree format. `TAG`s can also be `<Import/>`s, and that case is handled through the seperate `parseImport()` function, which is similar to `parseTag()` except it makes the type as an Import and doesn't accept arguments, only attributes. `TAGOPEN`s get further sorted into `parseBody()`, `parseBox()`, and `parsePrefab`. This covers the three posibilities for container tags. In all three cases it just adds all children to its AST, but with a different `"type":`. Once parsing it done it outputs the AST. This tree is important for the third and final stage. 

## Generating
`generator.py` takes in the Abstract Syntax Tree and sorts the parts into `Document`, `Import`, `Prefabs`, `Body`, `Box`, and `Tag`. Each case runs through a different but similar process: taking the input AST and restructuring its values into valid Toga code. For any non self-closing tags, this also involves generating code that adds the children to it. Prefabs are also added to a list which can then be references, and if a used `Tag` is in that list, then it uses the attributes from that already defined prefab. The generator then returns the finished Toga code.

It is then excectued in the `load()` function and returned to the Python file which called it.

## TML Code Example
```xml
<Import from="toga.style" import="Pack"/>

<!-- This is a comment -->
<Prefabs>
    <RedHi "Hello world" type="Label" style=Pack(color="#ff0000")/>
</Prefabs>

<Body>
    <RedHi/>
    <Box name="input_container"> 
        <TextInput name="name_input" flex=1/>
        <Button "Click me!" name="button" on_press=self.say_hello margin=5/>
    </Box>
</Body>
```