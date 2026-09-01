# Troubleshooting
## L001
A comment has been started with `<!--` but has not been closed. Any comments must be closed with `-->`. <br>
Error Example:
```xml
<!-- This comment does not close
<Body>
    <Label "Hi"/>
</Body>
```
Fix Example:
```xml
<!-- This comment does close -->
<Body>
    <Label "Hi"/>
</Body>
```

## P001
An import statement has been found not at the top of a file. All import statements should be before any other code. <br>
Error Example:
```xml
<Body>
    <Label "Hi"/>
</Body>

<Import from="Toga" import="Pack"/>
```
Fix Example:
```xml
<Import from="Toga" import="Pack"/>

<Body>
    <Label "Hi"/>
</Body>
```

## P002
A tag non-self closing has been used in the TML code which is unknown to the language. <br>
Error Example:
```xml
<ThisTagIsBad>
    <Label "hi"/>
</ThisTagIsBad>
```
Fix Example:
```xml
<Body>
    <Label "hi"/>
</Body>
```

## P003
Somehow in lexing, a token has been passed to the parser that isn't recognised. It is highly unlikey that this error will be encountered. The primary purpose it was added is for development.

## P004
This is an unclosed non self-closing tag. All non self-closing tags must be closed after their inner code. <br>
Error Example:
```xml
<Body>
    <Box>
        <Label "hi"/>
</Body>
```
Fix Example:
```xml
<Body>
    <Box>
        <Label "hi"/>
    </Box>
</Body>
```

## G001
A prefab has been used in the body without assigning a name. All instances of a prefab must have a name to distinguish it from other uses. <br>
Error Example:
```xml
<Prefabs>
    <WideHi "Hi" type="Label" margin=5>
</Prefabs>

<Body>
    <WideHi/>
</Body>
```
Fix Example:
```xml
<Prefabs>
    <WideHi "Hi" type="Label" margin=5>
</Prefabs>

<Body>
    <WideHi name="instance1"/>
</Body>
```

## G002
Any children of an `<OptionContainer>` tag require a title attribute. <br>
Error Example:
```xml
<Body>
    <OptionContainer>
        <Box>
            <Label "Content here"/>
        </Box>
    </OptionContainer>
</Body>
```
Fix Example:
```xml
<Body>
    <OptionContainer>
        <Box title="Home">
            <Label "Content here"/>
        </Box>
    </OptionContainer>
</Body>
```

## M001
There is no `<Body>` tag containing the UI code. All TML UI code must be contained inside of a `<Body>` tag.
Error Example:
```xml
<Label "Hi"/>
```
Fix Example:
```xml
<Body>
    <Label "Hi"/>
</Body>
```