import csv

def QCFilter(groups, referenceList):
    
    f2 = open(referenceList, 'r', encoding='utf-8')

    with f2:
        references = csv.DictReader(f2, fieldnames = ("Title", "location", "LSOA", "ACTION", "ammendments", "notes", "link"))

        groups_QCFiltered = []
        
        print("GROUPS payload delivered to QCFilter: ", groups)
            
        
        #Cross-ref data 
        for group in groups:
            
            print("QC analysing group: {}".format(group["Title"]))
            
            #Skip header
            if group["Title"] == "Title":
                continue
            else:

                for ref in references:

                    #Skip header
                    if group["Title"] == "Title":
                        continue

                    #print("Using reference: ", ref["Title"])

                    print("PRINTING GROUP: ", group['Title'])
                    print("PRINTING REF: ", ref['Title'])

                    if group['Title'] == ref['Title']:
                        print("Reference entry found for group: ", ref["Title"])
                        #If ammendment exists to group, make ammendment and add to ammended groups list
                        if ref["Action"]:

                            if ref["Action"] == "DELETE":
                                print("Group {} deleted for reason {}".format(group["Title"], ref["notes"]))

                            elif ref["Action"] == "CHANGE":
                                group["LSOA"]=ref["ammendments"]
                                groups_QCFiltered.append(group)
                                print("Group {} changed for reason {}".format(group["Title"], ref["notes"]))

                            elif ref["Action"] == "SPLIT":
                                groups_QCFiltered.append(group)
                                group["LSOA"]=ref["ammendments"]
                                groups_QCFiltered.append(group)
                                print("Group {} split for reason {}".format(group["Title"], ref["notes"]))

                            else: 
                                groups_QCFiltered.append(group)
                                print("WARNING: Group ACTION not recognised for group {}".format(group["Title"]))

                        #If no ammendment exists to group, just add to ammended groups list
                        else: 
                            groups_QCFiltered.append(group)
                else:
                    print("Reference mismatch: ", group["Title"], ref["Title"])
    
    #Save output
    return(groups_QCFiltered)