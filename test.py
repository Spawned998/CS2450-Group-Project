import unittest
from unittest.mock import patch
from io import StringIO
import sys
import os

from prototype_UVSIM import UVSimulator, ProgramController, MainGridLayout, SimApp

class TestUVSimulator(unittest.TestCase):
  def setUp(self):
    self.uvsim = UVSimulator()

  def test_load_program_from_file(self):
    filename = "Test_Load.txt"
    program_content = "1010\n2009\n4300"
    with open(filename, "w") as file:
      file.write(program_content)
    self.uvsim.load_program_from_file(filename)
    self.assertEqual(self.uvsim.memory[:3], [1010, 2009, 4300])
    os.remove(filename)
  
  def test_load_program_from_file_invalid_file(self):
    filename = "InvalidFile.txt"
    output = StringIO()
    sys.stdout = output
    self.uvsim.load_program_from_file(filename)
    printed_false = output.getvalue().strip()
    sys.stdout = sys.__stdout__
    expected_false = 'No file found.'
    self.assertEqual(printed_false, expected_false)
    
  @patch('builtins.input', side_effect=["Test1.txt"])
  @patch('builtins.print')
  def test_user_interface_prints_welcome(self, mock_print, mock_input):
    with patch('builtins.input', side_effect=["exit"]):
      self.uvsim.user_interface()
    mock_print.assert_called_with('Welcome to UVSIM!')
    
  @patch('builtins.input', side_effect=["exit"])
  def test_user_interface_breaks_on_exit(self, mock_input):
    self.uvsim.user_interface()
    self.assertRaises(SystemExit)
    
  @patch('builtins.input', side_effect=["test1.txt", "exit"])
  def test_user_interface_loads_and_executes_program(self, mock_input):
    with patch.object(UVSimulator, 'load_program_from_file') as mock_load_program:
      with patch.object(UVSimulator, 'execute_program') as mock_execute_program:
        self.uvsim.user_interface()
        mock_load_program.assert_called_with("test1.txt")
        mock_execute_program.assert_called_once()

  @patch('builtins.input', side_effect=[5])
  def test_execute_program_read(self, mock_input):
    self.uvsim.memory[0] = 1005 
    self.uvsim.execute_program(1)
    self.assertEqual(self.uvsim.memory[5], 5)

  @patch('sys.stdout', new_callable=StringIO)
  def test_execute_program_write(self, mock_stdout):
    self.uvsim.memory[0] = 1105
    self.uvsim.memory[5] = 10
    self.uvsim.execute_program(1)
    self.assertEqual(mock_stdout.getvalue().strip(), "Output: 10")

  def test_execute_program_halt(self):
    self.uvsim.memory[0] = 4300
    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
      self.uvsim.execute_program()
      self.assertEqual(mock_stdout.getvalue().strip(), "Program halted.")
  
  @patch('builtins.input', side_effect=['10'])
  def test_verify_input_valid_input(self, mock_input):
    with patch('sys.stdout', new=StringIO()) as mock_stdout:
      result = self.uvsim.verify_input()
      self.assertEqual(result, 10)

  @patch('builtins.input', side_effect=['abc', '5'])
  def test_verify_input_then_invalid_input(self, mock_input):
    with patch('sys.stdout', new=StringIO()) as mock_stdout:
      result = self.uvsim.verify_input()
      self.assertEqual(result, 5)

  @patch('builtins.input', side_effect=['', '8'])
  def test_verify_input_empty_then_valid_input(self, mock_input):
    with patch('sys.stdout', new=StringIO()) as mock_stdout:
      result = self.uvsim.verify_input()
      self.assertEqual(result, 8)


  def test_opcode_20(self):
    self.uvsim.memory[0] = 2024
    self.uvsim.memory[24] = 27
    self.uvsim.execute_program()
    self.assertEqual(self.uvsim.accumulator, 27)

  def test_opcode_21(self):
    self.uvsim.memory[0] = 2112
    self.uvsim.accumulator = 30
    self.uvsim.execute_program()
    self.assertEqual(self.uvsim.memory[12], 30)

  def test_opcode_30(self):
    self.uvsim.memory[0] = 3030
    self.uvsim.memory[30] = 14
    expected_add = self.uvsim.accumulator + self.uvsim.memory[30]
    self.uvsim.execute_program()
    self.assertEqual(self.uvsim.accumulator, expected_add)

  def test_opcode_31(self):
    self.uvsim.memory[0] = 3132
    self.uvsim.memory[32] = 57
    expected_sub = self.uvsim.accumulator - self.uvsim.memory[32]
    self.uvsim.execute_program()
    self.assertEqual(self.uvsim.accumulator, expected_sub)

  def test_opcode_32(self):
    self.uvsim.memory[0] = 3210
    self.uvsim.memory[10] = 4
    expected_div = self.uvsim.accumulator // self.uvsim.memory[10]
    self.uvsim.execute_program()
    self.assertEqual(self.uvsim.accumulator, expected_div)
  
  def test_opcode_32_divide_by_zero(self):
    self.uvsim.memory[0] = 3223
    self.uvsim.memory[23] = 0
    output = StringIO()
    sys.stdout = output
    self.uvsim.execute_program()
    zero_error = output.getvalue().strip()
    sys.stdout = sys.__stdout__
    expected_zero = "Error: Division by zero"
    self.assertEqual(zero_error, expected_zero)

  def test_opcode_33(self):
    self.uvsim.memory[0] = 3333
    self.uvsim.memory[33] = 33
    expected_mult = self.uvsim.accumulator * self.uvsim.memory[33]
    self.uvsim.execute_program()
    self.assertEqual(self.uvsim.accumulator, expected_mult)

  def test_opcode_40(self):
    self.uvsim.memory[0] = 4005
    operand = 5
    self.uvsim.execute_program(operand)
    self.assertEqual(self.uvsim.instruction_counter, operand)
  
  def test_opcode_41(self):
    self.uvsim.memory[0] = 4175
    self.uvsim.accumulator = -1
    operand = 75
    self.uvsim.execute_program(operand)
    self.assertEqual(self.uvsim.instruction_counter, operand)

  def test_opcode_42(self):
    self.uvsim.memory[0] = 4202
    self.uvsim.accumulator = 0
    operand = 2
    self.uvsim.execute_program(operand) 
    self.assertEqual(self.uvsim.instruction_counter, operand)

