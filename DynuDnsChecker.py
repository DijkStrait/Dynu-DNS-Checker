#Creado por DijkStrait
#01/03/2020

import requests
import json
from time import sleep

def main(pool_interval,key,domain):
	print '[INFO] Obtaining the actual IP.'
	actual_IP = getIP()
	print '[INFO] The actual IP is %s' % actual_IP
	print '[INFO] Trying to update the IP for the first time.'
	if actual_IP != '0':
		changeIP(actual_IP,key,domain)
	while(True):
		sleep(pool_interval)#Comprobamos la IP cada 30 segundos
		new_IP = getIP()
		if new_IP != '0' and new_IP != actual_IP:
			actual_IP = new_IP
			print '[INFO] The IP has changed, updating.'
			changeIP(actual_I,key,domain)	
		
def getIP():
	try:
		r = requests.get('https://api.myip.com',headers={'Accept': 'application/json'})
		IP = json.loads(r.text)['ip']
		return IP
	except Exception:
		print '[ERROR] Error connecting to myip.com.'
		return '0'
	
def changeIP(ip,key,domain):
	key = key
	host = 'https://api.dynu.com/v2/'
	
	header = {'Accept': 'application/json','API-Key': key}
	#Obtenemos el id del dominio
	r = requests.get(host+'dns',headers=header)
	if r.status_code == 200:
		respuesta = json.loads(r.text)
		for dominio in respuesta['domains']:
			if dominio['unicodeName'] == domain:
				id = str(dominio['id'])
				old_IP = dominio['ipv4Address']
				print "[INFO] The ID of the domain is %s, trying to update the IP." % (id)
				datos = dominio
	else:
		print '[ERROR] Error trying to connect to Dynu.'
		return False
	if old_IP == ip:
		print '[INFO] The IP does not need to be updated.'
		return True
	datos['ipv4Address'] = ip
	r = requests.post(host+'dns/'+id,data=json.dumps(datos),headers=header)
	if r.status_code == 200:
		print '[SUCCESS] The IP has been updated successfully'
		return True
	else:
		print '[ERROR] Error updating the IP.'
		return False

if __name__ == "__main__":
	print "--------------Dynu DNS Checker--------------"
	sleep(1)
	print "[INFO] Reading configuration file."
	try:
		f = open("config.conf", "r")
	except FileNotFoundError:
		print "[ERROR] Error opening the file, aborting."
		exit(1)
	key = f.readline().replace('key:','').strip()
	domain = f.readline().replace('domain:','').strip()
	pool_interval = f.readline().replace('pool_interval:','').strip()
	f.close()
	main(int(pool_interval),key,domain)