import requests

url = 'http://addresses.loyce.club/Bitcoin_addresses_LATEST.txt.gz'

myfile = requests.get(url)

open('btc_latest.txt.gz', 'wb').write(myfile.content)
