# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['Address']


class Address(metaclass=PoolMeta):
    __name__ = 'party.address'

    edi_ean = fields.Char('EDI EAN code', size=35)
