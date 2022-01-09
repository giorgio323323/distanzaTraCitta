import pandas as pd


class distanzaTraCitta():
    '''
        # test classe distanzaCitta
        # esempio uso
        import distanzacitta

        # esempio uso
        import distanzacitta


        d = distanzacitta.distanzaTraCitta(verbose=False, shortDF = False)
        result, dist, tempo= d.distanzaNomeA2NomeB('Capriate San Gervasio', 'Capriate San Gervasio')
        result, dist, tempo= d.distanzaNomeA2NomeB('parabiago', 'milano')
        print("distanza [m]:" + str(dist) +" tempo di percorrenza [minuti]: " +str(tempo))


        file necessari:
            distanzeComuniLombardia.txt
            comuniLombardia.txt

        file origine:
            Elenco-comuni-italiani.csv
            Lombardia.txt
            vedi descrizione nelle funzioni estraiRegione() e estraiCampi()

        autore: giorgio323@gmail.com

        paesi non riconosciuti
        
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




        
    '''
    # apre i file e limette nei df
    def __init__(self, verbose = False, shortDF = False):

        self.verbose = verbose
        if self.verbose:
            print('df start loading, this may take longer than 30 seconds')        
        column_types= {'Origine': 'int32', 'Destinazione': 'int32', 'Total_Minu': 'int16', 'Total_Mete': 'int32'}
        if shortDF:        
            self.df = pd.read_csv('distanzeComuniLombardia.txt', delimiter=";", dtype=column_types, nrows=1000)
            print("loaded only 1000 rows of dataSet. 'shortDF' is set true")
        else:
            self.df = pd.read_csv('distanzeComuniLombardia.txt', delimiter=";", dtype=column_types)

        #cod;nome;provincia
        self.comuniLombardia = pd.read_csv('comuniLombardia.txt', delimiter=";", encoding='mbcs')
    
        if self.verbose:
            print('df loaded')


    def distanzaCodeAtoCodeB(self, _origine=16051, _destinazione=16029):
        if not _origine in self.df.values:
            print(str(_origine) + ' origine non esiste')
            result = -1
            return result, 0, 0

        if not _destinazione in self.df.values:
            print(str(_destinazione) + 'destinazione non esiste')
            result = -1
            return result, 0, 0


        item= self.df.loc[(self.df['Origine'] == _origine) & (self.df['Destinazione'] == _destinazione)]
        if self.verbose:
            print(item['Total_Mete'])
            print(item['Total_Minu'])
            
        return 0, item['Total_Mete'].values[0], item['Total_Minu'].values[0]


    def nome2codice(self, _nomeComune = 'PARABIAGO'):
        if _nomeComune in self.comuniLombardia.values:
            elemento= self.comuniLombardia[self.comuniLombardia['nome'] == _nomeComune][:]
            codice  = elemento['cod'].values[0]
            if self.verbose:
                print("nome, codice" + _nomeComune + str(codice))
        else:
            if self.verbose:
                print(_nomeComune + ' non esiste')
            codice = -1
        return codice

    def distanzaNomeA2NomeB(self, _nomeA, _nomeB):
        _nomeA = self.sanifica_nome(_nomeA)
        _nomeB = self.sanifica_nome(_nomeB)
    
        nomeCodiceA= self.nome2codice(_nomeA.upper())
        if self.verbose:
            print(nomeCodiceA)
        nomeCodiceB= self.nome2codice(_nomeB.upper())
        if self.verbose:
            print(nomeCodiceB)
            
        if (nomeCodiceA!=-1) and (nomeCodiceB != -1):
            _result, d, t = self.distanzaCodeAtoCodeB(nomeCodiceA, nomeCodiceB)
            return _result, d, t
        else:
            return -1, 0, 0

    # alcuni nomi nella matrice hanno un numero aggiunto in fondo
    # MILANO 1, MILANO 2 sino a 16, monza busto e altri
    # questa funzione rimuove il numero alla fine permettendo di trovarlo
    def sanifica_nome(self, nome):
        chars = "0123456789"
        for c in chars:
            nome = nome.replace(c, '')
        nome= nome.rstrip()
        return nome

    


    # funzioni usati per filtrare i file di origine e ottenerne di più piccoli
    # sono qui come copie.
    
    #http://www.notespoint.com/pandas-dataframe-chunks/
    # File di ingresso dal sito ISTAT
    # https://www.istat.it/storage/codici-unita-amministrative/Elenco-comuni-italiani.xls
    # genera un file con i comuni di una regione
    # rimossi leading zeros
    def estraiRegione():
        # Cod                 nome          prov   regione
        fileIn = open("Elenco-comuni-italiani.csv","r")
        fileOut= open("comuniLombardia.txt","w")

        fineFile = False

        #for i in range (0,10):
        while not fineFile:
            linea = fileIn.readline()
            if linea:
                linea = linea.replace("\n", "")
                field = linea.split(';')
                #print(field)
                if field[3] == "Lombardia":
                    lineaOut = str(int(float(field[0])))+";"+field[1].upper()+";"+field[2].upper()+"\n"
                    print(lineaOut)
                    fileOut.write(lineaOut)
            else:
                fineFile = True            

        fileIn.close() #to change file access modes
        fileOut.close() #to change file access modes


    # ISTAT Matrici di contiguità, distanza e pendolarismo
    # https://www.istat.it/it/archivio/157423
    # genera un file togliendo la stinga origine destinazione
    # codici, tempi, distanze stanno in 32 bit e il file dovrebbe stare in menmoria
    def estraiCampi():
        #0      1       2            3          4
        #Name   Origine Destinazione Total_Minu Total_Mete
        fileIn = open("Lombardia.txt","r")
        fileOut= open("distanzeComuniLombardia.txt","w")

        fineFile = False
        count = 0
        #for i in range (0,10):
        while not fineFile:
            linea = fileIn.readline()
            if linea:
                linea = linea.replace("\n", "")
                linea = linea.replace(",", ".") # numeri sono con virgola
                field = linea.split(';')
                #print(field)
                if count == 0:
                    lineaOut = field[1]+";"+field[2]+";"+field[3]+";"+field[4]+"\n"
                else:
                    lineaOut = ""
                    for j in range (1,4):
                        lineaOut += str(int(float(field[j]))) + ";"
                    lineaOut += str(int(float(field[4]))) + "\n"
                    
                #print(lineaOut)
                fileOut.write(lineaOut)
                count += 1
                if (count%1750)==0:
                    print(count)
            else:
                fineFile = True            

        fileIn.close() 
        fileOut.close()




    # funzioni di test e verifica uso memoria

    def testDistanzeLombardia():
        #https://vincentteyssier.medium.com/optimizing-the-size-of-a-pandas-dataframe-for-low-memory-environment-5f07db3d72e
        #Name   Origine Destinazione Total_Minu Total_Mete
        #distanzeLombardia = pd.read_csv('Lombardia.txt', delimiter=";", nrows=100)
        #distanzeLombardia = pd.read_csv('distanzeComuniLombardia.txt', delimiter=";")
        #print(distanzeLombardia.head())
        '''
        >>> distanzeLombardia.info()
     <class 'pandas.core.frame.DataFrame'>
        RangeIndex: 11256601 entries, 0 to 11256600
        Data columns (total 4 columns):
        Origine         int64
        Destinazione    int64
        Total_Minu      int64
        Total_Mete      int64
        dtypes: int64(4)
        memory usage: 343.5 MB
        '''


        '''
        df = pd.read_csv('distanzeComuniLombardia.txt', delimiter=";", nrows=10)
        df['Origine']=pd.to_numeric(df['Destinazione'], downcast='integer')
        df['Destinazione']=pd.to_numeric(df['Origine'], downcast='integer')
        df['Total_Minu']=pd.to_numeric(df['Total_Minu'], downcast='integer')
        df['Total_Mete']=pd.to_numeric(df['Total_Mete'], downcast='integer')

        # create the dict of index names and optimized datatypes
        dtypes = df.dtypes
        colnames = dtypes.index
        types = [i.name for i in dtypes.values]
        column_types = dict(zip(colnames, types))
        column_types= {'Origine': 'int16', 'Destinazione': 'int16', 'Total_Minu': 'int16', 'Total_Mete': 'int16'}

        RangeIndex: 11256601 entries, 0 to 11256600
        Data columns (total 4 columns):
        Origine         int16
        Destinazione    int16
        Total_Minu      int16
        Total_Mete      int16
        dtypes: int16(4)
        memory usage: 85.9 MB
        '''
        
        column_types= {'Origine': 'int16', 'Destinazione': 'int16', 'Total_Minu': 'int16', 'Total_Mete': 'int16'}
        distanzeLombardia = pd.read_csv('distanzeComuniLombardia.txt', delimiter=";", dtype=column_types)
        print(distanzeLombardia.info())
        
        
        #a=distanzeLombardia[distanzeLombardia['Name'] == '16051 - 15221'][:]
        #print (a)


    def testComuniItalia():
        comuniItalia = pd.read_csv('Elenco-comuni-italiani.csv', delimiter=";", encoding='mbcs')
        #print(comuniItalia)
        # Cod                 nome          prov   regione
        #comuniItalia.loc[:,"prov"]

        a=comuniItalia[comuniItalia['nome'] == 'Parabiago'][:]
        print (a)

        a=comuniItalia[comuniItalia['Cod'] == 16051][:]
        print (a)

