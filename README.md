# CS2450-Group-Project
A repository for the CS2450 Software Engineering Group Project - Spring 2024

# prototype UVSIM.py
Our product. It is a virtual machine that reads a file and executes the commands in the file. It has a 100-word memory and interprets BasicML. Files can contain 4 digit commands or 6 digit commands.

How to use: 
Run the python file prototype_UVSIM.py. This will open up a GUI. In the input File input field, enter the file path to the file you want to run. It will be able to run a file from anywhere in the computer, provided the file path is correct. For example, if the file is in your C: drive, enter C:\FolderYourFileIsIn\FileYouWantToRun.txt into the input field and press the Run button to run the file. If the program requires you to input any commands, it will prompt you from the output field. Enter a valid command into the Read input field, and press submit. Pressing Submit will continue file execution. Anything the program writes out will be in the Write field. Any errors will appear in the Output field, and the program will notify you when it is finished executing in the Output Field. The program supports 4-digit words and 6-digit words, but not mixed files. It will convert 4-digit word files into 6 digit word files. All commands entered into the read field when prompted need to be 6 digit words.

Using the color picker: 
Enter 3 rgb values between 1 and 255, all seperated by commas, into the primary or secondary color fields, and click the apply button next to the field to change the colors. 
Here is an example: 
Primary Color: 155,155,155
Clicking apply in this example will change the primary color to gray.

Using the editor:
Enter the file name, and click the Load into File button. Every value in memory is loaded in as a space seperated value. You can edit the values individually, as well as copy, paste, and cut. 
Make sure the values are always seperated by one space and are valid 4 digit commands! Press the Save File button when you are finished editing to save the edits. 

Opening New Tabs:
If you wish to open multiple files at the same time, pressing the New Tab button will open a new instance of the simulator in a new tab. Each tab will be able to run parallel to each other with no interference. 

6 digit file commands currently implemented:
Read = 010 - Prompts user to input a command from command line.
Write = 011 - Displays a word from the specified memory location onto the screen. The specified memory location is the last 2 digits of a word.
Load = 020 - Load a word from a specific memory location to the accumulator.
Store = 021 - Store a word from the accumulator into a specific location. 
Add = 030 - add accumulator and specified word together
Subtract = 031 - subtract specified word from accumulator
Divide = 032 - divide accumulator by specified word
Multiply = 033 - multiply accumulator and specified word
Branch = 040 - branch to a specific memory location
BranchNeg = 041 - branch if accumulator is negative
BranchZero = 042 - branch if accumulator is zero
Halt = 043 - stop the program

4 digit words implemented file commands (depracated):
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
