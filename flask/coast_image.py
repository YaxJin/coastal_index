class CoastImage:
    def __init__(self, time, location, imgName, result, GPS=None, desc=None):
        self.__time = time
        self.__location = location
        self.__imgName = imgName
        self.__result = result
        self.__GPS = GPS
        self.__desc = desc

    def getTimeStamp(self):
        return self.time
    
    def getLoaction(self):
        return self.location

    def getImgName(self):
        return self.imgName
    
    def getResult(self):
        return self.result

    def getGPS(self):
        return self.GPS

    def getDesc(self):
        return self.desc

    

    