import time
import configparser
from KalturaClient import *
# Set execution parameters
import sys

from KalturaClient.Plugins.Core import KalturaFilterPager, KalturaMediaEntryFilter, KalturaEntryType

sys.setrecursionlimit(10000)

# Load configuration from INI file
config = configparser.ConfigParser()
config.read('config.ini')

# Configuration settings
partner_id = config['DEFAULT']['PID']
secret = config['DEFAULT']['admin_secret']
timezone = config['DEFAULT']['timezone']

# Set the Kaltura API session
kaltura_config = KalturaConfiguration(4979732)
kaltura_config.serviceUrl = 'https://admin.kaltura.com/'
client = KalturaClient(kaltura_config)

# Use an existing Kaltura session key
ks = "djJ8NDk3OTczMnwpVVRfQucqi4lgp7JTmByjhCxFJvzLtmz1wc0uVBTQrFMpA9GHjueMUBzFfs_RprTiA0m2RAz88THEsPNAuCMuCWpx8G8o__FRVWucIRCt0Ejv13U0elMy46nqKqwOxacPkUZ1jvgZm0iJ_TRgLcxX4FXUrYHZvZTp-ET8HP_7ng"
client.setKs(ks)
# Ensure session key (KS) is valid by checking user info
try:
    user_info = client.user.getClientInfo()  # Check if the session works
    print(f"Client Info: {user_info}")
except Exception as e:
    print(f"Error with session: {e}")

print(f"{time.strftime('%a, %d %b %Y %H:%M:%S +0000')}: Starting")


# Fetch entries from Kaltura
def get_full_list_of_entries(client):
    """Return an array of all entries per filter criteria."""
    global entry
    counter = 1
    dots_array = []
    all_entries = {}
    pager = KalturaFilterPager()
    pager.pageIndex = 1  # Start with the first page
    pager.pageSize = 500  # Fetch up to x entries per request
    last_created_at = 0
    last_entry_ids = ""
    cont = True

    filter = KalturaMediaEntryFilter()
    filter.statusIn = "2"  # Only active entries
    filter.orderBy = "-createdAt"  # Sort by creation date, descending

    while cont:
        if last_created_at != 0:
            filter.createdAtLessThanOrEqual = last_created_at
        if last_entry_ids != "":
            filter.idNotIn = last_entry_ids

        # Delay to avoid overloading the server
        time.sleep(0.025)

        # Fetch entries
        try:
            results = client.media.list(filter, pager)

            # Print the raw response from the API for debugging
            print(f"API Response: {results}")  # This will show what the API returns

            if not results.objects:
                cont = False  # No more entries, exit the loop
            else:
                for entry in results.objects:
                    all_entries[entry.id] = entry

                # Update last_entry_ids and last_created_at for the next page
                if last_created_at != entry.createdAt:
                    last_entry_ids = ""

                if last_entry_ids != "":
                    last_entry_ids += ","
                last_entry_ids += entry.id
                last_created_at = entry.createdAt

                # Increase the counter and increment the pageIndex for the next request
                counter += 1
                pager.pageIndex += 1  # Move to the next page

            # Print progress every iteration
            print_progress(f"Building list of entries ({counter}) {''.join(dots_array)}")
            dots_array.append(".")
            if len(dots_array) > 5:
                dots_array = []

        except Exception as e:
            print(f"Error during API call: {e}")
            break

    return all_entries if all_entries else {}


# Function to print progress on the same line in terminal
def print_progress(x):
    """Print progress, overwrite the line each time."""
    sys.stdout.write("\r\033[0K" + x)
    sys.stdout.flush()


# Start fetching entries
entries = get_full_list_of_entries(client)

# Check if entries are found and print their details
if entries:
    print(f"\nFound {len(entries)} entries with views and plays:")
    for entry in entries.values():
        print(f"Entry ID: {entry.id}")
        # print(f"Entry Name: {entry.name}")
        # print(f"ReferenceId: {entry.referenceId}")
        # print(f"Status: {entry.status}")
        print(f"Plays: {entry.plays}")
        print(f"Views: {entry.views}")
        print("-" * 40)
else:
    print("No entries found.")
    # Always return a dictionary, even if empty


def print_progress(x):
    """Print progress, overwrite the line each time."""
    sys.stdout.write("\r\033[0K" + x)
    sys.stdout.flush()
