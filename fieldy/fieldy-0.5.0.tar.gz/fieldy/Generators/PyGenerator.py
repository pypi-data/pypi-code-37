from fieldy import get_base_types
import re

class PyGenerator:
  def __init__(self, schema_manager, path):
    self.schema_manager = schema_manager
    self.path = path

  def load_schema(self, schema_name):
    imports_py = ['import json', 'from datetime import datetime']
    dependent_schemas = []
    schema = self.schema_manager.schemas[schema_name]
    for field_name in schema['fields']:
      field = schema['fields'][field_name]
      if field['type'] not in get_base_types():
        imports_py.append('from {path} import {dep}'.format(path=self.path, dep=re.sub(r'\[|\]|\{|\}', '', field['type'])))
    schema_py = '  schema = {schema}'.format(schema=str(schema))
    init_py = [
      '  def __init__(self, dic):',
      '    if type(dic) == str:',
      '      dic = json.loads(dic)',
      '    if type(dic) != dict:',
      '      raise Exception(\'dic should be a dict.\')',
      '    schema_fields = self.schema[\'fields\']',
      '    for key in schema_fields:',
      '      if key not in dic and schema_fields[key][\'required\']:',      
      '        raise Exception(\'missing required field\')',
      '      setattr(self, key, schema_fields[key][\'default\'])',
      '    for key in dic:',
      '      if key not in schema_fields:',
      '        raise Exception(\'field not in schema\')',
      '      field_type = schema_fields[key][\'type\']',
      '      setattr(self, key, self.parse_field(field_type, dic[key]))',
    ]

    parse_field_py = [
      '  def parse_field(self, field_type, field_value):',
      '    if field_type[0] == \'[\' and field_type[-1] == \']\':',
      '      ret = []',
      '      for field in field_value:',
      '        ret.append(self.parse_field(field_type[1:-1], field))',
      '      return ret',
      '    if field_type[0] == \'{\' and field_type[-1] == \'}\':',
      '      ret = {}',
      '      for field in field_value:',
      '        ret[field](self.parse_field(field_type[1:-1], field_value[field]))',
      '      return ret',
      '    if field_type == \'integer\':',
      '      return int(field_value)',
      '    elif field_type == \'string\':',
      '      return str(field_value)',
      '    elif field_type == \'float\':',
      '      return float(field_value)',
      '    elif field_type == \'boolean\':',
      '      return boolean(field_value)',
      '    elif field_type == \'any\':',
      '      return field_value',
      '    elif field_type == \'date\':',
      '      return datetime.strptime(field_value, \'%Y-%m-%d\')',
      '    else:',
      '      return eval(\'{}(field_value)\'.format(field_type))',
    ]
    return '{imports}\n\nclass {class_name}:\n{schema}\n\n{parse_field}\n\n{init}'.format(
      imports = '\n'.join(imports_py),
      class_name = schema_name,
      schema = schema_py,
      parse_field = '\n'.join(parse_field_py),
      init = '\n'.join(init_py),
    )

