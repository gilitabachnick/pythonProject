
from KalturaClient import *
from KalturaClient.Plugins.Core import *



def get_entry_list(client, entry_filter, pager):

    """
    Fetch a page of entries from the Kaltura API.
    """
    return client.baseEntry.list(entry_filter, pager).objects


config = KalturaConfiguration()
config.serviceUrl = "https://www.kaltura.com/"
client = KalturaClient(config)
ks = client.generateSessionV2(
      "df9eb5fb200fa6cf44bdd5510b2f7991",
      "edward.zhu@kaltura.com",
      KalturaSessionType.ADMIN,
      4979732)
client.setKs(ks)

filter = KalturaBaseEntryFilter()
pager = KalturaFilterPager()
pager.pageIndex = 24
pager.pageSize = 50

result = client.baseEntry.list(filter, pager)
results = {'objects': []}
for _ in range(100):
    # Fetch a page of entries
    entries_1 = get_entry_list(client, filter, pager)
print(entries_1)
