# importing the requests library 
import requests 
import json
import simplekml
import sys

# api-endpoint 
URL = "http://predict.cusf.co.uk/api/v1/"

print('Enter flight parameters below\r\n')
ascent_rate = input('Ascent rate (m/s): ')
launch_datetime = input('Launch time (YYYY-MM-DDTHH:MM:SSZ): ')
launch_latitude = input('Launch latitude:  ')
launch_longitude = input('Launch longitude: ')
launch_altitude = input('Launch altitude (m): ')
profile = input('Flight profile: ')

PARAMS = {'ascent_rate': float(ascent_rate),
          'launch_altitude': float(launch_altitude),
          'launch_datetime': launch_datetime,
          'launch_latitude': float(launch_latitude),
          'launch_longitude': (float(launch_longitude) + 360) % 360,
          'profile': profile
}

if profile == 'standard_profile':
    imm_cutdown = input('Immediate cutdown? (1/0): ')
    imm_cutdown = int(cutdown)
    if(cutdown):
        burst_altitude = int(launch_altitude) + 10
    else:
        burst_altitude = input('Burst altitude: ')
    descent_rate = input('descent_rate: ')
    PARAMS['burst_altitude'] = float(burst_altitude)
    PARAMS['descent_rate'] = float(descent_rate)
    
elif profile == 'float_profile':
    imm_cutdown = 0
    float_cutdown = input('Cutdown at end of float? (1/0): ')
    float_cutdown = int(float_cutdown)
    if(float_cutdown):
        descent_rate = input('Descent rate at end of floating period (m/s): ')
    stop_datetime = input('Stop time (YYYY-MM-DDTHH:MM:SSZ): ')
    float_altitude = input('Float altitude (m): ')
    PARAMS['stop_datetime'] = stop_datetime
    PARAMS['float_altitude'] = float(float_altitude)
    
else:
    print('Error in profile name')
    sys.exit()
    
# 2019-09-15T12:00:00Z

# sending get request and saving the response as response object 
r = requests.get(url = URL, params = PARAMS) 

# extracting data in json format 
data = r.json() 
with open("data_file.json", "w") as write_file:
    json.dump(data, write_file)

kml = simplekml.Kml()
linestring = kml.newlinestring(name='Trajectory')

coords = []

if(not imm_cutdown):
    for x in data['prediction'][0]['trajectory']:
        coords.append((((x['longitude'] + 180) % 360) - 180, x['latitude'], x['altitude'])) 
    
for x in data['prediction'][1]['trajectory']:
    coords.append((((x['longitude'] + 180) % 360) - 180, x['latitude'], x['altitude'])) 

#Launch point placemark
if(not imm_cutdown):
    pnt = kml.newpoint()
    pnt.name = 'Launch'
    lon = data['prediction'][0]['trajectory'][0]['longitude']
    lat = data['prediction'][0]['trajectory'][0]['latitude']
    pnt.coords = [((lon + 180) % 360 - 180, lat )]

#Burst Point placemark
pnt = kml.newpoint()
if profile == 'standard_profile':
    pnt.name = 'Burst'
else:
    pnt.name = 'Float Start'
    
end = len(data['prediction'][0]['trajectory']) - 1
lon = data['prediction'][0]['trajectory'][end]['longitude']
lat = data['prediction'][0]['trajectory'][end]['latitude']
pnt.coords = [((lon + 180) % 360 - 180, lat )]

#Landing/Float Point placemark
pnt = kml.newpoint()
if profile == 'standard_profile':
    pnt.name = 'Landing'
else:
    pnt.name = 'Float end'

end = len(data['prediction'][1]['trajectory']) - 1
lon = data['prediction'][1]['trajectory'][end]['longitude']
lat = data['prediction'][1]['trajectory'][end]['latitude']
pnt.coords = [((lon + 180) % 360 - 180, lat )]

if(float_cutdown):
    PARAMS = {'ascent_rate': 0.1,
          'launch_altitude': float(float_altitude),
          'launch_datetime': stop_datetime,
          'launch_latitude': data['prediction'][1]['trajectory'][end]['latitude'],
          'launch_longitude': data['prediction'][1]['trajectory'][end]['longitude'],
          'profile': 'standard_profile',
          'burst_altitude' : float(float_altitude) + 10,
          'descent_rate' : float(descent_rate)
    }
    r = requests.get(url = URL, params = PARAMS) 

    # extracting data in json format 
    data = r.json() 
    with open("data_file.json", "w") as write_file:
        json.dump(data, write_file)
        
    for x in data['prediction'][1]['trajectory']:
        coords.append((((x['longitude'] + 180) % 360) - 180, x['latitude'], x['altitude'])) 

    linestring.coords = coords
    linestring.altitudemode = simplekml.AltitudeMode.relativetoground
    linestring.extrude = 1
    linestring.style.linestyle.color = '50000000'
    linestring.style.polystyle.color = '990000ff'
    
    pnt = kml.newpoint()
    pnt.name = 'Landing'
    end = len(data['prediction'][1]['trajectory']) - 1
    lon = data['prediction'][1]['trajectory'][end]['longitude']
    lat = data['prediction'][1]['trajectory'][end]['latitude']
    pnt.coords = [((lon + 180) % 360 - 180, lat )]
    
    kml.save("trajectory.kml")
