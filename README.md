# IPCOORD - IP Coordinator for dubious DHCP servers


The main objective of this code is to set up a RESTfull service for
managing names and IPs for computers accessible in the same network.

Tools used

- web.py
- python-mysql
- MySQL

### How to install it


* We are supposing that the user has installed `MySQL`, `python-mysql`
  and `web.py` packages

1. Create two tables, `users` and `mach_map` in MySQL:

   CREATE TABLE users (email VARCHAR(50) PRIMARY KEY, skey VARCHAR(30));
   CREATE TABLE mach_map (name VARCHAR(20), ip VARCHAR(20), skey VARCHAR(30), updated TIMESTAMP, KEY(name,skey));

2. Start the server

   python ipcoord.py 8080

3. Use `curl --request` to insert, get and delete machines and users (see API below)

### API

* User creation is done by sending a GET request to `/ipcoord/keygen` and sending an e-mail as main key.

  $ curl --request GET 'localhost:8080/ipcoord/keygen?email@lalala.com'
  iJ2xzSaF_TlI7s5kHynvudAVeEfhXU

* Machine insertion is done at route `/ipcoord`