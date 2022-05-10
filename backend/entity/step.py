class Step:
    def __init__(self, functionName, paramOne, paramTwo, length):
        self.functionName = functionName
        self.paramOne = paramOne
        self.paramTwo = paramTwo
        self.length = length
    
    def functionName(self):
        return self._functionName

    def paramOne(self):
        return self._paramOne

    def paramTwo(self):
        return self._paramTwo
    
    def length(self):
        return self._length