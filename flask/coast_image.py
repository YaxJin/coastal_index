class CoastImage:
    def __init__(self, time, location, imgName, result={"score":0, "objects":None}, GPS=None, desc=None):
        self.__time = time
        self.__location = location
        self.__imgName = imgName
        self.__result = result
        self.__GPS = GPS
        self.__desc = desc
        self.__credibility = 1

    def getTimeStamp(self):
        return self.__time
    
    def getLoaction(self):
        return self.__location

    def getImgName(self):
        return self.__imgName
    
    def getResult(self):
        return self.__result

    def getGPS(self):
        return self.__GPS

    def getDesc(self):
        return self.__desc

    def getCredibility(self):
        return self.__credibility

    def setResult(self, newResult):
        self.__result = newResult

    def setScore(self, newScore):
        self.__result["score"] = newScore

    def setCredibility(self, newCredibility):
        self.__credibility = newCredibility
  