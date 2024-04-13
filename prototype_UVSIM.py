from math import e

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.properties import ObjectProperty

class UVSimulator:
    def __init__(self):
        # Initialize UVSim components
        self.memory = [0] * 250
        self.accumulator = 0
        self.instruction_counter = 0
        self.filename = ""

    def save_program_to_file(self):
        #Open file and write out
        try:
            with open(self.filename, 'w') as file:
                for memory in self.memory:

                    #Write each memory value on a new line
                    file.write(f"{str(memory)}\n")

        except IOError as e:
            print("Write error occurred: ", e)

        finally:
            print(f"File {self.filename} closing.")

    def six_digit_conversion(self):
        #Track if any words were changed
        words_updated = False

        #Iterate through each memory location
        for i in range(len(self.memory)):

            #If the length of the word is 4 digits
            if len(str(self.memory[i])) == 4:

                #For testing
                print(f"Converting to six-digit.")

                #Separate opcode & operand
                opcode = str(self.memory[i] // 100)
                operand = str(self.memory[i] % 100)

                #Append a leading 0 to operand
                new_operand = "{:03d}".format(int(operand))

                #For testing
                print(f"New operand: {new_operand}")

                #Write new 6 digit word back to same memory location
                self.memory[i] = int(opcode + new_operand)

                #Flag that words were changed
                words_updated = True
        
        return words_updated
                

    def load_program_from_file(self, passed_filename):
        self.filename = passed_filename

        need_to_write_out_file = False
        # Load BasicML program from a text file into memory starting at location 00
        try:
            with open(self.filename, 'r') as file:
                program = [int(line.strip()) for line in file]
            self.memory[:len(program)] = program

            #Convert any 4-digit file to six digit file
            need_to_write_out_file = self.six_digit_conversion()

            if(need_to_write_out_file == True):
                #Write out to file with new values
                self.save_program_to_file()
            return True
            
        except Exception as e:
            return False

    def verify_input(self, entry):
        #Verify the user enters a 6 digit value- reject all other inputs.
        if len(entry) == 6:
            try:
                int(entry)
            except Exception as e:
                return False
            return True
        return False
        
#simulator = UVSimulator()

class ProgramController:
    def __init__(self, simulator):
        self.simulator = simulator
        self.output = [] #used to write output to GUI
        self.read_control = False #used to stop program to grab read input from gui
        self.value = 0 #used to store read input from gui
        self.done = True #used to stop gui from outputting prematurely


    def execute_program(self, max_iterations = 250):
    # Execute BasicML program
        while (self.simulator.instruction_counter < max_iterations):
            instruction = self.simulator.memory[self.simulator.instruction_counter]
            if instruction == -99999:
                return "\nEnd of file."
                
            elif len(str(instruction)) == 5:
                opcode = instruction // 1000
                operand = instruction % 1000
                    
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
                if self.math_execution(opcode, operand):
                    return self.math_execution(opcode, operand)
                

            elif (opcode == 40 or
                  opcode == 41 or
                  opcode == 42):
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

#control = ProgramController(simulator)

class MainGridLayout(Widget):
    file = ObjectProperty(None)
    read = ObjectProperty(None)

    #ObjectProperty to hold callback reference to SimTabs instance
    sim_tabs = ObjectProperty(None)

    def __init__(self, passed_simulator, passed_control, **kwargs):
        super().__init__(**kwargs)
        self.file = ""
        self.read = ""
        self.input_notification = False
        self.primary_color_input = ""
        self.secondary_color_input = ""

        self.simulator = passed_simulator
        self.control = passed_control

    def press_file(self):
        '''this method activates when the run button is clicked'''
        if not self.file or (self.ids.file.text != self.file):
            self.file = self.ids.file.text #this grabs the data from the field

            file_input = self.simulator.load_program_from_file(self.file)
        else:
            file_input = True

        self.control.read_control=False
        self.control.done= True
        self.simulator.instruction_counter = 0

        if file_input is True:
            #checks fileinput
            result = self.control.execute_program()
            if self.control.done is True:
                for output in self.control.output:
                    self.ids.output.text += "\n" + str(result)
                self.ids.output.text += "\n" + str(result)
                self.ids.write.text = str(self.control.output)

            else:
                self.ids.output.text += str(result)
        else:
            self.ids.output.text = "\nFile Not Found"

    def load_into_editor(self):
        #clear editor field
        self.ids.edit.text = ""
        
        #load file
        if not self.file or (self.ids.file.text != self.file):
            self.file = self.ids.file.text #this grabs the data from the field

            file_input = self.simulator.load_program_from_file(self.file)
        else:
            file_input = True

        if file_input is True:
            #populate the editor
            for item in self.simulator.memory:
                self.ids.edit.text += f"{str(item)} "
        
        else:
            self.ids.output.text = "\nFile Not Found"

    def press_read(self):
        #when Gui submit button is pressed, input is verified and execution continues from where it left off
        
        #Pull data entered from user
        self.read = self.ids.read.text

        #Verify entered data is in correct format.
        input_verification = self.simulator.verify_input(self.read) 

        #If input is verified
        if input_verification is True:

            #Clear any prior messages in output field
            self.ids.output.text = ""

            #Pass back read value to controller
            self.control.value = int(self.read)

            #Set read_control to True to give back loop control
            self.control.read_control = True

            #Resumes execute program
            verified = self.control.execute_program()

            #If gui is ready to output
            if self.control.done is True:

                self.ids.output.text += str(verified)
                self.ids.write.text = str(self.control.output)
                self.ids.read.text = ''

            else:
                self.ids.output.text += str(verified)
                self.ids.write.text = str(self.control.output)
                self.ids.read.text = ''

        #If input is not verified.
        else:
            self.ids.output.text += f"\n{self.read} is Invalid. Please enter a 6 digit number."
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
            if (r > 255 or g > 255 or b > 255) or (r < 1 or g < 1 or g < 1):
                raise OverflowError
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

        except OverflowError:
            self.ids.output.text += "\nInvalid primary color input. Please enter a number between 1 and 255"

    def press_save(self):

        #Pull commands from the editor and store in a list
        int_list = self.ids.edit.text.split(" ")

        #Iterate through list
        for i in range(249):
            try:
                #Check if value is outside valid opcode range
                if (int(int_list[i]) < 10000) or (int(int_list[i]) >= 44000):

                    #If value is -99999, store in memory
                    if int(int_list[i]) == -99999:
                        self.simulator.memory[i] = int(int_list[i])

                    #If value is 0, store in memory
                    elif int(int_list[i]) == 0:
                        self.simulator.memory[i] = int(int_list[i])

                    #Otherwise invalid value
                    else:
                        self.ids.output.text += "\nInvalid value in editor"
                        return False
                
                #If value > 10000 and value < 10000, store in memory
                else:
                    self.simulator.memory[i] = int(int_list[i])
        
            #If any errors are thrown, return false
            except ValueError:
                return False
            
        #No errors thrown: write out to file
        self.simulator.save_program_to_file()

    def press_new_tab(self):

        #Callback to SimTabs instance
        self.sim_tabs.add_tab()
        

class SimTabs(TabbedPanel):
    #List to hold UVSim instances
    num_instances = 0

    def __init__(self, **kwargs):
        super(SimTabs, self).__init__(**kwargs)

        #Create default sim instance
        default_sim = UVSimulator()

        #Create default control instance
        default_control = ProgramController(default_sim)

        #Create view tab instance passing in default_sim, default_control, and Sim_Tabs callback reference
        default_instance = MainGridLayout(default_sim, default_control, sim_tabs = self)

        #Set tab text to display default
        self.default_tab_text = 'Default'
        
        #Increase num_instances
        self.num_instances += 1

        #Display default instance
        self.default_tab_content = default_instance

    
    def add_tab(self):

        #Create new sim instance
        new_sim = UVSimulator()

        #Create new control_instance
        new_control = ProgramController(new_sim)

        #Create new view tab instance
        new_layout = MainGridLayout(new_sim, new_control, sim_tabs = self)

        #increase num_instances
        self.num_instances += 1

        #Display instance number in tab
        new_tab = TabbedPanelItem(text = f"{self.num_instances}")
        
        #Store layout into tab content
        new_tab.content = new_layout

        #Add tab to SimTabs instance
        self.add_widget(new_tab)

class SimApp(App):
    def build(self):
        return SimTabs()

def main():
    SimApp().run()

if __name__=="__main__":
    main()
