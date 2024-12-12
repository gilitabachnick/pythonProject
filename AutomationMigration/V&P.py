from KalturaClient import *
from KalturaClient.Plugins.Core import *


# Function to compare views and plays
def compare_views_plays(id_1, id_2):
    print(f"Checking ID {id_1.id} (views: {id_1.views}, plays: {id_1.plays}) "
          f"with ReferenceID {id_2.id} (views: {id_2.views}, plays: {id_2.plays})")

    # Handle missing values (None or not set)
    if id_1.views is None or id_2.views is None:
        print(f"Warning: Views missing for ID {id_1.id} or ReferenceID {id_2.id}.")
    elif id_1.views != id_2.views:
        print(f"Error: Views mismatch for ID {id_1.id} and ReferenceID {id_2.id}. "
              f"Expected views: {id_2.views}, but got {id_1.views}.")

    if id_1.plays is None or id_2.plays is None:
        print(f"Warning: Plays missing for ID {id_1.id} or ReferenceID {id_2.id}.")
    elif id_1.plays != id_2.plays:
        print(f"Error: Plays mismatch for ID {id_1.id} and ReferenceID {id_2.id}. "
              f"Expected plays: {id_2.plays}, but got {id_1.plays}.")

    if id_1.views == id_2.views and id_1.plays == id_2.plays:
        print(f"ID {id_1.id} and ReferenceID {id_2.id} are identical in views and plays.")


# First API call to get IDs
config_1 = KalturaConfiguration()
config_1.serviceUrl = "https://www.kaltura.com/"
client_1 = KalturaClient(config_1)
ks_1 = client_1.generateSessionV2(
    "93197500f7977a4536d9857712b0a4be",
    "rcarpenter@kollective.com",
    KalturaSessionType.ADMIN,
    2908641
)
client_1.setKs(ks_1)

filter_1 = KalturaBaseEntryFilter()
pager_1 = KalturaFilterPager()
pager_1.pageSize = 50
pager_1.pageIndex = 1
result_1 = client_1.baseEntry.list(filter_1, pager_1)


# Second API call to get Reference IDs
config_2 = KalturaConfiguration()
config_2.serviceUrl = "https://www.kaltura.com/"
client_2 = KalturaClient(config_2)
ks_2 = client_2.generateSessionV2(
    "951da37fb871bf0646d6a1f6f33a14ff",
    "gili.tabachnick@kaltura.com",
    KalturaSessionType.ADMIN,
    5928002
)
client_2.setKs(ks_2)

filter_2 = KalturaBaseEntryFilter()
pager_2 = KalturaFilterPager()
pager_2.pageSize = 50
pager_2.pageIndex = 1
result_2 = client_2.baseEntry.list(filter_2, pager_2)



# Iterate through all entries in API 1 and compare with all entries in API 2
for entry_1 in result_1.objects:

    # Check if the entry from API 1 has a matching ReferenceID in API 2
    match_found = False
    for entry_2 in result_2.objects:
        if entry_1.id == entry_2.referenceId:
            print(f"Found match for ID {entry_1.id} and ReferenceID {entry_2.referenceId}.")
            compare_views_plays(entry_1, entry_2)
            match_found = True
            break  # Stop searching further once we find a match





