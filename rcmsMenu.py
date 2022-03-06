#!/usr/bin/env python

import time
from datetime import date
from os import system
from os import path
from functions import ibmPCommTLS
from functions import readConfig
from functions import ibmRetain
# from .functions import readConfig
# from .functions import ibmPCommTLS
# from . functions import ibmRetain

mainMenu = ['-------------IBM RCMS MENU-------------',
            '\033[0;90m'
            'Function',
            '\tCc. Current Config',
            '\tLl. Connect & Login',
            '\tPp. Print Current Page',
            '\tRr. Read Me',
            '\tMm. Main Menu',
            '\tHh. Help',
            '\tQq. Quit',
            '\033[0m'

            '\033[0;36m'
            'Call Read',
            '\tcr,[call no]     //eg. cr,p462yk9',
            '\tcr,[call no],w   //read the call every 60s waiting PARTS exist.',
            '\033[0m'

            '\033[0;35m'
            'Call Search&Read   //Only Support SDLNCN&SDLINC',
            '\tcs   //search for current user.',
            '\tcs,[cust no.],[notes id],[call type],[call queue]',
            '\033[0m'

            '\033[0;91m'
            'Call & Product Inventory',
            '\tci,[cust no.],[mach sn],[mach type]',
            '\tin,[mach type],[mach sn],[cust no.]',
            '\033[0m'

            '\033[0;33m'
            'SSR Information',
            '\tw,[ssr name],[ssr sn],[ssr retain id]',
            '\tNot Supported Yet!',
            '\033[0m'

            '\033[0;37m'
            'Time Report',
            '\tred //report list & summary for current user)',
            '\tred,b,s,w,t,e,d,[ssr SNs],[date from],[date to]',
            '\tb: backup to file;',
            '\ts: record list & summary (default date cutoff); ',
            '\tw: weekly summary (ignore date);',
            '\tt: UT summary for team(cut-off cycle);',
            '\te: team EPSB overlap verify;',
            '\td: one day detail;',
            '\tdate format: 200930; Only 1 date specified, deadline will be today.',
            '\tfor "t" or "e", if more than 1 ssr specified, config ignored.',
            '\033[0m'

            '\033[0;31m'
            'PMH',
            "\tz    //Search Current User's Opened PMH or last PMH been read before.",
            '\tz,args1,args2,args3,...',
            '\targs: [pmh no.: 49501 or 49501,000,672],',
            '\t[cust no.: 805543|0805543|00805543],',
            '\t[cust name: Gansu ICBC],',
            '\t[mach type: 1814],[mach sn: 78k15c8],',
            '\t[queue: SSRNW],[branch no.: "000"],',
            '\t[User Name: Zhang Zhi Jie],',
            '\t[pmh stat close|open]',
            '\tdr,[retain id] (read profile)',
            '\tce,[mach sn] (Create PMH)',
            '\tce,snap,[file dir]   //Analyze snap file & generate call. Coming...',
            '\tce,call no.  //rcms call no.; not supported yet.',
            '\033[0m\n']

subMenu4cr = ['Repeat',
              'export']

mainMenuIndex = ['C', 'L', 'P', 'R', 'Q', 'M', 'H']
cmdSet = ('CR', 'CS', 'CI', 'IN', 'RED', 'Z', 'DR', 'CE')
wait4Sec = 60
lastCallNo = ''
lastCallNoList = []
lastPMHNo = ''
autoLogin = True
host1 = ''
host2 = ''
ssrSN = ''
passwd = ''
cutFrom = ''
cutTo = ''
redSave2dir = path.abspath(path.join(path.dirname(__file__), 'log'))
teamSSRList = []
epsbSSRList2Check = []
rcmsConf = {}
retainConf = {}
cutoffDate = []

ibmPCommTLS.debugPrint('Verify config...', color='white')
try:
    rcmsConf = readConfig.getRCMSConf()
    cutoffDate = readConfig.getCutoffDate()
    teamSSRList = readConfig.getTeamSSRList()
    retainConf = readConfig.getRetainConf()
    for key in rcmsConf:
        print('\033[0;31m{:<12}: \033[0m{:.>25}'.format(key, rcmsConf[key]))

    print('\033[0;31mCutoff From : \033[0m\t{:.>23}'.format(cutoffDate[0]))
    print('\033[0;31mCutoff To   : \033[0m\t{:.>23}'.format(cutoffDate[1]))

    print('\033[0;31mTeam SSR List (first 6): \033[0m\n{}'.format(teamSSRList[0:6]))

    for key in retainConf:
        print('\033[0;31m{:<8}: \033[0m{:.>29}'.format(key, retainConf[key]))
