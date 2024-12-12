from KalturaClient import *
from KalturaClient.Plugins.Core import *

config = KalturaConfiguration()
config.serviceUrl = "https://www.kaltura.com/"
client = KalturaClient(config)
# ks = client.generateSessionV2(
#       "YOUR_KALTURA_SECRET",
#       "YOUR_USER_ID",
#       KalturaSessionType.ADMIN,
#       YOUR_PARTNER_ID)
client.setKs("djJ8MjkwODY0MXyKnYBukokze6X0TE40mpoZ8OiafUaEbZB_WfCRN6wLx6aLof5KGVifpBlqXHAhQAnmFw98J0znti06zrryf87xXSiJ48rB8iy_TAyiLuyb1QnH1Kd9Dy9VB3Nw-FhBjs7VFWcb9mKOUlYBDnX_GqHH")

filter = KalturaBaseEntryFilter()
pager = KalturaFilterPager()

result = client.baseEntry.list(filter, pager)
print(result)
print(result.totalCount)
