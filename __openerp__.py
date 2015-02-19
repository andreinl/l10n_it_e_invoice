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

{
    'name': "Electronic Invoice",
    'version': '3.1.1.1-alfa3',
    'category': 'Account',
    'description': """
Electronic Invoice Management - Italian Law
Modulo di gestione fatturazione elettronica

Attenzione! Il modulo al momento non è ancora utilizzabile.

TODO:
Le funzionalità da implemntare per poter almeno testare la correttezza del XML composto:
- Concludere compilazione dei campi assolutamente indispensabili per la produzione della
  fattura PA
- Aggiungere e (o) collegare le tabelle:
  - RegimeFiscale
  - TipoCassa
  - ModalitaPagamento
  - TipoDocumento
  - Natura

- write tests
- Chiedere a cosa serve nr_bollo


Campi opzionali
Il tracciato di fatturaPA prevede l'indicazione di numerosi campi opzionali, che al momento non vengono supportati.
Questo è l'elenco dei campi non esportati. Nel codice sono commentati e preceduti con ***:

Testata
1.2.1.3.4 CedentePrestatore.DatiAnagrafici.Anagrafica.Titolo
1.2.1.3.5 CedentePrestatore.DatiAnagrafici.Anagrafica.CodEORI
1.2.1.4 CedentePrestatore.DatiAnagrafici.AlboProfessionale
1.2.1.5 CedentePrestatore.DatiAnagrafici.ProvinciaAlbo
1.2.1.6 CedentePrestatore.DatiAnagrafici.NumeroIscrizioneAlbo
1.2.1.7 CedentePrestatore.DatiAnagrafici.DataIscrizioneAlbo
Il seguente attributo non è opzionale, ma la quantità di clienti che hanno bisogno di questa funzionalità è minimo:
1.2.3 DatiAnagrafici.StabileOrganizzazione
1.3 RappresentanteFiscale
1.4.1.3.4 Titolo
1.4.1.3.5 CodEORI
1.5 TerzoIntermediarioOSoggettoEmittente
1.6 SoggettoEmittente

Fattura
2.1.1.7.8 DatiGenerali.DatiGeneraliDocumento.DatiCassaPrevidenziale.RiferimentoAmministrazione
2.1.1.8 DatiGenerali.DatiGeneraliDocumento.ScontoMaggiorazione
2.1.1.10 Arrotondamento
2.1.1.11 Causale
2.1.2 DatiOrdineAcquisto
2.1.2.1 DatiGenerali.DatiOrdineAcquisto.RiferimentoNumeroLinea
2.1.2.4 DatiGenerali.DatiOrdineAcquisto.NumItem
2.1.2.5 DatiGenerali.DatiOrdineAcquisto.CodiceCommessaConvenzione
2.1.3 DatiGenerali.DatiContratto (come 2.1.2.1/3/4/5)
2.1.4 DatiGenerali.DatiConvenzione (come 2.1.2.1/3/4/5)
2.1.5 DatiGenerali.DatiRicezione
2.1.6 DatiGenerali.DatiFattureCollegate
2.1.7 DatiGenerali.DatiSAL
2.1.8.3 DatiGenerali.DatiDDT.RiferimentoNumeroLinea
2.1.9.1 DatiGenerali.DatiTrasporto.DatiAnagraficiVettore
2.1.9.2 DatiGenerali.DatiTrasporto.Mezzo
2.1.9.8 DatiGenerali.DatiTrasporto.PesoNetto
2.1.9.9 DatiGenerali.DatiTrasporto.DataOraRitiro
2.1.9.13 DatiGenerali.DatiTrasporto.DataOraConsegna
2.1.10 DatiGenerali.FatturaPrincipale
2.2.1.2 DatiGenerali.DettaglioLinee.TipoCessionePrestazione
2.2.1.7 DatiGenerali.DettaglioLinee.DataInizioPeriodo
2.2.1.8 DatiGenerali.DettaglioLinee.DataFinePeriodo
2.2.1.10.3 DatiGenerali.DettaglioLinee.ScontoMaggiorazione.Importo
2.2.1.15 DatiGenerali.DettaglioLinee.RiferimentoAmministrazione
2.3 DatiVeicoli
2.4.2.1 DatiPagamento.DettaglioPagamento.Beneficiario
2.4.2.3 DatiPagamento.DettaglioPagamento.DataRiferimentoTerminiPagamento
2.4.2.4 DatiPagamento.DettaglioPagamento.GiorniTerminiPagamento
2.4.2.7 DatiPagamento.DettaglioPagamento.CodUfficioPostale
2.4.2.8 DatiPagamento.DettaglioPagamento.CognomeQuietanziante
2.4.2.9 DatiPagamento.DettaglioPagamento.NomeQuietanziante
2.4.2.10 DatiPagamento.DettaglioPagamento.CFQuietanziante
2.4.2.11 DatiPagamento.DettaglioPagamento.TitoloQuietanziante
2.4.2.17 DatiPagamento.DettaglioPagamento.ScontoPagamentoAnticipato
2.4.2.18 DatiPagamento.DettaglioPagamento.DataLimitePagamentoAnticipato
2.4.2.19 DatiPagamento.DettaglioPagamento.PenalitàPagamentiRitardati
2.4.2.20 DatiPagamento.DettaglioPagamento.DataDecorrenzaPenale
2.4.2.21 DatiPagamento.DettaglioPagamento.CodicePagamento


Controllo conformità del documento
http://sdi.fatturapa.gov.it/SdI2FatturaPAWeb/ControllaFatturaAction.do

Visualizzazione:
https://sdi.fatturapa.gov.it/SdI2FatturaPAWeb/AccediAlServizioAction.do?pagina=visualizza_file_sdi

""",
    'author': 'Apulia Software srl <info@apuliasoftware.it>, Didotech srl <info@didotech.com>',
    'website': 'www.apuliasoftware.it, www.didotech.com',
    'license': 'AGPL-3',
    "depends": [
        'account',
        'revenue_stamp',
        'l10n_base_data_it',
    ],
    "data": [
        'security/security.xml',
        'security/ir.model.access.csv',
        'partner/partner_view.xml',
        'company/company_view.xml',
        'account/account_view.xml',
        'report/account_report.xml',
        'account/e-invoice_data.xml',
        'wizard/send_invoice_view.xml',
        'e_invoice_data.xml'
    ],
    "active": False,
    "installable": True,
    'external_dependencies': {
        'python': [
            'lxml',
        ]
    }
}
