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
              f"Expected views: {id_1.views}, but got {id_2.views}.")

    if id_1.plays is None or id_2.plays is None:
        print(f"Warning: Plays missing for ID {id_1.id} or ReferenceID {id_2.id}.")
    elif id_1.plays != id_2.plays:
        print(f"Error: Plays mismatch for ID {id_1.id} and ReferenceID {id_2.id}. "
              f"Expected plays: {id_1.plays}, but got {id_2.plays}.")

    if id_1.views == id_2.views and id_1.plays == id_2.plays:
        print(f"ID {id_1.id} and ReferenceID {id_2.id} are identical in views and plays.")


# Function to get a list of entries with pagination
def get_entry_list(client, filter=None):
    if not filter:
        filter = KalturaBaseEntryFilter()  # Initialize filter if not provided

    entries = []
    pager = KalturaFilterPager()
    pager.pageIndex = 1
    pager.pageSize = 50  # Fetch 50 entries per page
    results = client.baseEntry.list(filter, pager)


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


# First API call to get IDs
config_1 = KalturaConfiguration()
config_1.serviceUrl = "https://www.kaltura.com/"
client_1 = KalturaClient(config_1)
client_1.setKs("djJ8MjkwODY0MXyv4DQYjdAThsd_7VavTzEHe00-epkcj0MSfVC_qrEAy-GdBnY0x59a6qIgpYTHiZeZB2xgZPvy2KL7StIexfaLSgbIBNqcdX6UhtWEABNWupdDZl8l4M6cr6EU4r01gxUHJ13-9aLGxvuASoakJTBG")

# Get all entries from API 1 (using pagination)
filter_1 = KalturaBaseEntryFilter()
entries_1 = get_entry_list(client_1, filter_1)


# Second API call to get Reference IDs
config_2 = KalturaConfiguration()
config_2.serviceUrl = "https://www.kaltura.com/"
client_2 = KalturaClient(config_2)
client_2.setKs("djJ8NTkyODAwMnx4TEj2fbXkMKsFmxiN8aZIcOuwNE-qEtLouOOWkoLMeh2fjSve9QseuSaw24x8alu2gZ4oTRrAR_7WfYn2ze-nZ5JEsBch2OM8s6EUIYOoKfTaoMdyEuVy9SszuQdAHdv6jvv7Q8TxEJXcbMePP7OVISGUUhYRm1K73bj0JvoF9A")

# Get all entries from API 2 (using pagination)
filter_2 = KalturaBaseEntryFilter()
entries_2 = get_entry_list(client_2, filter_2)


# Iterate through all entries in API 1 and compare with all entries in API 2
match_found = 0

for entry_1 in entries_1:
    # Check if the entry from API 1 has a matching ReferenceID in API 2

    for entry_2 in entries_2:
        if entry_1.id == entry_2.referenceId:
            print(f"Found match for ID {entry_1.id} and ReferenceID {entry_2.referenceId}.")
            compare_views_plays(entry_1, entry_2)
            match_found += 1
            break  # Stop searching further once we find a match

print(f"Total matches found: {match_found}")




