__author__ = 'GuiducciGrillandaLoPiccolo'

from bitarray import bitarray

class FileHandler():

    def __init__(self):
        self.fileTable = [] #sessionID + partList

    def getFileTable(self):
        return self.fileTable

    def setFileTable(self,fileTable):
        self.fileTable = fileTable


    def newTable(self,sessionID,lenFile,lenPart):
        """
        This method create a new fileTable's entry, when a peer add a NEW FILE
        Poi setta a 1 tutte le parti della prima riga (il peer e' la sorgente)
        """

        #creo la tabella e valorizzo la prima riga (corrisponde al peer sorgente per quel file)

        fileTable = self.getFileTable()

        row = []
        row.append(sessionID) #aggiungo il sessionID come primo elemento della fileTable
        partList = []
        numParts = lenFile/lenPart #calcolo il numero delle parti
        numByteDifetto = numParts/8 #approssimazione per difetto del numero dei byte da utilizzare
        for i in range(0,numByteDifetto):
            partList.append('11111111') #creo la partList con N byte (ognuno con 8 bit a 1)
        if numParts % 8 != 0: #se c'e' resto nella divisione
            offset = numParts % 8 #offset di bit che andranno messi a 1 nell'ultimo byte
            partList.append('0' * (8-offset) + '1' * offset )
        row.append(partList) #inserisco la partList alla fileTable -> ora ho sessionID|partList
        fileTable.append(row)

        self.setFileTable(fileTable)

        return numParts #restituisco il numero delle parti per quel particolare file


    def updateTable(self,sessionID,numpart_to_update,filetable_to_update):
        """
        This method Set the row of fileTable, specifying the partList
        """

        self.setFileTable(filetable_to_update)

        fileTable = self.getFileTable()

        dim_partList = len(fileTable[0][1])

        #controllo se sessionID gia' presente nella tabella
        found = False
        for i in range(0,len(fileTable)):
            if sessionID == fileTable[i][0]:
                index = i
                found = True

        if found == False:

            row = []
            row.append(sessionID) #aggiungo il sessionID come elemento della fileTable
            partList = []
            newByte = '00000000'
            for i in range(0,dim_partList):
                partList.append(newByte) #creo la partList con N byte (ognuno con 8 bit a 0) -> partList=Byte0|Byte1|Byte2...
            row.append(partList) #inserisco la partList alla fileTable -> ora ho sessionID|partList
            fileTable.append(row)
            index = len(fileTable)-1

        #in ogni caso aggiorno gli uni
        partList = fileTable[index][1]

        numByte = numpart_to_update / 8

        offset = numpart_to_update % 8

        byte = partList[numByte]
        new_byte = ""
        for i in range(0,len(byte)):
            if i != 8-offset:
                new_byte += byte[i]
            else:
                new_byte += '1'
        partList[numByte] = new_byte

        self.setFileTable(fileTable)

        #devo contare quante parti ha il peer di quel file
        #in pratica devo contare gli 1 in quella riga
        cont = 0
        for i in range(0,len(partList)):
            for j in range(0,8):
                if partList[i][j] == '1':
                    cont += 1

        return cont #restituisco il numero di parti che questo peer possiede di questo file

    def tryLogout(self,filetable_to_update):

        self.setFileTable(filetable_to_update)

        fileTable = self.getFileTable()

        #tento la cancellazione
        #per poter cancellare il peer dalla tabella deve essere che almeno uno degli altri peer abbia un 1 per ogni 1 della sorgente
        cont = 0
        canlogout = True
        sorgente = fileTable[0][1]

        for j in range(len(fileTable[0][1])): #j = indice byte
            for k in range(0,8): #k = indice del bit
                bit_ok=False
                for i in range(1,len(fileTable)): #i = indice della riga
                    if fileTable[i][1][j][k] == sorgente[j][k]: #se bit sono uguali, posso passare ad esaminare il bit successivo
                        bit_ok=True #questo bit e' soddisfatto
                if bit_ok==False:
                    canlogout=False #questo bit non e' soddisfatto, quindi non posso fare logout
                if bit_ok and sorgente[j][k] == '1':
                    cont += 1


        if canlogout == True: #se mi posso sloggare

            fileTable.pop(0) #elimino l'elemento 0 (peer sorgente)
            self.setFileTable(fileTable) #aggiorno la tabella, altrimenti non ce n'e' bisogno visto che non l'ho modificata

        to_return = []
        to_return.append(canlogout)
        to_return.append(cont)

        return to_return

    def deleteParts(self,sessionID, filetable_to_update):

        self.setFileTable(filetable_to_update)

        fileTable = self.getFileTable()

        k=0
        pop=False
        cont = 0
        while k < len(fileTable):

            if fileTable[k][0] == sessionID:

                partList = fileTable[k][1]

                #conto quanti 1 nella riga del peer
                for i in range(0,len(partList)):
                    for j in range(0,8):
                        if partList[i][j] == '1':
                            cont += 1

                fileTable.pop(k) #elimino la riga

                self.setFileTable(fileTable) #visto che ho fatto pop aggiorno la tabella

                pop=True

            else:

                k += 1

        to_return = []
        to_return.append(pop)
        to_return.append(cont)

        return to_return

    def fetchstring(self,randomID,filetable,peersdb):

        #peersdb = sessionID, IP, port

        numhitpeer = 0
        to_send = ""

        self.setFileTable(filetable)

        filetable = self.getFileTable()

        for i in range(0,len(filetable)):
            numhitpeer += 1
            sessionID = filetable[i][0]
            print sessionID
            #dal sessionID recupero ip e porta dalla peersdb
            for j in range(0,len(peersdb)):
                if peersdb[j][0] == sessionID:
                    ipp2p = peersdb[j][1]
                    pp2p = peersdb[j][2]
            to_send += ipp2p + pp2p #intanto scrivo ip e porta

            partlist = filetable[i][1]
            print partlist
            #devo trasformare partlist in una successione di 0 e 1
            for k in range(0,len(partlist)):
                ba = bitarray(partlist[k]) #dalla stringa ricavo l'oggetto bitarray
                to_send += ba.tobytes() #scrivo gli 8 bit come un singolo byte

        numhitpeer_form = '%(#)03d' % {"#" : int(numhitpeer)} #numhitpeer formattata per bene

        total = numhitpeer_form + to_send

        print total

        return total