from pyangbind import modules


class StringBinding(modules.PybindModule):
  string_leaf = modules.YANGString(yang_name="string-leaf")
  default_string_leaf = modules.YANGString(default="foo", yang_name="default-string-leaf")


class IntBinding(modules.PybindModule):
  int8_leaf = modules.YANGInt8(yang_name="int8-leaf")
  int16_leaf = modules.YANGInt16(yang_name="int16-leaf")
  int32_leaf = modules.YANGInt32(yang_name="int32-leaf")
  int64_leaf = modules.YANGInt64(yang_name="int64-leaf")
  uint8_leaf = modules.YANGUInt8(yang_name="uint8-leaf")
  uint16_leaf = modules.YANGUInt16(yang_name="uint16-leaf")
  uint32_leaf = modules.YANGUInt32(yang_name="uint32-leaf")
  uint64_leaf = modules.YANGUInt64(yang_name="uint64-leaf")
