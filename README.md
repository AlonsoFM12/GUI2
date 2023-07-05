# GUI2


---

# GUI Description

The GUI features several "LabelFrames" to enhance user interaction with the application. Below is a description of each one:

## Folder location
In this section, users can select the folder they wish to analyze. A Label will display the selected folder's address.

## Machine / Files
These two LabelFrames allow users to select parameters for the files they want to work with.

## Search
In this section, there is an Entry field where users can input the number of searches they want to perform. Upon clicking the "Generate search boxes" button, a new LabelFrame named "Parameter Input" will be generated. Within this LabelFrame, two Entry fields will be created for each search. The first one is for entering the "UID," and the second one is for the "Event."

## Output
In this final LabelFrame, users can select the type of output for the results.

For this version, only "Numerical value" and "Percentage value" outputs are enabled. For each of these output types, two text files will be generated. The first file will contain the addresses of the files that have a "?" in any of the columns. The second file will be a table including the serial number, usage, searches performed, and whether a question mark [?] was found in any line.

---