except KeyError:
    print('\n')
    ibmPCommTLS.debugPrint('Key Error!, Check Config File.'
                           'Make sure keys include "host1", "host2", '
                           '"ssrSN", "teamSSRList", "epsbSSRList".')
    exit(127)

rcmsHost1 = rcmsConf['host1']
rcmsHost2 = rcmsConf['host2']
ssrSN = rcmsConf['ssrSN']
rcmsPwd = rcmsConf['passwd']
retainHost1 = retainConf['host1']
retainHost2 = retainConf['host2']
retainID = retainConf['retainID']
retainPwd = retainConf['passwd']

cutFrom = cutoffDate[0].replace('20', '', 1)
cutTo = cutoffDate[1].replace('20', '', 1)

for word in readConfig.getRCMSConf()['epsbSSRList'].split(','):
    epsbSSRList2Check.append(word.strip("'").strip('"').strip())

if not rcmsPwd:
    rcmsPwd = input('Enter your RCMS Password: ')
    if input('Confirm (Y/n): ').upper() != 'Y':
        exit(127)

if not retainPwd:
    retainPwd = input('Enter your Retain Password: ')
    if input('Confirm (Y/n): ').upper() != 'Y':
        exit(127)

ibmPCommTLS.debugPrint('Init IBM RCMS PComm Emulator...')
rcms = ibmPCommTLS.rcms(rcmsHost1, rcmsHost2, ssrSN, rcmsPwd)
ibmPCommTLS.debugPrint('RCMS Init Done.', color='green')
ibmPCommTLS.debugPrint('Init IBM Retain System...')
# *** need to modify
retain = ibmRetain.retain(retainHost1, retainHost2, retainID, retainPwd)
ibmPCommTLS.debugPrint('Retain Init Done.', color='green')
input('Enter Main Menu with Any Key.')
for menu in mainMenu:
    print(menu)

