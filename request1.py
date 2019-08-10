# importing the requests library 
import requests 
import json
# api-endpoint 
URL = "http://predict.cusf.co.uk/api/v1/"

# defining a params dict for the parameters to be sent to the API 
PARAMS = {'ascent_rate': 5.0,
          'burst_altitude': 30000.0,
          'descent_rate': 10.0,
          'launch_altitude': 0,
          'launch_datetime': '2019-08-11T23:00:00Z',
          'launch_latitude': 50.0,
          'launch_longitude': 0.01,
          'profile': 'standard_profile'           
}

# sending get request and saving the response as response object 
r = requests.get(url = URL, params = PARAMS) 

# extracting data in json format 
data = r.json() 
with open("data_file.json", "w") as write_file:
    json.dump(data, write_file)
    
print(data['prediction'][0]['trajectory'])

i = 0
latitudes = []
longitudes = []
altitudes = []
for x in data['prediction'][0]['trajectory']:
    print(x)
    """
    latitudes[i] = x['latitude']
    longitudes[i] = x['longitude']
    altitudes[i] = x['altitude']
    i = i + 1
    """
    
"""    
f = open("KML.txt", "w")
f.write("<KML_File>\n")
f.write("<Document>\n")
for line in List2:
    f.write("\t<Placemark>")
    f.write("\t\t<decription>" + str(row[0]) + "</description>")
    f.write("\t\t<Point>")
    f.write("\t\t\t<coordinates>" + str(row[2]) + str(row[1]) + "</coordinates>")
    f.write("\t\t</Point>")
    f.write("\t</Placemark>")
f.write("</Document>\n")
f.write("</kml>\n")
f.close()
"""    
#deserialized = json.dumps(data,indent=4)
#print(deserialized[0])

#latitude = data['prediction']['stage']['ascent']['trajectory']['latitude']

# printing the output 
#print("Latitude:%s" %(latitude)) 
