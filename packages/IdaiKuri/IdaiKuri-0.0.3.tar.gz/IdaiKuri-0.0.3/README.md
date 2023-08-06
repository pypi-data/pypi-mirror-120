# IdaiKuri (Generic Simple Template Engine)

- A Generic Simple Template Engine which maps Function Calls and Variables in templates(based on regex pattern) with code to create Files as variants of the Template Choosen.
- Check out the example code in repo ( https://github.com/Palani-SN/IdaiKuri ) for reference

## Filler

- To be used to fill a template from code using 
   - variables and function definitions in code and
   - function calls in template
- Sample usage of the file is as given below (Refer TemplateFiles for template examples)

```python
from IdaiKuri.Filler import FillerTemplateEngine as TemplateEngine
from IdaiKuri.Filler import Interface

TE = TemplateEngine();
TE.InFile("TemplateFiles/Template_DefaultCase1.html", True); 
temp_vars = TE.VARS();

temp_vars.Portrait = "images/GuidoVanRossum.png";
temp_vars.Logo = "images/PythonLogo.png";
temp_vars.FullName = "Guido Van Rossum";
temp_vars.Position = "Python's Benevolent Dictator for life";
temp_vars.Quote = "In Python, every symbol you type is essential.";
temp_vars.Author = "Guido van Rossum";
result_dict = TE.OutFile(temp_vars, "GeneratedFiles/GuidoVanRossum_DefaultCase1.html");
```
### CodeFlow

![](https://github.com/Palani-SN/IdaiKuri/blob/master/FillerCodeflow.PNG?raw=true)

### Interface (Decorator)

- Interface is the decorator to be used to define methods in child class extended from Filler.py/TemplateEngine class
- Sample code for using Interface decorator is shown below (Refer Examples for more understanding)

```python
from IdaiKuri.Filler import FillerTemplateEngine as TemplateEngine
from IdaiKuri.Filler import Interface

class AdvancedTemplate(TemplateEngine):
    @Interface
    def get_portrait(self, name):
        return "images/"+name.replace(" ","")+".png";
    @Interface
    def get_logo(self, contrib):
        return "images/"+contrib+"Logo.png"
```
### TemplateEngine (class from Filler.py)

- Initialising class helps to configure the RegexEdges and it also validates the pattern based on the second parameter FuncCallTemplate
- Arguments
  - Arg1 - RegexEdges (a tuple with start and end delimiters)
  - Arg2 - FuncCallTemplate is the sample string with "self.FUNC_CALL()" keyword to validate the RegexEdges
- Sample regex configurations in TemplateEngine Initialisation is shown below.

```python
## Default RegexEdges=("{{", "}}"),
## FuncCallTemplate="{{self.FUNC_CALL()}}"
TE1 = TemplateEngine();

## RegexEdges=("_StArT_", "_eNd_"),
## FuncCallTemplate="_StArT_self.FUNC_CALL()_eNd_"
TE2 = TemplateEngine(("_StArT_", "_eNd_"), "_StArT_self.FUNC_CALL()_eNd_");

## RegexEdges=("<<", ">>"),
## FuncCallTemplate="<<self.FUNC_CALL()>>"
TE3 = TemplateEngine(("<<", ">>"), "<<self.FUNC_CALL()>>");

## RegexEdges=("\\[\\[", "\\]\\]"),
## FuncCallTemplate="[[self.FUNC_CALL()]]"
TE4 = TemplateEngine(("\\[\\[", "\\]\\]"), "[[self.FUNC_CALL()]]");

## RegexEdges=("{\\[<{\\[", "}\\]>}\\]"),
## FuncCallTemplate="{[<{[self.FUNC_CALL()}]>}]"
TE5 = TemplateEngine(("{\\[<{\\[", "}\\]>}\\]"), "{[<{[self.FUNC_CALL()}]>}]");
```
#### InFile()

- Gets the Template Name/Path of the template function calls that is going to be used.
- Will initialize the MapDict for updating the function calls in the template.

```python
## Definition
def InFile(self, TemplateName, DebugTokens=False):
```
- Arguments
  - Arg1 - TemplateName (a String that contains the Path/Name of the template)
  - Arg2 - DebugTokens (If True prints the function calls of template, If false doesnt print)

#### VARS()

- Returns an Instance of the an empty class, for argument variables storage.

#### OutFile()

- Defines the file Name/Path that needs to be generated with the filled content from the template.
- It edits the template based on the dependencies/arguments of the template function calls.

```python
## Definition
def OutFile(self, FuncArgVars, UniqueName):
```
- Arguments
  - Arg 1 - FuncArgVars (an instance of class with appropriate members filled)
  - Arg 2 - UniqueName (filename to be generated with the edited template content)
- Returns 
  - MapDict -  the result as a dictionary ( keys : func_calls and values : Return_values)

## Parser

- To be used to parse a file by comparing
  - function calls in a template and
  - file that is generated using the template
- Sample usage of the file is as given below (Refer TemplateFiles for template examples)

```python
from IdaiKuri.Parser import ParserTemplateEngine as TemplateEngine

PE = TemplateEngine();
print("\n", "Template_DefaultCase1.html", "GuidoVanRossum_DefaultCase1.html", "\n");
diffdict = PE.Root("TemplateFiles/Template_DefaultCase1.html", "GeneratedFiles/GuidoVanRossum_DefaultCase1.html");
for key in diffdict.keys():
    print("   ", key, "->", diffdict[key]);
```
### CodeFlow

![](https://github.com/Palani-SN/IdaiKuri/blob/master/ParserCodeflow.PNG?raw=true)

### TemplateEngine (class from Parser.py)

- Initialising class helps to configure the RegexEdges and it also validates the pattern based on the second parameter FuncCallTemplate
- Arguments
  - Arg1 - RegexEdges (a tuple with start and end delimiters)
  - Arg2 - FuncCallTemplate is the sample string with "self.FUNC_CALL()" keyword to validate the RegexEdges
- Sample regex configurations in TemplateEngine Initialisation is shown below

```python
## Default RegexEdges=("{{", "}}"),
## FuncCallTemplate="{{self.FUNC_CALL()}}"
TE1 = TemplateEngine();

## RegexEdges=("_StArT_", "_eNd_"),
## FuncCallTemplate="_StArT_self.FUNC_CALL()_eNd_"
TE2 = TemplateEngine(("_StArT_", "_eNd_"), "_StArT_self.FUNC_CALL()_eNd_");

## RegexEdges=("<<", ">>"),
## FuncCallTemplate="<<self.FUNC_CALL()>>"
TE3 = TemplateEngine(("<<", ">>"), "<<self.FUNC_CALL()>>");

## RegexEdges=("\\[\\[", "\\]\\]"),
## FuncCallTemplate="[[self.FUNC_CALL()]]"
TE4 = TemplateEngine(("\\[\\[", "\\]\\]"), "[[self.FUNC_CALL()]]");

## RegexEdges=("{\\[<{\\[", "}\\]>}\\]"),
## FuncCallTemplate="{[<{[self.FUNC_CALL()}]>}]"
TE5 = TemplateEngine(("{\\[<{\\[", "}\\]>}\\]"), "{[<{[self.FUNC_CALL()}]>}]");
```
#### Root()

- Parses the template Name/Path and file Name/Path.
- Returns the differences between them as a dict.

```python
## Definition
def Root(self, TemplateName, FileName):
```
- Arguments
  - Arg 1 - TemplateName (Name of the template to be edited)
  - Arg 2 - FileName (filename to be generated with the edited template content)
- Returns 
  - RootDict - the result as a dictionary (keys : func_calls and values : Return_values)