# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2014 Andrea Cometa All Rights Reserved.
#                       www.andreacometa.it
#                       openerp@andreacometa.it
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
from ftplib import FTP
import logging
import base64
import pooler
from datetime import datetime
from xml.dom.minidom import parse
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from cStringIO import StringIO

_logger = logging.getLogger('Sending E-Invoice')


class CheckXml(object):

    def __init__(self, cr, uid, context):
        self.pool = pooler.get_pool(cr.dbname)
        self.company_vat = self.pool['res.company'].get_vat(cr, uid, False, context)
        ftp_vals = self.pool['res.partner'].get_e_invoice_transmission_vals(cr, uid, False, context)

        self.ftp = FTP()
        self.ftp.connect(ftp_vals['host'], int(ftp_vals['port']))
        self.ftp.login(ftp_vals['user'], ftp_vals['passwd'])
        self.destination = ftp_vals['destination_dir']

    @staticmethod
    def convert_timestamp(value):
        return datetime.fromtimestamp(
            int(value)/1e3).strftime(DEFAULT_SERVER_DATETIME_FORMAT)

    def read_xml_file(self, cr, uid, file_obj, invoice_id, context=None):
        parser = parse(file_obj)
        file_obj.seek(0)
        file_data = file_obj.read()
        vals = {
            'name': invoice_id,
            'xml_content': file_data
        }
        for tags in parser.getElementsByTagName("esito"):
            for node in tags.getElementsByTagName("timestamp"):
                for value in node.childNodes:
                    date = self.convert_timestamp(value.data)
                    vals.update({
                        'date': date})
            for node in tags.getElementsByTagName("stato"):
                for value in node.childNodes:
                    vals.update({
                        'status_code': value.data})
            for node in tags.getElementsByTagName("msgErrore"):
                for value in node.childNodes:
                    vals.update({
                        'status_desc': value.data})
            for node in tags.getElementsByTagName("nomeFileSdi"):
                for value in node.childNodes:
                    note = "Nome file firmato: " + value.data
                    vals.update({
                        'note': note})
                    self.pool['account.invoice'].write(
                        cr, uid, [invoice_id],
                        {'sdi_file_name': value.data}, context)
            for node in tags.getElementsByTagName("codStato"):
                for value in node.childNodes:
                    note = "Codice di Errore SDI: " + value.data
                    vals.update({'note': note})
        return vals

    def get_file_list(self, folder):
        # ----- Open the remote folder and read all the files
        # TODO: Handle unsafe situation
        self.ftp.cwd('%s%s' % (self.destination, folder))
        file_list = []
        filenames = []
        self.ftp.retrlines('LIST', file_list.append)
        for filename in file_list:
            filename = filename.split(None, 8)[-1]
            if not filename:
                _logger.info('No file found')
                continue
            if not filename.startswith(self.company_vat):
                continue

            filenames.append(filename)
        return filenames

    def check_output_xml_pa(self, cr, uid, context=None):
        account_invoice_obj = self.pool['account.invoice']

        for filename in self.get_file_list('output XML-PA'):
            # ----- Extracts invoice number from file name
            invoice_number = filename[13:].replace('_', '/')

            # ----- Search the invoice
            invoice_ids = account_invoice_obj.search(
                cr, uid, [('number', '=', invoice_number)])

            if not invoice_ids:
                _logger.info('No invoice found for number {0}'.format(invoice_number))

            # ----- Create an attachment
            invoice = account_invoice_obj.browse(cr, uid, invoice_ids[0], context)
            if invoice.einvoice_state == 'at':
                _logger.info('invoice already processed {0}'.format(invoice.number))
                continue

            lf = StringIO()
            self.ftp.retrbinary("RETR " + filename, lf.write, 8 * 1024)

            lf.seek(0)
            attachment_data = {
                'name': filename,
                'type': 'binary',
                'datas_fname': filename,
                'datas': base64.encodestring(lf.read()),  # open(local_filename, "rb").read()),
                'res_name': filename,
                'res_model': 'account.invoice',
                'res_id': invoice_ids[0],
            }
            lf.close()
            self.pool['ir.attachment'].create(cr, uid, attachment_data,
                                 context=context)

            vals = {'einvoice_state': 'at',
                    'history_ftpa': '%s\nScaricata ed allegata versione \
firmata digitalmente della fattura XML PA in data \
%s' % (invoice.history_ftpa, str(datetime.today()))}
            account_invoice_obj.write(cr, uid, [invoice_ids[0]], vals, context)
        return False

    def check_edi_state_file(self, cr, uid, context=None):
        account_invoice_obj = self.pool['account.invoice']

        for filename in self.get_file_list('output notifiche SdI'):
            # TODO: check what filename we get here and assign it to variables,
            #       not to list
            filename_value = filename.split('_')

            # ----- Search the invoice
            invoice_ids = account_invoice_obj.search(
                cr, uid, [('sdi_file_name', '=', filename_value[1])])

            if not invoice_ids:
                _logger.info('No invoice found for number %s' % (
                    filename_value[1]))

            # ----- Extract datas from XML file
            lf = StringIO()
            self.ftp.retrbinary("RETR " + filename, lf.write, 8 * 1024)
            lf.seek(0)
            vals = self.read_xml_file(
                cr, uid, lf, invoice_ids[0], context)
            lf.close()
            # ----- Move file in backup folder
            # TODO: handle unsafe situation
            self.ftp.rename(
                filename, self.destination + '/elaborati/' + filename)
            # ----- Write historic change
            self.pool['einvoice.history'].create(cr, uid, vals, context)
        return True

    def check_xml_state_file(self, cr, uid, context=None):
        account_invoice_obj = self.pool['account.invoice']

        for filename in self.get_file_list('Stati delle fatture'):
            # ----- Extracts invoice number from file name
            invoice_number = filename[13:22].replace('_', '/')

            # ----- Search the invoice
            invoice_ids = account_invoice_obj.search(
                cr, uid, [('number', '=', invoice_number)])

            if not invoice_ids:
                _logger.info('No invoice found for number %s' % (
                    invoice_number))
            # ----- Extract datas from XML file

            lf = StringIO()
            self.ftp.retrbinary("RETR " + filename, lf.write, 8*1024)
            # lf.close()
            lf.seek(0)
            vals = self.read_xml_file(
                cr, uid, lf, invoice_ids[0], context)
            lf.close()
            # ----- Move file in backup folder
            # TODO: handle unsafe situation
            self.ftp.rename(
                filename, self.destination + '/elaborati/' + filename)
            # ----- Write historic change
            self.pool['einvoice.history'].create(cr, uid, vals, context)
        return True

    def quit(self):
        _logger.info('Close FTP Connection')
        self.ftp.quit()


