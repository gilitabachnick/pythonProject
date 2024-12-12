import categories
from KalturaClient import *
from KalturaClient.Plugins.Core import *


# Function to compare the Entry count (This function calls function compare_metadata and function compare_entitlements)
def compare_entriescount(category_1, category_2, func_metadata, func_entitlements):
    print(f"Checking ID {category_1.id} (entries count: {category_1.entriesCount}) "
          f"with ReferenceID {category_2.id} (entries count: {category_2.entriesCount})")

    # Handle missing values (None or not set)
    if category_1.entriesCount is None or category_2.entriesCount is None:
        print(f"Warning: Count missing for ID {category_1.id} or ReferenceID {category_2.id}.")
    elif category_1.entriesCount != category_2.entriesCount:
        print(f"Error: Count mismatch for ID {category_1.id} and ReferenceID {category_2.id}. "
              f"Expected entries count: {category_1.entriesCount}, but got {category_2.entriesCount}.")

    if category_1.entriesCount == category_2.entriesCount:
        print(f"ID {category_1.id} and ReferenceID {category_2.id} are identical in entries count.")
        func_metadata(category_1, category_2)
        func_entitlements(category_1, category_2)


# Function to compare the MetaData
def compare_metadata(category_a, category_b):

    if str(category_a.fullName) == str(category_b.fullName):
        print(f"the full name is{category_a.fullName}")
    else:
        print(f"Expected full name: {category_a.fullName}, but got {category_b.fullName}.")
    if not category_a.description and not category_b.description:
        print(f"the description of both is empty.")
    elif str(category_a.description) == str(category_b.description):
        print(f"the description is{category_a.description}")
    # elif str(category_a.description) != str(category_b.description):
    else:
        print(f"Error: description mismatch for ID {category_a.id} and ReferenceID {category_b.id}. "
              f"Expected description: {category_a.description}, but got: {category_b.description}.")
    if not category_a.tags and not category_a.tags:
        print(f"No tags for both")
    elif str(category_a.tags) == str(category_b.tags):
        print(f"the tags is '{category_a.tags}' ")
    else:
        print(f"Error: tags mismatch for ID {category_a.id} and ReferenceID {category_b.id}. "
              f"Expected tags: {category_a.tags}, but got: {category_b.tags}.")


# Function to compare the Entitlements
def compare_entitlements(category_one, category_two):
    if str(category_one.privacyContexts) == str(category_two.privacyContexts):
        print(f"the Privacy Context Label is '{category_one.privacyContexts}'")
    else:
        print(f"Error: Privacy Context Label mismatch for ID {category_one.id} and ReferenceID {category_two.id}. "
              f"Expected Privacy Context Label: {category_one.privacyContexts}, but got: {category_two.privacyContexts}.")
    if category_one.privacy.value == category_two.privacy.value:
        print(f"the Content Privacy is '{category_one.privacy.value}'")
    else:
        print(f"Error: Content Privacy mismatch for ID {category_one.id} and ReferenceID {category_two.id}. "
              f"Expected Content Privacy: {category_one.privacy.value}, but got: {category_two.privacy.value}.")
    if category_one.appearInList.value == category_two.appearInList.value:
        print(f"the Category Listing is '{category_one.appearInList.value}'")
    else:
        print(f"Error: Category Listing mismatch for ID {category_one.id} and ReferenceID {category_two.id}. "
              f"Expected Category Listing: {category_one.appearInList.value}, but got: {category_two.appearInList.value}.")
    if category_one.contributionPolicy.value == category_two.contributionPolicy.value:
        print(f"the Content Publish Permissions is '{category_one.contributionPolicy.value}'")
    else:
        print(f"Error: Content Publish Permissions mismatch for ID {category_one.id} and ReferenceID {category_two.id}. "
              f"Expected Content Publish Permissions: {category_one.contributionPolicy.value}, but got: {category_two.contributionPolicy.value}.")
    if category_one.moderation.value == category_two.moderation.value:
        print(f"the Moderate Content is '{category_one.moderation.value}'")
    else:
        print(f"Error: Moderate Content mismatch for ID {category_one.id} and ReferenceID {category_two.id}. "
              f"Expected Moderate Content: {category_one.moderation.value}, but got: {category_two.moderation.value}.")
    if category_one.inheritanceType.value == category_two.inheritanceType.value:
        print(f"the Inherit Users Permissions is '{category_one.inheritanceType.value}'")
    else:
        print(f"Error: Inherit Users Permissions mismatch for ID {category_one.id} and ReferenceID {category_two.id}. "
            f"Expected Inherit Users Permissions: {category_one.inheritanceType.value}, but got: {category_two.inheritanceType.value}.")

    if category_one.defaultPermissionLevel.value == category_two.defaultPermissionLevel.value:
        print(f"the default Permission Level is '{category_one.defaultPermissionLevel.value}'")
    else:
        print(f"Error: default Permission Level for ID {category_one.id} and ReferenceID {category_two.id}. "
              f"Expected default Permission Level: {category_one.defaultPermissionLevel.value}, but got: {category_two.defaultPermissionLevel.value}.")
    if not category_one.owner and not category_two.owner:
        print(f"the Owner of both is empty.")
    elif str(category_one.owner) == str(category_two.owner):
        print(f"the Owner is '{category_one.owner}'")
    else:
        print(f"Error: Owner mismatch for ID {category_one.id} and ReferenceID {category_two.id}. "
              f"Expected Owner: {category_one.owner}, but got: {category_two.owner}.")
    if category_one.membersCount == category_two.membersCount:
        print(f"the Permitted Users is '{category_one.membersCount}'")
    else:
        print(f"Error: Permitted Users mismatch for ID {category_one.id} and ReferenceID {category_two.id}. "
              f"Expected Permitted Users: {category_one.membersCount}, but got: {category_two.membersCount}.")


