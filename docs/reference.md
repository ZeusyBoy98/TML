# Syntax Reference

## Imports
- Imports must be put in self closing tags at the top of a TML file. 
- The syntax is `<Import from="location" import="thing"` 
- The quotes are optional, `from=location import=thing` is also valid TML code.

## Comments
- TML comments are the same as HTML comments T
- They can be single line or multi-line
- They cannot go inside of other code e.g. `<Label <!--Comment--> />` is not valid TML code.

## Body
- All TML user interface code should be inside the `<Body></Body>` tags.
- Anything outside of these tags is either an `<Import>` or a `<Prefab>`

## Referencing
- If you want to be able to refer to a TML element in a python file, a `name="INSERT_NAME_HERE"` attribute must be added.
- It can then be referred to with `self.INSERT_NAME_HERE`

## Tags
- All TML tags are self closing, except for `<Body></Body>`, `<Box></Box>`, and `<Prefabs></Prefabs>`
- This means that when using a label or a button, text that will be displayed on it must go in quotes after the tag opening.
- This is called the "argument" e.g. `<Label "Hello"/>`

## Attributes
- Any Toga attributes you wish to use in a tag can go after the argument.
- If you don't have an argument, they can go after the tag opening. 
- The syntax for attributes will be the same as Toga syntax, except no commas separating attributes e.g. `<Label "Hi" name="label1" margin=5/>`

## Prefabs
- See Syntax Overview