class account_invoice(orm.Model):
    _inherit = "account.invoice"

    _columns = {
        'nr_bollo': fields.char('Numero Bollo', size=10),
        'codice_commessa': fields.char('Codice Commessa', size=64),
        # Commented, because it is not eInvoice related.
        # 'codice_cup': fields.char('Codice CUP', size=64),
        # 'codice_cig': fields.char('Codice CIG', size=64),
        'history_ftpa': fields.text('Storico Trasmissione'),
        'sdi_file_name': fields.char('Sdi File Name', size=128),
        'einvoice_state': fields.selection(
            (('draft', 'Draft'),
             ('sent', 'Sent to Trasmitter'),
             ('at', 'Avvenuta Trasmissione'),
             ('dt', 'Notifica Decorrenza Termini'),
             ('ec', 'Notifica Esito Cessionario Committente'),
             ('mc', 'Notifica Mancanza Consegna'),
             ('ne', 'Notifica Esito Cedente Prestatore'),
             ('ns', 'Notifica di Scarto'),
             ('rc', 'Ricevuta di Consegna'),
             ('se', 'Notifica di Scarto Esito Cessionario Commitente'),
        ), 'E-Invoice State'),
        'history_change': fields.one2many(
            'einvoice.history', 'name', 'Historic Change'),
        'e_invoice_seq': fields.char('Progressivo invio', size=16, readonly=True)
    }

    _defaults = {
        'einvoice_state': 'draft',
    }

    def create(self, cr, uid, vals, context=None):
        if vals:
            journal_id = vals.get('journal_id', False)
            partner_id = vals.get('partner_id', False)

            if journal_id and partner_id and self.pool['account.journal'].browse(cr, uid, journal_id, context).e_invoice:
                partner = self.pool['res.partner'].browse(cr, uid, partner_id, context)
                if not partner.ipa_code:
                    raise orm.except_orm(
                        _('Error'),
                        _('Electronic Invoice but IPA code not found in partner'))
        return super(account_invoice, self).create(cr, uid, vals, context)

    def force_check_einvoice_status(self, cr, uid, ids, context=None):
        return self.check_einvoice_status(cr, uid, ids, context)

    @staticmethod
    def check_einvoice_status(cr, uid, ids, context=None):
        check = CheckXml(cr, uid, context)
        try:
            # ----- Loop all the folders on ftp server and check files
            # check.check_output_xml_pa(cr, uid, context)
            # check.check_edi_state_file(cr, uid, context)
            # check.check_xml_state_file(cr, uid, context)
            pass
        except:
            raise orm.except_orm('Error', 'Error to FTP')
        finally:
            check.quit()
        return {}


class account_journal(orm.Model):
    _inherit = "account.journal"

    _columns = {
        'e_invoice': fields.boolean(
            'Electronic Invoice',
            help="Check this box to determine that each entry of this journal\
 will be managed with Italian protocol for Electronical Invoice. Please use\
 the sequence like PA/xxxxxx"),
        'printing_module': fields.many2one(
            'ir.actions.report.xml', 'Printing Module',
            help="Printing module for e-invoice"),
    }

    _defaults = {
        'e_invoice': False,
    }


class einvoice_history(orm.Model):

    _name = "einvoice.history"

    _columns = {
        'name': fields.many2one(
            'account.invoice', 'Invoice', required=True, ondelete='cascade'),
        'date': fields.datetime('Date Action', required=True),
        'note': fields.text('Note'),
        'status_code': fields.char('Status Code', size=25),
        'status_desc': fields.text('Status Desc'),
        'xml_content': fields.text('XML File Content'),
    }
