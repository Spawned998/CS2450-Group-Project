from math import e

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

class UVSimulator:
    def __init__(self):
        # Initialize UVSim components
        self.memory = [0] * 100
        self.accumulator = 0
        self.instruction_counter = 0

    def load_program_from_file(self, filename):
        # Load BasicML program from a text file into memory starting at location 00
        try:
            with open(filename, 'r') as file:
                program = [int(line.strip()) for line in file]
            self.memory[:len(program)] = program
            return True
            
        except Exception as e:
            return False

    def verify_input(self, entry):
        #Verify the user enters a 4 digit value- reject all other inputs.
        if len(entry) == 4:
            try:
                int(entry)
            except Exception as e:
                return False
            return True
        return False
        
simulator = UVSimulator()

class ProgramController:
    def __init__(self, simulator):
        self.simulator = simulator
        self.output = [] #used to write output to GUI
        self.read_control = False #used to stop program to grab read input from gui
        self.value = 0 #used to store read input from gui
        self.done = True #used to stop gui from outputting prematurely

    def execute_program(self, max_iterations = 100):
    # Execute BasicML program
        while (self.simulator.instruction_counter < max_iterations):
            instruction = self.simulator.memory[self.simulator.instruction_counter]
            if instruction == -99999:
                return "\nEnd of file."
                
            opcode = instruction // 100
            operand = instruction % 100

            # if opcode == 10:  # READ
            #     #exits the loop so the user can input in the read field
            #     if self.read_control is True:
            #         self.simulator.memory[operand] = self.value
            #         self.read_control = False
            #         self.done = True
            #     else:
            #         self.done = False
            #         return "\nPlease input command in Read Field"
                    
            if( opcode == 10 or
                opcode == 11 or
                opcode == 20 or
                opcode == 21):
                if self.load_store_execution(opcode, operand):
                    return self.load_store_execution(opcode, operand)


            elif (opcode == 30 or
                  opcode == 31 or
                  opcode == 32 or
                  opcode == 33):
                self.math_execution(opcode, operand)
                if self.math_execution(opcode, operand):
                    return self.math_execution(opcode, operand)
                

            elif (opcode == 40 or
                  opcode == 41 or
                  opcode == 42):
                self.branch_execution(opcode, operand)
                if self.branch_execution(opcode, operand):
                    return self.branch_execution(opcode, operand)

            elif opcode == 43:  # HALT
                return "\nProgram halted."
                
            
            else:
                #Invalid opcode
                return (f"\nInvalid opcode: {opcode} is not a valid command.\nExiting program.")
                
            self.simulator.instruction_counter += 1

    
    def load_store_execution(self, opcode, operand):
        if opcode == 10:  # READ
            #exits the loop so the user can input in the read field
            if self.read_control is True:
                self.simulator.memory[operand] = self.value
                self.read_control = False
                self.done = True
            else:
                self.done = False
                return "\nPlease input command in Read Field"
                    
        elif opcode == 11:  # WRITE
            self.output.append(self.simulator.memory[operand])

        elif opcode == 20:  # LOAD
            self.simulator.accumulator = self.simulator.memory[operand]

        elif opcode == 21:  # STORE
            self.simulator.memory[operand] = self.simulator.accumulator


    def math_execution(self, opcode, operand):
        if opcode == 30:  # ADD
                self.simulator.accumulator += self.simulator.memory[operand]

        elif opcode == 31:  # SUBTRACT
            self.simulator.accumulator -= self.simulator.memory[operand]

        elif opcode == 32:  # DIVIDE
            if self.simulator.memory[operand] != 0:
                self.simulator.accumulator //= self.simulator.memory[operand]
            else:
                return "\nError: Division by zero"

        elif opcode == 33:  # MULTIPLY
            self.simulator.accumulator *= self.simulator.memory[operand]


    def branch_execution(self, opcode, operand):
        if opcode == 40:  # BRANCH
            self.simulator.instruction_counter = operand
            

        elif opcode == 41:  # BRANCHNEG
            if self.simulator.accumulator < 0:
                self.simulator.instruction_counter = operand

        elif opcode == 42:  # BRANCHZERO
            if self.simulator.accumulator == 0:
                self.simulator.instruction_counter = operand

