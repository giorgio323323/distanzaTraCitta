# distanzaTraCitta
distanze e tempi tra comuni in lombardia
cerca nel db distanza e tempo  di percorrenza tra due città. Fonte ISTAT

questo repository contiene modulo e files per ricercare distanze tempi di percorrenza tra comuni in Lomabardia Italia.
é basato su dati provenienti dal sito ISTAT:

**ISTAT Matrici di contiguità, distanza e pendolarismo**
Per alcune regioni, tra cui la lombardia, sono presenti file contenenti distanze e tempi di percorrenza tra comuni.
 https://www.istat.it/it/archivio/157423

**Codici dei comuni italiani**
 https://www.istat.it/storage/codici-unita-amministrative/Elenco-comuni-italiani.xls


## uso

### prepara il file dati.
funzioni usati per filtrare i file di origine e ottenerne di più piccoli

procedura:
* scarica
   https://www.istat.it/storage/codici-unita-amministrative/Elenco-comuni-italiani.xls
   https://www.istat.it/it/archivio/157423

* mettili nello stesso folder dove si trova questo script e se necessario unzippali.
* esegui python generaFiles.py
nel terminale iniziano a scorrere i dati trattati. Il processo pernde qualche minuto.
* vengono generati due file:
   comuniLombardia.txt
   distanzeComuniLombardia.txt




nel folder vanno copiati tre file:

* distanzacitta.py; modulo contenente la classe
* distanzeComuniLombardia.txt
* comuniLombardia.txt

il modulo usa Pandas.
I nomi vengono trasformati in UPPERCASE.
result vale -1 in caso di errore

## codice di esempio

        # esempio uso
        import distanzacitta

        d = distanzacitta.distanzaTraCitta(verbose=False, shortDF = False)
        result, dist, tempo= d.distanzaNomeA2NomeB('Capriate San Gervasio', 'Capriate San Gervasio')
        
		result, dist, tempo= d.distanzaNomeA2NomeB('parabiago', 'milano')
		if result != -1
	        print("distanza [m]:" + str(dist) +" tempo di percorrenza [minuti]: " +str(tempo))
		else:
			print("errore")

## note sul metodo
### compattamento dei dati per la memoria
Il file di origine:
	Lombardia.txt
non poteva essere caricato interamente in memoria

Il primo campo 'origine-destinazione' è stato quindi eliminato. Questo ha permesso di avere solo mumeri.

operazione analoga sul file "Elenco-comuni-italiani.csv". Questo è stato filtrato per avere solo i comuni lombardi.

Le funzioni di conversione sono contenute nel modulo.

### test del modulo

il modulo è stato testato con l'elenco comuni presenti nella matrice origine destinazione di regione lombardia.
fonte: https://www.dati.lombardia.it/stories/s/5tsd-gjin
In questa matrice alcuni comuni sono divisi in zone. Ad esempio Milano è suddiviso in 16 settori. 
Questi divisioni non sono presenti nel file ISTAT. Il modulo distanzaCitta provvede a rimuovere numeri al termine del nome. Quindi passare MILANO oppure MILANO 3 da lo stesso risultato.

i seguenti paesi nonsono  riconosciuti

BOVISIO MASCIAGO
CADREZZATE - OSMATE
CANTU'
CASSINA DE PECCHI
CORTEOLONA
CUNARDO - MASCIAGO PRIMO
FENEGRO'
GAZZADA - SCHIANNO
GIUSSAGO - ROGNANO
MUGGIO'
RIVANAZZANO TERME - ROCCA SUSELLA
ROE' VOLCIANO
TRAVACO' SICCOMARIO
TREMOSINE
UGGIATE - TREVANO
VERMEZZO
VIGGIU'
ZELO SURRIGONE
ZERBOLO'




