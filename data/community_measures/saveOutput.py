import json
import csv

def saveOutput(groups, output, geomWelshGrps, URLs, filenames):

   filename_output_groups = filenames["output_groups"]
   filename_output_groupCount = filenames["output_groupCount"]
   filename_output_URLs = filenames["output_URLs"]
   filename_output_review  = filenames["output_groupCopyForReview"] 

   #Write to geojson
   geoJSON_groups = {"type": "FeatureCollection", "features": groups}
   with open(filename_output_groups, 'w') as grps:
      json.dump(geoJSON_groups, grps)

   geoJSON_groupsCount = {"type": "FeatureCollection", "features": output}
   with open(filename_output_groupCount, 'w') as grpsC:
      json.dump(geoJSON_groupsCount, grpsC)

   #Write URLs to json
   with open(filename_output_URLs, 'w') as urls:
      json.dump(URLs, urls)

   #To CSV Operation
   f = open(filename_output_review, 'w', encoding='utf-8', newline="")
   with f:
      writer = csv.writer(f)
      for row in geomWelshGrps:
         writer.writerow(row)