import unittest

from tests.modules import test_bindings


class IntTypesTests(unittest.TestCase):

  def setUp(self):
    self.binding = test_bindings.IntBinding()

  def test_set_int_to_lower_bounds(self):
    bounds = {
      'int8': -2**7,
      'int16': -2**15,
      'int32': -2**31,
      'int64': -2**63,
      'uint8': 0,
      'uint16': 0,
      'uint32': 0,
      'uint64': 0
    }
    for size, lower_bound in bounds.items():
      with self.subTest(size=size, lower_bound=lower_bound):
        allowed = True
        try:
          setattr(self.binding, '{}_leaf'.format(size), lower_bound)
        except ValueError:
          allowed = False
        self.assertTrue(allowed)

  def test_set_int_below_lower_bounds(self):
    bounds = {
      'int8': -2**7 - 1,
      'int16': -2**15 - 1,
      'int32': -2**31 - 1,
      'int64': -2**63 - 1,
      'uint8': -1,
      'uint16': -1,
      'uint32': -1,
      'uint64': -1
    }
    for size, lower_bound in bounds.items():
      with self.subTest(size=size, lower_bound=lower_bound), self.assertRaises(ValueError):
        setattr(self.binding, '{}_leaf'.format(size), lower_bound)

  def test_set_int_to_upper_bounds(self):
    bounds = {
      'int8': 2**7 - 1,
      'int16': 2**15 - 1,
      'int32': 2**31 - 1,
      'int64': 2**63 - 1,
      'uint8': 2**8 - 1,
      'uint16': 2**16 - 1,
      'uint32': 2**32 - 1,
      'uint64': 2**64 - 1
    }
    for size, upper_bound in bounds.items():
      with self.subTest(size=size, upper_bound=upper_bound):
        allowed = True
        try:
          setattr(self.binding, '{}_leaf'.format(size), upper_bound)
        except ValueError:
          allowed = False
        self.assertTrue(allowed)

  def test_set_int_above_upper_bounds(self):
    bounds = {
      'int8': 2**7,
      'int16': 2**15,
      'int32': 2**31,
      'int64': 2**63,
      'uint8': 2**8,
      'uint16': 2**16,
      'uint32': 2**32,
      'uint64': 2**64
    }
    for size, upper_bound in bounds.items():
      with self.subTest(size=size, upper_bound=upper_bound), self.assertRaises(ValueError):
        setattr(self.binding, '{}_leaf'.format(size), upper_bound)


if __name__ == "__main__":
  unittest.main()
