import grequests
import json
# port should be [80,81,82,83] or [21,80,3306]
class portscan:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.result=[]
    def scan(self):
        tasks = [grequests.post("http://tools.hexlt.org/api/portscan", json={"ip": self.address, "port": port}) for port
                 in self.port]
        res = grequests.map(tasks, size=30)
        for i in res:
            result = json.loads(i.text)
            if result['status']:
                self.result.append(result['port'])
        return self.result

print (portscan("localhost",[21,80,81,888,443,5000,8000]).scan())
