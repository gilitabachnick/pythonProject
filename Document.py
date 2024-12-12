from KalturaClient import *
from KalturaClient.Plugins.Core import *
from KalturaClient.Plugins.Document import *


def compare_metadata(document_a, document_b):
    if str(document_a.name) == str(document_b.name):
        print(f"the Name is {document_a.name}")
    else:
        print(f"Error: name mismatch for ID {document_a.id} and ReferenceID {document_b.id}. "
              f"Expected name: {document_a.name}, but got: {document_b.name}.")
    if not str(document_a.description) and not str(document_b.description):
        print(f"No description for both")
    elif str(document_a.description) == str(document_b.description):
        print(f"the description is '{document_a.description}' ")
    else:
        print(f"Error: description mismatch for ID {document_a.id} and ReferenceID {document_b.id}. "
              f"Expected description: {document_a.description}, but got: {document_b.description}.")
    if not str(document_a.tags) and not str(document_b.tags):
        print(f"No tags for both")
    elif str(document_a.tags) == str(document_b.tags):
        print(f"the tags is '{document_a.tags}' ")
    else:
        print(f"Error: tags mismatch for ID {document_a.id} and ReferenceID {document_b.id}. "
              f"Expected tags: {document_a.tags}, but got: {document_b.tags}.")













def get_document_list(client, filter=None):
    if not filter:
        filter = KalturaDocumentEntryFilter()  # Initialize filter if not provided

    documents = []
    pager = KalturaFilterPager()
    pager.pageIndex = 1
    pager.pageSize = 50  # Fetch 50 documents per page
    results = client.document.documents.list(filter, pager)


    try:
        while True:
            results = client.document.documents.list(filter, pager)  # Fetch documents using pagination
            if results.totalCount > 0:
                documents.extend(results.objects)  # Add the documents to the list
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

    return documents


# First API call to get document IDs
config_1 = KalturaConfiguration()
config_1.serviceUrl = "https://www.kaltura.com/"
client_1 = KalturaClient(config_1)
client_1.setKs('djJ8MjkwODY0MXwTFg92XPwlr2z2FckcY85YhQzTsfRMvW8itfWvrDZullVIWeASqD2hiE-xnXVs-Gon0WcdceJhr7RIrHp5buTD_-PnEmrwSB27mMFb8FANjTiK8Sd10T6dv_Jx8--DmrgkAQpy7LKSJVe7RMqOTW0v')

filter_1 = KalturaDocumentEntryFilter()
documents_1 = get_document_list(client_1, filter_1)



# second API call to get document IDs/referenceIDs
config_2 = KalturaConfiguration()
config_2.serviceUrl = "https://www.kaltura.com/"
client_2 = KalturaClient(config_1)
client_2.setKs('djJ8NTkyODAwMnz4jCjBJ3coI-m0wsActRKFcbNtzyRRwWDbskkrzk7mbVJ2mez5_SjRJWVu-s6sa731SwHziXo9Czep4sdZvAOAlHWcLSH8oOUcRU6z4Fj7T_4BOLCRX_gI4mvT_-GKVSL1EypnEVfTl-rtXpSKjudlaSOUiHXsF3qVPtM9Sec6HA')

filter_2 = KalturaDocumentEntryFilter()
documents_2 = get_document_list(client_2, filter_2)

match_found = 0

for document_1 in documents_1:
    # Check if the documentID from API 1 has a matching documentID in API 2)
    for document_2 in documents_2:
        if document_1.id == document_2.referenceId:
            print(f"Found match for ID {document_1.id} and ReferenceID {document_2.referenceId}.")
            compare_metadata(document_1, document_2)
            match_found += 1
            break


print(f"Total matches found: {match_found}")







