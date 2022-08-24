# Infoblox WAPI Framework

This is a framework that connects to the API of an Infoblox DDI appliance.

## Authentication

Credentials are stored in JSON format, in the same directory as the `bigiq.py` file. The name of the file should be `credentials.json`.

Other authentication methods, such as KDBX, have been tested, but this way it keeps the hard-coded passwords out of the source code.

```
{
	"servers":	{
		"arbitrary_name":	{
			"host": "",
			"username": "",
			"password": ""
		}
	}
}
```

The name of the credentials is arbitrary and references parameters for hostname/ip, username, and password.

API calls will be made to `https://` + host.

Authenticate occurs automatically upon instantiation of the object.

## Getting Started

To instantiate a `DNS` object, pass a string of the credential name created in the "Authentication" section :

```
>>> credential_name = 'arbitrary_name'
>>> d = DNS(credential_name)
```

## WAPI Features

As of the most recent update to the main `dns.py`, grabbing lists of A Records list of IPAM networks are the only features written.

To add a specific type of record to traverse, modify the GET URI path according to the record type. Available types are :
- allrecords    ( !!! Retrieves entire Zone !!! see below )
- record:a
- record:cname
- record:txt
- etc.

```
>>> record_type = 'record:cname'
>>> data = d.get(record_type, params={})
```

To dump the entire Zone :

```
>>> zone = 'yoursite.com'
>>> data = d.get_zone(zone)
```

To find an A Record by IP address :

```
>>> ip = '192.168.1.100'
>>> data = d.get_record_a_of_ip(ip)
```

To find all network assignments under a known super-network :

```
>>> network = '192.168.0.0/24'
>>> data = d.get_network(network)
```

To find all network assignments under a super-network where only a few octets are known :

```
>>> network = '192.'
>>> data = d.get_network_fuzzy(network)
```

To find all IPv4 addresses under a known network :

```
>>> network = '192.168.0.0/24'
>>> data = d.get_network_addresses(network)
```