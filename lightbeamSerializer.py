import urllib.request, json 
from builtins import list
    

class LightBeamResult:
  def __init__(self):
    self.items = list()
  def add(self, item):
    self.items.append(item)
  def describe(self):
    for item in self.items:
        item.describe()            
  def toJSON(self):
    return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    
        
class FirstParty:
  def __init__(self, hostname, location, image):
    self.hostname = hostname
    self.location = location
    self.image = image
    self.thirdParties = list()    
  def addThirdParty(self, third_party):
    self.thirdParties.append(third_party)    
  def describe(self):
    print("[" + self.hostname + "]: " + str(len(self.thirdParties)) + " third parties")
    for thirdParty in self.thirdParties:
        if thirdParty != None:
            thirdParty.describe()

class ThirdParty:
  def __init__(self, hostname, location):
    self.hostname = hostname
    self.location = location    
  def describe(self):
    print("     	▹ " + self.location.to_string().ljust(40, ' ') + self.hostname)            

class Location:
  def __init__(self, country, country_code, lat, long, city):
    self.country = country
    self.country_code = country_code
    self.lat = lat
    self.long = long
    self.city = city    
  def to_string(self):
    if self.city != "":
        return self.city + ", " + self.country  + "(" + self.country_code + ")"
    else:
        return "Unknown"
    
    
    
    
    
def loadData():
    with urllib.request.urlopen("https://raw.githubusercontent.com/learning-things-123/reimagined-octo-bassoon/main/lightbeamData.json") as url:
        json_data = json.loads(url.read().decode())
        result = LightBeamResult()
        for key, entry in json_data.items():
            if entry['firstParty'] == True:
                website =  buildFirstParty(key, entry)
                result.add(website)
        return result
                
def buildFirstParty(hostname, node):
    location = fetchLocation(hostname)
    website = FirstParty(hostname, location, node['favicon'])
    for key in node['thirdParties']:
        thirdParty = buildThirdParty(key)
        website.addThirdParty(thirdParty)
    return website        

def buildThirdParty(hostname):
    location = fetchLocation(hostname)
    website = ThirdParty(hostname, location)
    return website

def fetchLocation(hostname):
    with urllib.request.urlopen("http://api.ipstack.com/" + hostname + "?access_key=76f1e6940e387f7c343d4798ac180697") as url:
        json_data = json.loads(url.read().decode())
        country = json_data['country_name'] or ""
        country_code = json_data['country_code'] or ""
        lat = json_data['latitude'] or ""
        long = json_data['longitude'] or ""
        city = json_data['city'] or ""
        return Location(country, country_code, lat, long, city)
        


#print(loadData().toJSON())
print(loadData().describe())
