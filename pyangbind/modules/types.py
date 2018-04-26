from __future__ import unicode_literals

from decimal import Decimal

import six


class YANGType(object):
  _value = None

  def __init__(self, yang_name, default=None, is_config=True):
    self.yang_name = yang_name
    self.default = default
    self.is_config = is_config

  def contribute_to_class(self, cls, name):
    cls._fields[name] = self

  def check(self, value):
    return True


class YANGBool(YANGType):
  true_values = ["true", "True", True, 1, "1"]
  false_values = ["false", "False", False, 0, "0"]

  def yang_type(self):
    return 'boolean'

  def check(self, value):
    return value in self.true_values or value in self.false_values

  def to_python(self, value):
    if value in self.true_values:
      return True
    elif value in self.false_values:
      return False
    raise ValueError('{} is not a valid value for type {}'.format(value, self.yang_type()))


class YANGString(YANGType):

  def to_python(self, value):
    return six.text_type(value)

  def yang_type(self):
    return 'string'


class YANGInt(YANGType):
  signed = True

  def to_python(self, value):
    if six.PY2 and self.bit_size > 32:
      return long(value)  # NOQA: F821
    return int(value)

  def yang_type(self):
    return ''.join(['u' if not self.signed else '', 'int', str(self.bit_size)])

  def check(self, value):
    try:
      value = self.to_python(value)
    except (ValueError, TypeError):
      return False

    upper_bound = (2 ** (self.bit_size if not self.signed else self.bit_size - 1)) - 1
    lower_bound = (-2 ** (self.bit_size - 1)) if self.signed else 0
    return lower_bound <= value <= upper_bound


class YANGInt8(YANGInt):
  bit_size = 8


class YANGUInt8(YANGInt8):
  signed = False


class YANGInt16(YANGInt):
  bit_size = 16


class YANGUInt16(YANGInt16):
  signed = False


class YANGInt32(YANGInt):
  bit_size = 32


class YANGUInt32(YANGInt32):
  signed = False


class YANGInt64(YANGInt):
  bit_size = 64


class YANGUInt64(YANGInt64):
  signed = False


class YANGDecimal64(YANGType):

  def yang_type(self):
    return 'decimal64'

  def to_python(self, value):
    return Decimal(value)

  def check(self, value):
    try:
      self.to_python(value)
    except (ValueError, TypeError):
      return False
    return True


class YANGUnion(YANGType):
  _current_child = None

  def __init__(self, yang_name, default=None, children=None):
    if not children:
      raise ValueError("child types must be declared for a union")
    self._children = children

  def check(self, value):
    for child in self._children:
      if child.check(value):
        self._current_child = child
        return True
    return False
