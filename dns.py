import os
import json
import base64
import requests
requests.packages.urllib3.disable_warnings()

class DNS(object):
	def __init__(self, config=None):
		if config is None:
			print('[E] No configuration filename not provided')
		else:
			self.load_configuration(config)
		return
	
	def load_configuration(self, config, params={}):
		if config == 'custom':
			'''
			Requires:
				host - WAPI Host
				username - SSO of user
				password - PIN + Token
			'''
			self.host = params['host']
			self.authenticate(connection_info)
			return
		config_file = 'configuration.json'
		path = os.path.abspath(__file__)
		dir_path = os.path.dirname(path)
		with open(f'{dir_path}/{config_file}','r') as f:
			raw_file = f.read()
		config_raw = json.loads(raw_file)
		if config not in config_raw['servers']:
			print('[E] Configuration not found in configuration.json')
		else:
			connection_info = config_raw['servers'][config]
			self.host = connection_info['host']
			#return connection_info
			#self.collector = connection_info['host']
			self.authenticate(connection_info)
		return
	
	def authenticate(self, connection_info):
		self.base_url = f'https://{self.host}/wapi/v2.9.1'
		self.session = requests.Session()
		self.session.trust_env = False
		_proxies = {
			'http':	'',
		}
		self.session.proxies = _proxies
		'''
		un_pw = f'{connection_info["username"]}:{connection_info["password"]}'.encode()
		un_pw_b64 = base64.b64encode(un_pw).decode()
		auth_headers = {
			'Authorization': f'Basic {un_pw_b64}'
		}
		self.session.headers.update(auth_headers)
		'''
		url = f'{self.base_url}/network?_max_results=1'
		response_raw = self.session.get(
			url,
			auth=(
				connection_info['username'],
				connection_info['password'],
			),
			verify=False,
		)
		return
	
	def get(self, method, params={}):
		url = f'{self.base_url}/{method}?'
		_params = {
			'_paging':	1,
			'_return_as_object':	1,
			'_max_results':	10000,
			'_return_fields+':	'extattrs',
		}
		if params:
			for key in params:
				_params[key] = params[key]
		#
		response_raw = self.session.get(
			url,
			#auth=(self.username,self.password),
			params=_params,
			verify=False,
		)
		if response_raw.status_code != 200:
			return {
				'success':	False,
				'result':	'',
				'response':	response_raw,
			}
		#
		data_raw = json.loads(response_raw.text)
		results = []
		if 'next_page_id' in data_raw:
			while 'next_page_id' in data_raw:
				results += data_raw['result']
				next_page_id = data_raw['next_page_id']
				_params['_page_id'] = next_page_id
				response_raw = self.session.get(
					url,
					#auth=(self.username,self.password),
					params=_params,
					verify=False,
				)
				data_raw = json.loads(response_raw.text)
				results += data_raw['result']
		else:
			results = data_raw['result']
		return {
			'success':	True,
			'result':	results,
			'response':	response_raw,
		}
		return
	
	def get_bare(self, method, params={}):
		# no extattrs
		url = f'{self.base_url}/{method}?'
		_params = {
			'_paging':	1,
			'_return_as_object':	1,
			'_max_results':	10000,
			#'_return_fields+':	'extattrs',
		}
		if params:
			for key in params:
				_params[key] = params[key]
		#
		response_raw = self.session.get(
			url,
			#auth=(self.username,self.password),
			params=_params,
			verify=False,
		)
		if response_raw.status_code != 200:
			return {
				'success':	False,
				'result':	'',
				'response':	response_raw,
			}
		#
		data_raw = json.loads(response_raw.text)
		results = []
		if 'next_page_id' in data_raw:
			while 'next_page_id' in data_raw:
				results += data_raw['result']
				next_page_id = data_raw['next_page_id']
				_params['_page_id'] = next_page_id
				response_raw = self.session.get(
					url,
					#auth=(self.username,self.password),
					params=_params,
					verify=False,
				)
				data_raw = json.loads(response_raw.text)
				results += data_raw['result']
		else:
			results = data_raw['result']
		return {
			'success':	True,
			'result':	results,
			'response':	response_raw,
		}
		return
	
	def get_network(self, network):
		response_raw = self.get(
			'network',
			params={
				'network':	network,
			}
		)
		return response_raw
	
	def get_network_fuzzy(self, network):
		response_raw = self.get(
			'network',
			params={
				'network~':	network,
			}
		)
		return response_raw
	
	def get_network_by_location(self, location):
		response_raw = self.get(
			'network',
			params={
				'*u_location_code':	location,
			}
		)
		return response_raw
	
	def get_network_addresses(self, network):
		response_raw = self.get(
			'ipv4address',
			params={
				'network':	network,
			}
		)
		return response_raw
	
	def get_address(self, address):
		response_raw = self.get(
			'ipv4address',
			params={
				'ip_address':	address,
			}
		)
		return response_raw
	
	def get_record_a_of_ip(self, address):
		response_raw = self.get(
			'record:a',
			params={
				'ipv4addr':	address,
			}
		)
		return response_raw
	
	def get_record_a_of_name(self, name):
		response_raw = self.get(
			'record:a',
			params={
				'name~':	name,
			}
		)
		return response_raw
	
	def get_zone(self, zone):
		response_raw = self.get_bare(
			'allrecords',
			params={
				'zone':	zone,
			},
		)
		return response_raw
	
	##
	## specific purpose
	##
	
	def get_network_of_ip(self, ip):
		r = self.get_address(ip)
		if r['success']:
			return r['result'][0]['network']
		else:
			return ''
		
if __name__ == '__main__':
	d = DNS('gm')
	
	zone = 'yoursite.com'
	#d.get_zone(zone)
