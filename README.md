# CS2450-Group-Project
A repository for the CS2450 Software Engineering Group Project - Spring 2024

# prototype UVSIM.py
Our product. It is a virtual machine that reads a file and executes the commands in the file. It has a 250-word memory and interprets BasicML. Files can contain 4 digit commands or 6 digit commands.

How to use: 
Run the python file prototype_UVSIM.py. This will open up a GUI. In the input File input field, enter the file path to the file you want to run. It will be able to run a file from anywhere in the computer, provided the file path is correct. For example, if the file is in your C: drive, enter C:\FolderYourFileIsIn\FileYouWantToRun.txt into the input field and press the Run button to run the file. If the program requires you to input any commands, it will prompt you from the output field. Enter a valid command into the Read input field, and press submit. Pressing Submit will continue file execution. Anything the program writes out will be in the Write field. Any errors will appear in the Output field, and the program will notify you when it is finished executing in the Output Field. 
If you wish to open multiple files at the same time, pressing the New Tab button will open a new instance of the simulator in a new tab. Each tab will be able to run parallel to each other with no interference. 

Using the color picker: 
Enter 3 rgb values between 1 and 255, all seperated by commas, into the primary or secondary color fields, and click the apply button next to the field to change the colors. 
Here is an example: 
Primary Color: 155,155,155
Clicking apply in this example will change the primary color to gray.

Using the editor:
Enter the file name, and click the Load into File button. Every value in memory is loaded in as a space seperated value. You can edit the values individually, as well as copy, paste, and cut. 
Make sure the values are always seperated by one space and are valid 4 digit commands! Press the Save File button when you are finished editing to save the edits. 

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
The GUI will have an Input file field, Read field, Write field, Accumulator field, and Output field. 
To begin, type the file name you want to run into the Input file field at the top, the press the Run button. It will run the program from the file and write the output to the Write field. The final accumulator will be displayed on the Accumulator field, and the whole memory or any errors encountered are displayed in the Output Field on the bottom. 
If there are any READ commands in the file, you will be prompted to enter a BasicML command. Pressing Submit will continue execution of the file. 
If the file contains muliple READ commands, you will need to enter a command into the Read field and press Submit each time. 
Once the program finishes, you may enter a different file to run in the Input field or exit the program.
