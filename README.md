# Python-Stylesheet-Parser
Stylesheet parser
The topic of this task is to build a program that parses the hypothetical file format shown below.

The program should detect whether the parsed file matches the grammar of the language. If the file is incorrect, specify precisely where the error is in the file (giving at least the line number).

It is important to prepare a separate text file with the grammar (in the form of production, distinguishing between terminal and non-terminal symbols) before writing the parser.

An example of a valid file
Below is a file format that resembles a combination of CSS and Python script.
Indentation in this format is crucial. We only consider tabs as indentation.
You can assume that the file ends with a blank line.

[Valid file example](good.txt)

Invalid file
Example errors that will help you develop correct grammar:

[Invalid file example](bad.txt)
