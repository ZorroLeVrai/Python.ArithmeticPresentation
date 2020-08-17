import re
from enum import Enum

operation_pattern = "\s*[-+]\s*"

def arithmetic_arranger(problems, is_displayed=False):
  error_checker = ErrorChecker(problems)
  error = error_checker.check_errors()
  if (len(error)>0):
    return error

  operation_list = list()
  for problem in problems:
    operation = ArithmeticOperation(problem)
    operation_list.append(operation.to_tupple())

  arranged_operations = arrange_operations(operation_list, is_displayed)
  return arranged_operations

def arrange_operations(operation_list, is_displayed):
  lines = [ "", "", "", ""]
  for operation_item in operation_list:
    for index in range(4):
      if lines[index] != "":
        lines[index] += " "*4
      lines[index] += operation_item[index]

  if is_displayed:
    return "\n".join(lines)
  else:
    return "\n".join(lines[:3])

class ArithmeticOperation:
  def __init__(self, problem):
    if problem.find('+') >= 0:
      self.operand = Operator.PLUS
    else:
      self.operand = Operator.MINUS

    self.numbers = re.split(operation_pattern, problem)

  def to_tupple(self):
    nb_ldigits = len(self.numbers[0])
    nb_rdigits = len(self.numbers[1])
    max_digits = max([nb_ldigits, nb_rdigits])
    number_left_str = ArithmeticOperation.get_number_str(self.numbers[0], nb_ldigits, max_digits)
    number_right_str = ArithmeticOperation.get_number_str(self.numbers[1], nb_rdigits, max_digits)
    operand_str = '+' if Operator.PLUS == self.operand else '-'
    left_num = int(self.numbers[0])
    right_num = int(self.numbers[1])
    if Operator.PLUS == self.operand:
      operand_str = '+'
      op_result = str(left_num + right_num)
    else:
      operand_str = '-'
      op_result = str(left_num - right_num)
    result_str = ArithmeticOperation.get_number_str(op_result, len(op_result), max_digits)
    return (' ' + number_left_str, operand_str + number_right_str, '-'*(2+max_digits), ' ' + result_str)


  def get_number_str(num_str, nb_digits, max_digits):
    return "{0}{1}".format(' '*(max_digits - nb_digits + 1), num_str)


class Operator(Enum):
  PLUS = 1
  MINUS = 2

class ErrorChecker:
  operator_pattern = re.compile(".+[+-].+")
  digit_pattern = re.compile("^[0-9]+$")

  def __init__(self, problems):
    self.problems = problems

  def check_errors(self):
    if len(self.problems) > 5:
      return "Error: Too many problems."

    for problem in self.problems:
      error = self.check_single_problem(problem)
      if (len(error)>0):
        return error
      
      return ""

  def check_single_problem(self, problem):
    if not (re.match(self.operator_pattern, problem)):
      return "Error: Operator must be '+' or '-'."

    numbers = re.split(operation_pattern, problem)
    for number in numbers:

      if not (re.match(self.digit_pattern, number)):
        return "Error: Numbers must only contain digits."
      if len(number)>4:
        return "Error: Numbers cannot be more than four digits."
    
    return ""