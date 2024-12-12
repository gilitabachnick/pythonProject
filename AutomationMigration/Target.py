from KalturaClient import *
from KalturaClient.Plugins.Core import *
from KalturaClient import KalturaConfiguration
from KalturaClient.Plugins.Core import KalturaFilterPager


# Kaltura API setup
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


# Define a helper function to fetch entries using the client and filter
def get_entry_list(client, entry_filter, pager):

    """
    Fetch a page of entries from the Kaltura API.
    """
    return client.baseEntry.list(entry_filter, pager).objects


# Pagination setup
filter_1 = KalturaBaseEntryFilter()  # Set your filter criteria if needed
pager = KalturaFilterPager()
pager.pageSize = 50  # Set the number of entries to fetch per page
pager.pageIndex = 1  # Start from the first page

# Fetch all entries
results = {'objects': []}

for _ in range(100):
    # Fetch a page of entries
    entries_1 = get_entry_list(client_1, filter_1, pager)

    # Add entries to results
    if entries_1:
        results['objects'].extend(entries_1)
    else:
        print("No more entries to fetch. Stopping.")
        break  # Stop if no entries are returned

    # Check if fewer than pageSize objects were returned
    if len(entries_1) < pager.pageSize:
        print("Reached the last page. Stopping.")
        break

    # Increment page index for the next API call

    # Debug output to show progress
    print(f"Page {pager.pageIndex} fetched. Total objects: {len(results['objects'])}")
    pager.pageIndex += 1

# Final output
print(f"Total entries fetched: {len(results['objects'])}")

# # First API call to get IDs
# config_1 = KalturaConfiguration()
# config_1.serviceUrl = "https://www.kaltura.com/"
# client_1 = KalturaClient(config_1)
# ks_1 = client_1.generateSessionV2(
#     "951da37fb871bf0646d6a1f6f33a14ff",
#     "gili.tabachnick@kaltura.com",
#     KalturaSessionType.ADMIN,
#     5928002
# )
# client_1.setKs(ks_1)

# Get all entries from API 1 (using pagination)
# filter_1 = KalturaBaseEntryFilter()
entries_1 = get_entry_list(client_1, filter_1, pager)

# # Extract the IDs from the first API call result
# ids_first_api = [entry.id for entry in result_1.objects]
#
# # Second API call to get ReferenceIDs (keeping it unchanged)
# config_2 = KalturaConfiguration()
# config_2.serviceUrl = "https://www.kaltura.com/"
# client_2 = KalturaClient(config_2)
# ks_2 = client_2.generateSessionV2(
#     "aa986464f64e7d6445ae8cc81fa43141",  # Your first API key
#     "tobrien8@bloomberg.net",  # Your first email
#     KalturaSessionType.ADMIN,  # Session Type
#     5721612  # Partner ID
# )
# client_2.setKs(ks_2)
#
# filter_2 = KalturaBaseEntryFilter()
# pager_2 = KalturaFilterPager()
#
# result_2 = client_2.baseEntry.list(filter_2, pager_2)
#
# # Extract the ReferenceIDs from the second API call result
# reference_ids_second_api = [entry.referenceId for entry in result_2.objects]
#
# # Compare and check if any id matches referenceId
# matching_found = False
# for id_value in ids_first_api:
#     if id_value in reference_ids_second_api:
#         print(f"Matching ID found: {id_value}")
#         matching_found = True
#
# # If no match is found, print this message
# if not matching_found:
#     print("No matching IDs found.")
