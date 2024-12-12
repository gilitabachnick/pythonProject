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


# Function to get all entries from the API
def get_all_entries(client, filter=None):
    entries = []
    pager = KalturaFilterPager()
    pager.pageSize = 50

    try:
        while True:
            results = client.baseEntry.list(filter, pager)  # Fetch entries using pagination
            if results.totalCount > 0:
                entries.extend(results.objects)  # Add the entries to the list
                # If there are fewer than 50 objects, we've reached the last page
                if len(results.objects) < 50:
                    break
            else:
                print("No entries found")
                return []

            pager.pageIndex += 1  # Move to the next page

    except Exception as e:
        print(f"Error: {str(e)}")
        return []

    return entries


# First API call to get IDs (entries from API 1)
config_1 = KalturaConfiguration()
config_1.serviceUrl = "https://www.kaltura.com/"
client_1 = KalturaClient(config_1)
# ks_1 = client_1.generateSessionV2(
#     "df9eb5fb200fa6cf44bdd5510b2f7991",  # Your session key
#     "edward.zhu@kaltura.com",  # Your email
#     KalturaSessionType.ADMIN,  # Session Type
#     4979732  # Partner ID
# )
client_1.setKs("djJ8MjkwODY0MXzqqUqMwLqS3ceC8NOM9KhvvMVBSUxwd9FV4-kmIbaWyXl7yswwIWC2p4IpYRIIOJRu3qM4XFPmWfweTjtQaLDe-Xkdkj7U1QPgsXAieTHjXxA_H00_je_10dyFU0xLmMNUnkvx083Sm9t3xjar6JYj")
filter_1 = KalturaBaseEntryFilter()
result_1 = get_all_entries(client_1, filter_1)  # Retrieve all entries from API 1


# Second API call to get Reference IDs (entries from API 2)
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
result_2 = get_all_entries(client_2, filter_2)  # Retrieve all entries from API 2

# Track processed IDs to avoid duplicate comparisons
processed_ids = set()

# Flag to check if we find a match
no_match_found = set()

# 1. Print the list of all IDs from API 1
# print("List of all IDs from API 1 to be checked against Reference IDs:")
# for entry_1 in result_1:
#     print(f"ID: {entry_1.id}")
#
# # 2. Print the list of all Reference IDs from API 2
# print("\nList of all ReferenceIDs from API 2:")
# for entry_2 in result_2:
#     print(f"ReferenceID: {entry_2.referenceId}")

# 3. Match entries from result_1 with referenceId's from result_2
for entry_1 in result_1:
    match_found = False  # Reset match found flag for each entry_1

    # Compare current entry_1's id with every referenceId in result_2
    for entry_2 in result_2:
        if entry_1.id == entry_2.referenceId:
            compare_views_plays(entry_1, entry_2)
            processed_ids.add(entry_1.id)  # Mark this entry as processed
            match_found = True
            break  # Exit once a match is found

    # If no match was found, track it
    if not match_found:
        no_match_found.add(entry_1.id)

# # Log any IDs from API 1 that had no corresponding referenceId in API 2
# if no_match_found:
#     print(f"\nNo matches found for the following IDs from API 1 in Reference IDs from API 2:")
#     for missing_id in no_match_found:
#         print(f"Missing ReferenceID: {missing_id}")
# else:
#     print("All entries from API 1 have matching Reference IDs in API 2.")


