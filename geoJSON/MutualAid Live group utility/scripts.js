var output=[]

var xhttp = new XMLHttpRequest();
xhttp.open("GET", "https://raw.githubusercontent.com/Covid-Mutual-Aid/search-by-postcode/master/data/groups.json", true);
xhttp.onload = function() {
                
    //Parse JSON
    var ourData = JSON.parse(xhttp.responseText);
        console.log("GOT data: ", ourData);

    //Reformat JSON to geoJSON
    ourData.forEach(reformat);
        console.log("Reformatted data: ", output);
    
    //Preview formatted geoJSON
    //ourData.forEach(reformatToCSV);
    document.getElementById("output-div").innerHTML=JSON.stringify(
        {
        "type": "FeatureCollection",
        "features": output
        })

    /*document.getElementById("output-div").innerHTML=JSON.stringify({"names":names,"latitude":lats,"longitude":longs});
    */
}
xhttp.send();

function inWales(row){
    
    //SOURCE DATA MIXES LNG AND LAT
    lat=row["location_coord"]["lat"]
    long=row["location_coord"]["lng"]
    id=row["id"]
    
    if (lat <=53.45 && lat >=51.35 && long >=-5.5 && long <=-2.65){
            console.log("Welsh group identified: ", row)
        return(true)
    } else {
            console.log("Group excluded: ", row)
        return(false)}
}

function reformat(row){
    
    console.log("Formatting: ", row)
    
    if (inWales(row) == true){
        
        output.push({
              "type": "Feature",
              "geometry": {
                "type": "Point",
                "coordinates": [row["location_coord"]["lng"], row["location_coord"]["lat"]]
              },
              "properties": {
                "name": row["name"],
                "location_name": row["location_name"],
                "link": row["link_facebook"]
              }
        }) 
    }
}

//OPTIONAL: Convert to CSV instead
var names=[]
var lats=[]
var longs=[]
function reformatToCSV(row){
    names.push(row["name"])
    lats.push(row["location_coord"]["lat"])
    longs.push(row["location_coord"]["lng"])
}