while True:
    # system('clear')
    prompt = input('CMD=> ').upper()
    while ' ,' in prompt or ', ' in prompt:
        prompt = prompt.replace(' ,', ',').replace(', ', ',')
    if not prompt.startswith(cmdSet) and prompt not in mainMenuIndex:
        ibmPCommTLS.debugPrint('Input not Permitted.', color='red')
        continue

    """
    # Auto login is embedded in object 'rcms'.
    if prompt not in mainMenuIndex:
        if rcms.currPageType() != rcms.pages['CMD=>']:
            ibmPCommTLS.debugPrint('SYSTEM ERROR! ENTER "L/l" TO LOGIN.', color='red')
            if autoLogin:
                ibmPCommTLS.debugPrint('Auto login to IBM RCMS...')
                rcms.login()
                rcms.printCurrScreen()
                ibmPCommTLS.debugPrint('Login done. Start jobs unfinished before.', color='green')
            else:
                input('\nPress Enter to be Continue!\n')
                continue
    """

    if prompt == 'C':
        print('\033[0;37mCurrent Config:\033[0m')
        for rc in rcmsConf:
            print('\033[0;31m{}: \033[0m{}'.format(rc.upper(), rcmsConf[rc]))
        for rc in retainConf:
            print('\033[0;31m{}: \033[0m{}'.format(rc.upper(), retainConf[rc]))
        print('\033[0;37mCurrent Cut-Off Day:\033[0m {}--{}'.format(cutFrom, cutTo))

    elif prompt == 'L':
        ibmPCommTLS.debugPrint('Connect to IBM RCMS host and login.')
        rcms.go2MainMenu()
        ibmPCommTLS.debugPrint('Connected, RCMS login done.')
        rcms.printCurrScreen()

    elif prompt == 'P':
        rcms.printCurrScreen()

    elif prompt == 'R':
        ibmPCommTLS.debugPrint('Nothing.', color='yellow')

    elif prompt == 'M' or prompt == 'H':
        system('clear')
        for menu in mainMenu:
            print(menu)

    elif prompt == 'Q':
        rcms.disconnect()
        rcms.quit()
        ibmPCommTLS.debugPrint('Quit', color='green')
        exit(0)

    # Call read by no.
    elif prompt.startswith('CR'):
        tmpList = prompt.split(',')
        if len(tmpList) == 2:
            callNo = tmpList[1]
            rcms.callRead(callNo)
            continue

        elif len(tmpList) == 3:
            callNo = tmpList[1]
            while True:
                callInfo = rcms.callRead(callNo)
                if '0000' in callInfo['action plan']:
                    ibmPCommTLS.debugPrint('Parts found, print call info.', color='green')
                    break
                if 'PERCALL' in callInfo['comments'] or 'CLS' in callInfo['st']:
                    ibmPCommTLS.debugPrint('Percall or Call closed, '
                                           'find parts in comment.', color='yellow')
                    break
                ibmPCommTLS.debugPrint('No part found, wait 30s for next loop.')
                time.sleep(wait4Sec)
            lastCallNo = callNo
            continue

        else:
            # ibmPCommTLS.debugPrint('Read Call No Error!', color='red')
            ibmPCommTLS.debugPrint('No Call No. or wrong args, read the last one.', color='red')
            rcms.callRead()

    # Call search.
    elif prompt.startswith('CS'):
        srchArgs = prompt.split(',')
        srchArgs.remove('CS')
        callNoList = rcms.callSrchPlus(srchArgs)
        for call in callNoList:
            print(call)
        prompt = input('(1-99) to Read, Enter back to menu: ')
        if prompt:
            try:
                rcms.callRead(callNoList[int(prompt) - 1][3:10])
            except ValueError:
                ibmPCommTLS.debugPrint('Value Error!')
            except IndexError:
                ibmPCommTLS.debugPrint('Index out of range!')

    # Call Inventory
    elif prompt.startswith('CI'):
        ciArgs = prompt.split(',')
        ciArgs.remove('CI')
        callInvList = rcms.callInquiryPlus(ciArgs)
        for ci in callInvList:
            print(ci)
        prompt = input('(1-99) to Read, Enter back to menu: ')
        if prompt:
            try:
                rcms.callRead(callInvList[int(prompt) - 1][3:10])
            except ValueError:
                ibmPCommTLS.debugPrint('Value Error!')
            except IndexError:
                ibmPCommTLS.debugPrint('Index out of range!')

    elif prompt.startswith('IN'):
        # inArgs = prompt.lstrip('IN,').split(',')
        inArgs = prompt.split(',')
        inArgs.remove('IN')
        proInvList = rcms.proInvPlus(inArgs)
        for pi in proInvList:
            print(pi)
        if len(proInvList) == 1:
            for pidtl in rcms.proInvDetail():
                print(pidtl)

    elif prompt.startswith('RED'):
        # redArgs = prompt.lstrip('RED,').split(',')
        redArgs = prompt.split(',')
        redArgs.remove('RED')
        rcms.redPlus(redArgs, cutFrom, cutTo, teamSSRList, epsbSSRList2Check)

    elif prompt.startswith('Z'):
        pmhArgs = prompt.split(',')
        pmhArgs.remove('Z')
        retain.readProPlus(pmhArgs)
        # print('No args, nothing got.')

    elif prompt.startswith('DR'):
        drArgs = prompt.split(',')
        drArgs.remove('DR')
        if not drArgs:
            drArgs.append('149715')
        print(drArgs)
        retain.displayProfile(drArgs[0])

    elif prompt.startswith('CE'):
        ceArgs = prompt.split(',')
        ceArgs.remove('CE')
        proInvList = rcms.proInvPlus(ceArgs)
        machDetail = ''
        if len(proInvList) == 0:
            input('Nothing found, please verify the machine serial number.')
            continue
        elif len(proInvList) != 1:
            for pi in proInvList:
                print(pi)
            prompt = input('More then 1 machine found, choose one: ')
            try:
                machDetail = proInvList[int(prompt)-1]
            except KeyError:
                print('Input error!')
        else:
            machDetail = proInvList[0]
        print(machDetail)
        retain.callEntryPlus(machDetail, retainConf['locQueue'])

