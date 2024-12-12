from KalturaClient import *
from KalturaClient.Plugins.Core import *
import time
import os
import configparser
from datetime import datetime


def get_entry_list(client, cat_id=0):
    entries = {}
    counter = 1
    dots_array = []
    pager = KalturaFilterPager()
    pager.page_size = 50  # Correct argument name is `page_size` not `pageSize`

    # Create the media entry filter
    filter = KalturaMediaEntryFilter()
    filter.status_in = "2"  # Define the statuses for the filter
    filter.order_by = "-createdAt"  # Sort by created date, descending
    results = client.media.list(filter, pager)
    cont = True
    last_created_at = 0
    last_entry_ids = ""
    for entry in results.objects:
        entries[entry.id] = entry
        if last_created_at != entry.createdAt:
            last_entry_ids = ""

        if last_entry_ids:
            last_entry_ids += ","
        last_entry_ids += entry.id
        last_created_at = entry.createdAt
        counter += 1

        # Print progress
        print(f"\rBuilding list of entries ({counter}) {''.join(dots_array)}", end="")
        dots_array.append(".")
        if len(dots_array) > 5:
            dots_array = []

    return entries


# First API call to get IDs
config_1 = KalturaConfiguration()
config_1.serviceUrl = "https://www.kaltura.com/"
client_1 = KalturaClient(config_1)
ks_1 = client_1.generateSessionV2(
    "df9eb5fb200fa6cf44bdd5510b2f7991",
    "edward.zhu@kaltura.com",
    KalturaSessionType.ADMIN,
    4979732
)
client_1.setKs(ks_1)
# filter_1 = KalturaBaseEntryFilter()
# pager_1 = KalturaFilterPager()
# pager_1.pageSize = 100
# pager_1.pageIndex = 1
entries_1 = get_entry_list(client_1)
print(entries_1)

# # Second API call to get Reference IDs
# config_2 = KalturaConfiguration()
# config_2.serviceUrl = "https://www.kaltura.com/"
# client_2 = KalturaClient(config_2)
# ks_2 = client_2.generateSessionV2(
#     "951da37fb871bf0646d6a1f6f33a14ff",
#     "gili.tabachnick@kaltura.com",
#     KalturaSessionType.ADMIN,
#     5928002
# )
# client_2.setKs(ks_2)
#
# filter_2 = KalturaBaseEntryFilter()
# pager_2 = KalturaFilterPager()
# pager_2.pageSize = 100
# pager_2.pageIndex = 1
# entries_2 = get_entry_list(client_2, filter_2)