control = ProgramController(simulator)

class MainGridLayout(Widget):
    file = ObjectProperty(None)
    read = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file = ""
        self.read = ""
        self.input_notification = False
        self.primary_color_input = ""
        self.secondary_color_input = ""

    def press_file(self):
        '''this method activates when the run button is clicked'''
        self.file = self.ids.file.text #this grabs the data from the field

        file_input = simulator.load_program_from_file(self.file)
        control.read_control=False
        control.done= True
        simulator.instruction_counter = 0

        if file_input is True:
            #checks fileinput
            result = control.execute_program()
            if control.done is True:
                self.ids.output.text += str(result) + '\n' + str(simulator.memory)
                self.ids.write.text = str(control.output)
                self.ids.file.text = ''

                #populate the editor
                for item in simulator.memory:
                    self.ids.edit.text += f"{str(item)}\n"

            else:
                self.ids.output.text += str(result)
        else:
            self.ids.output.text = "\nFile Not Found"
            self.ids.file.text = ''

    def press_read(self):
        #when Gui submit button is pressed, input is verified and execution continues from where it left off
        
        #Pull data entered from user
        self.read = self.ids.read.text

        #Verify entered data is in correct format.
        input_verification = simulator.verify_input(self.read) 

        #If input is verified
        if input_verification is True:

            #Pass back read value to controller
            control.value = int(self.read)

            #Set read_control to True to give back loop control
            control.read_control = True

            #Resumes execute program
            verified = control.execute_program()

            #If gui is ready to output
            if control.done is True:

                #If controller.output is true
                if control.output:
                    self.ids.output.text += str(control.output)
                self.ids.output.text += str(verified) + '\n' + str(simulator.memory)
                self.ids.write.text = str(control.output)
                self.ids.read.text = ''

            else:
                self.ids.output.text += str(verified)

        #If input is not verified.
        else:
            self.ids.output.text += "\nInput Invalid. Try Again"
            return

    def press_primary_color(self):
        # Get the RGB input from the background color input field
        primary_color_text = self.ids.primary_color_input.text.strip()
        try:
            # Split the RGB input string into individual components
            r, g, b = map(int, primary_color_text.split(','))
            if (r > 255 or g > 255 or b > 255) or (r < 1 or g < 1 or g < 1):
                raise OverflowError
            # Normalize the RGB values to the range of 0-1
            r /= 255
            g /= 255
            b /= 255
            
            #set primary color
            self.ids.background.canvas.before.children[0].rgba = (r, g, b, 1)
            #reset input field
            self.ids.primary_color_input.text = ""

        except ValueError:
            self.ids.output.text += "\nInvalid primary color input. Please enter comma-separated RGB values."

        except OverflowError:
            self.ids.output.text += "\nInvalid primary color input. Please enter a number between 1 and 255"
    def press_secondary_color(self):
        # Get the RGB input from the text color input field
        buttons = ["run_button", "help", "submit_button", "primary_color_button", "secondary_color_button"]
        secondary_color_text = self.ids.secondary_color_input.text.strip()
        try:
            # Split the RGB input string into individual components
            r, g, b = map(int, secondary_color_text.split(','))
            # Normalize the RGB values to the range of 0-1
            r /= 255
            g /= 255
            b /= 255
            # Set the text color
            for button_id in buttons:
                button = self.ids[button_id]
                button.background_color = (r, g, b, 1)
            self.ids.secondary_color_input.text = ""
        except ValueError:
            # Handle invalid input
            self.ids.output.text += "\nInvalid secondary color input. Please enter comma-separated RGB values."

class SimApp(App):
    def build(self):
        return MainGridLayout()

def main():
    SimApp().run()

if __name__=="__main__":
    main()
