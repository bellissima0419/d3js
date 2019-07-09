var url = 'api/stats'

d3.json(url, function(response) {
  console.log('response[0]: ', response[0].devsPerMill);
  var counter = 0 

  var mindevsPerMill = response.reduce(function(prev, curr) {
    return prev.devsPerMill < curr.devsPerMill ? prev : curr;
    }).devsPerMill;
    console.log('mindevsPerMill: ', mindevsPerMill);

 var maxdevsPerMill = response.reduce(function(prev, curr) {
    return prev.devsPerMill < curr.devsPerMill ? curr : prev;
    }).devsPerMill;
    console.log('maxdevsPerMill: ', maxdevsPerMill);


  response.forEach(element => {
    Object.entries(element).forEach(([key,value]) => counter += element["respondentCount"]);
    
  });

  var circleMarkers = [];
  var percapitaMarkers = [];

  for (var i = 0; i < response.length; i++) {

    var location = response[i].location;
    var perCapita = response[i].devsPerMill;
    if (location && perCapita) {
    
    // Conditionals for countries points
    var color = "";
    if (response[i].devsPerMill > 50) {
      color = "#b71540";
    }
    else if (response[i].devsPerMill > 30) {
      color = "DeepPink";
    }
    else if (response[i].devsPerMill > 20) {
      color = "Coral";
    }
    else if (response[i].devsPerMill > 10){
      color = "DarkCyan"
    }
    else {
      color = "MediumTurquoise";
    }
  
    // Add circles to map

    // var myScale = d3.scaleLinear()
    // .domain(d3.extent([0, 200]))
    // .range([150000, 1200000]);
    var  colorScale = d3.scaleLinear()
    .domain(d3.extent([0,20949]))
    .range([150000, 1200000]);

    var percapitaScale = d3.scaleLinear()
    .domain(d3.extent([mindevsPerMill, maxdevsPerMill]))
    .range([150000, 500000]);


    circleMarkers.push(
      L.circle(response[i].location, {
        fillOpacity: 0.4,
        color: 'black',
        fillColor: color,
        weight: 0.4,
        // fillColor: colorScale(response[i].respondentCount/2),
        // Adjust radius
        // radius: (parseInt(response[i].respondentCount) + 150000) * 2
        radius: colorScale(response[i].respondentCount)
  
    //   }).bindPopup("<p>" + response[i].country + "</p> <hr> <p>: " + response[i].respondentCount +  "</p>")
    // )
  }).bindPopup(`<p>${response[i].country}</p><hr> <p>Respondent Count ${response[i].respondentCount}</p>`)
  )


    percapitaMarkers.push(
      L.circle(response[i].location, {
        fillOpacity: 0.4,
        color: 'black',
        fillColor: color,
        weight: 0.4,
        // fillColor: colorScale(response[i].respondentCount/2),
        // Adjust radius
        // radius: (parseInt(response[i].respondentCount) + 150000) * 2
        // radius: myScale(response[i].respondentCount/response[i].devsPerMill)
        radius: percapitaScale(response[i].devsPerMill)

  
      }).bindPopup("<h4>" + response[i].country + "</h4> <hr>Per Capita: " + response[i].devsPerMill +  "</>")
      
    )
    
   }
  }

  var cityLayer = L.layerGroup(circleMarkers);
  var percapitaLayer = L.layerGroup(percapitaMarkers);

  var light = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 5,
    // minZoom: 1.5,
    zomm: 1.4,
    id: "mapbox.light",
    accessToken: API_KEY
  });
  
  var dark = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 5,
    // zominZoomom: 1.5,
    zomm: 1.4,
    id: "mapbox.dark",
    accessToken: API_KEY
  });
  
  // Only one base layer can be shown at a time
  var baseMaps = {
    Light: light,
    Dark: dark
  };

  var overlayMaps = {
    'Total Respondents': cityLayer,
    'Percapita': percapitaLayer
  };

  var myMap = L.map("map", {
    center: [33.886917,9.537499],
    // center: [15.5994, -28.6731],
    zoom: 1.5,
    // maxBounds: 1.5,
    layers: [light, cityLayer]

  });

  // myMap.setMinZoom( myMap.getBoundsZoom( myMap.options.maxBounds ) );

  // setMaxBounds
  
  L.control.layers(baseMaps, overlayMaps).addTo(myMap);

});

// Loop through the cities array and create one marker for each city object

// console.log('countries[0].location: ', countries[0].location);



