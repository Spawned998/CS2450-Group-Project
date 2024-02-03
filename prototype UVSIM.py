class UVSimulator:
    def __init__(self):
        # Initialize UVSim components
        self.memory = [0] * 100
        self.accumulator = 0
        self.instruction_counter = 0

    def load_program(self, program):
        # Load BasicML program into memory starting at location 00
        for i in range(len(program)):
            self.memory[i] = program[i]

    def execute_program(self):
        # Execute BasicML program
        while True:
            instruction = self.memory[self.instruction_counter]
            opcode = instruction // 100
            operand = instruction % 100

            if opcode == 10:  # READ
                value = int(input("Enter a value: "))
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
                print(program)
                break

            self.instruction_counter += 1

# Example program to demonstrate the UVSimulator
program = [+1007, +2010, +3011, +1100, +4300]

# Create UVSimulator instance
uvsim = UVSimulator()

# Load program into UVSimulator memory
uvsim.load_program(program)

# Execute program
uvsim.execute_program()
