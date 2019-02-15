# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import party
from . import address


def register():
    Pool.register(
        address.Address,
        party.Party,
        party.PartyIdentifier,
        module='party_edi', type_='model')
