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

    def verify_input(self):
        #Verify the user enters a digit - reject all other inputs.
        isValid = False
        user_entry = ""
        
        while(isValid == False):
            
            user_entry = (input("Enter a value: "))
            
            try:
                user_entry = int(user_entry)
                
            except Exception as e:
                print("Invalid input. Please enter a numerical value.")
                
            else:
                isValid = True
                
        return user_entry
                

    def execute_program(self, max_iterations = 100):
        # Execute BasicML program
        while (self.instruction_counter < max_iterations):
            instruction = self.memory[self.instruction_counter]
            if instruction == -99999:
                return "End of file."
                

            opcode = instruction // 100
            operand = instruction % 100

            if opcode == 10:  # READ
                value = self.verify_input()
                self.memory[operand] = value

            elif opcode == 11:  # WRITE
                print("Output:", self.memory[operand])

            elif opcode == 20:  # LOAD
                self.accumulator = self.memory[operand]

            elif opcode == 21:  # STORE
                self.memory[operand] = self.accumulator

            elif opcode == 30:  # ADD
                self.accumulator += self.memory[operand]

            elif opcode == 31:  # SUBTRACT
                self.accumulator -= self.memory[operand]

            elif opcode == 32:  # DIVIDE
                if self.memory[operand] != 0:
                    self.accumulator //= self.memory[operand]
                else:
                    return "Error: Division by zero"
                

            elif opcode == 33:  # MULTIPLY
                self.accumulator *= self.memory[operand]

            elif opcode == 40:  # BRANCH
                self.instruction_counter = operand
                continue

            elif opcode == 41:  # BRANCHNEG
                if self.accumulator < 0:
                    self.instruction_counter = operand
                    continue

            elif opcode == 42:  # BRANCHZERO
                if self.accumulator == 0:
                    self.instruction_counter = operand
                    continue

            elif opcode == 43:  # HALT
                return "Program halted."
                
            
            else:
                #Invalid opcode
                return (f"Invalid opcode: {opcode} is not a valid command.\nExiting program.")
                

            self.instruction_counter += 1

sim = UVSimulator()

class MainGridLayout(Widget):
    file= ObjectProperty(None)
    read = ObjectProperty(None)

    def press_file(self):

        file = self.ids.file.text

        file_input = sim.load_program_from_file(file)
        if file_input is True:
            sim.execute_program()

            self.ids.output.text= f'Output: {sim.memory}'
            self.ids.file.text = ''
        else:
            self.ids.output.text = "File Not Found"
            self.ids.file.text = ''

    def press_read(self):
        read = self.read.text

        print(f'read: {read}')

        self.ids.read.text= ""


class SimApp(App):
    def build(self):
        return MainGridLayout()

def main():
    SimApp().run()
    # mysim = UVSimulator()
    # mysim.load_program_from_file("Test2.txt")
    # mysim.execute_program()

if __name__=="__main__":
    main()