class TestMainGridLayout(unittest.TestCase):
    def setUp(self):
        self.main_layout = MainGridLayout()

    def test_press_file_loads_program(self):
        # Mock the file input
        self.main_layout.ids.file.text = "test_program.txt"
        
        # Mock the execution of program
        with patch.object(SimApp, 'build') as mock_build:
            self.main_layout.press_file()
            mock_build.assert_called_once()

    def test_press_read_with_valid_input(self):
        # Mock the read input
        self.main_layout.ids.read.text = "1234"
        
        # Mock the execution of program
        with patch.object(SimApp, 'build') as mock_build:
            self.main_layout.press_read()
            mock_build.assert_called_once()

    def test_press_read_with_invalid_input(self):
        # Mock the invalid read input
        self.main_layout.ids.read.text = "abcd"
        
        # Mock the output
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.main_layout.press_read()
            self.assertIn("Input Invalid. Try Again", mock_stdout.getvalue())

    def test_press_primary_color_with_valid_input(self):
        # Mock the primary color input
        self.main_layout.ids.primary_color_input.text = "255, 0, 0"
        
        # Mock the primary color setting
        with patch.object(self.main_layout.ids.background.canvas.before.children[0], 'rgba') as mock_rgba:
            self.main_layout.press_primary_color()
            mock_rgba.assert_called_once_with((1.0, 0.0, 0.0, 1))

    def test_press_secondary_color_with_valid_input(self):
        # Mock the secondary color input
        self.main_layout.ids.secondary_color_input.text = "0, 255, 0"
        
        # Mock the secondary color setting for each button
        buttons = ["run_button", "help", "submit_button", "primary_color_button", "secondary_color_button"]
        with patch.object(self.main_layout.ids, 'background_color') as mock_background_color:
            for button_id in buttons:
                self.main_layout.press_secondary_color()
                mock_background_color.assert_called_with((0.0, 1.0, 0.0, 1))

class TestUVSimulatorWordLength(unittest.TestCase):
    def setUp(self):
        self.uvsim = UVSimulator()

    def test_load_program_from_file_with_six_digit_words(self):
        # Create a test file with six-digit words
        filename = "Test_Load_Six_Digit_Words.txt"
        program_content = "001010\n002009\n004300"
        with open(filename, "w") as file:
            file.write(program_content)
        
        # Load the program from the test file
        self.uvsim.load_program_from_file(filename)
        
        # Check if the memory is loaded correctly
        expected_memory = [1010, 2009, 4300] + [0] * 247  # Expected memory with 6-digit words
        self.assertEqual(self.uvsim.memory, expected_memory)
        
        # Clean up
        os.remove(filename)

    def test_load_program_from_file_old_format(self):
        # Create a test file with four-digit words
        filename = "Test_Load_Four_Digit_Words.txt"
        program_content = "1010\n2009\n4300"
        with open(filename, "w") as file:
            file.write(program_content)
        
        # Load the program from the test file
        self.uvsim.load_program_from_file(filename)
        
        # Check if the memory is loaded correctly
        expected_memory = [1010, 2009, 4300] + [0] * 247  # Expected memory with 6-digit words
        self.assertEqual(self.uvsim.memory, expected_memory)
        
        # Clean up
        os.remove(filename)

    def test_execute_program_with_six_digit_math_operations(self):
        # Load a program with six-digit math operations
        self.uvsim.memory[0] = 301010  # ADD operation with a six-digit operand
        self.uvsim.memory[10] = 500000  # Operand with six digits
        self.uvsim.execute_program()
        
        # Check if the ADD operation is executed correctly
        self.assertEqual(self.uvsim.accumulator, 501010)
    
if __name__ == '__main__':
  unittest.main()
