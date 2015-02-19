l10n_it_e-invoice
=================

Fatturazione Elettronica per Openerp
------------------------------------

**Attenzione!** Questo modulo funziona esclusivamente sottoscrivendo un contratto con il provider di servizi di Fatturazione Elettronica Esterno

Per info e adesioni:

* info@apuliasoftware.it
* info@didotech.com

Il modulo permette di inviare o scaricare la fattura in formato PDF o XML (questa seconda funzionalità è in fase di sviluppo e non è ancora pronta per l'utilizzo).

Installazione
-------------
Il modulo dipende da alcuni moduli esterni, che si possono trovare nella repository https://github.com/iw3hxn/LibrERP:

* **revenue stamp** - Questo modulo è necessario per la gestione del bollo in fattura.
* **l10n_it_base** - Fra le altre cose aggiunge la tabella res_province necessaria per avere le province. l10n_base_data_it dipende da questo modulo.
* **l10n_base_data_it** - Fra le altre cose il modulo aggiunge le province italiane.

Può essere che siano richiesti anche:

* **l10n_it_account**
* **account_invoice_entry_date**
* **account_vat_period_end_statement**
* **report_webkit**

n.b.: per altre versioni del programma è possibile che i moduli siano sostituiti da altri moduli o debbano essere migrati.

Istruzioni operative
--------------------
Per poter produrre una fattura elettronica è necessario rispettare le seguenti condizioni che non servono per la stampa della fattura tradizionale:

* Il *Giornale* deve essere di tipo "E-Invoice Journal"
* Nella configurazione dell'Azienda deve essere impostato *eInvoice transmitter*.
* Se l'azienda è iscritta nel registro delle imprese, deve essere compilata la scheda REA nella configurazione dell'Azienda.
* Nella scheda del partner selezionato come transmitter sulla scheda *E-Invoice* è necessario indicare i parametri del protocollo. Al giorno d'oggi è supportato il "Download" e "FTP". Attenzione: *Destination File path for e-invoice* è il percorso sul server di destinazione indicato dal fornitore del servizio.

A destra sulla view della Fattura si trova l'action **Send E-Invoice**. Questa action richiama la view che permette di scegliere il formato della fattura (PDF o XML) e inviare o scaricare il file generato.

Spiegazioni tecniche
--------------------
La composizione della fattura avviene all'interno del file wizard/wizard_send_invoice.py. Dipendentemente dal formato viene usata la funzione create_report() che produce il file in PDF o create_xml().

La funzione create_xml() raccoglie i dati necessari e poi chiama le funzioni della classe InvoicePa del file xml_pa/xml_invoice.py che man mano compongono tutto il file XML.

Chiunque avesse voglia di collaborare deve prima di tutto leggere la description dentro file \_\_openerp\_\_.py che contiene diverse utili informazioni.

