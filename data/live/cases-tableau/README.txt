Uses Python tableau server client (& documentation):
https://tableau.github.io/server-client-python/docs/

The Welsh covid data is located here:
https://public.tableau.com/profile/public.health.wales.health.protection#!/vizhome/RapidCOVID-19virology-Public/Summary

but I dug down and found that it is an iFrame (clone) of this:
https://covid19-phwdata.nhs.wales/

which in turn is an iFrame of this:
https://public.tableau.com/views/RapidCOVID-19virology-Public/Headlinesummary?:display_count=y&:embed=y&:showAppBanner=false&:showVizHome=no

This is the closest I can get to the data and should be the best source for any Scraping. Though there is some anti-tamper device which you can disable by hiding these two elements: id=primaryContentLink & a href-"phw/wales" (i.e., the two elements which will are full screen and will redirect the page if clicked on)