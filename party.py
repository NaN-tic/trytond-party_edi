# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval

__all__ = ['Party']


class Party(metaclass=PoolMeta):
    __name__ = 'party.party'

    allow_edi = fields.Boolean('Allow EDI', help='Allow EDI communications')
    edi_operational_point = fields.Char('EDI Operational Point', size=35)
