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

            elif opcode == 30:  # ADD
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

            elif opcode == 40:  # BRANCH
                self.simulator.instruction_counter = operand
                continue

            elif opcode == 41:  # BRANCHNEG
                if self.simulator.accumulator < 0:
                    self.simulator.instruction_counter = operand
                    continue

            elif opcode == 42:  # BRANCHZERO
                if self.simulator.accumulator == 0:
                    self.simulator.instruction_counter = operand
                    continue

            elif opcode == 43:  # HALT
                return "\nProgram halted."
                
            
            else:
                #Invalid opcode
                return (f"\nInvalid opcode: {opcode} is not a valid command.\nExiting program.")
                
            self.simulator.instruction_counter += 1



control = ProgramController(simulator)

class MainGridLayout(Widget):
    file = ObjectProperty(None)
    read = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file = ""
        self.read = ""
        self.input_notification = False

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
                self.ids.accumulator.text = str(simulator.accumulator)
                self.ids.write.text = str(control.output)
                self.ids.file.text = ''

            else:
                self.ids.output.text += str(result)
        else:
            self.ids.output.text = "\nFile Not Found"
            self.ids.file.text = ''

    def press_read(self):
        #when Gui submit button is pressed, input is verified and execution continues from where it left off
        self.read = self.ids.read.text
        input_verification = simulator.verify_input(self.read) 
        if input_verification is True:
            control.value = int(self.read)
            control.read_control = True
            verified = control.execute_program()
            if control.done is True:
                if control.output:
                    self.ids.output.text += str(control.output)
                    print("accessed control.output")
                self.ids.output.text += str(verified) + '\n' + str(simulator.memory)
                self.ids.accumulator.text = str(simulator.accumulator)
                self.ids.write.text = str(control.output)
                self.ids.file.text = ''

            else:
                self.ids.output.text += str(verified)
            #right now, I'm having trouble making it continue where it left off
        else:
            self.ids.output.text += "\nInput Invalid. Try Again"
            return

        

class SimApp(App):
    def build(self):
        return MainGridLayout()

def main():
    SimApp().run()

if __name__=="__main__":
    main()
