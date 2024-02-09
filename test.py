import unittest
from unittest.mock import patch
from io import StringIO
import sys
import os

from prototype_UVSIM import UVSimulator

class TestUVSimulator(unittest.TestCase):
  def setUp(self):
    self.uvsim = UVSimulator()

  def test_load_program_from_file(self):
    filename = "Test1.txt"
    program_content = "1010\n2009\n4300"
    with open(filename, "w") as file:
      file.write(program_content)
    self.uvsim.load_program_from_file(filename)
    self.assertEqual(self.uvsim.memory[:3], [10, 9, 43])
    os.remove(filename)

  @patch('builtins.input', side_effect=[5])
  def test_execute_program_write(self, mock_input):
    self.uvsim.memory[0] = 1005 
    self.uvsim.execute_program()
    self.assertEqual(self.uvsim.memory[5], 5)

  @patch('sys.stdout', new_callable=StringIO)
  def test_execute_program_write(self, mock_stdout):
    self.uvsim.memory[0] = 1105
    self.uvsim.memory[5] = 10
    self.uvsim.execute_program()
    self.assertEqual(mock_stdout.getvalue().strip(), "Output: 10")

  def test_execute_program_branch(self):
    self.uvsim.memory[0] = 4005
    self.uvsim.execute_program()
    self.assertEqual(self.uvsim.instruction_count, 5)

  def test_execute_program_halt(self):
    self.uvsim.memory[0] = 4300
    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
      self.uvsim.execute_program()
      self.assertEqual(mock_stdout.getvalue().strip(), "Program halted.")

if __name__ == '__main__':
  unittest.main()
