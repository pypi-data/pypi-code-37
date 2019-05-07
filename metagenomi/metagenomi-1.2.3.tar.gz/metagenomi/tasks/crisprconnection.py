from metagenomi.tasks.taskbase import MgTask
from metagenomi.helpers import to_int


class CrisprConnection(MgTask):
    def __init__(self, mgid, **data):
        if not len(data):
            raise ValueError('Cannot initialize a mapping with no data')

        MgTask.__init__(self, mgid, **data)

        self.total_hits = to_int(self.d.get('total_hits'))
        self.total_spacers_w_targets = to_int(self.d.get('total_spacers_w_targets'))
        self.total_target_contigs = to_int(self.d.get('total_target_contigs'))

        self.protospacer_hits = self.d.get('protospacer_hits', 'None')
        self.database_contigs = self.d.get('database_contigs', 'None')

        self.schema = {**self.schema, **{
            'total_hits': {'required': True, 'type': 'integer'},
            'total_spacers_w_targets': {'required': True, 'type': 'integer'},
            'total_target_contigs': {'required': True, 'type': 'integer'},
            'protospacer_hits': {'required': True, 'type': 's3file'},
            'database_contigs': {'required': True, 'type': 's3file'}
            }
        }

        if self.check:
            self.validate()

    def write(self):
        '''
        Create new Mapping entry
        '''
        self._update(self.whoami(), self.to_dict(validate=True, clean=True))
