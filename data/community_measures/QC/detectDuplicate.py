def detectDuplicate(LA, URL):
    
    #Find root URL
    if re.search('facebook', URL):
        
        print("facebook URL found: ", URL)
        
        if re.search('groups/', URL):
            fbGroupId = URL.split('groups/')[1]
            fbGroupId_tail = re.search('/',fbGroupId)

            if fbGroupId_tail:
                standardisedLink = fbGroupId.split('/')[0]
                print(standardisedLink)

            else:
                standardisedLink = fbGroupId
                print(standardisedLink)
                
        elif re.search('facebook.com/', URL): 
            standardisedLink = URL.split('facebook.com/')[1]
            print(standardisedLink)
        
        else: 
            standardisedLink = URL 
            print(standardisedLink)
    else:
        standardisedLink = URL
        print(standardisedLink)
    
    if LA not in URLs:
        URLs[LA]=[]
        return(False)
    elif standardisedLink in URLs[LA]:
        return(True)
    else:
        URLs[LA].append(standardisedLink)
        return(False)   