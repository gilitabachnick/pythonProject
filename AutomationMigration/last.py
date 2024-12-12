import string

from KalturaClient import *
from KalturaClient.Plugins.Core import *

# First API call to get IDs
config_1 = KalturaConfiguration()
config_1.serviceUrl = "https://www.kaltura.com/"
client_1 = KalturaClient(config_1)
# ks_1 = client_1.generateSessionV2(
#     "93197500f7977a4536d9857712b0a4be",  # Your first API key
#     "rcarpenter@kollective.com",  # Your first email
#     KalturaSessionType.ADMIN,  # Session Type
#     2908641  # Partner ID
# )
client_1.setKs("djJ8MjkwODY0MXzqqUqMwLqS3ceC8NOM9KhvvMVBSUxwd9FV4-kmIbaWyXl7yswwIWC2p4IpYRIIOJRu3qM4XFPmWfweTjtQaLDe-Xkdkj7U1QPgsXAieTHjXxA_H00_je_10dyFU0xLmMNUnkvx083Sm9t3xjar6JYj")

filter_1 = KalturaBaseEntryFilter()
# filter_1.statusEqual = string.READY
pager_1 = KalturaFilterPager()
pager_1.pageIndex = 1
pager_1.pageSize = 50  # Set the page size here (e.g., 50 entries per page)

# Fetch all entries from API call 1
result_1 = []
while True:
    current_page = client_1.baseEntry.list(filter_1, pager_1)
    result_1.extend(current_page.objects)
    if current_page.totalCount <= pager_1.pageIndex * pager_1.pageSize:
        break
    pager_1.pageIndex += 1

# Second API call to get referenceId, views, and plays
config_2 = KalturaConfiguration()
config_2.serviceUrl = "https://www.kaltura.com/"
client_2 = KalturaClient(config_2)
# ks_2 = client_2.generateSessionV2(
#     "951da37fb871bf0646d6a1f6f33a14ff",  # Your second API key
#     "gili.tabachnick@kaltura.com",  # Your second email
#     KalturaSessionType.ADMIN,  # Session Type
#     5928002  # Partner ID
# )
client_2.setKs("djJ8NTkyODAwMnxlAmfX9QDpe5pmEEwC__f6ruJJCOVN2CIbk2U45U0IjDrzmMHiwOX1A05znS5migItHPlcwpkDa9iuyddPH-AI3NdM5VleDfUnZFf2FbGP4wWy5LzIlsVARlpkidFREbue3oeyNYdd2D-nwz6fk6NdbFJWwZeeGaSrV0Tb5cAPsA")

filter_2 = KalturaBaseEntryFilter()
pager_2 = KalturaFilterPager()
pager_2.pageIndex = 1
pager_2.pageSize = 50  # Set the page size for second API call as well

# Fetch all entries from API call 2
result_2 = []
while True:
    current_page_2 = client_2.baseEntry.list(filter_2, pager_2)
    result_2.extend(current_page_2.objects)
    if current_page_2.totalCount <= pager_2.pageIndex * pager_2.pageSize:
        break
    pager_2.pageIndex += 1

# Create a dictionary for easy lookup of referenceId in API Call 2
reference_data = {}
for entry_2 in result_2:
    reference_data[entry_2.referenceId] = {
        'views': getattr(entry_2, 'views', None),
        'plays': getattr(entry_2, 'plays', None)
    }


# Function to compare views and plays between entries from two API calls
def compare_views_and_plays(id_1, reference_id_2):
    # Check if the referenceId exists in API Call 2
    if reference_id_2 in reference_data:
        print(f"Found match: {id_1} == {reference_id_2}")

        # Access views and plays for entry_2
        views_2 = reference_data[reference_id_2].get('views')
        plays_2 = reference_data[reference_id_2].get('plays')

        if views_2 is None or plays_2 is None:
            print(f"Error: Views or plays missing for referenceId {reference_id_2}")
            return

        print(f"Reference {reference_id_2} - Views: {views_2}, Plays: {plays_2}")

        # Find the corresponding entry in result_1
        for entry_1 in result_1:
            if entry_1.id == id_1:
                views_1 = getattr(entry_1, 'views', None)
                plays_1 = getattr(entry_1, 'plays', None)

                if views_1 is None or plays_1 is None:
                    print(f"Error: Views or plays missing for id {id_1}")
                    return

                print(f"Entry {id_1} - Views: {views_1}, Plays: {plays_1}")

                # Compare the views and plays
                if views_1 != views_2 or plays_1 != plays_2:
                    print(f"Error: Mismatch for ID {id_1} and Reference ID {reference_id_2}.")
                    print(f"Expected Views: {views_2}, Plays: {plays_2} but found Views: {views_1}, Plays: {plays_1}")
                    return
                else:
                    print(f"Match found! Views and Plays are the same for ID {id_1} and Reference ID {reference_id_2}.")
                    return
    else:
        print(f"No match found for referenceId {reference_id_2}.")


# Iterate through the list of entries from API call 1 and compare them with API call 2
found_matches = 0
found_nomatches = 0
for entry_1 in result_1:
    id_1 = entry_1.id
    found_match = False

    # Check if the ID matches the Reference ID in the lookup dictionary
    if id_1 in reference_data:
        print(f"ID {id_1} matches Reference ID {id_1}.")
        compare_views_and_plays(id_1, id_1)
        found_matches += 1
        found_match = True

    if not found_match:
        found_nomatches += 1


print(f"Total matches found: {found_matches}")
print(f"No match found for: {found_nomatches} ")
