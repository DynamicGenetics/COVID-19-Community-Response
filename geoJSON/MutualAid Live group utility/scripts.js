var output=[]

var xhttp = new XMLHttpRequest();
xhttp.open("GET", "https://raw.githubusercontent.com/Covid-Mutual-Aid/search-by-postcode/master/data/groups.json", true);
xhttp.onload = function() {
                var ourData = JSON.parse(xhttp.responseText);
                console.log("GOT data: ",ourData);
                ourData.forEach(reformat);
                console.log("Reformatted data: ",output);
                document.getElementById("output-div").innerHTML=JSON.stringify(
                    {
                    "type": "FeatureCollection",
                    "features": output
                    })
                }
xhttp.send();

function inWales(row){
    
    lat=row["location_coord"]["lat"]
    long=row["location_coord"]["lng"]
    id=row["id"]
    
    if (lat <=90 && lat >=-90 && long <= 180 && long >=-180){
        return(true)
    } else {
        console.log("Group excluded: ")
        return(false)}
}

function reformat(row){
    
    if (inWales(row) == true){
        
        output.push({
              "type": "Feature",
              "geometry": {
                "type": "Point",
                "coordinates": [row["location_coord"]["lat"], row["location_coord"]["lng"]]
              },
              "properties": {
                "name": row["name"],
                "location_name": row["location_name"],
                "link": row["link_facebook"]
              }
        })    
    
    }
}