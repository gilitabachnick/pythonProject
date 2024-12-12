from KalturaClient import *
from KalturaClient.Plugins.Core import *
from KalturaClient.Plugins.Metadata import *


def compare_metadata(customSchema_a, customSchema_b):
    if not str(customSchema_a.systemName) and not str(customSchema_b.systemName):
        print(f"No system name for both")
    elif str(customSchema_a.systemName) == str(customSchema_b.systemName):
        print(f"the system name is '{customSchema_a.systemName}' ")
    else:
        print(f"Error: system name mismatch for ID {customSchema_a.id} and ID {customSchema_b.id}. "
              f"Expected system name: {customSchema_a.systemName}, but got: {customSchema_b.systemName}.")
    if not str(customSchema_a.description) and not str(customSchema_b.description):
        print(f"No description for both")
    elif str(customSchema_a.description) == str(customSchema_b.description):
        print(f"the description is '{customSchema_a.description}' ")
    else:
        print(f"Error: description mismatch for ID {customSchema_a.id} and ID {customSchema_b.id}. "
              f"Expected description: {customSchema_a.description}, but got: {customSchema_b.description}.")
    if str(customSchema_a.xsd) == str(customSchema_b.xsd):
        print("xsd True")
    else:
        print("xsd False")
    if customSchema_a.createMode.value == customSchema_b.createMode.value:
        print('create Mode True')
    else:
        print('Create Mode False')












def get_MetadataProfile_list(client, filter):
    if not filter:
        filter= KalturaMetadataProfileFilter()
        filter.metadataObjectTypeEqual = KalturaMetadataObjectType.ENTRY

    CustomSchemas = []
    pager = KalturaFilterPager()
    pager.pageIndex = 1
    pager.pageSize = 50  # Fetch 50 CustomSchemas per page
    results = client.metadata.metadataProfile.list(filter, pager)

    try:
        while True:
            results = client.metadata.metadataProfile.list(filter, pager)   # Fetch CustomSchemas using pagination
            if results.totalCount > 0:
                CustomSchemas.extend(results.objects)  # Add the CustomSchemas to the list
                # If there are fewer than 50 objects, we've reached the last page
                if len(results.objects) < 50:
                    break
            else:
                print("No CustomSchemas found")
                return []

            pager.pageIndex += 1  # Move to the next page

    except Exception as e:
        print(f"Error: {str(e)}")
        return []

    return CustomSchemas









# First API call to get Custom Schema
config_1 = KalturaConfiguration()
config_1.serviceUrl = "https://www.kaltura.com/"
client_1 = KalturaClient(config_1)
client_1.setKs("djJ8MjkwODY0MXxvWeksUOVyoyOWxrq8psNuzN1C5s9Mr5EnajcD88LYhAJotq3FRJ8Dhvc90HP9rgVvK-o2rDtA_SMSQ8j8bK5soulC0OVe5zsSiD-yvAkkz6IR7AVS-mr1WHcuwrg8pHUQrFqlsxj0mQl1YSrowhFs")

# Get all items from API 1 (using pagination)
filter_1 = KalturaMetadataProfileFilter()
filter_1.metadataObjectTypeEqual = KalturaMetadataObjectType.ENTRY
CustomSchemas_1 = get_MetadataProfile_list(client_1, filter_1)


# Second API call to get Custom Schema
config_2 = KalturaConfiguration()
config_2.serviceUrl = "https://www.kaltura.com/"
client_2 = KalturaClient(config_2)
client_2.setKs("djJ8NTkyODAwMnz4jCjBJ3coI-m0wsActRKFcbNtzyRRwWDbskkrzk7mbVJ2mez5_SjRJWVu-s6sa731SwHziXo9Czep4sdZvAOAlHWcLSH8oOUcRU6z4Fj7T_4BOLCRX_gI4mvT_-GKVSL1EypnEVfTl-rtXpSKjudlaSOUiHXsF3qVPtM9Sec6HA")

# Get all items from API 2 (using pagination)
filter_2 = KalturaMetadataProfileFilter()
filter_1.metadataObjectTypeEqual = KalturaMetadataObjectType.ENTRY
CustomSchemas_2 = get_MetadataProfile_list(client_2, filter_2)

match_found = 0

for customSchema_1 in CustomSchemas_1:
    # Check if the CustomSchema Name from API 1 has a matching CustomSchema Name in API 2)
    for customSchema_2 in CustomSchemas_2:
        if str(customSchema_1.name) == str(customSchema_2.name):
            print(f"Found match for ID {customSchema_1.id} and ID {customSchema_2.id}.")
            compare_metadata(customSchema_1, customSchema_2)
            match_found += 1
            break


print(f"Total matches found: {match_found}")