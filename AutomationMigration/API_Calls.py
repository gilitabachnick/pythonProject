from KalturaClient import *
from KalturaClient.Plugins.Core import *

# Function to compare views and plays with additional checks
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
    "df9eb5fb200fa6cf44bdd5510b2f7991",  # Your session key
    "edward.zhu@kaltura.com",  # Your email
    KalturaSessionType.ADMIN,  # Session Type
    4979732  # Partner ID
)
client_1.setKs(ks_1)

filter_1 = KalturaBaseEntryFilter()
pager_1 = KalturaFilterPager()
pager_1.pageSize = 1000
result_1 = client_1.baseEntry.list(filter_1, pager_1)

# Second API call to get Reference IDs
config_2 = KalturaConfiguration()
config_2.serviceUrl = "https://www.kaltura.com/"
client_2 = KalturaClient(config_2)
ks_2 = client_2.generateSessionV2(
    "951da37fb871bf0646d6a1f6f33a14ff",  # Your session key for API 2
    "gili.tabachnick@kaltura.com",  # Your email for API 2
    KalturaSessionType.ADMIN,  # Session Type
    5928002  # Partner ID
)
client_2.setKs(ks_2)

filter_2 = KalturaBaseEntryFilter()
pager_2 = KalturaFilterPager()
pager_2.pageSize = 1000
result_2 = client_2.baseEntry.list(filter_2, pager_2)

# Retrieve all reference IDs from API Call 2 into a set for fast lookup
reference_ids_set = set(entry.referenceId for entry in result_2.objects)

# Track processed IDs to avoid duplicate comparisons
processed_ids = set()

# Match entries from result_1 with referenceId's from result_2
for entry_1 in result_1.objects:
    # Ensure each entry_1 is only processed once
    if entry_1.id not in processed_ids and entry_1.id in reference_ids_set:
        matching_entry_2 = next(entry for entry in result_2.objects if entry.referenceId == entry_1.id)
        compare_views_plays(entry_1, matching_entry_2)
        processed_ids.add(entry_1.id)  # Mark this entry as processed


