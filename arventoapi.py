import requests
import datetime
from datetime import timezone
import pytz
from statistics import mean

authenticationURL = 'https://ws.arvento.com/api/v1/login'
generalReportURL = 'https://ws.arvento.com/api/v1/report/general'

class ArventoAPI:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.sid = None

    def authenticate(self):
        data = {
            "userName": self.username,
            "password": self.password
        }

        try:
            res = requests.post(authenticationURL, data = data)
            response = res.json()
        except:
            return self.authenticate()

        if ('Record' in response) and ('sessionId' in response['Record']):
            self.sid = response['Record']['sessionId']
        else:
            print('Unable to authenticate')

    
    def getHistoricalDataDaily(self, device_id, day):

        if self.sid is None:
            self.authenticate()
            return self.getHistoricalDataDaily(device_id, day)

        if int(day) < 10:
            daystart = '0'+str(day)
        else:
            daystart = str(day)

        dayend = int(day)+1

        if dayend < 10:
            dayend = '0'+str(dayend)
        else:
            dayend = str(dayend)

        data = {
            "Nodes": [
                device_id
            ],
            "StartDate": '202004{}000000'.format(daystart),
            "EndDate": '202004{}000000'.format(dayend),
            "Options": [
                "locationInfo"
            ]
        }

        print(data)

        headers = {
            'Authorization': 'sid {}'.format(self.sid)
        }

        try:
            res = requests.post(generalReportURL, json=data, headers=headers)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            # print('day {} failed'.format(day))
            self.sid = None
            return []

        response = res.json()

        if ('List' in response) and isinstance(response['List'], list):
            return [ { 'datetime': datetime.datetime.strptime(d['DateTime']+' +07:00','%Y%m%d%H%M%S %z'), 'longitude': d['Longitude'], 'latitude': d['Latitude'], 'speed': d['SpeedKmPerHour'] } for d in response['List']]
        else:
            # print('day {} failed'.format(day))
            self.sid = None
            return []


    def getHistoricalData(self, device_id, timestart, timeend):

        # inputted data would be 2020-04-16 19:34:23 +07:00

        timestart_ = datetime.datetime.strptime(timestart, '%Y-%m-%d %H:%M:%S %z').astimezone(pytz.utc)
        timeend_ = datetime.datetime.strptime(timeend, '%Y-%m-%d %H:%M:%S %z').astimezone(pytz.utc)

        if self.sid is None:
            self.authenticate()
            return self.getHistoricalData(device_id, timestart, timeend)
            
        data = {
            "Nodes": [
                device_id
            ],
            "StartDate": timestart_.strftime('%Y%m%d%H%M%S'),
            "EndDate": timeend_.strftime('%Y%m%d%H%M%S'),
            "Options": [
                "locationInfo"
            ]
        }

        # print(data)

        headers = {
            'Authorization': 'sid {}'.format(self.sid)
        }

        try:
            res = requests.post(generalReportURL, json=data, headers=headers)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            self.sid = None   
            return {
                'trajectory_arr': [],
                'trajectory_size': 0,
                'timestamps': [],
                'speed': [],
                'average_speed': 0,
                'max_speed': 0
            }
        
        try:
            response = res.json()
        except:
            self.sid = None   
            return {
                'trajectory_arr': [],
                'trajectory_size': 0,
                'timestamps': [],
                'speed': [],
                'average_speed': 0,
                'max_speed': 0
            }

        if ('List' in response) and isinstance(response['List'], list):

            # too slow
            # filteredList = [d for d in response['List'] if (datetime.datetime.strptime(d['DateTime']+' +07:00','%Y%m%d%H%M%S %z') >= timestart_) and (datetime.datetime.strptime(d['DateTime']+' +07:00','%Y%m%d%H%M%S %z') <= timeend_)]

            # timestart_n = int(timestart_.strftime('%Y%m%d%H%M%S'))
            # timeend_n = int(timeend_.strftime('%Y%m%d%H%M%S'))

            # filteredList = [d for d in response['List'] if (int(d['DateTime']) >= timestart_n) and (int(d['DateTime']) <= timeend_n)]
            filteredList = response['List']

            longlat = [ '{},{}'.format(i['Longitude'],i['Latitude']) for i in filteredList]
            
            # 20200618070546
            time = [i['DateTime'] for i in filteredList]
            time = list(map(lambda x: datetime.datetime.strptime(x, '%Y%m%d%H%M%S').replace(tzinfo=timezone.utc).timestamp(), time))

            # SpeedKmPerHour
            speed = [i['SpeedKmPerHour'] for i in filteredList]

            return {
                'trajectory_arr': longlat,
                'trajectory_size': len(longlat),
                'timestamps': time,
                'speed': speed,
                'average_speed': mean(speed),
                'max_speed': max(speed)
            }

        else:
             # might be expired token.
            self.sid = None   
            return {
                'trajectory_arr': [],
                'trajectory_size': 0,
                'timestamps': [],
                'speed': [],
                'average_speed': 0,
                'max_speed': 0
            }
           

# arvento = ArventoAPI(username='ptastech', password='astech')
# test = arvento.getHistoricalData(device_id='1021252', timestart='2020-04-01 09:16:24 +0700', timeend= '2020-04-01 11:52:37 +0700')
# test = arvento.getHistoricalDataDaily(device_id='1021341', day=1)
# print(test)