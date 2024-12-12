from KalturaClient import *
from KalturaClient.Plugins.Core import *

# Function to compare views and plays with additional checks
def compare_views_plays(entry_1, entry_2):
    print(f"Checking ID {entry_1.id} (views: {entry_1.views}, plays: {entry_1.plays}) "
          f"with ReferenceID {entry_2.id} (views: {entry_2.views}, plays: {entry_2.plays})")

    # Handle missing values (None or not set)
    if entry_1.views is None or entry_2.views is None:
        print(f"Warning: Views missing for ID {entry_1.id} or ReferenceID {entry_2.id}.")
    elif entry_1.views != entry_2.views:
        print(f"Error: Views mismatch for ID {entry_1.id} and ReferenceID {entry_2.id}. "
              f"Expected views: {entry_2.views}, but got {entry_1.views}.")

    if entry_1.plays is None or entry_2.plays is None:
        print(f"Warning: Plays missing for ID {entry_1.id} or ReferenceID {entry_2.id}.")
    elif entry_1.plays != entry_2.plays:
        print(f"Error: Plays mismatch for ID {entry_1.id} and ReferenceID {entry_2.id}. "
              f"Expected plays: {entry_2.plays}, but got {entry_1.plays}.")

    if entry_1.views == entry_2.views and entry_1.plays == entry_2.plays:
        print(f"ID {entry_1.id} and ReferenceID {entry_2.id} are identical in views and plays.")


# Corrected get_entry_list function with pagination logic
def get_entry_list(client, filter=None):
    if not filter:
        filter = KalturaBaseEntryFilter()  # Initialize filter if not provided

    entries = []
    pager = KalturaFilterPager()
    pager.page_index = 1
    pager.page_size = 100  # Fetch 100 entries per page

    try:
        while True:
            results = client.baseEntry.list(filter, pager)  # Fetch entries using pagination
            if results.totalCount > 0:
                entries.extend(results.objects)  # Add the entries to the list
                # If there are fewer than 100 objects, we've reached the last page
                if len(results.objects) < 100:
                    break
            else:
                print("No entries found")

            pager.page_index += 1  # Move to the next page

    except Exception as e:
        print(f"Error: {str(e)}")

    return entries


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
entries_1 = get_entry_list(client_1, filter_1)  # Fetch all entries from API 1

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
entries_2 = get_entry_list(client_2, filter_2)  # Fetch all entries from API 2

# Retrieve all reference IDs from API Call 2 into a set for fast lookup
reference_ids_set = set(entry.referenceId for entry in entries_2 if entry.referenceId)

# Track processed IDs to avoid duplicate comparisons
processed_ids = set()

# Match entries from entries_1 with referenceId's from entries_2
for entry_1 in entries_1:
    # Ensure each entry_1 is only processed once
    if entry_1.id not in processed_ids and entry_1.id in reference_ids_set:
        matching_entry_2 = next(entry for entry in entries_2 if entry.referenceId == entry_1.id)
        compare_views_plays(entry_1, matching_entry_2)
        processed_ids.add(entry_1.id)  # Mark this entry as processed
