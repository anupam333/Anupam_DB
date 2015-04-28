class db():

    def __init__(self):
        self.setDict = {"begin": 0, 'commit': 0, 'transct': {}}
        self.valVar = {}
        self.varOccur = {}
        self.rollBackArr = []

    def getTracDict(self):
        return {'value': [], 'name': ''}

    def setValues(self, val, name):
        # If the value does not exists and variable as either
        if str(val) not in self.valVar.keys() and name not in self.varOccur.keys():
            self.valVar[str(val)] = [name]
            self.varOccur[name] = str(val)

        # If variable exists

        elif name in self.varOccur.keys() and str(val) in self.valVar.keys():
            oldVal = self.varOccur[name]
            self.valVar[str(oldVal)].remove(name)  # Remove the old value
            self.varOccur[name] = str(val)  # Insert the new value
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

        # If no such variable exists, brand new start
        if len(self.setDict['transct'].keys()) == 0:
            self.setDict['transct'][name] = [val]

        else:

            # If such a variable exists
            if name in self.setDict['transct'].keys():
                # We need to remember only transaction has a 'Begin'
                if self.setDict['begin'] == 1:
                    # Reduce unset dict value
                    if self.setDict['transct'][name][-1] == 'unset':
                        pass

                    self.setDict['transct'][name].append(val)
                else:
                    self.setDict['transct'][name] = [val]
            else:
                # If no such variable exists
                self.setDict['transct'][name] = [val]

        # print "At set values:  ", self.valVar

        if self.setDict['begin'] == 1:  # serialize it
            self.rollBackArr.append({'set': name})
        # print "At set values again: ", self.setDict

    def getValues(self, name):
        if self.setDict['begin'] == 0:
            if name in self.setDict['transct'].keys():
                return self.setDict['transct'][name][-1]
            else:
                return 'NULL'
        else:
            # After rollbacks till all variables are gone
            if name in self.setDict['transct'].keys():
                if self.setDict['transct'][name][-1] == 'unset':
                    return 'NULL'
                else:
                    return self.setDict['transct'][name][-1]
            else:
                return 'NULL'

    def getnumequalto(self, val):
        if str(val) in self.valVar.keys():
            return len(self.valVar[str(val)])

        else:
            return 0

    def unset(self, name):
        if name in self.setDict['transct'].keys():
            if self.setDict['begin'] == 0:
                val = self.setDict['transct'][name][-1]
                del self.setDict['transct'][name]
                self.reduceCounter(val, name)
            else:
                # don't want to unset already unsetted variable
                if self.setDict['transct'][name][-1] != 'unset':
                    self.setDict['transct'][name].append(
                        'unset')
                    self.rollBackArr.append({'unset': name})
                    # this number will used to subtract from numequalto
                    # get the value of the variable
                    varVal = self.varOccur[name]

                    #self.unsetCounter += 1
                    self.reduceCounter(varVal, name)

        else:
            print "No such value exists"

    def reduceCounter(self, val, name):
        del self.varOccur[name]
        #self.unsetCounter += 1
        if len(self.valVar[str(val)]) > 1:
            self.valVar[str(val)].remove(name)
        else:
            del self.valVar[str(val)]

    def rollback(self):
        #         print 'rollback', self.rollBackArr
        #         print 'valVar', self.valVar
        #         print 'setdict', self.setDict
        #         print 'varoccur', self.varOccur
        if self.setDict['begin'] == 0:
            print "Incorrect input"
            return
        if self.setDict['commit'] == 0 and len(self.rollBackArr) > 0:
            transactionDict = self.rollBackArr[-1]
            type = transactionDict.keys()[0]
            name = transactionDict[type]
            if len(self.setDict['transct'][name]) == 1:
                val = self.setDict['transct'][name].pop()
                del self.setDict['transct'][name]
                self.rollBackArr.pop()
            else:
                val = self.setDict['transct'][name].pop()
                self.rollBackArr.pop()

            if type == 'set':
                self.reduceCounter(val, name)

        elif len(self.rollBackArr) == 0:
            print "No transactions"
        elif self.setDict['commit'] == 0:
            print "Transaction has been committed and cannot be rolled back"

        # set self.valVar array again
        self.valVar = {}
        self.varOccur = {}
        for x in self.setDict['transct'].keys():
            valArray = self.setDict['transct'][x]
            self.varOccur[x] = valArray[-1]
            if valArray[-1] != 'unset':
                if valArray[-1] in self.valVar.keys():
                    self.valVar[str(valArray[-1])].append(x)
                else:
                    self.valVar[str(valArray[-1])] = [x]
        # set varoccur array again

    def commit(self):
        self.setDict['commit'] = 1
        #self.unsetCounter = 0
        self.rollBackArr = []
        delArray = []
        for name in self.setDict['transct']:
            finalVal = self.setDict['transct'][name][-1]
            if finalVal == 'unset':
                delArray.append(name)
            else:
                self.setDict['transct'][name] = [finalVal]
        for name in delArray:
            del self.setDict['transct'][name]
        self.setDict['begin'] = 0


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
                # DB.commit()
                DB.setDict['begin'] = 1
                DB.setDict['commit'] = 0

            elif ip[:8].lower() == 'rollback':
                if len(ipArr) != 1:
                    print 'Incorrect input'
                    continue
                DB.rollback()

            elif ip[:6].lower() == 'commit':
                if len(ipArr) != 1 or DB.setDict['begin'] != 1:
                    print 'Incorrect input'
                    continue
                DB.commit()
            else:
                print 'Incorrect input'
    except EOFError:
        print 'We reached end of File'


if __name__ == "__main__":
    main()
