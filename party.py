# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields, ModelSQL, ModelView
from trytond.pool import PoolMeta, Pool

SUPPLIER_TYPE = [
    ('NADSCO', 'Legal Supplier'),
    ('NADBCO', 'Legal Purchaser'),
    ('NADSU', 'Supplier'),
    ('NADBY', 'Purchaser'),
    ('NADII', 'Invoice Issuer'),
    ('NADIV', 'Invoice Receiver'),
    ('NADDP', 'Stock Receiver'),
    ('NADPW', 'NADPW'),
    ('NADPE', 'NADPE'),
    ('NADPR', 'Payment Issuer'),
    ('NADDL', 'Endorser'),
    ('NAD', 'NAD'),
    ('NADMR', 'Message Receiver'),
    ('NADUC', 'Final Receiver'),
    ('NADSH', 'Sender'),
    ('NADMS', 'Message Sender')
    ]


class Configuration(metaclass=PoolMeta):
    __name__ = 'party.configuration'

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.identifier_types.selection += [
            ('edi_head', 'EDI Operational Point (Head Office)')]
        cls.identifier_types.selection += [
            ('edi_pay', 'EDI Operational Point (Who Pays)')]


class Party(metaclass=PoolMeta):
    __name__ = 'party.party'

    allow_edi = fields.Boolean('Allow EDI', help='Allow EDI communications')
    edi_operational_point_head = fields.Function(
        fields.Char('EDI Operational Point (Head Office)', size=35),
        'get_edi_operational_point_head',
        setter='set_edi_operational_point_head')
    edi_operational_point_pay = fields.Function(
        fields.Char('EDI Operational Point (Who Pays)', size=35),
        'get_edi_operational_point_pay',
        setter='set_edi_operational_point_pay')

    def get_edi_operational_point_head(self, name=None):
        for identifier in self.identifiers:
            if identifier.type == 'edi_head':
                return identifier.code
        return None

    @classmethod
    def set_edi_operational_point_head(cls, parties, name, value):
        Identifier = Pool().get('party.identifier')
        for party in parties:
            identifier = Identifier.search([
                    ('party', '=', party.id),
                    ('type', '=', 'edi_head')
                ], limit=1)
            if identifier:
                Identifier.write([identifier[0]], {'code': value})
            else:
                Identifier.create([{
                            'party': party,
                            'type': 'edi_head',
                            'code': value,
                            }])

    def get_edi_operational_point_pay(self, name=None):
        for identifier in self.identifiers:
            if identifier.type == 'edi_pay':
                return identifier.code
        return None

    @classmethod
    def set_edi_operational_point_pay(cls, parties, name, value):
        Identifier = Pool().get('party.identifier')
        for party in parties:
            identifier = Identifier.search([
                    ('party', '=', party.id),
                    ('type', '=', 'edi_pay')
                ], limit=1)
            if identifier:
                Identifier.write([identifier[0]], {'code': value})
            else:
                Identifier.create([{
                            'party': party,
                            'type': 'edi_pay',
                            'code': value,
                            }])


class SupplierEdiMixin(ModelSQL, ModelView):
    type_ = fields.Selection(SUPPLIER_TYPE, 'Type')
    edi_code = fields.Char('Edi Code')
    name = fields.Char('Name')
    commercial_register = fields.Char('Comercial Register')
    street = fields.Char('Street')
    city = fields.Char('City')
    zip = fields.Char('zip')
    vat = fields.Char('Vat')
    country_code = fields.Char('Country_code')
    party = fields.Many2One('party.party', 'Party')
    address = fields.Many2One('party.address', 'Address')
    section = fields.Char('Section')
    cip = fields.Char('CIP', help="Supplier's internal code, "
        "assigned by the buyer")

    def read_NADMR(self, message):
        self.type_ = 'NADMR'
        self.edi_code = message.pop(0) if message else ''

    def read_NADBIV(self, message):
        self.type_ = 'NADBIV'
        self.edi_code = message.pop(0) if message else ''
        if message:
            self.vat = message.pop(0)

    def read_NADPW(self, message):
        self.type_ = 'NADPW'
        self.edi_code = message.pop(0) if message else ''

    def read_NADSH(self, message):
        self.type_ = 'NADSH'
        self.edi_code = message.pop(0) if message else ''

    def read_NADUC(self, message):
        self.type_ = 'NADUC'
        self.edi_code = message.pop(0) if message else ''

    def read_NADPR(self, message):
        self.type_ = 'NADPR'
        self.edi_code = message.pop(0) if message else ''

    def search_party(self):
        pool = Pool()
        PartyId = pool.get('party.identifier')
        PartyAddress = pool.get('party.address')

        domain = []
        if self.edi_code:
            domain += [('type', '=', 'edi_head'), ('code', '=', self.edi_code)]
        if domain == []:
            return
        identifier = PartyId.search(domain, limit=1)
        if identifier:
            self.party = identifier[0].party
        elif hasattr(self, 'vat'):
            domain = [('type', '=', 'vat'), ('code', '=', self.vat)]
            identifier = PartyId.search(domain, limit=1)
            if identifier:
                self.party = identifier[0].party
        domain = [('edi_ean', '=', self.edi_code)]
        addresses = PartyAddress.search(domain, limit=1)
        if addresses:
            self.address = addresses[0]
            if not hasattr(self, 'party'):
                self.party = self.address.party
        return
