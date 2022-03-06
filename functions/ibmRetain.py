# import ibmPCommTLS
# import readConfig
from functions import ibmPCommTLS
import tkinter as tk
from tkinter import *
from functions import readConfig


# IBM's Remote Technical Assistance Information Network (RETAIN)
class retain(ibmPCommTLS.x3270):
    def __init__(self, host, backupHost, retainID, passwd):
        self.host = host
        self.backupHost = backupHost
        self.retainID = retainID
        self.passwd = passwd
        self.pmhNo = ''

        self.txtFromGui = ''

        # need get strings from "PROF" command
        # 7, 21, 20 strip()
        self.userID = ''
        # 1, 21, 30 strip()
        self.userName = ''
        self.userTele = ''

        self.ctryNo = '672'
        self.ctryCode = '80K'
        self.brNo = ['000', '117', '175', '174', '124', '123']

        self.locQueues = ['SSRSC', 'SSRGZ', 'SSRSW', 'SSREC',
                         'SSRSH', 'SSRCC', 'SSRZJ', 'SSRNC',
                         'SSRBJ', 'SSRNE', 'SSRNW', 'SSRI', 'SSRZ']
        self.locQueue = ''
        self.tsgQueue = ['ESTSG', 'ASTSG', 'TSGPWR', 'TSGSTR', 'APNGPH', 'HCSTR']
        # self.tsgQueue = ''
        self.noQueue = 'NOCH'
        self.proStat = ['CLOSE', 'OPEN']
        # zSeries: estsg, 80K   | # iSeries: astsg,80K
        # pSeries: tsgpwr, 80K  | # Storage: tsgstr,80K
        # PureFlex: apngph, 80K | # Storage Health Check: HCSTR,80K

        self.srchArgsDict = {}
        self.ceArgsDict = {}
        self.txtFmtCode = {'POWER': '5012',
                           'DS345K': '1724',
                           'V7K': '5258',
                           'DS8K': '1794'}

        ibmPCommTLS.x3270.__init__(self, self.host, self.backupHost)
        self.pages = {'ACDN': 'First page after connected.',
                      # 24, 1, 4

                      'RESPOND': 'RETAIN login interface.',
                      # 12, 20, 7

                      '==>': 'Page after login.',
                      # 23, 2, 3

                      'CMD==>': 'PMH Interface.',
                      # 22, 2, 6

                      'ENDED': 'SESSION ENDED AT APPLICATION REQUEST'
                      # 2, 11, 5
                      }

    def currPageType(self):
        keyword = ''
        if self.getString(24, 1, 4) == 'ACDN':
            keyword = 'ACDN'
        elif self.getString(12, 20, 7) == 'RESPOND':
            keyword = 'RESPOND'
        elif self.getString(23, 2, 3) == '==>':
            keyword = '==>'
        elif self.getString(22, 2, 6) == 'CMD==>':
            keyword = 'CMD==>'
        elif self.getString(2, 11, 5) == 'ENDED':
            keyword = 'ENDED'
        if keyword:
            return self.pages[keyword]
        else:
            return ''

    def login2PMH(self):
        if not self.isConnected():
            self.connect()
        if not self.isConnected():
            ibmPCommTLS.debugPrint('Host {} connected failed, '
                                   'try to backup host {}.'
                                   .format(self.host, self.backupHost))
            self.connect(backup=True)
        if not self.isConnected():
            ibmPCommTLS.debugPrint('Both hosts connect failed, '
                                   'check network.', color='red')
            return False
        if self.currPageType() == self.pages['ACDN']:
            self.sendString(23, 1, 'RETAINP')
            self.sendEnter()
            if self.currPageType() == self.pages['RESPOND']:
                self.sendString(11, 7, self.retainID + '/' + self.passwd)
                self.sendEnter()
                # Get out from News page.
                self.sendPf(1)
                if self.currPageType() == self.pages['==>']:
                    self.sendString(23, 6, 'PMH')
                    self.sendEnter()
                    if self.currPageType() == self.pages['CMD==>']:
                        return True
        elif self.currPageType() == self.pages['==>']:
            # ibmPCommTLS.debugPrint('Already login, enter PMH page.')
            self.sendString(23, 6, 'PMH')
            self.sendEnter()
            if self.currPageType() == self.pages['CMD==>']:
                return True
        elif self.currPageType() == self.pages['CMD==>']:
            # ibmPCommTLS.debugPrint('Already in PMH page.')
            return True
        elif self.currPageType() == self.pages['ENDED']:
            ibmPCommTLS.debugPrint('Session ended for timeout.', color='red')
            self.disconnect()
            self.login2PMH()
        else:
            ibmPCommTLS.debugPrint('Unknown page, try "PA1" back to main menu!', color='red')
            self.sendPA(1)
            if self.currPageType() == self.pages['==>']:
                self.sendString(23, 6, 'PMH')
                self.sendEnter()
                if self.currPageType() == self.pages['CMD==>']:
                    return True
            else:
                ibmPCommTLS.debugPrint('Cannot return main menu, login remain failed.')
                return False

    def lostPasswd(self):
        """
        userid/LOST <ENTER> If you have forgotten your password. When the LOST
        Command is entered, your password will be sent to the userid/node as defined
        in your RETAIN registration record which is typically set to be the same as
        Userid/Node or Userid/Alternate Node as listed in BluePages.
        :return:
        """
        pass

    def changePasswd(self):
        """
        userid/curpwd-CHANGE/newpwd/ <ENTER> To change your password if
        this is the first time logging on to RETAIN, or if your password has
        expired, or if you have forgotten your password and have entered the LOST
        Command. Your password is required to be 8 characters in length and is your
        own choice. The password you choose is checked and if valid, you will be
        prompted to reenter it for verification.
        :return:
        """
        pass

    def getUserProf(self):
        """
        send string 'prof' (User Profile Facilit)
        PROF01     Name:  ZHANG, ZHI JIE
        RETAIN ID:  149715     Password last updated 20/08/23 (044 days ago)
        Employee Number:  AVR71D
        VM Node ID:       IBMCN
        VM User ID:       ZHIJIEZG
        Country Number:   672
        RETAIN Location:  000                  data fields, contact
        Telephone:        18193120005
        """
        if not self.login2PMH():
            self.login2PMH()

        self.sendPA(1)
        self.sendString(23, 6, 'PROF')
        self.sendEnter()
        self.userName = self.getString(1, 21, 20).strip().replace(',', '')
        self.userID = self.getString(7, 21, 20).strip()
        self.userTele = self.getString(21, 21, 11)
        self.sendPf(1)
        self.sendString(23, 6, 'PMH')
        self.sendEnter()

    def displayProfile(self, retainID='', prtText=True, modify=False):
        userProfile = []

        if not self.login2PMH():
            self.login2PMH()

        self.sendString(22, 9, 'DR ' + retainID)
        self.sendEnter()
        for row in range(1, 21):
            userProfile.append(self.getString(row, 2, 79))
        if prtText:
            for dr in userProfile:
                print(dr)
        if modify:
            # your mobile phone
            self.sendPf(3)
            ibmPCommTLS.debugPrint('Case insensitive.', color='yellow')
            # 14 --> 2
            if input('{}: {}, Modify or not (NO/yes)? '
                             .format('TEL', self.getString(2, 2, 18).strip('_'))).upper() == 'YES':
                self.sendString(2, 2, input('New Value: '))
            # should be 'IBM'
            if input('{}: {}, Modify or not (NO/yes)? '
                             .format('TERR', self.getString(1, 55, 3))).upper() == 'YES':
                self.sendString(1, 55, input('New Value: '))
            # should be '50K'
            if input('{}: {}, Modify or not (NO/yes)? '
                             .format('SCTR', self.getString(2, 55, 3))).upper() == 'YES':
                self.sendString(2, 55, input('New Value: '))
            # should be '80K'
            if input('{}: {}, Modify or not (NO/yes)? '
                             .format('HCTR', self.getString(3, 55, 3))).upper() == 'YES':
                self.sendString(3, 55, input('New Value: '))
            if input('{}: {}, Modify or not (NO/yes)? '
                             .format('OTHTER B/O', self.getString(3, 33, 3))).upper() == 'YES':
                self.sendString(3, 33, input('New Value: '))
            """
            # 'SUPPORT LEVEL': '3, 2, 1',
            # 'NLS': '5, 2, 1',
            # 'SURVEY OPTIONAL': '4, 30, 1',
            # 'ETR ID': '5, 30, 1',
            # 'PRIMARY QUEUES ONLY': '7, 4, 1',
            # 'ALL QUEUES': '8, 4, 1',
            # 'AUTO DISPATCH': '7, 35, 1',
            # 'NORMAL UNSOLS': '8, 25, 1',
            """
            for row in range(11, 21):
                if input('{}: {}, Modify or not (NO/yes)? '
                                 .format('PRIMARY', self.getString(row, 6, 6).strip('_'))).upper() == 'YES':
                    self.sendString(row, 6, input('New Value: '))
            # for debug
            ibmPCommTLS.debugPrint('Screen with new values: \n', color='cyan')
            self.printCurrScreen()
            prompt = input('Type word "ENTER" to save changes, or any key to cancel: ').upper()
            if prompt == 'ENTER':
                ibmPCommTLS.debugPrint('Changes applied.')
                self.sendEnter()
            else:
                ibmPCommTLS.debugPrint('Changes canceled!')
                self.sendPf(1)

        return userProfile

    # For Create PMH
    def callEntry(self, custNo, locQueue, machType, machMod, machSN,
                  priority='3', severity='3', sysDown=False, rcmsCallNo=''):
        PMHNo = ''
        brNo = self.brNo[0]
        if not self.login2PMH():
            self.login2PMH()

        ibmPCommTLS.debugPrint('Create Call for Machine: {}'.format(machType, machMod, machSN))
        self.getUserProf()
        self.sendString(22, 9, 'CE')
        self.sendEnter()
        self.sendString(1, 2, custNo[0:7])
        self.sendString(4, 2, locQueue[0:6])
        self.sendString(4, 9, self.ctryCode[0:3])
        self.sendString(4, 13, priority[0:1])
        self.sendString(4, 19, severity[0:1])
        self.sendString(5, 2, machType[0:4] + machMod[0:3] + '/' + machSN[0:7])
        self.sendString(6, 2, machType[0:4])
        self.sendString(6, 7, machSN[0:7])
        self.sendString(6, 15, self.ctryNo[0:3])
        self.sendString(6, 19, brNo)
        self.sendString(7, 2, self.userID + '@cn.ibm.com')
        self.sendString(7, 44, self.userTele)
        if sysDown:
            self.sendString(11, 57, 'Y')
        self.sendString(9, 2, input('Type Comments for this PMH(54 letters limited.): \n'))
        self.printCurrScreen()
        prompt = input('Confirm (YES/no): ').upper()
        if prompt== 'N' or prompt == 'NO':
            self.sendPf(1)
            return PMHNo
        self.sendEnter()
        # Add Queue full process
        self.sendEnter()
        self.sendEnter()
        PMHNo = self.getString(1, 38, 13)
        self.printCurrScreen()
        print('Describe your problem briefly (end with "EOF"): ')
        briefDesc = []
        while True:
            descLine = input()
            if descLine.upper() == 'EOF':
                break
            if descLine == '':
                descLine = '.'
            briefDesc.append(descLine)

        for bd in briefDesc:
            if len(bd) > 70:
                tmpIndex = briefDesc.index(bd)
                briefDesc.insert(tmpIndex, bd[0:71])
                briefDesc[tmpIndex] = bd[71:-1]
        self.printCurrScreen()

        for bd in briefDesc:
            self.sendString(6, 2, bd)
            self.sendEnter()
        self.sendPf(11)
        for row in range(14, 20):
            print(self.getString(row, 2, 50))
        self.sendPf(1)
        print('Created PMH No.: {}'.format(PMHNo))
        self.pmhNo = PMHNo
        return PMHNo

    # Not used, can deleted.
    def typeOfCEArgs(self, ceArgs, locQueue):
        machType = ''
        machSN = ''
        machMod = ''
        custNo = ''
        try:
            machDetail = ceArgs.split()
            print(machDetail)
            machType = machDetail[1]
            machSN = machDetail[3] + machDetail[4].replace('00', '', 1)
            machMod = machDetail[2]
            custNo = machDetail[5].replace('00', '0', 1)
            print(custNo)
        except IndexError:
            ibmPCommTLS.debugPrint('Get Machine Information Error! Try another SN.', color='red')

        if locQueue not in self.locQueues:
            ibmPCommTLS.debugPrint('Local Q not correct, set to "SSRBJ"')
            locQueue = 'SSRBJ'
            self.locQueue = locQueue

        # for IPS machine, customer name is necessary
        custName = ''
        # default pri&srv, system not down.
        priority = '3'
        severity = '3'
        sysDown = False

        prompt = input('Is System Down (No/yes)?').upper()
        if prompt == 'Y' or prompt == 'YES':
            sysDown = True

        prompt = input('Priority (Default 3): ')
        try:
            int(prompt)
        except ValueError:
            ibmPCommTLS.debugPrint('Input Error, set "3" as default.')
        else:
            if prompt:
                priority = prompt

        prompt = input('Severity (Default 3): ')
        try:
            int(prompt)
        except ValueError:
            ibmPCommTLS.debugPrint('Input Error, set "3" as default.')
        else:
            if prompt:
                severity = prompt

        print(machType, machMod, machSN, custNo, locQueue, sysDown, priority, severity)

        if not self.login2PMH():
            self.login2PMH()

        """
        for args in ceArgs:
            args = args.upper()
            if args in self.locQueues and not locQueue:
                locQueue = args
                continue
            if len(args) == 4:
                if self.srchProd(args) and not machType:
                    machType = args
                    continue
            if len(args) == 7 and not args.startswith('0'):
                if self.srchProd(args) and not machSN:
                    machSN = args
                    continue
        """

        # Get Machine Model, Cust name, Cust No.
        """
        self.sendString(22, 9, 'U: ' + machType + ' ' + machSN)
        self.sendEnter()
        if self.getString(6, 15, 2) + self.getString(6, 18, 5) == machSN:
            self.sendString(22, 9, '1')
            self.sendEnter()
        else:
            print('Result SN does match what your input! Show 1st screen, pls check.')
            for row in range(6, 21):
                rowData = self.getString(row, 5, 62)
                if rowData:
                    print(rowData)
        custNo = self.getString(1, 2, 7)
        custName = self.getString(1, 11, 36).rstrip('_')
        machMod = self.getString(5, 19, 3)
        """
        self.sendString(22, 9, 'C: ' + custNo)
        self.sendEnter()
        self.sendStringDirectly('1')
        self.sendEnter()
        custName = self.getString(1, 11, 35).rstrip('_')

        self.ceArgsDict = {'custNo': custNo, 'custName': custName, 'locQueue': locQueue,
                           'machType': machType, 'machSN': machSN, 'machMod': machMod,
                           'sysDown': sysDown, 'priority': priority, 'severity': severity}
        return self.ceArgsDict

    def callEntryPlus(self, ceArgs, locQueue):
        machType = ''
        machSN = ''
        machMod = ''
        custNo = ''
        try:
            machDetail = ceArgs.split()
            machType = machDetail[1]
            machSN = machDetail[3] + machDetail[4].replace('00', '', 1)
            machMod = machDetail[2]
            custNo = machDetail[5].replace('00', '0', 1)
        except IndexError:
            ibmPCommTLS.debugPrint('Get Machine Information Error! Try another SN.', color='red')

        if locQueue not in self.locQueues:
            ibmPCommTLS.debugPrint('Local Q not correct, set to "SSRBJ"')
            locQueue = 'SSRBJ'
            self.locQueue = locQueue

        # for IPS machine, customer name is necessary
        custName = ''
        # default pri&srv, system not down.
        priority = '3'
        severity = '3'
        sysDown = False

        prompt = input('Is System Down (No/yes)?').upper()
        if prompt == 'Y' or prompt == 'YES':
            sysDown = True

        prompt = input('Priority (Default 3): ')
        try:
            int(prompt)
        except ValueError:
            ibmPCommTLS.debugPrint('Input Error, set "3" as default.')
        else:
            if 1 <= int(prompt) <= 4:
                priority = prompt

        prompt = input('Severity (Default 3): ')
        try:
            int(prompt)
        except ValueError:
            ibmPCommTLS.debugPrint('Input Error, set "3" as default.')
        else:
            if 1 <= int(prompt) <= 4:
                severity = prompt

        if not self.login2PMH():
            self.login2PMH()

        # Get Machine Model, Cust name, Cust No.
        self.sendString(22, 9, 'C: ' + custNo)
        self.sendEnter()
        self.sendStringDirectly('1')
        self.sendEnter()
        custName = self.getString(1, 11, 35).rstrip('_')
        print(machType, machMod, machSN, custNo, custName, locQueue, sysDown, priority, severity)

        if input('Enter to be continue, or "Q" back to Main Menu: ').upper() == 'Q':
            return False
        self.callEntry(custNo, locQueue, machType, machMod, machSN, priority, severity, sysDown)

    def altSubRqst(self):
        """
        FORMAT:      alter (or press PF3)
        Description: Use the Alter command to change fields in a problem record.
        Usage Notes: Enter the command while viewing the problem record.
        subrequest type:
        1. CORRECTIVE REPAIR
        2. PREVENTIVE MAINTENANCE
        3. HEALTH & SAFETY CHECKS
        4. INSTALLATION
        5. MES
        :return: None
        """
        self.sendPf(3)
        self.sendPf(5)
        print('Select subrequest type:')
        for row in range(7, 12):
            print(self.getString(row, 6, 45))
        prompt = input()
        try:
            int(prompt)
        except ValueError:
            ibmPCommTLS.debugPrint('Wrong input!')
        else:
            if 0 <= int(prompt) < 6:
                self.sendString(19, 10, prompt)
            else:
                ibmPCommTLS.debugPrint('Wrong input, "1. corrective repair" for default.')
                self.sendString(19, 10, '1')
            self.sendEnter()
            self.sendEnter()
            # for debug
            self.printCurrScreen()

    def srchCust(self, custNo='', nameOrAddrOrCityOrZip='', listCPU=False):
        """
        C: 0805543 (7 letters)
        LIST: The LIST command will display all the CPU's for the
        customer number in the problem record currently being displayed.
        """
        custName = ''
        custCPUs = []
        if len(custNo) == 6:
            custNo = '0' + custNo
        if len(custNo) == 8 and custNo.startswith('00'):
            custNo = custNo.replace('0', '', 1)
        srchArgs = custNo
        if not self.login2PMH():
            self.login2PMH()
        if not custNo:
            srchArgs = nameOrAddrOrCityOrZip
        self.sendString(22, 9, 'C: ' + srchArgs)
        self.sendEnter()
        # self.printCurrScreen()
        if self.getString(4, 58, 8).strip() == '0':
            return []
        elif self.getString(4, 58, 8).strip() != '1':
            ibmPCommTLS.debugPrint('More than 1 records found, get 1st for result.')
        self.sendString(22, 9, '1')
        self.sendEnter()
        custNo = self.getString(1, 3, 6)
        custName = self.getString(1, 11, 36).rstrip('_')
        if listCPU:
            self.sendString(22, 9, 'LIST')
            self.sendEnter()
            custCPUs.append(self.getString(7, 4, 74))
            while True:
                for row in range(8, 20):
                    dataStr1 = self.getString(row, 4, 21)
                    dataStr2 = self.getString(row, 31, 21)
                    dataStr3 = self.getString(row, 58, 21)
                    if dataStr1:
                        custCPUs.append(dataStr1)
                    if dataStr2:
                        custCPUs.append(dataStr2)
                    if dataStr3:
                        custCPUs.append(dataStr3)
                self.sendEnter()
                if self.getString(8, 4, 3).strip() == '1':
                    break
        # print('{}:{}:{}'.format(srchArgs, custNo, custName))
        return [custNo, custName]

    def srchProd(self, machArgs):
        """
        Search Product
        Format:   U: <search argument>  |  T <title page number>
        Description:  The U: command allows you to search the CPU records.
        Support: 0+custNo, cust name, machine sn, machine type
        """
        if not self.login2PMH():
            self.login2PMH()
        self.sendString(22, 9, 'U: ' + machArgs)
        self.sendEnter()
        if self.getString(4, 25, 1).strip() == '0':
            return False
        return True

    def showMultiPages(self):
        while True:
            prompt = input('Type index to choose PMH No, '
                           'or "ENTER" to next page, '
                           '"q" to quit:\n').upper()
            if prompt == 'Q':
                break
            elif prompt == '':
                self.sendEnter()
                for row in range(6, 21):
                    rowData = self.getString(row, 5, 71)
                    if rowData:
                        print(rowData)
            else:
                self.sendString(22, 9, prompt)
                self.sendEnter()
                tmpStr = self.getString(1, 33, 18)
                if tmpStr.startswith('PMR: '):
                    proNo = tmpStr.lstrip('PMR: ')
                break

    def srchPro(self, srchArgsDict):
        """
        Format:   P:<search argument>  |  T <title page number>
        Description:   The P: command allows you to search problem files.
               The T command allows you to select one of the resulting
               title pages.
        {'custNo': custNo, 'custName': custName, 'proNo5b': proNo5b,
        'proNo13b': proNo13b, 'locQueue': locQueue, 'tsgQueue': tsgQueue,
        'ctryCode': ctryCode, 'ctryNo': ctryNO, 'brNo': brNo}
        :return:
        """
        proNo = ''
        if not self.login2PMH():
            self.login2PMH()
        self.typeOfPMHArgs(srchArgsDict)
        ctryCode = self.ctryCode
        if self.srchArgsDict['locQueue'] or self.srchArgsDict['tsgQueue']:
            if self.srchArgsDict['locQueue']:
                queue = self.srchArgsDict['locQueue']
            else:
                queue = self.srchArgsDict['tsgQueue']

            print('Search PMH from Q "{}" you type.'.format(queue))
            self.sendString(22, 9, 'CS ' + queue + ',' + ctryCode)
            self.sendEnter()
            while True:
                for row in range(7, 21):
                    rowData = self.getString(row, 3, 78).rstrip()
                    if len(rowData) > 4:
                        print(rowData)
                self.sendEnter()
                if self.getString(7, 4, 1) == '1':
                    break
            while True:
                """
                while True:
                    for row in range(7, 21):
                        rowData = self.getString(row, 3, 78).rstrip()
                        if len(rowData) > 4:
                            print(rowData)
                    self.sendEnter()
                    if self.getString(7, 4, 1) == '1':
                        break
                """

                prompt = input('Choose one to read: ')
                if not prompt:
                    return proNo
                self.sendString(22, 9, prompt)
                self.sendEnter()
                for row in range(1, 22):
                    rowData = self.getString(row, 1, 79)
                    print(rowData)
                prompt = input('Continue read with "Enter" or '
                               'Return to search result with "t": ')
                if not prompt:
                    tmpStr = self.getString(1, 33, 18)
                    if tmpStr.startswith('PMR: '):
                        proNo = tmpStr.lstrip('PMR: ')
                    return proNo
                elif prompt.upper() == 'T':
                    self.sendString(22, 9, 'T')
                    self.sendEnter()

        srchArgs = self.srchArgsDict['proNo5b'] \
                   + ' ' + self.srchArgsDict['brNo'] \
                   + ' ' + self.srchArgsDict['ctryNo'] \
                   + ' ' + self.srchArgsDict['custNo'] \
                   + ' ' + self.srchArgsDict['machType'] \
                   + ' ' + self.srchArgsDict['machSN'] \
                   + ' ' + self.srchArgsDict['userName'] \
                   + ' ' + self.srchArgsDict['proStat']
        print('Search args: {}'.format(srchArgs))
        self.sendString(22, 9, 'P: ' + srchArgs)
        self.sendEnter()
        for row in range(6, 21):
            rowData = self.getString(row, 5, 71).rstrip()
            if len(rowData) > 4:
                print(rowData)
        if self.getString(4, 27, 1) == '1':
            ibmPCommTLS.debugPrint('Only 1 record found, return PMH No.')
            proNo = self.getString(6, 9, 5) + ',' \
                    + self.getString(6, 16, 3) + ',' \
                    + self.getString(6, 22, 3)
        elif self.getString(4, 25, 1) == '0':
            ibmPCommTLS.debugPrint('No record found, abort.')
            return proNo
        else:
            while True:
                prompt = input('Type index to choose PMH No, '
                               'or "ENTER" to next page, '
                               '"q" to quit:\n').upper()
                if prompt == 'Q':
                    break
                elif prompt == '':
                    self.sendEnter()
                    for row in range(6, 21):
                        rowData = self.getString(row, 5, 71)
                        if rowData:
                            print(rowData)
                else:
                    self.sendString(22, 9, prompt)
                    self.sendEnter()
                    tmpStr = self.getString(1, 33, 18)
                    if tmpStr.startswith('PMR: '):
                        proNo = tmpStr.lstrip('PMR: ')
                    break
        print('Problem No.: {}'.format(proNo))
        return proNo

    def srchArchPro(self):
        """
        Archived Problem Search
        Format:   A:<search argument>  |  B:<search argument> | D:<search argument>

        Description:  The A:, B: or D: commands allow you to search archived PMRs.
               The B: will search all USA PMRS. A: will search EMEA
               business unit PMRs. D: will search AFE business unit PMRs.
               HW PMRs can be searched with just the A: command.
               All HW records are on SF2 and SW records on RTA.
        Usage notes:   Enter T <n> to display a page of titles from your previous
               search, where 'n' is the title page number.  If you do not
               specify a page, the first title page will be shown.

               Enter 'hit' number to view a specific archived record.

               Press PF5 to scan through problems on a title page or select
               a specific problem, then press PF5 to view the next archived
               record.
               For HELP error messages, refer to "HELP P:" messages.
        P; 01914 B000
        A; 01914 B000
        R 01914,000,672
        CS JL2RS,950
        :return:
        """
        pass

    def formatAlter(self, fmtCode):
        """
        Format: FA <global format number, local format number>
        Desc:   Allow you to insert a format in the alterable format area of the problem record.
                Once an alterable format has been added to the problem record, any alterables to
                the format using this command ard made only to the copy that resides in the
                problem record.
        Usage:  FA global format number - 100-9999 ard global format numbers.
                FA local format number - 0-99 are local format number.
                In this function, only a few format number are supported.
                '5012' for power server
                '1724' for DS3K/4K/5K
                '5258' for V7K
                '1794' for DS8K
        :return:
                True or False
        """
        if fmtCode not in self.txtFmtCode:
            return False

    def txtFieldGui(self):
        self.txtFromGui = ''

        def getValue():
            tmpStr = txtBox.get('1.0', tk.END)
            self.txtFromGui = tmpStr
            tmpWindow.destroy()

        tmpWindow = tk.Tk()
        frame = tk.Frame(tmpWindow, relief=RIDGE, borderwidth=2)
        frame.pack(fill=BOTH, expand=1)
        tmpWindow.title('Add Text to PMH')
        txtBox = tk.Text(width=80, heigh=6)
        txtBox.pack()
        # btnSave = tk.Button(master=frame, text='Get Text', command=tmpWindow.destroy)
        btnSave = tk.Button(master=frame, text='Get Text', command=getValue)
        btnSave.pack(side=BOTTOM)
        tmpWindow.mainloop()

    def addTxt(self, PF6=True, gui=False):
        """
        Desc:   The ADDTXT command is used to add narrative text.
                The user may use the PF6 key instead of keying the "ADDTXT"
                command or issue the DT command.
        Usage:  ADDTXT     -or-     DT      -or-    (PF6)
        """
        txt2Add = []
        print('Type text from GUI or command line (end with "EOF"): ')
        if gui:
            self.txtFieldGui()
            txt2Add = self.txtFromGui.split('\n')

        else:
            while True:
                txtLine = input()
                if txtLine.upper() == 'EOF':
                    break
                if txtLine == '':
                    txtLine = '.'
                txt2Add.append(txtLine)

        for txtLine in txt2Add:
            if len(txtLine) > 70:
                txt2Add.insert(txt2Add.index(txtLine), txtLine[0:71])
                txt2Add[txt2Add.index(txtLine)] = txtLine[71:-1]
        for txtLine in txt2Add:
            if not txtLine:
                txt2Add[txt2Add.index(txtLine)] = '.'
        print('\nText: ')
        for txtLine in txt2Add:
            print(txtLine)
        if input('\n"Enter" to add or "N" to cancel (Y/n)? ').upper() == 'N':
            return False
        if PF6:
            self.sendPf(6)
        for txtLine in txt2Add:
            self.sendString(6, 2, txtLine)
            self.sendEnter()
        self.sendPf(11)

    def callReqAddTxt(self, queue, disNxt=False):
        if disNxt:
            self.sendString(22, 9, 'DN/CD/CR')
        else:
            self.sendString(22, 9, 'CD/CR')
        self.sendEnter()
        self.sendString(3, 8, queue)
        # # # check 80K S4 P4
        # # # check change s4 p4 or not.
        self.sendString(15, 17, '1')
        self.sendString(15, 19, '1')
        self.sendString(16, 17, '1')
        self.sendString(16, 19, '1')
        self.sendString(17, 16, 'fsg')
        self.sendEnter()
        self.sendEnter()
        self.sendEnter()
        self.addTxt(PF6=False)

    def readProblem(self, proNo='', prtText=True):
        PMHInfo = []
        PMHText = []
        if not proNo and not self.pmhNo:
            return PMHInfo
        elif not proNo:
            ibmPCommTLS.debugPrint('Problem No. not input, '
                                   'read the last one {}.'.format(self.pmhNo), color='green')
            prompt = input('YES or no (default Yes): ').upper()
            if prompt == 'N' or prompt == 'NO':
                return PMHInfo
            proNo = self.pmhNo
        else:
            self.pmhNo = proNo

        # queue = self.srchArgsDict['tsgQueue']
        # Q to name defined above or self input???
        if not self.login2PMH():
            self.login2PMH()
        self.sendString(22, 9, 'R ' + proNo)
        self.sendEnter()
        if self.getString(23, 6, 41) == 'INVALID READ REQUEST, NO CALL DISPATCHED.':
            ibmPCommTLS.debugPrint('Wrong PMH No!')
            return PMHInfo
        if self.getString(23, 9, 20) == 'INPUT NOT RECOGNIZED':
            ibmPCommTLS.debugPrint('PMH No is necessary!')
            return PMHInfo
        if self.getString(23, 8, 27) == 'REQUESTED RECORD NOT FOUND.':
            return PMHInfo
        for row in range(1, 5):
            PMHInfo.append(self.getString(row, 2, 79))
        while True:
            for row in range(5, 21):
                PMHText.append(self.getString(row, 2, 79))
            self.sendEnter()
            if self.getString(18, 78, 2).strip() == '1':
                break
        PMHInfo.extend(PMHText)
        if prtText:
            for info in PMHInfo:
                if info.startswith(' +') or info.startswith(' -'):
                    info = '\033[0;31m' + info + '\033[0m'
                print(info)
        prompt = input('"AT" -> addtext;\n'
                       '"FA" -> format alter;\n'
                       '"AL" -> alter subrequest;\n'
                       '"CR" -> addtext & req;\n'
                       '"CC" -> complete call.\n'
                       '"RE" -> refresh call.\n\n'
                       '==> ').upper()
        if prompt == 'AT':
            self.addTxt()
        if prompt == 'FA':
            # *** need modify.
            print('not supported yet')
        if prompt == 'AL':
            self.altSubRqst()
        if prompt == 'CR':
            print('Valid TSG Q name: {}'.format(self.tsgQueue))
            print('Valid Local Q name: {}'.format(self.locQueues))
            print('Q to "{}" release dispatch.'.format(self.noQueue))
            prompt = input('\nType Q name: ').upper()
            if not prompt:
                print('No input, nothing changed.')
                return False
            elif prompt in self.locQueues:
                if input('Be sure Q to local queue "{}"(N to cancel)?'
                                 .format(prompt)).upper() == 'N':
                    return False
            elif prompt not in self.tsgQueue:
                print('Wrong Q name "{}", abort. Nothing changed.'.format(prompt))
                return False
            if input('CONFIRM: CR to "{}"?'.format(prompt)).upper() == 'N':
                return False
            self.callReqAddTxt(prompt, disNxt=True)
            if input('Read again or not (N/y)?').upper() == 'Y':
                self.readProblem(proNo=proNo)

        if prompt == 'CC':
            self.callComplete()

        if prompt == 'RE':
            print('Refresh the contend...')
            self.readProblem(self.pmhNo)

        return PMHInfo

    def readProPlus(self, argsList):
        self.readProblem(self.srchPro(argsList))

    def callComplete(self, PMHNo='', delete=False):
        """
        if not self.login2PMH():
            self.login2PMH()
        self.sendString(22, 9, 'R ' + PMHNo)
        self.sendEnter()
        'NOT ALLOWED, CALL IS CONNECTED'
        <23, 7>
        """
        if self.getString(3, 38, 24).strip().strip('_') != self.userID + '@cn.ibm.com':
            ibmPCommTLS.debugPrint('Seems you are attempting to '
                                   'close PMH not owned by yourself.', color='red')
            if input('Still want to close or cancel by "N": ').upper() == 'N':
                print('Process canceled.')
                return False
        self.sendString(22, 9, 'DN/CD/CC')
        self.sendEnter()
        if self.getString(23, 7, 60).strip() == 'NO CALLS FOUND FOR THIS PROBLEM':
            self.sendString(22, 9, 'R ' + PMHNo)
            self.sendEnter()
            self.sendString(22, 9, 'PC')
            self.sendEnter()
            self.sendEnter()
            self.sendPf(11)
        else:
            self.sendString(14, 14, 'CL')
            self.sendString(15, 17, '1')
            self.sendString(15, 19, '1')
            self.sendString(16, 17, '1')
            self.sendString(16, 19, '1')
            self.sendString(17, 16, 'fsg')
            self.sendEnter()
            self.addTxt(PF6=False)
        self.sendString(22, 9, 'R ' + PMHNo)
        self.sendEnter()
        if self.getString(1, 26, 2) == 'CL':
            return True
        else:
            return False

    def typeOfPMHArgs(self, zArgs):
        proNo5b = ''
        custNo = ''
        custName = ''

        locQueue = ''
        tsgQueue = ''
        ctryCode = ''
        ctryNO = ''
        brNo = ''
        proStat = ''

        machType = ''
        machSN = ''

        userName = ''

        print('zArgs: ', zArgs)
        if not zArgs:
            if self.pmhNo:
                # debug, deleted later
                print('No args for search, set pmh to self.pmhno.')
                proNo5b = self.pmhNo.split(',')[0]
                brNo = self.pmhNo.split(',')[1]
                ctryNO = self.pmhNo.split(',')[2]
        print(proNo5b)

        for args in zArgs:
            args = args.upper()
            if args in self.brNo and not brNo:
                brNo = args
                continue
            if args == self.ctryCode and not ctryCode:
                ctryCode = self.ctryCode
                continue
            if args == self.ctryNo and not ctryNO:
                ctryNO = self.ctryNo
                continue
            if args in self.locQueues and not locQueue:
                locQueue = args
                continue
            if args in self.tsgQueue and not tsgQueue:
                tsgQueue = args
                continue
            if args in self.proStat and not proStat:
                proStat = args
                continue
            if len(args) == 4:
                if self.srchProd(args) and not machType:
                    machType = args
                    continue
            if len(args) == 7 and not args.startswith('0'):
                if self.srchProd(args) and not machSN:
                    machSN = args
                    continue
            tmpList = self.srchCust(args)
            if tmpList and not custNo:
                custNo = tmpList[0]
                custName = tmpList[1]
                continue
            tmpList = self.srchCust(nameOrAddrOrCityOrZip=args)
            if tmpList and not custNo:
                custNo = tmpList[0]
                custName = tmpList[1]
                continue
            if len(args) == 5 and not proNo5b:
                proNo5b = args
                continue
            if not userName:
                userName = args
        self.srchArgsDict = {'custNo': custNo, 'custName': custName, 'proNo5b': proNo5b,
                             'locQueue': locQueue, 'tsgQueue': tsgQueue,
                             'ctryCode': ctryCode, 'ctryNo': ctryNO,
                             'brNo': brNo, 'proStat': proStat,
                             'machType': machType, 'machSN': machSN,
                             'userName': userName}

        i = 0
        for key in self.srchArgsDict:
            if self.srchArgsDict[key]:
                if key == 'proStat':
                    i += 13
                    continue
                i += 1
        if i == 0:
            self.srchArgsDict['userName'] = self.userName
            self.srchArgsDict['proStat'] = 'OPEN'
        elif i == 13:
            self.srchArgsDict['userName'] = self.userName

        if self.srchArgsDict['brNo']:
            self.srchArgsDict['brNo'] = 'B' + self.srchArgsDict['brNo']
        if self.srchArgsDict['ctryNo']:
            self.srchArgsDict['ctryNo'] = 'C' + self.srchArgsDict['ctryNo']
        if self.srchArgsDict['custNo']:
            self.srchArgsDict['custNo'] = '0' + self.srchArgsDict['custNo']
        if not self.srchArgsDict['ctryCode']:
            self.srchArgsDict['ctryCode'] = self.ctryCode

        print('test index: {}'.format(i))
        print(self.srchArgsDict)
        return self.srchArgsDict


if __name__ == '__main__':
    pass