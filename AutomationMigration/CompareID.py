import xml.etree.ElementTree as ET

# Sample XML strings
# xml_1 =
#
# xml_2 =


# Parse the XML strings
root_1 = ET.fromstring(xml_1)
root_2 = ET.fromstring(xml_2)

# Extract the IDs from each XML
ids_1 = [item.find('id').text for item in root_1.findall('.//item')]
ids_2 = [item.find('id').text for item in root_2.findall('.//item')]

# Compare the IDs
print("IDs in first XML:", ids_1)
print("IDs in second XML:", ids_2)

# Find IDs that are only in one of the XMLs
only_in_first = set(ids_1) - set(ids_2)
only_in_second = set(ids_2) - set(ids_1)

print("\nIDs only in the first XML:", only_in_first)
print("IDs only in the second XML:", only_in_second)