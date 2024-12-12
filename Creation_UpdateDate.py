from KalturaClient import *
from KalturaClient.Plugins.Core import *


def compare_creation_update(entry_a, entry_b):
    if str(entry_a.createdAt) == str(entry_b.createdAt):
        print(f"the creation date matches: {entry_a.createdAt} ")
    else:
        print(f"Error: creation date mismatch for ID {entry_a.id} and ReferenceID {entry_b.id}. "
              f"Expected creation date: {entry_a.createdAt}, but got: {entry_b.createdAt}.")
    if str(entry_a.updatedAt) == str(entry_b.updatedAt):
        print(f"the update date matches: {entry_a.updatedAt} ")
    else:
        print(f"Error: update date mismatch for ID {entry_a.id} and ReferenceID {entry_b.id}. "
              f"Expected update date: {entry_a.updatedAt}, but got: {entry_b.updatedAt}.")


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
client_1.setKs("djJ8MjkwODY0MXxvWeksUOVyoyOWxrq8psNuzN1C5s9Mr5EnajcD88LYhAJotq3FRJ8Dhvc90HP9rgVvK-o2rDtA_SMSQ8j8bK5soulC0OVe5zsSiD-yvAkkz6IR7AVS-mr1WHcuwrg8pHUQrFqlsxj0mQl1YSrowhFs")

# Get all entries from API 1 (using pagination)
filter_1 = KalturaBaseEntryFilter()
entries_1 = get_entry_list(client_1, filter_1)


# Second API call to get Reference IDs
config_2 = KalturaConfiguration()
config_2.serviceUrl = "https://www.kaltura.com/"
client_2 = KalturaClient(config_2)
client_2.setKs("djJ8NTkyODAwMnz4jCjBJ3coI-m0wsActRKFcbNtzyRRwWDbskkrzk7mbVJ2mez5_SjRJWVu-s6sa731SwHziXo9Czep4sdZvAOAlHWcLSH8oOUcRU6z4Fj7T_4BOLCRX_gI4mvT_-GKVSL1EypnEVfTl-rtXpSKjudlaSOUiHXsF3qVPtM9Sec6HA")

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
            compare_creation_update(entry_1, entry_2)
            match_found += 1
            break

print(f"Total matches found: {match_found}")
