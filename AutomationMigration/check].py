from KalturaClient import *
from KalturaClient.Plugins.Core import *

# First API call to get IDs
config_1 = KalturaConfiguration()
config_1.serviceUrl = "https://www.kaltura.com/"
client_1 = KalturaClient(config_1)
ks_1 = client_1.generateSessionV2(
    "df9eb5fb200fa6cf44bdd5510b2f7991",  # Your first API key
    "edward.zhu@kaltura.com",  # Your first email
    KalturaSessionType.ADMIN,  # Session Type
    4979732  # Partner ID
)
client_1.setKs(ks_1)

filter_1 = KalturaBaseEntryFilter()
pager_1 = KalturaFilterPager()
pager_1.pageIndex = 1
pager_1.pageSize = 500

result_1 = client_1.baseEntry.list(filter_1, pager_1)

# Second API call to get referenceId, views, and plays
config_2 = KalturaConfiguration()
config_2.serviceUrl = "https://www.kaltura.com/"
client_2 = KalturaClient(config_2)
ks_2 = client_2.generateSessionV2(
    "951da37fb871bf0646d6a1f6f33a14ff",  # Your second API key
    "gili.tabachnick@kaltura.com",  # Your second email
    KalturaSessionType.ADMIN,  # Session Type
    5928002  # Partner ID
)
client_2.setKs(ks_2)

filter_2 = KalturaBaseEntryFilter()
pager_2 = KalturaFilterPager()
pager_2.pageIndex = 1
pager_2.pageSize = 500

result_2 = client_2.baseEntry.list(filter_2, pager_2)


# Function to compare views and plays between entries from two API calls
def compare_views_and_plays(id_1, reference_id_2):
    # Find the entry in result_2 that matches referenceId (reference_id_2)
    for entry_2 in result_2.objects:
        if entry_2.referenceId == reference_id_2:
            print(f"Found match: {id_1} == {reference_id_2}")

            # Access views and plays for entry_2
            views_2 = getattr(entry_2, 'views', None)
            plays_2 = getattr(entry_2, 'plays', None)

            if views_2 is None or plays_2 is None:
                print(f"Error: views or plays missing for referenceId {reference_id_2}")
                return

            print(f"Reference {reference_id_2} - Views: {views_2}, Plays: {plays_2}")

            # Now, find the corresponding entry in result_1
            for entry_1 in result_1.objects:
                if entry_1.id == id_1:
                    views_1 = getattr(entry_1, 'views', None)
                    plays_1 = getattr(entry_1, 'plays', None)

                    if views_1 is None or plays_1 is None:
                        print(f"Error: views or plays missing for id {id_1}")
                        return

                    print(f"Entry {id_1} - Views: {views_1}, Plays: {plays_1}")

                    # Compare the views and plays only if id matches referenceId
                    if views_1 != views_2 or plays_1 != plays_2:
                        print(f"Error: Mismatch for ID {id_1} and Reference ID {reference_id_2}.")
                        print(f"Expected Views: {views_2}, Plays: {plays_2} but found Views: {views_1}, Plays: {plays_1}")
                        return
                    else:
                        print(f"Match found! Views and Plays are the same for ID {id_1} and Reference ID {reference_id_2}.")
                        return

    # If no match is found for reference_id_2
    print(f"No match found for referenceId {reference_id_2} with id {id_1}.")


# Iterate through the list of entries from API call 1 and compare them with API call 2
for entry_1 in result_1.objects:
    found_match = False
    for entry_2 in result_2.objects:
        # Check if ID matches Reference ID
        if entry_1.id == entry_2.referenceId:
            print(f"ID {entry_1.id} matches Reference ID {entry_2.referenceId}.")
            compare_views_and_plays(entry_1.id, entry_2.referenceId)
            found_match = True
            break  # No need to check further entries once we've found a match

    if not found_match:
        print(f"No match found for ID {entry_1.id} in API Call 2.")

