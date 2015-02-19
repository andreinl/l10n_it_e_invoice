# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2014 Apulia Software All Rights Reserved.
#                       www.apuliasoftware.it
#                       info@apuliasoftware.it
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import orm, fields
from openerp.tools.translate import _
import logging
_logger = logging.getLogger('E-Invoice - Company')


class res_company(orm.Model):

    _inherit = "res.company"

    _columns = {
        'e_invoice_transmitter': fields.many2one('res.partner', _('eInvoice transmitter'), domain="[('supplier', '=', True)]", help="Il partner che effettuerà la trasmissione verso la PA."),
        'rea': fields.boolean('Società iscritta nel registro delle imprese', help="""Società iscritta nel registro delle imprese"""),
        'rea_ufficio': fields.many2one('res.province', 'Provincia Ufficio REA', required=False),
        'rea_numero': fields.char('Numero REA', size=20, required=False),
        'capitale_sociale': fields.float('Capitale Sociale, €', digits=(12, 2), required=False, help="""Il campo deve contenere l’importo del capitale sociale effettivamente versato come risultante dall’ultimo bilancio; è previsto un valore numerico composto da un intero e da due decimali; i decimali, separati dall’intero con il carattere punto (“.”), vanno sempre indicati anche se pari a zero (es.: 28000000.00)."""),
        'socio_unico': fields.selection((('SU', u'Socio Unico'), ('SM', u'Società Pluripersonale')), 'Socio Unico', required=False),
        'forma_societaria': fields.selection((
            # ('di', u'Ditta Individuale'),
            # ('ss', u'Società Semplice'),
            # ('snc', u'Società in Nome Collettivo'),
            # ('sas', u'Società in Accomandita Semplice'),
            ('spa', u'Società per Azioni'),
            ('sapa', u'Società in accomandita per azioni'),
            ('srl', u'Società a responsabilità limitata'),
            ('altri', u'Altri')
        ), 'Forma societaria', required=False),
        'stato_liquidazione': fields.selection((
                                               ('LS', 'In Liquidazione'),
                                               ('LN', 'Non in Liquidazione')),
                                               'Stato Liquidazione', required=False)
    }

    def get_vat(self, cr, uid, company_id=False, context=None):
        if company_id:
            company = self.browse(cr, uid, company_id, context)
        else:
            company = self.pool.get('res.users').browse(
                cr, uid, uid, context).company_id

        if not company.vat:
            _logger.info('No VAT defined for company %s' % (company.name))
        return company.vat or '!'
