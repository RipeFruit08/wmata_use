import http.client
import urllib.request, urllib.parse, urllib.error
import base64, pprint, json, datetime, sys, os


API_KEY = os.environ['API_KEY']

station_name_fix = {
    "King St": "King St-Old Town",
    "McPherson Sq E": "McPherson Square",
    "Dupont Circle N": "Dupont Circle",
    "Metro Center N": "Metro Center",
    "Metro Center S": "Metro Center",
    "Metro Center E": "Metro Center",
    "Metro Center W": "Metro Center",
    "Gal Pl-Chntwn N": "Gallery Pl-Chinatown",
    "Gal Plc-Chntn E": "Gallery Pl-Chinatown",
    "Navy Yard E": "Navy Yard-Ballpark",
    "Arch-Navy Mem": "Archives-Navy Memorial-Penn Quarter",
    "Woodley Park-Zoo": "Woodley Park-Zoo/Adams Morgan",
    "Union Stn N": "Union Station",
    "Dunn Loring": "Dunn Loring-Merrifield",
    "Foggy Bottom": "Foggy Bottom-GWU",
    "E Falls Church": "East Falls Church",
    "Fed Triangle": "Federal Triangle"
}

def getStationList():

    headers = {
        # Request headers
        'api_key': API_KEY,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        #'LineCode': 'SV'
    })

    stations = []

    try:
        conn = http.client.HTTPSConnection('api.wmata.com')
        conn.request("GET", "/Rail.svc/json/jStations?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        stations = json.loads(data)['Stations']
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    ####################################
    print('getStationList')
    return stations

def getStationCode(name, stationList):
    code = None
    if name in station_name_fix:
        name = station_name_fix[name]
    for station in stationList:
        if station['Name'] == name:
            code = station['Code']
            return code

    return code

def stationToStationInfo(srcCode, dstCode):
    headers = {
        # Request headers
        'api_key': API_KEY,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'FromStationCode': srcCode,
        'ToStationCode': dstCode,
    })

    try:
        conn = http.client.HTTPSConnection('api.wmata.com')
        conn.request("GET", "/Rail.svc/json/jSrcStationToDstStationInfo?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

'''
stsInfo is StationToStationInfo as json
dateStr is a date string in the form of mm/dd/yy hh:mm AM/PM
'''
def getFare(stsInfo, dateStr):
    #print(stsInfo)
    mm = int(dateStr[0:2])
    dd = int(dateStr[3:5])
    yy = int(dateStr[6:8])
    hh = int(dateStr[9:11])
    mins = int(dateStr[12:14])
    tt = dateStr[15:17]
    d = datetime.date(2000+yy, mm, dd)
    weekno = d.weekday()
    #print(weekno)
    if yy >= 21 and mm >= 9 and weekno > 4:
        return 2.0
    else:
        peakFlag = isPeak(mins, hh, tt)
        fareKey = "PeakTime" if peakFlag else "OffPeakTime"
        #print(f'date {mm}/{dd}/{yy}')
        #print(f'time {hh}:{mins} {tt}')
        #print(fareKey)
        try:
            return stsInfo["StationToStationInfos"][0]["RailFare"][fareKey]
        except KeyError:
            print(stsInfo)

def isPeak(mins, hh, tt):
    # TODO this is disgusting, please fix it 
    # peak if between 5 am and 9:30 am
    if tt == "AM":
        if (hh == 9 and mins <= 30):
            return True
        elif hh == 9 and mins > 30:
            return False
        elif hh > 9:
            return False
        elif hh >= 5:
            return True
        else:
            return False
    # assume PM is the only other options 
    else:
        # peak if between 3 and 7 pm
        if hh >= 3 or hh <= 7:
            return True
        else:
            return False

def main():
    month = 'sep'
    if len(sys.argv) == 2:
        month = sys.argv[1]
    stationList = getStationList()
    fn = f'{month}_metro_use.csv'
    totalFare = 0
    with open(fn) as f:
        for line in f:
            tok = line.split(',')
            #print(line.strip())
            ride_time = tok[1]
            desc = tok[2]
            operator = tok[3]
            entry_station = tok[4]
            exit_station = tok[5]
            entry_station_code = getStationCode(entry_station, stationList)
            exit_station_code = getStationCode(exit_station, stationList)
            '''
            if entry_station_code == None or exit_station_code == None:
                print("Couldn't find station code(s).")
                print(f"{entry_station} -> {entry_station_code}")
                print(f"{exit_station} -> {exit_station_code}")
            '''
            product = tok[6]
            cost = tok[8]
            # rows marked as exit have both entry and exit stations
            if operator == 'Metrorail' and desc == 'Exit':
                #print(f'ride from {entry_station} to {exit_station} using {product} cost {cost} at {ride_time}')
                #print(f'query from {entry_station} to {exit_station}')
                data = stationToStationInfo(entry_station_code, exit_station_code)
                dataStr = data.decode('utf-8')
                dataJson = json.loads(dataStr)
                #fare = dataJson["StationToStationInfos"][0]["RailFare"]["PeakTime"]
                fare = getFare(dataJson, ride_time)
                print(f'fare from {entry_station}({entry_station_code}) to'+ \
                    f' {exit_station}({exit_station_code}) ' + \
                    f'on {ride_time} ' + \
                    f'is ${fare}')
                totalFare += fare

    print(f'total fare for month of {month.upper()} is ${totalFare}')

if __name__ == '__main__':
    main()