def get_category_list(client, filter=None):
    if not filter:
        filter = KalturaCategoryFilter()  # Initialize filter if not provided

    categories = []
    pager = KalturaFilterPager()
    pager.pageIndex = 1
    pager.pageSize = 50  # Fetch 50 categories per page
    results = client.category.list(filter, pager)


    try:
        while True:
            results = client.category.list(filter, pager)  # Fetch categories using pagination
            if results.totalCount > 0:
                categories.extend(results.objects)  # Add the categories to the list
                # If there are fewer than 50 objects, we've reached the last page
                if len(results.objects) < 50:
                    break
            else:
                print("No categories found")
                return []

            pager.pageIndex += 1  # Move to the next page

    except Exception as e:
        print(f"Error: {str(e)}")
        return []

    return categories




# First API call to get category IDs


config_1 = KalturaConfiguration()
config_1.serviceUrl = "https://www.kaltura.com/"
client_1 = KalturaClient(config_1)
client_1.setKs('djJ8MjkwODY0MXxvWeksUOVyoyOWxrq8psNuzN1C5s9Mr5EnajcD88LYhAJotq3FRJ8Dhvc90HP9rgVvK-o2rDtA_SMSQ8j8bK5soulC0OVe5zsSiD-yvAkkz6IR7AVS-mr1WHcuwrg8pHUQrFqlsxj0mQl1YSrowhFs')

# Get all categories from API 1 (using pagination)
filter_1 = KalturaCategoryFilter()
categories_1 = get_category_list(client_1, filter_1)



# second API call to get category IDs

config_2 = KalturaConfiguration()
config_2.serviceUrl = "https://www.kaltura.com/"
client_2 = KalturaClient(config_2)
client_2.setKs('djJ8NTkyODAwMnz4jCjBJ3coI-m0wsActRKFcbNtzyRRwWDbskkrzk7mbVJ2mez5_SjRJWVu-s6sa731SwHziXo9Czep4sdZvAOAlHWcLSH8oOUcRU6z4Fj7T_4BOLCRX_gI4mvT_-GKVSL1EypnEVfTl-rtXpSKjudlaSOUiHXsF3qVPtM9Sec6HA')

# Get all categories from API 2 (using pagination)
filter_2 = KalturaCategoryFilter()
categories_2 = get_category_list(client_2, filter_2)


match_found = 0

for category_1 in categories_1:
    # Check if the categoryID from API 1 has a matching categoryID in API 2)
    for category_2 in categories_2:
        if str(category_1.id) == str(category_2.referenceId):
            print(f"Found match for ID {category_1.id} and ReferenceID {category_2.referenceId}.")
            # compare_name_description(category_1, category_2)
            compare_entriescount(category_1, category_2, compare_metadata, compare_entitlements)
            # compare_category_metadata(category_1, category_2)
            match_found += 1
            break


print(f"Total matches found: {match_found}")







