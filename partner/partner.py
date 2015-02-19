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


class ResPartner(orm.Model):
    _inherit = "res.partner"

    _columns = {
        'ipa_code': fields.char('IPA Code', size=6, help=_(u"""il campo deve contenere il codice di 6 caratteri, presente su IndicePA tra le informazioni relative al servizio di fatturazione elettronica, associato all’ufficio che, all’interno dell’amministrazione destinataria, svolge la funzione di ricezione (ed eventualmente lavorazione) della fattura.
            In alternativa, è possibile valorizzare il campo con il codice Ufficio “centrale” o con il valore di default “999999”, quando ricorrono le condizioni previste dalle disposizioni della circolare interpretativa del Ministero dell’Economia e delle Finanze n.1 del 31 marzo 2014.""")),
        # Disabled at the moment. One who have a client with such needs will implement it.
        # 'estero_stabile_organizzazione': fields.boolean(_('Soggetto estero con stabile organizzazione in Italia'), help="""E' un soggetto che non risiede in Italia ma che, in Italia, dispone di una stabile organizzazione attraverso la quale svolge la propria attività""")
        'administration_reference': fields.char(_('Riferimento Amministrazione'), size=32, help="""Il campo è stato previsto per immettere in fattura un valore, riferito al cedente/prestatore, che possa in qualche modo agevolare il trattamento automatico della fattura da parte di chi la riceve"""),
        'e_invoice_host': fields.char('Destination host for e-invoice', size=128),
        'e_invoice_port': fields.char('Destination port for e-invoice', size=8),
        'e_invoice_username': fields.char('Username', size=64),
        'e_invoice_password': fields.char('Password', size=64),
        'e_invoice_file_path': fields.char('Destination File path for e-invoice',
                                              size=128,
                                              help='Path to the folder on the destination server where e-invoice should be putted'),
        'e_invoice_protocol': fields.selection((
            ('ftp', 'FTP'),
            ('local', _('Download')),
            # ('sftp', 'Secure FTP)),
        ), _('Transmission protocol'))
    }

    _defaults = {
        'e_invoice_protocol': 'local',
        'e_invoice_port': '21'
    }

    def get_e_invoice_transmission_vals(self, cr, uid, partner_id=False, context=None):
        if partner_id:
            partner = self.browse(cr, uid, partner_id, context)
        else:
            # ----- If there isn't a partner as parameter
            #       extracts it from user
            partner = self.pool['res.users'].browse(cr, uid, uid, context).company_id.e_invoice_transmitter

        if partner.e_invoice_protocol == 'ftp' and not partner.e_invoice_host:
            raise orm.except_orm(
                _('Error'),
                _('Define an FTP host for this partner')
            )

        return {
            'protocol': partner.e_invoice_protocol,
            'host': partner.e_invoice_host or False,
            'port': partner.e_invoice_port or '21',
            'user': partner.e_invoice_username or False,
            'passwd': partner.e_invoice_password or False,
            'destination_dir': partner.e_invoice_file_path or ''
        }
