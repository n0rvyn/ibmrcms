from datetime import date
import os

conFilesDir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config'))
# os.chdir(conFilesDir)
rcmsArgs = ['host1', 'host2', 'ssrSN', 'passwd', 'epsbSSRList']
rcmsConf = 'rcms.conf'
rcmsValues = {}

cutoffConf = 'cutoffDate.conf'
dateList = []
cutoffDate = []

teamSSRListConf = 'teamSSRList.conf'
teamSSRList = []

retainConf = 'retain.conf'
retainValues = {}
retainArgs = ['host1', 'host2', 'retainID', 'passwd', 'entryCmd', 'locQueue']


def getRCMSConf():
    if not os.path.isfile(conFilesDir + '/' + rcmsConf):
        raise FileNotFoundError('RCMS Config File Not Exist.')
    with open(conFilesDir + '/' + rcmsConf, 'r') as f:
        for dataLine in f.readlines():
            args = dataLine.split('=')[0].strip()
            if args in rcmsArgs:
                value = dataLine.split('=')[1].strip().strip("'").strip('"')
                rcmsValues[args] = value
        f.close()
    return rcmsValues


def getCutoffDate():
    if not os.path.isfile(conFilesDir + '/' + cutoffConf):
        raise FileNotFoundError('Cutoff Config File Not Exist.')
    with open(conFilesDir + '/' + cutoffConf, 'r') as f:
        for dataLine in f.readlines():
            if dataLine.startswith('20'):
                dateList.append(dataLine.replace('-', '').rstrip('\n'))
        currTimeMap = str(date.today()).replace('-', '')
        dateList.append(currTimeMap)
        dateList.sort()
        currDayIndex = dateList.index(currTimeMap)
        if int(dateList[currDayIndex]) - int(dateList[currDayIndex-1]) < 7:
            print('Less than 7 days since last cutoff.')
            print('Show the last cutoff cycle.')
            cutoffDate.append(dateList[currDayIndex-2])
            cutoffDate.append(dateList[currDayIndex-1])
        else:
            print('More than 7 days since last cutoff.')
            print('Show the current cutoff cycle.')
            cutoffDate.append(dateList[currDayIndex-1])
            cutoffDate.append(dateList[currDayIndex+1])
        f.close()
    return cutoffDate


def getTeamSSRList():
    if not os.path.isfile(conFilesDir + '/' + teamSSRListConf):
        raise FileNotFoundError('Team SSR List Not Exist.')
    with open(conFilesDir + '/' + teamSSRListConf, 'r') as f:
        for ssrList in f.readlines():
            if ssrList and not ssrList.startswith('#'):
                teamSSRList.append(ssrList.strip('\n').strip())
        f.close()
    return teamSSRList


def getRetainConf():
    if not os.path.isfile(conFilesDir + '/' + retainConf):
        raise FileNotFoundError('RETAIN Config File Not Exist.')
    with open(conFilesDir + '/' + retainConf, 'r') as f:
        for dataLine in f.readlines():
            args = dataLine.split('=')[0].strip()
            if args in retainArgs:
                value = dataLine.split('=')[1].strip().strip("'").strip('"')
                retainValues[args] = value
        f.close()
    return retainValues


if __name__ == '__main__':
    print(getRCMSConf())
    print(getRCMSConf()['host1'])
    print(getCutoffDate())
    print(getTeamSSRList())
    print(getRetainConf())

