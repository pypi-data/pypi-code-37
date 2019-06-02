from blargh.data_model.data_model import DataModel
from blargh.data_model.fields.field import Rel
from blargh.data_model.fields.field import Scalar

dm = DataModel('test_as_code')

# o1 object
o1 = dm.create_object('o1')
o1.add_field(Scalar('id', ext_name='id', writable=True, readonly=True, hidden=False, default=None, pkey=True, type_=int))

# o2 object
o2 = dm.create_object('o2')
o2.add_field(Scalar('id', ext_name='id', writable=True, readonly=True, hidden=False, default=None, pkey=True, type_=str))

# rel fields
def writable(instance):
    return False

o1.add_field(Rel('o2s', ext_name='o2s', writable=writable, readonly=False, hidden=False, default=None, stores=o2, multi=False, cascade=True))
o2.add_field(Rel('o1_id', ext_name='o1_id', writable=True, readonly=False, hidden=False, default=[], stores=o1, multi=True, cascade=False))

# connections
dm.connect(o2, 'o1_id', o1, 'o2s')