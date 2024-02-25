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

# class MainGridLayout
To operate the GUI, simply run the python file. First, input a valid txt file to the "Input File: " text box, then click the "Run" button.
If the inputted file is found to be invalid, the "Output: " text box will display the message "File Not Found".
Then, the "Output: " should prompt you to "Please input command in Read Field". Here, you should input a valid memory assignment, such as "3009", to the "Read: " text box, then click the "Submit" button.
The GUI will then run through "execute_program()", updating and outputting the memory value's to the "Output: " text box. 
Once the maximum memory value is met, the "Output: " text box will output "Program halted." from "execute_program()", and the "Accumulator: " text box will be updated to display the accumulator value.
Here you are safe to exit the program. 
