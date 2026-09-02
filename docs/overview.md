# Syntax Overview
The syntax for TML is similar to HTML, except it uses Toga attributes and tag names. <br>
Any Toga widget is supported in TML, as long as it is imported at the top of the file with correct TML import syntax. <br>
For instance, if the Toga code is `toga.Label("Hello", style=Pack(color=#ff0000))` then the TML code is `<Label "Hello" style=Pack(color=#ff0000)/>` <br>
It is very simple and very intutive if you already know Toga. <br>
The Toga documentation can be found here to see specifics of the framework: [Toga API Reference](https://toga.beeware.org/en/stable/reference/api/)

## Prefabs
Prefabs are a part of TML which isn't part of base Toga. They allow the definition of preset Toga widgets with custom tags, which may be reused later in the TML code.
- All prefabs must be defined in the `<Prefabs></Prefabs>`. 
- The structure for a prefab is `<CustomTagName "Argument if necessary" type="the normal Toga tag name e.g. Label" attribute1="this" attribute2=(that)/>`
- The prefab can then be called with `<CustomTagName name="name_of_this_instance"/>`
- Instances of prefabs can still be modified from their original, and attributes and arguments from the instance will be prioritised over the originals. <br> 
  Example: `<CustomTagName attribute1="I've changed my mind"/>`
