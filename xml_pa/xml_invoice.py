# -*- coding: utf-8 -*-

##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    Copyright (C) 2015 Didotech srl (<http://www.didotech.com>).
#
#                       All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (self.at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
#
# Ex. in format 1.0: http://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.0/IT01234567890_22222.xml
#

import lxml.etree as etree
import os

import pdb

class InvoicePa():
    def __init__(self):
        NSMAP = {
            'p': "http://www.fatturapa.gov.it/sdi/fatturapa/v1.1",
            'ds': "http://www.w3.org/2000/09/xmldsig#",
            'xsi': "http://www.w3.org/2001/XMLSchema-instance"
        }

        self.invoice = etree.Element('{http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}FatturaElettronica', nsmap=NSMAP, attrib={'versione': "1.1"})

        header = etree.SubElement(self.invoice, 'FatturaElettronicaHeader')

        # 1.1 <DatiTrasmissione>
        self.trasmissione = etree.SubElement(header, 'DatiTrasmissione')
        id_trasmittente = etree.SubElement(self.trasmissione, 'IdTrasmittente')
        self.trasmittente_paese = etree.SubElement(id_trasmittente, 'IdPaese')
        self.trasmittente_codice = etree.SubElement(id_trasmittente, 'IdCodice')

        self.progressivo_invio = etree.SubElement(self.trasmissione, 'ProgressivoInvio')
        self.formato_trasmissione = etree.SubElement(self.trasmissione, 'FormatoTrasmissione')
        self.codice_destinatario = etree.SubElement(self.trasmissione, 'CodiceDestinatario')
        self.contatti_trasmittente = etree.SubElement(self.trasmissione, 'ContattiTrasmittente')
        self.trasmittente_telefono = etree.SubElement(self.contatti_trasmittente, 'Telefono')
        self.trasmittente_email = etree.SubElement(self.contatti_trasmittente, 'Email')

        # 1.2 <CedentePrestatore>
        self.cedente = etree.SubElement(header, 'CedentePrestatore')
        self.cedente_dati = etree.SubElement(self.cedente, 'DatiAnagrafici')
        self.cedente_iva = etree.SubElement(self.cedente_dati, 'IdFiscaleIVA')
        self.cedente_iva_paese = etree.SubElement(self.cedente_iva, 'IdPaese')
        self.cedente_iva_codice = etree.SubElement(self.cedente_iva, 'IdCodice')

        self.cedente_codice_fiscale = etree.SubElement(self.cedente_dati, 'CodiceFiscale')
        self.cedente_anagrafica = etree.SubElement(self.cedente_dati, 'Anagrafica')
        self.cedente_anagrafica_denominazione = etree.SubElement(self.cedente_anagrafica, 'Denominazione')
        self.cedente_anagrafica_nome = etree.SubElement(self.cedente_anagrafica, 'Nome')
        self.cedente_anagrafica_cognome = etree.SubElement(self.cedente_anagrafica, 'Cognome')
        # ***
        # self.cedente_anagrafica_titolo = etree.SubElement(self.cedente_anagrafica, 'Titolo')
        # self.cedente_anagrafica_codeori = etree.SubElement(self.cedente_anagrafica, 'CodEORI')

        # ***
        # self.cedente_albo_professionale = etree.SubElement(self.cedente_dati, 'AlboProfessionale')
        # self.cedente_provincia_albo = etree.SubElement(self.cedente_dati, 'ProvinciaAlbo')
        # self.cedente_numero_iscrizione_albo = etree.SubElement(self.cedente_dati, 'NumeroIscrizioneAlbo')
        # self.cedente_data_iscrizione_albo = etree.SubElement(self.cedente_dati, 'DataIscrizioneAlbo')
        self.cedente_regime_fiscale = etree.SubElement(self.cedente_dati, 'RegimeFiscale')

        self.cedente_sede = etree.SubElement(self.cedente, 'Sede')
        self.cedente_sede_indirizzo =  etree.SubElement(self.cedente_sede, 'Indirizzo')
        # Already inside indirizzo
        # self.cedente_sede_numero_civico =  etree.SubElement(self.cedente_sede, 'NumeroCivico')
        self.cedente_sede_cap =  etree.SubElement(self.cedente_sede, 'CAP')
        self.cedente_sede_comune =  etree.SubElement(self.cedente_sede, 'Comune')
        self.cedente_sede_provincia =  etree.SubElement(self.cedente_sede, 'Provincia')
        self.cedente_sede_nazione =  etree.SubElement(self.cedente_sede, 'Nazione')

        # ***
        # self.cedente_stabile = etree.SubElement(self.cedente, 'StabileOrganizzazione')
        # self.cedente_stabile_indirizzo =  etree.SubElement(self.cedente_stabile, 'Indirizzo')
        # self.cedente_stabile_numero_civico =  etree.SubElement(self.cedente_stabile, 'NumeroCivico')
        # self.cedente_stabile_cap =  etree.SubElement(self.cedente_stabile, 'CAP')
        # self.cedente_stabile_comune =  etree.SubElement(self.cedente_stabile, 'Comune')
        # self.cedente_stabile_provincia =  etree.SubElement(self.cedente_stabile, 'Provincia')
        # self.cedente_stabile_nazione =  etree.SubElement(self.cedente_stabile, 'Nazione')

        self.cedente_rea = etree.SubElement(self.cedente, 'IscrizioneREA')
        self.cedente_rea_ufficio = etree.SubElement(self.cedente_rea, 'Ufficio')
        self.cedente_rea_numero = etree.SubElement(self.cedente_rea, 'NumeroREA')
        self.cedente_rea_capitale_sociale = etree.SubElement(self.cedente_rea, 'CapitaleSociale')
        self.cedente_rea_socio_unico = etree.SubElement(self.cedente_rea, 'SocioUnico')
        self.cedente_rea_stato_liquidazione = etree.SubElement(self.cedente_rea, 'StatoLiquidazione')

        self.cedente_contatti = etree.SubElement(self.cedente, 'Contatti')
        self.cedente_contatti_telefono = etree.SubElement(self.cedente_contatti, 'Telefono')
        self.cedente_contatti_fax = etree.SubElement(self.cedente_contatti, 'Fax')
        self.cedente_contatti_email = etree.SubElement(self.cedente_contatti, 'Email')

        self.cedente_riferimento_amministrazione = etree.SubElement(self.cedente, 'RiferimentoAmministrazione')

        # ***
        # 1.3 <RappresentanteFiscale>
        # self.rappresentante = etree.SubElement(header, 'RappresentanteFiscale')
        # self.rappresentante_dati = etree.SubElement(self.rappresentante, 'DatiAnagrafici')
        # self.rappresentante_iva = etree.SubElement(self.rappresentante_dati, 'IdFiscaleIVA')
        # self.rappresentante_iva_paese = etree.SubElement(self.rappresentante_iva, 'IdPaese')
        # self.rappresentante_iva_codice = etree.SubElement(self.rappresentante_iva, 'IdCodice')
        #
        # self.rappresentante_codice_fiscale = etree.SubElement(self.rappresentante_dati, 'CodiceFiscale')
        # self.rappresentante_anagrafica = etree.SubElement(self.rappresentante_dati, 'Anagrafica')
        # self.rappresentante_denominazione = etree.SubElement(self.rappresentante_anagrafica, 'Denominazione')
        # self.rappresentante_nome = etree.SubElement(self.rappresentante_anagrafica, 'Nome')
        # self.rappresentante_cognome = etree.SubElement(self.rappresentante_anagrafica, 'Cognome')
        # self.rappresentante_titolo = etree.SubElement(self.rappresentante_anagrafica, 'Titolo')
        # self.rappresentante_codeori = etree.SubElement(self.rappresentante_anagrafica, 'CodEORI')

        # 1.4 <CessionarioCommittente> - destinatario
        self.cessionario = etree.SubElement(header, 'CessionarioCommittente')
        self.cessionario_dati = etree.SubElement(self.cessionario, 'DatiAnagrafici')
        self.cessionario_iva = etree.SubElement(self.cessionario_dati, 'IdFiscaleIVA')
        self.cessionario_iva_paese = etree.SubElement(self.cessionario_iva, 'IdPaese')
        self.cessionario_iva_codice = etree.SubElement(self.cessionario_iva, 'IdCodice')

        self.cessionario_codice_fiscale = etree.SubElement(self.cessionario_dati, 'CodiceFiscale')
        self.cessionario_anagrafica = etree.SubElement(self.cessionario_dati, 'Anagrafica')
        self.cessionario_denominazione = etree.SubElement(self.cessionario_anagrafica, 'Denominazione')
        self.cessionario_nome = etree.SubElement(self.cessionario_anagrafica, 'Nome')
        self.cessionario_cognome = etree.SubElement(self.cessionario_anagrafica, 'Cognome')
        # ***
        # self.cessionario_titolo = etree.SubElement(self.cessionario_anagrafica, 'Titolo')
        # self.cessionario_codeori = etree.SubElement(self.cessionario_anagrafica, 'CodEORI')

        self.cessionario_sede = etree.SubElement(self.cessionario, 'Sede')
        self.cessionario_sede_indirizzo =  etree.SubElement(self.cessionario_sede, 'Indirizzo')
        # OpenERP / Odoo doesn't have this field, so we don't need it
        # self.cessionario_sede_numero_civico =  etree.SubElement(self.cessionario_sede, 'NumeroCivico')
        self.cessionario_sede_cap =  etree.SubElement(self.cessionario_sede, 'CAP')
        self.cessionario_sede_comune =  etree.SubElement(self.cessionario_sede, 'Comune')
        self.cessionario_sede_provincia =  etree.SubElement(self.cessionario_sede, 'Provincia')
        self.cessionario_sede_nazione =  etree.SubElement(self.cessionario_sede, 'Nazione')

        # ***
        # 1.5 <TerzoIntermediarioOSoggettoEmittente>
        # self.intermediario = etree.SubElement(header, 'TerzoIntermediarioOSoggettoEmittente')
        # self.intermediario_dati = etree.SubElement(self.intermediario, 'DatiAnagrafici')
        # self.intermediario_iva = etree.SubElement(self.intermediario_dati, 'IdFiscaleIVA')
        # self.intermediario_iva_paese = etree.SubElement(self.intermediario_iva, 'IdPaese')
        # self.intermediario_iva_codice = etree.SubElement(self.intermediario_iva, 'IdCodice')
        #
        # self.intermediario_codice_fiscale = etree.SubElement(self.intermediario_dati, 'CodiceFiscale')
        # self.intermediario_anagrafica = etree.SubElement(self.intermediario_dati, 'Anagrafica')
        # self.intermediario_denominazione = etree.SubElement(self.intermediario_anagrafica, 'Denominazione')
        # self.intermediario_nome = etree.SubElement(self.intermediario_anagrafica, 'Nome')
        # self.intermediario_cognome = etree.SubElement(self.intermediario_anagrafica, 'Cognome')
        # self.intermediario_titolo = etree.SubElement(self.intermediario_anagrafica, 'Titolo')
        # self.intermediario_codeori = etree.SubElement(self.intermediario_anagrafica, 'CodEORI')

        # ***
        # 1.6 <SoggettoEmittente>
        # self.emittente = etree.SubElement(header, 'SoggettoEmittente')

        # 2 <FatturaElettronicaBody>
        self.body = etree.SubElement(self.invoice, 'FatturaElettronicaBody')

        # 2.1 <DatiGenerali>
        self.dati_generali = etree.SubElement(self.body, 'DatiGenerali')

        self.documento = etree.SubElement(self.dati_generali, 'DatiGeneraliDocumento')
        self.documento_tipo = etree.SubElement(self.documento, 'TipoDocumento')
        self.documento_divisa = etree.SubElement(self.documento, 'Divisa')
        self.documento_data = etree.SubElement(self.documento, 'Data')
        self.documento_numero = etree.SubElement(self.documento, 'Numero')
        self.documento_ritenuta = etree.SubElement(self.documento, 'DatiRitenuta')
        self.documento_ritenuta_tipo = etree.SubElement(self.documento_ritenuta, 'TipoRitenuta')
        self.documento_ritenuta_importo = etree.SubElement(self.documento_ritenuta, 'ImportoRitenuta')
        self.documento_ritenuta_aliquota = etree.SubElement(self.documento_ritenuta, 'AliquotaRitenuta')
        self.documento_ritenuta_causale_pagamento = etree.SubElement(self.documento_ritenuta, 'CausalePagamento')

        self.documento_bollo = etree.SubElement(self.documento, 'DatiBollo')
        self.documento_bollo_virtuale = etree.SubElement(self.documento_bollo, 'BolloVirtuale')
        self.documento_bollo_importo = etree.SubElement(self.documento_bollo, 'ImportoBollo')

        self.documento_cassa_previdenza = etree.SubElement(self.documento, 'DatiCassaPrevidenziale')
        self.documento_cassa_previdenza_tipo = etree.SubElement(self.documento_cassa_previdenza, 'TipoCassa')
        self.documento_cassa_previdenza_aliquota = etree.SubElement(self.documento_cassa_previdenza, 'AlCassa')
        self.documento_cassa_previdenza_importo_contributo = etree.SubElement(self.documento_cassa_previdenza, 'ImportoContributoCassa')
        self.documento_cassa_previdenza_imponibile = etree.SubElement(self.documento_cassa_previdenza, 'ImponibileCassa')
        self.documento_cassa_previdenza_iva = etree.SubElement(self.documento_cassa_previdenza, 'AliquotaIVA')
        self.documento_cassa_previdenza_ritenuta = etree.SubElement(self.documento_cassa_previdenza, 'Ritenuta')
        self.documento_cassa_previdenza_natura = etree.SubElement(self.documento_cassa_previdenza, 'Natura')
        # ***
        # self.documento_cassa_previdenza_amministrazione = etree.SubElement(self.documento_cassa_previdenza, 'RiferimentoAmministrazione')

        # *** Non esiste in OpenERP/Odoo
        # self.documento_sconto = etree.SubElement(self.documento, 'ScontoMaggiorazione')
        # self.documento_sconto_tipo = etree.SubElement(self.documento_sconto, 'Tipo')
        # self.documento_sconto_percentuale = etree.SubElement(self.documento_sconto, 'Percentuale')
        # self.documento_sconto_importo = etree.SubElement(self.documento_sconto, 'Importo')

        self.documento_totale = etree.SubElement(self.documento, 'ImportoTotaleDocumento')
        # ***
        # self.documento_arrotondamento = etree.SubElement(self.documento, 'Arrotondamento')
        # self.documento_causale = etree.SubElement(self.documento, 'Causale')
        self.documento_art_73 = etree.SubElement(self.documento, 'Art73')

        self.ordine_acquisto = etree.SubElement(self.dati_generali, 'DatiOrdineAcquisto')
        # ***
        # self.ordine_acquisto_linea = etree.SubElement(self.ordine_acquisto, 'RiferimentoNumeroLinea')
        self.ordine_acquisto_documento = etree.SubElement(self.ordine_acquisto, 'IdDocumento')
        self.ordine_acquisto_data = etree.SubElement(self.ordine_acquisto, 'Data')
        # ***
        # self.ordine_acquisto_numero_linea = etree.SubElement(self.ordine_acquisto, 'NumItem')
        # self.ordine_acquisto_commessa = etree.SubElement(self.ordine_acquisto, 'CodiceCommessaConvenzione')
        self.ordine_acquisto_cup = etree.SubElement(self.ordine_acquisto, 'CodiceCUP')
        self.ordine_acquisto_cig = etree.SubElement(self.ordine_acquisto, 'CodiceCIG')

        # ***
        # self.contratto = etree.SubElement(self.dati_generali, 'DatiContratto')
        # self.convenzione = etree.SubElement(self.dati_generali, 'DatiConvenzione')
        # self.ricezione = etree.SubElement(self.dati_generali, 'DatiRicezione')
        # self.fatture_collegate = etree.SubElement(self.dati_generali, 'DatiFattureCollegate')
        # self.sal = etree.SubElement(self.dati_generali, 'DatiSAL')
        # self.sal_riferimento = etree.SubElement(self.sal, 'RiferimentoFase')

        # 2.1.8 <DatiDDT>: can be repeated so the code is moved to the function
        # 2.1.9 <DatiTrasporto>: Moved in separate function because of DDT block
        # 2.1.10 <FatturaPrincipale>: Moved in separate function because of DDT block



        # 2.2 <DatiBeniServizi>
        self.beni_servizi = etree.SubElement(self.body, 'DatiBeniServizi')

        # ***
        # 2.3 <DatiVeicoli>
        # self.veicolo = etree.SubElement(self.body, 'DatiVeicoli')
        # self.veicolo_data = etree.SubElement(self.veicolo, 'Data')
        # self.veicolo_percorso = etree.SubElement(self.veicolo, 'TotalePercorso')
        
        # 2.4 <DatiPagamento>
       
        # ***
        # self.pagamento_dettaglio_sconto = etree.SubElement(self.pagamento_dettaglio, 'ScontoPagamentoAnticipato')
        # self.pagamento_dettaglio_data_limite = etree.SubElement(self.pagamento_dettaglio, 'DataLimitePagamentoAnticipato')
        # self.pagamento_dettaglio_penalita = etree.SubElement(self.pagamento_dettaglio, 'PenalitaPagamentiRitardati')
        # self.pagamento_dettaglio_data_penale = etree.SubElement(self.pagamento_dettaglio, 'DataDecorrenzaPenale')
        # self.pagamento_dettaglio_codice = etree.SubElement(self.pagamento_dettaglio, 'CodicePagamento')
        #
        # # 2.5 <Allegati>
        # self.allegato = etree.SubElement(self.body, 'Allegati')
        # self.allegato_nome = etree.SubElement(self.allegato, 'NomeAttachment')
        # self.allegato_compressione = etree.SubElement(self.allegato, 'AlgoritmoCompressione')
        # self.allegato_formato = etree.SubElement(self.allegato, 'FormatoAttachment')
        # self.allegato_descrizione = etree.SubElement(self.allegato, 'DescrizioneAttachment')
        # self.allegato_allegato = etree.SubElement(self.allegato, 'Attachment')

    def __unicode__(self):
        return etree.tounicode(self.invoice, pretty_print=True)

    def __str__(self):
        return etree.tounicode(self.invoice, pretty_print=True)

    def set_dati_trasmissione(self, dati_trasmissione):
        self.trasmittente_paese.text = dati_trasmissione['paese']
        self.trasmittente_codice.text = dati_trasmissione['fiscalcode']
        self.formato_trasmissione.text = dati_trasmissione['format']
        self.codice_destinatario.text = dati_trasmissione['ipa_code']

        if dati_trasmissione.get('phone'):
            self.trasmittente_telefono.text = dati_trasmissione['phone']
        else:
            self.contatti_trasmittente.remove(self.trasmittente_telefono)

        if dati_trasmissione.get('email'):
            self.trasmittente_email.text = dati_trasmissione['email']
        else:
            self.contatti_trasmittente.remove(self.trasmittente_email)

        if not len(self.contatti_trasmittente):
            self.trasmissione.remove(self.contatti_trasmittente)

    def set_progressivo_invio(self, progressivo):
        self.progressivo_invio.text = progressivo

    def set_cedente_prestatore(self, cedente_prestatore):
        self.cedente_iva_paese.text = cedente_prestatore['country']
        self.cedente_iva_codice.text = cedente_prestatore['iva']

        if cedente_prestatore.get('fiscalcode'):
            self.cedente_codice_fiscale.text = cedente_prestatore['fiscalcode']
        else:
            self.cedente_dati.remove(self.cedente_codice_fiscale)

        if cedente_prestatore.get('denominazione'):
            self.cedente_anagrafica_denominazione.text = cedente_prestatore['denominazione']
            self.cedente_anagrafica.remove(self.cedente_anagrafica_nome)
            self.cedente_anagrafica.remove(self.cedente_anagrafica_cognome)
        else:
            self.cedente_anagrafica_nome.text = cedente_prestatore['nome']
            self.cedente_anagrafica_cognome.text = cedente_prestatore['cognome']
            self.cedente_anagrafica.remove(self.cedente_anagrafica_denominazione)

        # invoice_pa.cedente_regime_fiscale.text = cedente_prestatore['regime_fiscale']

        self.cedente_sede_indirizzo.text = cedente_prestatore['street']
        self.cedente_sede_cap.text = cedente_prestatore['zip']
        self.cedente_sede_comune.text = cedente_prestatore['city']

        if cedente_prestatore.get('province'):
            self.cedente_sede_provincia.text = cedente_prestatore['province']
        else:
            self.cedente_sede.remove(self.cedente_sede_provincia)

        self.cedente_sede_nazione.text = cedente_prestatore['country']

        if cedente_prestatore.get('rea_office'):
            self.cedente_rea_ufficio.text = cedente_prestatore['rea_office']
            self.cedente_rea_numero.text = cedente_prestatore['rea_number']
            if cedente_prestatore.get('capitale_sociale'):
                self.cedente_rea_capitale_sociale.text = cedente_prestatore['capitale_sociale']
            else:
                self.cedente_rea.remove(self.cedente_rea_capitale_sociale)

            if cedente_prestatore.get('socio_unico'):
                self.cedente_rea_socio_unico.text = cedente_prestatore['socio_unico']
            else:
                self.cedente_rea.remove(self.cedente_rea_socio_unico)

            self.cedente_rea_stato_liquidazione.text = cedente_prestatore['stato_liquidazione']
        else:
            self.cedente.remove(self.cedente_rea)

        if cedente_prestatore.get('phone'):
            self.cedente_contatti_telefono.text = cedente_prestatore['phone']
        else:
            self.cedente_contatti.remove(self.cedente_contatti_telefono)

        if cedente_prestatore.get('fax'):
            self.cedente_contatti_fax.text = cedente_prestatore['fax']
        else:
            self.cedente_contatti.remove(self.cedente_contatti_fax)

        if cedente_prestatore.get('email'):
            self.cedente_contatti_email.text = cedente_prestatore['email']
        else:
            self.cedente_contatti.remove(self.cedente_contatti_email)

        if cedente_prestatore.get('reference'):
            self.cedente_riferimento_amministrazione.text = cedente_prestatore['reference']
        else:
            self.cedente.remove(self.cedente_riferimento_amministrazione)



    def set_destinatario(self, destinatario):
        if destinatario.get('vat_country'):
            self.cessionario_iva_paese.text = destinatario['vat_country']
            self.cessionario_iva_codice.text = destinatario['vat']
            self.cessionario_dati.remove(self.cessionario_codice_fiscale)
        else:
            self.cessionario_codice_fiscale.text = destinatario['fiscalcode']
            self.cessionario_iva.remove(self.cessionario_iva_paese)
            self.cessionario_iva.remove(self.cessionario_iva_codice)

        if destinatario.get('fiscalcode_firstname'):
            self.cessionario_nome.text = destinatario['fiscalcode_firstname']
            self.cessionario_cognome.text = destinatario['fiscalcode_surname']
            self.cessionario_anagrafica.remove(self.cessionario_denominazione)
        else:
            self.cessionario_denominazione.text = destinatario['name']
            self.cessionario_anagrafica.remove(self.cessionario_nome)
            self.cessionario_anagrafica.remove(self.cessionario_cognome)

        self.cessionario_sede_indirizzo.text = destinatario['street']
        self.cessionario_sede_cap.text = destinatario['zip']
        self.cessionario_sede_comune.text = destinatario['city']

        if destinatario.get('province'):
            self.cessionario_sede_provincia.text = destinatario['province']
        else:
            self.cessionario_sede.remove(self.cessionario_sede_provincia)

        self.cessionario_sede_nazione.text = destinatario['country']

    def set_dati_generali(self, dati_generali):
        # self.documento_tipo.text = dati_generali['type']
        self.documento_divisa.text = dati_generali['currency']
        self.documento_data.text = dati_generali['date']
        self.documento_numero.text = dati_generali['number']

        if dati_generali.get('ritenuta_tipo'):
            self.documento_ritenuta_tipo.text = dati_generali['ritenuta_tipo']
            self.documento_ritenuta_importo.text = dati_generali['ritenuta_importo']
            self.documento_ritenuta_aliquota.text = dati_generali['ritenuta_aliquota']
            self.documento_ritenuta_causale_pagamento.text = dati_generali['ritenuta_causale_pagamento']
        else:
            self.documento.remove(self.documento_ritenuta)

        if dati_generali.get('bollo', False) == 'SI':
            self.documento_bollo_virtuale.text = dati_generali['bollo']
            self.documento_bollo_importo.text = dati_generali['bollo_importo']
        else:
            self.documento.remove(self.documento_bollo)

        if dati_generali.get('inps_tipo'):
            self.documento_cassa_previdenza_tipo.text = dati_generali['inps_tipo']
            self.documento_cassa_previdenza_aliquota.text = dati_generali['inps_aliquota']
            self.documento_cassa_previdenza_importo_contributo.text = dati_generali['inps_importo']
            self.documento_cassa_previdenza_imponibile.text = dati_generali['inps_imponibile']
            self.documento_cassa_previdenza_iva.text = dati_generali['inps_iva']
            self.documento_cassa_previdenza_ritenuta.text = dati_generali['inps_ritenuta']
            self.documento_cassa_previdenza_natura.text = dati_generali['inps_natura']
        else:
            self.documento.remove(self.documento_cassa_previdenza)

        self.documento_totale.text = dati_generali['total']

        if dati_generali.get('art_73'):
            self.documento_art_73.text = dati_generali['art_73']
        else:
            self.documento.remove(self.documento_art_73)

        if dati_generali.get('acquisto_documento'):
            self.ordine_acquisto_documento.text = dati_generali['acquisto_documento']
            self.ordine_acquisto_data.text = dati_generali['acquisto_data']
            self.ordine_acquisto_cup.text = dati_generali['acquisto_cup']
            self.ordine_acquisto_cig.text = dati_generali['acquisto_cig']
        else:
            self.dati_generali.remove(self.ordine_acquisto)

    def add_ddt(self, number, data_ddt):
        ddt = etree.SubElement(self.dati_generali, 'DatiDDT')
        ddt_numero = etree.SubElement(ddt, 'NumeroDDT')
        ddt_data = etree.SubElement(ddt, 'DataDDT')
        # ***
        # ddt_numero_linea = etree.SubElement(self.ddt, 'RiferimentoNumeroLinea')
        ddt_numero.text = number
        ddt_data.text = data_ddt

    def add_trasporto(self):
        self.trasporto = etree.SubElement(self.dati_generali, 'DatiTrasporto')
        # ***
        # self.trasporto_vettore = etree.SubElement(self.trasporto, 'DatiAnagraficiVettore')
        # self.trasporto_vettore_iva = etree.SubElement(self.trasporto_vettore, 'IdFiscaleIVA')
        # self.trasporto_vettore_iva_paese = etree.SubElement(self.trasporto_vettore_iva, 'IdPaese')
        # self.trasporto_vettore_iva_codice = etree.SubElement(self.trasporto_vettore_iva, 'IdCodice')
        #
        # self.trasporto_vettore_codice_fiscale = etree.SubElement(self.trasporto_vettore, 'CodiceFiscale')
        # self.trasporto_vettore_anagrafica = etree.SubElement(self.trasporto_vettore, 'Anagrafica')
        # self.trasporto_vettore_denominazione = etree.SubElement(self.trasporto_vettore_anagrafica, 'Denominazione')
        # self.trasporto_vettore_nome = etree.SubElement(self.trasporto_vettore_anagrafica, 'Nome')
        # self.trasporto_vettore_cognome = etree.SubElement(self.trasporto_vettore_anagrafica, 'Cognome')
        # self.trasporto_vettore_titolo = etree.SubElement(self.trasporto_vettore_anagrafica, 'Titolo')
        # self.trasporto_vettore_codeori = etree.SubElement(self.trasporto_vettore_anagrafica, 'CodEORI')
        #
        # self.trasporto_vettore_licenza_guida = etree.SubElement(self.trasporto_vettore, 'NumeroLicenzaGuida')
        #
        # self.trasporto_mezzo = etree.SubElement(self.trasporto, 'MezzoTrasporto')
        self.trasporto_causale = etree.SubElement(self.trasporto, 'CausaleTrasporto')
        self.trasporto_numero_colli = etree.SubElement(self.trasporto, 'NumeroColli')
        self.trasporto_descrizione = etree.SubElement(self.trasporto, 'Descrizione')
        self.trasporto_unita_misura = etree.SubElement(self.trasporto, 'UnitaMisuraPeso')
        self.trasporto_peso_lordo = etree.SubElement(self.trasporto, 'PesoLordo')
        # ***
        # self.trasporto_peso_netto = etree.SubElement(self.trasporto, 'PesoNetto')
        # self.trasporto_data_ora_ritiro = etree.SubElement(self.trasporto, 'DataOraRitiro')
        self.trasporto_data = etree.SubElement(self.trasporto, 'DataInizioTrasporto')
        self.trasporto_resa_tipo = etree.SubElement(self.trasporto, 'TipoResa')
        self.trasporto_resa = etree.SubElement(self.trasporto, 'IndirizzoResa')
        self.trasporto_resa_indirizzo =  etree.SubElement(self.trasporto_resa, 'Indirizzo')
        self.trasporto_resa_numero_civico =  etree.SubElement(self.trasporto_resa, 'NumeroCivico')
        self.trasporto_resa_cap =  etree.SubElement(self.trasporto_resa, 'CAP')
        self.trasporto_resa_comune =  etree.SubElement(self.trasporto_resa, 'Comune')
        self.trasporto_resa_provincia =  etree.SubElement(self.trasporto_resa, 'Provincia')
        self.trasporto_resa_nazione =  etree.SubElement(self.trasporto_resa, 'Nazione')

        # ***
        # self.trasporto_data_ora_consegna = etree.SubElement(self.trasporto, 'DataOraConsegna')

    def add_fattura_principale(self):
        self.fattura_principale = etree.SubElement(self.dati_generali, 'FatturaPrincipale')
        self.fattura_principale_numero = etree.SubElement(self.fattura_principale, 'NumeroFatturaPrincipale')
        self.fattura_principale_data = etree.SubElement(self.fattura_principale, 'DataFatturaPrincipale')

    def add_line(self, values):
        linea = etree.SubElement(self.beni_servizi, 'DettaglioLinee')

        linea_numero = etree.SubElement(linea, 'NumeroLinea')
        linea_numero.text = str(values['number'])
        # ***
        # linea_tipo_cessione = etree.SubElement(self.linea, 'TipoCessionePrestazione')
        # linea_articolo = etree.SubElement(linea, 'CodiceArticolo')
        # linea_articolo_tipo = etree.SubElement(linea_articolo, 'CodiceTipo')
        # linea_articolo_valore = etree.SubElement(linea_articolo, 'CodiceValore')

        linea_descrizione = etree.SubElement(linea, 'Descrizione')
        linea_descrizione.text = values['descrizione']
        linea_quantita = etree.SubElement(linea, 'Quantita')
        linea_quantita.text = values['quantity']
        linea_unita_misura = etree.SubElement(linea, 'UnitaMisura')
        linea_unita_misura.text = values['uom']

        # ***
        # linea_data_inizio = etree.SubElement(linea, 'DataInizioPeriodo')
        # linea_data_fine = etree.SubElement(linea, 'DataFinePeriodo')
        linea_prezzo = etree.SubElement(linea, 'PrezzoUnitario')
        linea_prezzo.text = values['unit_price']
        for discount in values['sconti']:
            if discount['tipo']:
                linea_sconto = etree.SubElement(linea, 'ScontoMaggiorazione')
                linea_sconto_tipo = etree.SubElement(linea_sconto, 'Tipo')
                linea_sconto_tipo.text = discount['tipo']
                linea_sconto_percentuale = etree.SubElement(linea_sconto, 'Percentuale')
                linea_sconto_percentuale.text = discount['percentuale']
                # *** OpenERP usa discount percentuale
                # linea_sconto_importo = etree.SubElement(linea_sconto, 'Importo')

        linea_totale = etree.SubElement(linea, 'PrezzoTotale')
        linea_totale.text = values['totale']

        linea_iva = etree.SubElement(linea, 'AliquotaIVA')
        linea_iva.text = values['iva']

        if values.get('ritenuta', False):
            linea_ritenuta = etree.SubElement(linea, 'Ritenuta')
            linea_ritenuta.text = 'SI'

        if values.get('natura', False):
            linea_natura = etree.SubElement(linea, 'Natura')
            linea_natura.text = values['natura']

        # ***
        # linea_amministrazione = etree.SubElement(linea, 'RiferimentoAmministrazione')

        # TODO: capire come valorizzare:
        # linea_altro = etree.SubElement(linea, 'AltriDatiGestionali')
        # linea_altro_tipo_dato = etree.SubElement(linea_altro, 'TipoDato')
        # linea_altro_testo = etree.SubElement(linea_altro, 'RiferimentoTesto')
        # linea_altro_numero = etree.SubElement(linea_altro, 'RiferimentoNumero')
        # linea_altro_data = etree.SubElement(linea_altro, 'RiferimentoData')

    def set_aliquota(self, values):
        riepilogo = etree.SubElement(self.beni_servizi, 'DatiRiepilogo')
        riepilogo_aliquota_iva = etree.SubElement(riepilogo, 'AliquotaIVA')
        #riepilogo_natura = etree.SubElement(riepilogo, 'Natura')
        #riepilogo_spese = etree.SubElement(riepilogo, 'SpeseAccessorie')
        riepilogo_arrotondamento = etree.SubElement(riepilogo, 'Arrotondamento')
        riepilogo_imponibile = etree.SubElement(riepilogo, 'ImponibileImporto')
        riepilogo_imponibile.text = values['imponibile']
        riepilogo_imposta = etree.SubElement(riepilogo, 'Imposta')
        riepilogo_imposta.text = values['imposta']
        riepilogo_esigibilita_iva = etree.SubElement(riepilogo, 'EsigibilitaIVA')
        riepilogo_normativo = etree.SubElement(riepilogo, 'RiferimentoNormativo')

    def set_pagamento(self, values):
        pagamento = etree.SubElement(self.body, 'DatiPagamento')
        pagamento_condizioni = etree.SubElement(pagamento, 'CondizioniPagamento')
        pagamento_condizioni.text = values['condizioni']
        pagamento_dettaglio = etree.SubElement(pagamento, 'DettaglioPagamento')
        # ***
        # pagamento_dettaglio_beneficiario = etree.SubElement(pagamento_dettaglio, 'Beneficiario')
        # TODO: compilare come indicato nella tabella
        # pagamento_dettaglio_modalita = etree.SubElement(pagamento_dettaglio, 'ModalitaPagamento')
        # pagamento_dettaglio_modalita.text = values['modalita']
        # ***
        # pagamento_dettaglio_data_termini = etree.SubElement(pagamento_dettaglio, 'DataRiferimentoTerminiPagamento')
        # pagamento_dettaglio_giorni_termini = etree.SubElement(pagamento_dettaglio, 'GiorniTerminiPagamento')
        pagamento_dettaglio_data_scadenza = etree.SubElement(pagamento_dettaglio, 'DataScadenzaPagamento')
        pagamento_dettaglio_data_scadenza.text = values['scadenza']
        pagamento_dettaglio_importo = etree.SubElement(pagamento_dettaglio, 'ImportoPagamento')
        pagamento_dettaglio_importo.text = values['importo']
        # ***
        # pagamento_dettaglio_ufficio_postale = etree.SubElement(pagamento_dettaglio, 'CodUfficioPostale')
        # pagamento_dettaglio_quietanzante_cognome = etree.SubElement(pagamento_dettaglio, 'CognomeQuietanzante')
        # pagamento_dettaglio_quietanzante_nome = etree.SubElement(pagamento_dettaglio, 'NomeQuietanzante')
        # pagamento_dettaglio_quietanzante_cfq = etree.SubElement(pagamento_dettaglio, 'CFQuietanzante')
        # pagamento_dettaglio_quietanzante_titolo = etree.SubElement(pagamento_dettaglio, 'TitoloQuietanzante')
        if values.get('istituto_finanziario', False):
            pagamento_dettaglio_istituto_finanziario = etree.SubElement(pagamento_dettaglio, 'IstitutoFinanziario')
            pagamento_dettaglio_istituto_finanziario.text = values['istituto_finanziario']
            if values.get('iban', False):
                pagamento_dettaglio_iban = etree.SubElement(pagamento_dettaglio, 'IBAN')
                pagamento_dettaglio_iban.text = values['iban']
            else:
                pagamento_dettaglio_abi = etree.SubElement(pagamento_dettaglio, 'ABI')
                pagamento_dettaglio_abi.text = values['abi']
                pagamento_dettaglio_cab = etree.SubElement(pagamento_dettaglio, 'CAB')
                pagamento_dettaglio_cab.text = values['cab']
            if values.get('bic', False):
                pagamento_dettaglio_bic = etree.SubElement(pagamento_dettaglio, 'BIC')
                pagamento_dettaglio_bic.text = values['bic']

    def validate(self):
        # f = file('Schema_del_file_xml_FatturaPA_versione_1.1.xsd', 'r')
        # xmlschema_doc = etree.parse(f)
        # pdb.set_trace()
        # xmlschema = etree.XMLSchema(xmlschema_doc)

        xmlschema = etree.XMLSchema(file=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Schema_del_file_xml_FatturaPA_versione_1.1.xsd'))
        # return xmlschema.validate(self.invoice)
        return xmlschema.assertValid(self.invoice)


# ============================================
if __name__ =='__main__':
    invoice_pa = InvoicePa()
    if invoice_pa.validate():
        print('Valid XML')
    else:
        print("XML file doesn't validate")
    pdb.set_trace()
    print invoice_pa
