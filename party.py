# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta, Pool

__all__ = ['Party', 'PartyIdentifier']


class Party(metaclass=PoolMeta):
    __name__ = 'party.party'

    allow_edi = fields.Boolean('Allow EDI', help='Allow EDI communications')
    edi_operational_point = fields.Function(
        fields.Char('EDI Operational Point', size=35),
        'get_edi_operational_point', setter='set_edi_operational_point')

    def get_edi_operational_point(self, name=None):
        for identifier in self.identifiers:
            if identifier.type == 'edi':
                return identifier.code
        return None

    @classmethod
    def set_edi_operational_point(cls, parties, name, value):
        Identifier = Pool().get('party.identifier')
        for party in parties:
            identifier = Identifier.search([
                    ('party', '=', party.id),
                    ('type', '=', 'edi')
                ], limit=1)
            if identifier:
                Identifier.write([identifier[0]], {'code': value})
            else:
                Identifier.create([{
                            'party': party,
                            'type': 'edi',
                            'code': value,
                            }])


class PartyIdentifier(metaclass=PoolMeta):
    __name__ = 'party.identifier'

    @classmethod
    def __setup__(cls):
        super(PartyIdentifier, cls).__setup__()
        cls.type.selection.append(('edi', 'EDI Operational Point'))
