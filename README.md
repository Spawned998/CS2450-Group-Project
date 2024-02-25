# CS2450-Group-Project
A repository for the CS2450 Software Engineering Group Project - Spring 2024

# prototype UVSIM.py
Our product. It is a virtual machine that reads a file and executes the commands in the file. It has a 100-word memory and interprets BasicML. Words are 4 digits long.

How to use: 
Simply run the python file. All commands are given using the commmand line. Currently, you will be prompted to give a file to read. Enter "exit" to close the program. Test1.txt and Test2.txt are included in this folder for convenient testing. Make sure your file path is correct when entering the file. 

Currently implemented file commands:
Read = 10 - Prompts user to input a command from command line.
Write = 11 - Displays a word from the specified memory location onto the screen. The specified memory location is the last 2 digits of a word.
Load = 20 - Load a word from a specific memory location to the accumulator.
Store = 21 - Store a word from the accumulator into a specific location. 
Add = 30 - add accumulator and specified word together
Subtract = 31 - subtract specified word from accumulator
Divide = 32 - divide accumulator by specified word
Multiply = 33 - multiply accumulator and specified word
Branch = 40 - branch to a specific memory location
BranchNeg = 41 - branch if accumulator is negative
BranchZero = 42 - branch if accumulator is zero
Halt = 43 - stop the program

The file may contain a "-99999" sentinel value as well, but is not necessary. 

# test.py
Our unit tests to ensure everything continues to work correctly as we add more to the project.

# GUI
How to use: 
Make sure kivy is installed on your python environment. 
run prototype_UVSIM.py to open the Graphical User Interface.
The GUI will have an Input file field, Read field, Write field, Accumulator field, and Output field. Help and Debug menu are just placeholders for now, but will be implemented in the future. 
To begin, type the file name you want to run into the Input file field at the top, the press the Run button. It will run the program from the file and write the output to the Write field. The final accumulator will be displayed on the Accumulator field, and the whole memory or any errors encountered are displayed in the Output Field on the bottom. 
If there are any READ commands in the file, you will be prompted to enter a BasicML command. Pressing Submit will continue execution of the file. 
If the file contains muliple READ commands, you will need to enter a command into the Read field and press Submit each time. 
Once the program finishes, you may enter a different file to run in the Input field or exit the program.
