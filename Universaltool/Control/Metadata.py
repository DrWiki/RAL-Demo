import numpy as np
import pandas as pd
import threading
class metadata:
    # this is the metadata structure that need's
    def __init__(self):
        self.DataStreamT=[]
        self.DataStreamsudoT=[]
        self.NUM = -1
        self.trig = 0
        self.Silence = 0
        self.DataStreamX = []
        self.DataStreamY = []
        self.DataStreamZ = []
        self.DataStreamRX = []
        self.DataStreamRY = []
        self.DataStreamRZ = []
        self.DataStreamList = [self.DataStreamT,
                               self.DataStreamX,self.DataStreamY,self.DataStreamZ,
                               self.DataStreamRX,self.DataStreamRY,self.DataStreamRZ]
        self.filedataX = []
        self.filedataY = []
        self.filedataindexX = 0
        self.filedataindexY = 0

        self.CurrentdataX = 0
        self.CurrentdataY = 0
        self.CurrentdataZ = 0
        self.CurrentdataRX = 0
        self.CurrentdataRY = 0
        self.CurrentdataRZ = 0

        self.datareadyX = False
        self.datareadyY = False
        self.datareadyZ = False
        self.datareadyRX = False
        self.datareadyRY = False
        self.datareadyRZ = False

        # self.Maxnum = 1000

        # self.th = threading.Thread(target=self.autosaveandcut)
    #
    # def

    def save(self, path, mode = 'w'):
        for i in range(5):
            print(len(self.DataStreamList[i]))

        if mode=='w':
            list_res = {"T": self.DataStreamT, "X": self.DataStreamX, "Y": self.DataStreamY, "Z": self.DataStreamZ
                        , "RX": self.DataStreamRX}

        elif mode=="a":
            list_res = np.array([self.DataStreamT, self.DataStreamX, self.DataStreamY, self.DataStreamZ
                                    , self.DataStreamRX]).T

        xml_df = pd.DataFrame(list_res, index=None)
        xml_df.to_csv(path, index=None, mode=mode)
        print("OK")

    def fill(self):
        for i in range(10):
            self.DataStreamT.append(i)
            self.DataStreamX.append(i)
            self.DataStreamY.append(i)
            self.DataStreamZ.append(i)
            self.DataStreamRX.append(i)
            self.DataStreamRY.append(i)
            self.DataStreamRZ.append(i)

if __name__ == '__main__':
    D = metadata()
    D.fill()
    D.save("./1.csv", "a")
