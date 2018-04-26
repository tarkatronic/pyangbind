from __future__ import unicode_literals

import inspect

import six


class PybindBase(type):
  """This borrows heavily from django.db.models.ModelBase."""

  def __new__(cls, name, bases, namespace, **kwargs):
    new_namespace = {'__module__': namespace.pop('__module__', None)}
    classcell = namespace.pop('__classcell__', None)
    if classcell is not None:
      new_namespace['__classcell__'] = classcell
    new_class = super(PybindBase, cls).__new__(cls, name, bases, new_namespace, **kwargs)

    new_class.add_to_class('_fields', {})

    # Add all attributes to the class.
    for obj_name, obj in namespace.items():
        new_class.add_to_class(obj_name, obj)

    return new_class

  def add_to_class(cls, name, value):
    if not inspect.isclass(value) and hasattr(value, 'contribute_to_class'):
      value.contribute_to_class(cls, name)
    else:
      setattr(cls, name, value)


class PybindModule(six.with_metaclass(PybindBase, object)):

  def __init__(self):
    for name, field in self._fields.items():
      setattr(self, name, field.default)

  def __setattr__(self, name, value):
    if name in self._fields and value is not None:
      if not self._fields[name].check(value):
        raise ValueError('{} is not a valid value for type {}'.format(value, self._fields[name].yang_type()))
    self.__dict__[name] = value
