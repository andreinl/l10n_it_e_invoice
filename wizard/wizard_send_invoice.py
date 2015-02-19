# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Andre@ (<a.gallina@cgsoftware.it>)
#    All Rights Reserved
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
from tools.translate import _
import logging
import netsvc
import os
from ftplib import FTP
import datetime
from cStringIO import StringIO


import pdb

from openerp.addons.l10n_it_e_invoice.xml_pa import xml_invoice

_logger = logging.getLogger('Sending E-Invoice')


class WizardSendInvoice(orm.TransientModel):

    _name = "wizard.send.invoice"
    _description = "Wizard For Sening E-Invoice"

    _columns = {
        'file_format': fields.selection((
            ('xmlpa', 'XML PA'),
            ('pdf', 'PDF')
        ), 'Invoice format', required=True),
        'data': fields.binary("File", readonly=True),
        'name': fields.char('Filename', 32, readonly=True),
        'state': fields.selection((
            ('choose', 'choose'),   # choose
            ('get', 'get'),         # get the file
        )),
    }

    _defaults = {
        'file_format': 'xmlpa',
        'state': 'choose'
    }

    @staticmethod
    def create_report(cr, uid, res_ids,
                      report_name=False,
                      data=False, context=False):
        if not report_name or not res_ids:
            return (
                False,
                Exception('Report name and Resources ids are required !!!')
            )
        try:
            service = netsvc.LocalService("report." + report_name)
            report, file_format = service.create(cr, uid, res_ids, data, context)
            return True, report
        except Exception, e:
            print 'Exception in create report:', e
            return False, str(e)

    @staticmethod
    def upload_file(ftp_vals, destination, file_name, report):
        file_to_upload = StringIO()
        file_to_upload.write(report)
        file_to_upload.seek(0)
        try:
            ftp = FTP()
            ftp.connect(ftp_vals['host'], int(ftp_vals['port']))
            ftp.login(ftp_vals['user'], ftp_vals['passwd'])
            try:
                ftp.cwd(destination)
                # move to the desired upload directory
                _logger.info('Currently in: %s', ftp.pwd())
                _logger.info('Uploading: %s', file_name)

                ftp.storbinary('STOR ' + file_name, file_to_upload)

                _logger.info('Done!')
            finally:
                _logger.info('Close FTP Connection')
                file_to_upload.close()
                ftp.quit()
        except:
           raise orm.except_orm('Error', 'Error in FTP')
        
        _logger.info('Done!')

    def send_invoice(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        wizards = self.browse(cr, uid, ids, context)

        if len(wizards) == 1:
            output_format = wizards[0].file_format
        else:
            raise orm.except_orm(_('Error'), _("More than one wizard?!"))

        # ---- Select the printing module to print and create PDF
        invoice_ids = context.get('active_ids', [])
        invoice_obj = self.pool['account.invoice']
        invoice = invoice_obj.browse(cr, uid, invoice_ids, context)[0]

        if not invoice.number:
            raise orm.except_orm(
               _('Warning!'),
               _("You can't send an Invoice which is not validated yet."),
            )

        if not invoice.company_id.partner_id.vat:
            raise orm.except_orm(
               _('Warning!'),
               _("Please indicate vat number of the Partner connected to Company"),
            )

        # ---- check if invoice can be send to SDI
        if not invoice.journal_id.e_invoice:
            raise orm.except_orm(
                _('Error'),
                _('Is not E-Invoice check your Journal config!'))
        if invoice.einvoice_state not in ('draft', 'sent'):
            raise orm.except_orm(
                _('Error!'),
                _('invoice has already been processed, \
                   you can not proceed to send!'))

        # ---- Standard for file name is:
        # ---- ITpartita_iva_mittente<...>.pdf
        file_name = invoice.company_id.partner_id.vat
        #~ file_name += '<' + invoice.number.replace('/', '_') + '>'
        file_name += invoice.number.replace('/', '_')

        if output_format == 'pdf':
            report_name = invoice.journal_id.printing_module.report_name or False
            result, report = self.create_report(
                cr, uid, invoice_ids, report_name, False, context)
            einvoice_file = result and report or False
            # ---- Setting the folder where to put pdf file
            folder = 'input flusso PDF'
            extension = 'pdf'
        elif output_format == 'xmlpa':
            folder = 'input flusso XML'
            einvoice_file = self.create_xml(cr, uid, invoice_ids, context)
            extension = 'xml'

        if not einvoice_file:
            raise orm.except_orm(
                _('Error'),
                _('E-invoice is not ready!'))

        transmission_vals = self.pool['res.partner'].get_e_invoice_transmission_vals(cr, uid, False, context)

        if transmission_vals['protocol'] == 'ftp':

            destination = os.path.join(transmission_vals['destination_dir'], folder)
            self.upload_file(transmission_vals, destination, file_name, einvoice_file)
            einvoice_file.close()
            history = invoice.history_ftpa or ''
            history = '%s\n' % (history)
            history = "%sFattura inviata in data %s" % (
                history, str(datetime.datetime.today()))
            invoice_obj.write(
                cr, uid, invoice_ids[0],
                {'history_ftpa': history, 'einvoice_state': 'sent'}, context)
            return {'type': 'ir.actions.act_window_close'}
        elif transmission_vals['protocol'] == 'local':
            out = einvoice_file.encode("base64")
            file_name += '.{extension}'.format(extension=extension)
            return self.write(cr, uid, ids, {'state': 'get', 'data': out, 'name': file_name}, context=context)

    @staticmethod
    def close_window(cr, uid, ids, context=None):
        return {'type': 'ir.actions.act_window_close'}

    def create_xml(self, cr, uid, invoice_ids, context):
        assert len(invoice_ids) == 1, 'We can create one invoice at a time'
        invoice = self.pool['account.invoice'].browse(cr, uid, invoice_ids[0], context)

        if not invoice.company_id.e_invoice_transmitter:
            raise orm.except_orm(
                 _('Warning!'),
                 _("Please select eInvoice Transmitter for your Company")
            )

        invoice_pa = xml_invoice.InvoicePa()

        # [1.1] DatiTrasmissione
        # AL: Vorrei sapere, ma qualcuno seriamente pensa che questo formato verrà utilizzato fuori dall'Italia?
        for address in invoice.company_id.e_invoice_transmitter.address:
            if address.type == 'default':
                break
        else:
            address = invoice.company_id.e_invoice_transmitter.address[0]

        dati_trasmissione = {}

        if address.country_id:
            dati_trasmissione['paese'] = address.country_id.code

            if invoice.company_id.e_invoice_transmitter.fiscalcode:
                if address.country_id.code.upper() == 'IT':
                    dati_trasmissione['fiscalcode'] = invoice.company_id.e_invoice_transmitter.fiscalcode
                else:
                    # May be we can take some other field? At the moment we are just doing the same as for Italy
                    dati_trasmissione['fiscalcode'] = invoice.company_id.e_invoice_transmitter.fiscalcode
            else:
                raise orm.except_orm(_('Error'), _("No fiscalcode defined for partner '{partner}'.".format(partner=invoice.company_id.e_invoice_transmitter.name)))
        else:
            raise orm.except_orm(_('Error'), _("No country defined for partner '{partner}'.".format(partner=invoice.company_id.e_invoice_transmitter.name)))

        # The sequencer is always the same. In theory we should never recreate eInvoice
        # We move everything to the end of the code, so sequencer will grow only if everything is Ok
        # if invoice.e_invoice_seq:
        #     invoice_pa.progressivo_invio.text = invoice.e_invoice_seq
        # else:
        #     invoice_pa.progressivo_invio.text = self.pool['ir.sequence'].get(cr, uid, 'e_invoice_pa')
        #     invoice.write({'e_invoice_seq': invoice_pa.progressivo_invio.text})

        dati_trasmissione['format'] = 'SDI11'

        if invoice.partner_id.ipa_code:
            dati_trasmissione['ipa_code'] = invoice.partner_id.ipa_code
        else:
            raise orm.except_orm(_('Error'), _("No IndicePA for partner '{partner}'.".format(partner=invoice.partner_id.name)))

        if address.phone:
            dati_trasmissione['phone'] = address.phone

        if address.email:
            dati_trasmissione['email'] = address.email

        invoice_pa.set_dati_trasmissione(dati_trasmissione)

        # 1.2 CedentePrestatore
        cedente_prestatore = {}

        for address_prestatore in invoice.company_id.partner_id.address:
            if address.type == 'default':
                break
        else:
            address_prestatore = invoice.company_id.e_invoice_transmitter.address[0]

        if address_prestatore.country_id:
            cedente_prestatore['country'] = address_prestatore.country_id.code

            if invoice.company_id.partner_id.vat:
                if address_prestatore.country_id.code.upper() == 'IT':
                    cedente_prestatore['iva'] = invoice.company_id.partner_id.vat.lstrip('IT')
                else:
                    # May be we can take some other field? At the moment we are just doing the same as for Italy
                    # Can it happened that that "Cedente/prestatore" is not an italian company?
                    # TODO: decide if we need to strip letters from the left
                    cedente_prestatore['iva'] = invoice.company_id.partner_id.vat
            else:
                raise orm.except_orm(_('Error'), _("No VAT defined for partner '{partner}'.".format(partner=invoice.company_id.e_invoice_transmitter.name)))
        else:
            raise orm.except_orm(_('Error'), _("No country defined for partner '{partner}'.".format(partner=invoice.company_id.e_invoice_transmitter.name)))

        if invoice.company_id.partner_id.fiscalcode:
            cedente_prestatore['fiscalcode'] = invoice.company_id.partner_id.fiscalcode

        if invoice.company_id.partner_id.individual:
            cedente_prestatore['nome'] = invoice.company_id.partner_id.fiscalcode_firstname
            cedente_prestatore['cognome'] = invoice.company_id.partner_id.fiscalcode_surname
        else:
            cedente_prestatore['denominazione'] = invoice.company_id.partner_id.name

        # TODO: Connect OpenERP with Official Table "RegimeFiscale"
        # cedente_prestatore['regime_fiscale'] = invoice.company_id.partner_id...

        cedente_prestatore['street'] = address_prestatore.street + ((address_prestatore.street2 and ' ' + address_prestatore.street2) or '')
        cedente_prestatore['zip'] = address_prestatore.zip
        cedente_prestatore['city'] = address_prestatore.city

        if address_prestatore.country_id.code == 'IT':
            cedente_prestatore['province'] = address_prestatore.province.code

        cedente_prestatore['country'] = address_prestatore.country_id.code

        # TODO: Implement the case when "il cedente/prestatore è un soggetto che non risiede in Italia ma che,
        #  in Italia, dispone di una stabile organizzazione"
        # if address_prestatore.estero_stabile_organizzazione:

        if invoice.company_id.rea:
            cedente_prestatore['rea_office'] = invoice.company_id.rea_ufficio.code
            cedente_prestatore['rea_number'] = invoice.company_id.rea_numero
            if invoice.company_id.forma_societaria in ('spa', 'sapa', 'srl'):
                cedente_prestatore['capitale_sociale'] = "{:.2f}".format(invoice.company_id.capitale_sociale)

            if invoice.company_id.forma_societaria == 'srl':
                cedente_prestatore['socio_unico'] = invoice.company_id.socio_unico

            cedente_prestatore['stato_liquidazione'] = invoice.company_id.stato_liquidazione

        if address_prestatore.phone:
            cedente_prestatore['phone']= address_prestatore.phone

        if address_prestatore.fax:
            cedente_prestatore['fax'] = address_prestatore.fax

        if address_prestatore.email:
            cedente_prestatore['email'] = address_prestatore.email

        if invoice.partner_id.administration_reference:
            cedente_prestatore['reference'] = invoice.partner_id.administration_reference

        invoice_pa.set_cedente_prestatore(cedente_prestatore)

        # 1.4 CessionarioCommittente - Destinatario
        destinatario = {}

        address_cessionario = False
        for address in invoice.partner_id.address:
            if address.type == 'invoice':
                address_cessionario = address
                break
            elif address.type == 'default':
                address_cessionario = address
        else:
            if not address_cessionario:
                address_cessionario = invoice.partner_id.address[0]

        if invoice.partner_id.vat and invoice.partner_id.vat.upper() == 'IT':
            destinatario['vat_country'] = address_cessionario.country_id.code.upper()
            destinatario['vat'] = invoice.partner_id.vat.lstrip('IT')
        elif invoice.partner_id.fiscalcode:
            destinatario['fiscalcode'] = invoice.partner_id.fiscalcode
        else:
            raise orm.except_orm(
                _('Warning!'),
                _("Please set VAT e (o) Fiscalcode for partner {name}".format(name=invoice.partner_id.name))
            )

        if invoice.partner_id.individual:
            if invoice.partner_id.fiscalcode_firstname:
                destinatario['fiscalcode_firstname'] = invoice.partner_id.fiscalcode_firstname
            else:
                raise orm.except_orm('Warning', 'Per favore indicare il nome per il codice fiscale')

            if invoice.partner_id.fiscalcode_surname:
                destinatario['fiscalcode_surname'] = invoice.partner_id.fiscalcode_surname
            else:
                raise orm.except_orm('Warning', 'Per favore indicare il cognome per il codice fiscale')
        else:
            destinatario['name'] = invoice.partner_id.name

        if address_cessionario.street:
            destinatario['street'] = address_cessionario.street + ((address_cessionario.street2 and ' ' + address_cessionario.street2) or '')
        else:
            raise orm.except_orm('Warning', "Per favore indicare l'indirizzo corretto per il cliente {cliente}".format(cliente=invoice.partner_id.name))

        destinatario['zip'] = address_cessionario.zip
        destinatario['city'] = address_cessionario.city
        if address_cessionario.country_id.code == 'IT':
            destinatario['province'] = address_cessionario.province.code
        destinatario['country'] = address_cessionario.country_id.code

        invoice_pa.set_destinatario(destinatario)

        # 2 FatturaElettronicaBody
        # 2.1 DatiGenerali
        dati_generali = {}

        # TODO: vedere con S
        # dati_generali['type'] =
        dati_generali['currency'] = invoice.currency_id.name.upper()
        dati_generali['date'] = invoice.date_invoice
        dati_generali['number'] = invoice.number

        # TODO: con S: come capire che cedente soggeto a ritenuta?
        # ritenuta = False
        # if ritenuta:
            # dati_generali['ritenuta_tipo'] =
            # dati_generali['ritenuta_importo'] =
            # dati_generali['ritenuta_aliquota'] =
            # dati_generali['ritenuta_causale_pagamento'] =

        # TODO: ricordare che "ai sensi dell’art. 8 del DPR n.642/1972 nei rapporti con lo Stato,
        # o con enti parificati per legge allo Stato, agli effetti tributari, l’imposta di bollo è
        # a carico del fornitore e pertanto l’importo corrispondente non deve essere incluso nel
        # campo ImponibileImporto (2.2.2.5)."
        if invoice.partner_id.charge_revenue_stamp:
            for invoice_line in invoice.invoice_line:
                if invoice_line.product_id.unique_revenue_stamp_id:
                    dati_generali['bollo'] = 'SI'
                    dati_generali['bollo_importo'] = "{:.2f}".format(invoice_line.price_subtotal)
                    break

        # TODO: gestione Cassa Previdenza
        # gestione_inps = False
        # if gestione_inps:
        #     dati_generali['inps_tipo'] =
        #     dati_generali['inps_aliquota'] =
        #     dati_generali['inps_importo'] =
        #     dati_generali['inps_imponibile'] =
        #     dati_generali['inps_iva'] =
        #     dati_generali['inps_ritenuta'] =
        #     dati_generali['inps_natura'] =

        dati_generali['total'] = "{:.2f}".format(invoice.amount_total)

        # TODO: Aggiungere gestione Art73
        # è stato emesso secondo modalità e termini stabiliti con decreto ministeriale ai sensi
        #  dell’articolo 73 del DPR 633/72; ciò consente al cedente/prestatore
        # l’emissione nello stesso anno di più documenti aventi lo stesso numero
        # art73 = False
        # if art73:
        #     dati_generali['art_73'] = 'SI'


        # TODO: Gestione informazione del Ordine d'acquisto (non è obbligatorio)
        # ordine_acquisto = False
        # if ordine_acquisto:
        #     dati_generali['acquisto_documento'] =
        #     dati_generali['acquisto_data'] =
        #     dati_generali['acquisto_cup'] =
        #     dati_generali['acquisto_cig'] =

        invoice_pa.set_dati_generali(dati_generali)

        if invoice.origin:
            ddts = [origin for origin in invoice.origin.split(':') if origin.strip()[:3] == 'OUT']
            if ddts:
                stock_picking_obj = self.pool['stock.picking']
                ddt_ids = stock_picking_obj.search(cr, uid, [('name', 'in', ddts)])
                if ddt_ids:
                    for ddt in stock_picking_obj.browse(cr, uid, ddt_ids, context):
                        invoice_pa.add_ddt(ddt.ddt_number, ddt.ddt_date)

        # Solo per fattura differita o accompagnatoria
        # TODO: S: tipo fattura, serve se non c'è un vettore(?).
        # Sembra che tutto il blocco non è obbligatorio (per il momento)
        # trasporto = False
        # if trasporto:
        #     invoice_pa.add_trasporto()
        #     invoice_pa.trasporto_causale =
        #     invoice_pa.trasporto_numero_colli =
        #     invoice_pa.trasporto_descrizione =
        #     invoice_pa.trasporto_unita_misura =
        #     invoice_pa.trasporto_peso_lordo =

        # Sembra che tutto il blocco non è obbligatorio (per il momento)
        #invoice_pa.add_fattura_principale()

        # 2.2 DatiBeniServizi
        for number, line in enumerate(invoice.invoice_line, start=1):
            # TODO: Sembra che il codice non è obbligatorio
            codici_articolo = [] # codice_tipo, codice_valore

            invoice_pa.add_line({
                'number': number,
                # TODO: discutere con S
                # 'tipo_cessione':  ,  # Non è obbligatorio
                'codici_articolo': codici_articolo,
                'descrizione': line.name,
                'quantity': '{:.2f}'.format(line.quantity),
                'uom': line.uos_id.name,
                # 'inizio_periodo': ,
                # 'fine_periodo':,
                'unit_price': '{:.2f}'.format(line.price_unit),
                'sconti': [{
                    'tipo': (line.discount > 0 and 'SC') or (line.discount < 0 and 'MG') or False,
                    'percentuale': '{:.2f}'.format(line.discount),
                    'importo': False,
                }],
                'totale': '{:.2f}'.format(line.price_subtotal),
                # TODO: chiedere conferma della correttezza a S
                'iva': '{:.2f}'.format(line.invoice_line_tax_id[0].amount * 100),
                'ritenuta': False,
                # TODO: chiedere a S
                # 'natura':
                # 'altri_dati': {
                #     'tipo':
                #     'testo':
                #     'numero':,
                #     'data'
                # },
            })

        # 2.2.2 DatiRiepilogo
        for tax_line in invoice.tax_line:
            invoice_pa.set_aliquota({
                # TODO: capire da dove si può prilevare i valori di IVA
                # 'aliquota_iva': '{:.2f}'.format(tax_line.
                # 'natura':
                # 'spese':
                # 'arrotondamento':
                'imponibile': '{:.2f}'.format(tax_line.base_amount),
                'imposta': '{:.2f}'.format(tax_line.tax_amount),
                # TODO: chiedere a S:
                #'esigibilita_iva': 'I',
                #'normativo'
            })

        # 2.3 DatiVeicoli - non è obbligatorio

        # 2.4 DatiPagamento
        for pagamento in invoice.maturity_ids:
            # TODO: Capire se la fattura è la fattura dell'anticipo (TP03)
            if len(invoice.maturity_ids) == 1:
                condizioni = 'TP02'
            else:
                condizioni = 'TP01'

            pagamento = {
                'condizioni': condizioni,
                # TODO: inserire le modalità del pagamento nella tabella 'Termini di pagamento'
                # 'modalita':
                'scadenza': pagamento.date_maturity,
                'importo': '{:.2f}'.format(pagamento.debit)
            }

            # TODO: Capire quando serve indicare Istituto Finanziario
            istituto_finanziario = False
            if istituto_finanziario:
                # pagamento.update({
                #     'istituto_finanziario':
                #     'iban':
                #     'abi':
                #     'cab':
                #     'bic':
                # })
                pass

            invoice_pa.set_pagamento(pagamento)

        # Sequenza deve essere aggiornata alla fine!
        if invoice.e_invoice_seq:
            invoice_pa.set_progressivo_invio(invoice.e_invoice_seq)
        else:
            invoice_pa.set_progressivo_invio(self.pool['ir.sequence'].get(cr, uid, 'e_invoice_pa'))
            invoice.write({'e_invoice_seq': invoice_pa.progressivo_invio.text})

        print invoice_pa

        # pdb.set_trace()
        #
        # if invoice_pa.validate():
        #     print('Valid XML')
        # else:
        #     print("XML file doesn't validate")

        # pdb.set_trace()
        return unicode(invoice_pa)
