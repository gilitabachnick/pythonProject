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
# ks_1 = client_1.generateSessionV2(
#     "93197500f7977a4536d9857712b0a4be",  # Your session key
#     "rcarpenter@kollective.com",  # Your email
#     KalturaSessionType.ADMIN,  # Session Type
#     2908641  # Partner ID
# )
client_1.setKs("djJ8MjkwODY0MXwbXyxCypgDZCKpYoBw_BmehjX6uow3a07KXewhZvoV6rGh4PMl6PgJ6zDTFNZxC3GTaJ0js32ZGVLV7mn4j0OHkrZiW2OBFQdaomB_JqHPnVlIuMgM7yVtkgv5opNLHovzQqOkCFiUYxv9MFc9Hg0L")

filter_1 = KalturaBaseEntryFilter()
pager_1 = KalturaFilterPager()
pager_1.pageSize = 50
pager_1.pageIndex = 1
result_1 = client_1.baseEntry.list(filter_1, pager_1)

# Second API call to get Reference IDs
config_2 = KalturaConfiguration()
config_2.serviceUrl = "https://www.kaltura.com/"
client_2 = KalturaClient(config_2)
# ks_2 = client_2.generateSessionV2(
#     "951da37fb871bf0646d6a1f6f33a14ff",  # Your session key for API 2
#     "gili.tabachnick@kaltura.com",  # Your email for API 2
#     KalturaSessionType.ADMIN,  # Session Type
#     5928002  # Partner ID
# )
client_2.setKs("djJ8NTkyODAwMnxb_A7TjTmTrj_z3691cxNBwVkDauX9q_-Kid1nU97kt3il-R9gPJskEM5nroN_vSq3aIhqAEQodMcvJ6H7W-t1STllLZz3DBcDMoYFHKVMHovbo4_G-mb-wE04QroCHXs0ZOBIwCumeYaNKfUhf11SqTJcuQIqRV7x9yuU6MIRFg")

filter_2 = KalturaBaseEntryFilter()
pager_2 = KalturaFilterPager()
pager_2.pageSize = 50
pager_2.pageIndex = 1
result_2 = client_2.baseEntry.list(filter_2, pager_2)

# Retrieve all reference IDs from API Call 2 into a set for fast lookup
reference_ids_set = set(entry.referenceId for entry in result_2.objects)

# Track processed IDs to avoid duplicate comparisons
processed_ids = set()

# Match entries from result_1 with referenceId's from result_2
while True:
    for entry_1 in result_1.objects:
        # Ensure each entry_1 is only processed once
        if entry_1.id not in processed_ids and entry_1.id in reference_ids_set:
            matching_entry_2 = next(entry for entry in result_2.objects if entry.referenceId == entry_1.id)
            compare_views_plays(entry_1, matching_entry_2)
            processed_ids.add(entry_1.id)  # Mark this entry as processed

    # Check if there are more pages for API call 1
    if len(result_1.objects) < pager_1.pageSize:
        break  # Exit the loop if no more pages are available
    else:
        pager_1.pageIndex += 1
        result_1 = client_1.baseEntry.list(filter_1, pager_1)

# Reset processed IDs for second API call
processed_ids = set()

# Pagination for API call 2
while True:
    for entry_2 in result_2.objects:
        # Ensure each entry_2 is processed only once
        if entry_2.referenceId not in processed_ids and entry_2.referenceId in processed_ids:
            matching_entry_1 = next(entry for entry in result_1.objects if entry.id == entry_2.referenceId)
            compare_views_plays(matching_entry_1, entry_2)
            processed_ids.add(entry_2.referenceId)  # Mark this entry as processed

    # Check if there are more pages for API call 2
    if len(result_2.objects) < pager_2.pageSize:
        break  # Exit the loop if no more pages are available
    else:
        pager_2.pageIndex += 1
        result_2 = client_2.baseEntry.list(filter_2, pager_2)



