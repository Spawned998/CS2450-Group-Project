from math import e


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
            print('No file found.')
            return False

    def user_interface(self):
        #gives the user interface
        print('Welcome to UVSIM!')
        while True:
            file = input('\nEnter your BasicML filename(type exit to close): ')
            if file.lower() == "exit":
                break
            else:
                load_successful = self.load_program_from_file(file)
            
            if (load_successful):
                self.execute_program()
                return
                #remove before turning in, this is for testing
                #print(self.memory)

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
                    print("Error: Division by zero")
                    break

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
                print("Program halted.")
                break
            
            else:
                #Invalid opcode
                print(f"Invalid opcode: {opcode} is not a valid command.")
                print("Exiting program.")
                break

            self.instruction_counter += 1

def main():
    uvsim = UVSimulator()
    uvsim.user_interface()

if __name__=="__main__":
    main()