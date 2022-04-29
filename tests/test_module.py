
# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.pool import Pool


class PartyEdiTestCase(ModuleTestCase):
    'Test PartyEdi module'
    module = 'party_edi'

    @with_transaction()
    def test_party_identifiers(self):
        'Party Identifiers'
        pool = Pool()
        Configuration = pool.get('party.configuration')
        PartyIdentifier = pool.get('party.identifier')

        _TYPE = ('edi_head', 'EDI Operational Point (Head Office)')
        self.assertTrue(_TYPE in Configuration.identifier_types.selection)
        self.assertTrue(_TYPE in PartyIdentifier.get_types())
        _TYPE = ('edi_pay', 'EDI Operational Point (Who Pays)')
        self.assertTrue(_TYPE in Configuration.identifier_types.selection)
        self.assertTrue(_TYPE in PartyIdentifier.get_types())


del ModuleTestCase
