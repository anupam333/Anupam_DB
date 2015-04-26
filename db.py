class db():
    def __init__(self):
        self.setDict = {"begin":0, 'commit':0, 'transct':{}}
        self.valVar = {}
        self.varOccur = {}
        self.rollBackArr = []
        self.unsetCounter = 0
    
    def getTracDict(self):
        return {'value':[], 'name':''}
    
    def setValues(self,val,name):
            
        if str(val) not in self.valVar.keys() and name not in self.varOccur.keys(): #If the value does not exists and variable as either
            self.valVar[str(val)] = [name]
            self.varOccur[name] = str(val)
            
        elif name in self.varOccur.keys() and str(val) in self.valVar.keys(): #If variable exists
            oldVal = self.varOccur[name]
            self.valVar[oldVal].remove(name) #Remove the old value
            self.varOccur[name] = str(val) #Insert the new value
            self.valVar[str(val)].append(name)
            
        elif name not in self.varOccur.keys() and str(val) in self.valVar.keys():
            self.valVar[str(val)].append(name)
            self.varOccur[name] = str(val)
            
        elif name in self.varOccur.keys() and str(val) not in self.valVar.keys():
            oldVal = self.varOccur[name]
            del self.varOccur[name]
            self.valVar[oldVal].remove(name)
            self.valVar[str(val)] = [name]
            self.varOccur[name] = str(val)
            
                    
                            
            
        if len(self.setDict['transct'].keys()) == 0: #If no such variable exists, brand new start
            self.setDict['transct'][name] = [val]
            
            
        else: 
            
            if name in self.setDict['transct'].keys():  #If such a variable exists
                if self.setDict['begin'] == 1: #We need to remember only transaction has a 'Begin'
                    self.setDict['transct'][name].append(val)
                else:
                    self.setDict['transct'][name] = [val]
            else:
                self.setDict['transct'][name] = [val]   # If no such variable exists
                
        if self.setDict['begin'] == 1:  #serialize it
            self.rollBackArr.append({'set': name})
                
    def getValues(self,name):
        if self.setDict['begin'] == 0:
            if name in self.setDict['transct'].keys():
                return self.setDict['transct'][name][-1]
            else:
                return 'NULL'
        else:
            if name in self.setDict['transct'].keys():#After rollbacks till all variables are gone
                if self.setDict['transct'][name][-1] == ')(*&^%$#@!unset!@#$%^&*()':
                    
                    return 'NULL'
                else:
                    return self.setDict['transct'][name][-1]
            else:
                return 'NULL'
                
        
        
                
    def getnumequalto(self, val):
        #self.valVar = {}
        #self.varOccur = {}
        if str(val) in self.valVar.keys():
            
            return len(self.valVar[str(val)]) - self.unsetCounter
        else:
            return 0
        
    def unset(self, name):
        if self.setDict['begin'] == 0:
            val = self.setDict['transct'][name][-1]
            del self.setDict['transct'][name]
            self.reduceCounter(val, name)
        else:
            self.setDict['transct'][name].append(')(*&^%$#@!unset!@#$%^&*()')
            self.rollBackArr.append({'unset': name})
            
            
            self.unsetCounter += 1 #this number will used to subtract from numequalto
            
    def reduceCounter(self, val, name):
        del self.varOccur[name]
        if len(self.valVar[str(val)]) > 1:
            self.valVar[str(val)].remove(name)
        else:
            del self.valVar[str(val)]
            
        
    def rollback(self):
        if self.setDict['begin'] == 0:
            print "Incorrect input"
            return
        if self.setDict['commit'] == 0 and len(self.rollBackArr) > 0:
            transactionDict = self.rollBackArr[-1]
            type = transactionDict.keys()[0]
            name = transactionDict[type]
            
            
            if self.setDict['transct'][name][-1] == ')(*&^%$#@!unset!@#$%^&*()':
                self.unsetCounter  = self.unsetCounter-1
            
            if len(self.setDict['transct'][name]) == 1:
                val = self.setDict['transct'][name].pop()
                del self.setDict['transct'][name]
                self.rollBackArr.pop()
            else:
                val = self.setDict['transct'][name].pop()
                self.rollBackArr.pop()
            if name == 'set':
                self.reduceCounter(val,name)
                
        elif len(self.rollBackArr) == 0:
            print "No transactions"
            
        elif self.setDict['commit'] == 0:
            print "Transaction has been committed and cannot be rolled back"
            


    def commit(self):
        self.setDict['commit'] = 1
        self.rollBackArr = []
        for name in self.setDict['transct']:
            finalVal = self.setDict['transct'][name][-1]
            self.setDict['transct'][name] = [finalVal]
        
            

    
    
def main():
    try:
        DB = db()
        exit = False
        while exit == False:
            ip = raw_input().rstrip()
            ipArr = ip.split(" ")
            if ip.lower() == 'end':
                print 'Bye'
                exit = True
                
            elif ip[:3].lower() == 'set':
                if len(ipArr) != 3:
                    print 'Incorrect input'
                    continue
                DB.setValues(ipArr[2], ipArr[1])
                
            elif ip[:10].lower() == 'numequalto':
                if len(ipArr) != 2:
                    print 'Incorrect input'
                    continue
                print DB.getnumequalto(ipArr[1])
                
            elif ip[:3].lower() == 'get':
                if len(ipArr) != 2:
                    print 'Incorrect input'
                    continue
                print DB.getValues(ipArr[1]) 
                
            elif ip[:5].lower() == 'unset':
                if len(ipArr) != 2:
                    print 'Incorrect input'
                    continue
                DB.unset(ipArr[1])
                
            elif ip[:5].lower() == 'begin':
                if len(ipArr) != 1:
                    print 'Incorrect input'
                    continue
                DB.setDict['begin'] = 1
                DB.setDict['commit'] = 0
                
            elif ip[:8].lower() == 'rollback':
                if len(ipArr) != 1:
                    print 'Incorrect input'
                    continue
                DB.rollback()
                
            elif ip[:6].lower() == 'commit':
                if len(ipArr) != 1:
                    print 'Incorrect input'
                    continue
                DB.commit() 
                           
            else:
                print 'Incorrect input'
    except EOFError:
        print 'We reached end of File'
    
    
if __name__ == "__main__":
    main()
    