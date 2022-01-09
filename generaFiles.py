# funzioni usati per filtrare i file di origine e ottenerne di più piccoli
# procedura:
# scarica
#   https://www.istat.it/storage/codici-unita-amministrative/Elenco-comuni-italiani.xls
#   https://www.istat.it/it/archivio/157423
# mettili nello stesso folder dove si trova questo script e se necessario unzippali.
# esegui python generaFiles.py
# nel terminale iniziano a scorrere i dati trattati. Il processo pernde qualche minuto.
# vengono generati due file:
#   comuniLombardia.txt
#   distanzeComuniLombardia.txt
#
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
            if (count%10000)==0:
                print(count)
        else:
            fineFile = True            

    fileIn.close() 
    fileOut.close()


estraiRegione()
estraiCampi()
