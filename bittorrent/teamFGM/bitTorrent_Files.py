__author__ = 'maurizio'

import re

class FileHandler():

    FileTable=[]

    def getFileTable(self):
        return self.FileTable

    def setFileTable(self,FileTable):
        self.FileTable = FileTable

    def rowSetting(self,PartNum):
        """
        This method Set the row of FileTable, specifying the PartList
        """
        FileTable = self.getFileTable()
        dim = len(FileTable)

        self.Peer = FileTable[dim-1][0]
        print "I'm handling the peer with SessionID " + Peer
        self.PartList = FileTable[dim-1][1]
        
        

    def createRow(self,SessionID,LenFile,LenPart):
        """
        This method create a row for FileTable, composed by SessionID|PartList for tracing the file's parts for any peer
        """
        FileTable = self.getFileTable()

        print FileTable

        row = []
        row.append(SessionID) #aggiungo il SessionID come primo elemento della FileTable
        PartList = []
        NewByte = '00000000'
        numOfByte=LenFile/LenPart #mi calcolo la divisione intera, cioè la parte intera inferiore
        if LenFile%LenPart != 0: #valuto se la divisione è perfetta oppure se c'e' del resto
            numOfByte = numOfByte + 1 #se c'e' il resto, allora aggiungo un byte
        for i in numOfByte-1:
            PartList.append(NewByte) #creo la PartList con N byte (ognuno con 8 bit a 0) -> PartList=Byte0|Byte1|Byte2...
        row.append(PartList) #inserisco la PartList alla FileTable -> ora ho SessionID|PartList

        FileTable.append(row)

        self.setFileTable(FileTable)


    def newEntry(self,SessionID,LenFile,LenPart,FileTable):
        """
        This method create a new FileTable's entry, when a peer add a NEW FILE -> the PartList are all-1
        """
        self.createRow(SessionID,LenFile,LenPart) #inizialmente creo la nuova riga
        self.getFileTable()

        print FileTable
        
        dim = len(FileTable)

        PartList = FileTable[dim-1][1]

        print PartList #TODO debug


        FirstBitToSet = ((LenFile/LenPart)-1)*8 #estrapolo i primi byte (gruppi di 8 bit) che posso settare a 1
        i1 = 0
        while i1 < FirstBitToSet :
            PartList[i1]= '1'
            i1 = i1 + 1

        if LenFile%LenPart == 0 :
            UpperBound = (LenFile/LenPart)*8
        else :
            UpperBound = ((LenFile/LenPart)+1)*8
        LastBitToSet = UpperBound - LenPart%8
        i1 = LastBitToSet
        while i1 < UpperBound :
            PartList[i1] = '1'
            i1 = i1 + 1

        FileTable[dim-1][1]=PartList #sovrascrivo la PartList
        self.setFileTable()





