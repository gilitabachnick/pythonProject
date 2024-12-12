from KalturaClient import *

config = KalturaConfiguration(PARTNER_ID)
config.serviceUrl = "https://admin.kaltura.com/"
client = KalturaClient(config)
filter = KalturaCategoryFilter()
pager = None
result = client.category.list(filter, pager)