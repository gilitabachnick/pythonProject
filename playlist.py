from KalturaClient import *
from KalturaClient.Plugins.Core import *


def compare_metadata(playlist_a, playlist_b):
    if str(playlist_a.name) == str(playlist_b.name):
        print(f"the Name is {playlist_a.name}")
    else:
        print(f"Error: name mismatch for ID {playlist_a.id} and ReferenceID {playlist_b.id}. "
              f"Expected name: {playlist_a.name}, but got: {playlist_b.name}.")
    if not str(playlist_a.description) and not str(playlist_b.description):
        print(f"No description for both")
    elif str(playlist_a.description) == str(playlist_b.description):
        print(f"the description is '{playlist_a.description}' ")
    else:
        print(f"Error: tags mismatch for ID {playlist_a.id} and ReferenceID {playlist_b.id}. "
              f"Expected description: {playlist_a.description}, but got: {playlist_b.description}.")
    if not str(playlist_a.tags) and not str(playlist_b.tags):
        print(f"No tags for both")
    elif str(playlist_a.tags) == str(playlist_b.tags):
        print(f"the tags is '{playlist_a.tags}' ")
    else:
        print(f"Error: tags mismatch for ID {playlist_a.id} and ReferenceID {playlist_b.id}. "
              f"Expected tags: {playlist_a.tags}, but got: {playlist_b.tags}.")

def get_playlist_list(client, filter=None):
    if not filter:
        filter = KalturaPlaylistFilter()  # Initialize filter if not provided

    playlists = []
    pager = KalturaFilterPager()
    pager.pageIndex = 1
    pager.pageSize = 50  # Fetch 50 documents per page
    results = client.playlist.list(filter, pager)


    try:
        while True:
            results = client.playlist.list(filter, pager)  # Fetch playlists using pagination
            if results.totalCount > 0:
                playlists.extend(results.objects)  # Add the documents to the list
                # If there are fewer than 50 objects, we've reached the last page
                if len(results.objects) < 50:
                    break
            else:
                print("No documents found")
                return []

            pager.pageIndex += 1  # Move to the next page

    except Exception as e:
        print(f"Error: {str(e)}")
        return []

    return playlists


# First API call to get playlist IDs
config_1 = KalturaConfiguration()
config_1.serviceUrl = "https://www.kaltura.com/"
client_1 = KalturaClient(config_1)
client_1.setKs('djJ8MjkwODY0MXwTFg92XPwlr2z2FckcY85YhQzTsfRMvW8itfWvrDZullVIWeASqD2hiE-xnXVs-Gon0WcdceJhr7RIrHp5buTD_-PnEmrwSB27mMFb8FANjTiK8Sd10T6dv_Jx8--DmrgkAQpy7LKSJVe7RMqOTW0v')

filter_1 = KalturaPlaylistFilter()
playlists_1 = get_playlist_list(client_1, filter_1)



# second API call to get playlist IDs/referenceIDs
config_2 = KalturaConfiguration()
config_2.serviceUrl = "https://www.kaltura.com/"
client_2 = KalturaClient(config_1)
client_2.setKs('djJ8NTkyODAwMnz4jCjBJ3coI-m0wsActRKFcbNtzyRRwWDbskkrzk7mbVJ2mez5_SjRJWVu-s6sa731SwHziXo9Czep4sdZvAOAlHWcLSH8oOUcRU6z4Fj7T_4BOLCRX_gI4mvT_-GKVSL1EypnEVfTl-rtXpSKjudlaSOUiHXsF3qVPtM9Sec6HA')

filter_2 = KalturaPlaylistFilter()
playlists_2 = get_playlist_list(client_2, filter_2)

match_found = 0

for playlist_1 in playlists_1:
    # Check if the playlistID from API 1 has a matching playlistID in API 2)
    for playlist_2 in playlists_2:
        if playlist_1.id == playlist_2.referenceId:
            print(f"Found match for ID {playlist_1.id} and ReferenceID {playlist_2.referenceId}.")
            compare_metadata(playlist_1, playlist_2)
            match_found += 1
            break


print(f"Total matches found: {match_found}")
