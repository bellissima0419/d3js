// Create a map object
// var myMap = L.map("map", {
//   center: [15.5994, -28.6731],
//   zoom: 1.4
// });



// L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
//   attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
//   maxZoom: 18,
//   id: "mapbox.streets-basic",
//   accessToken: API_KEY
// }).addTo(myMap);

//  var sample_response = {
//   "code": "US",
//   "country": "United States",
//   "latitude": 37.09024,
//   "location": [37.09024,-95.712891],
//   "longitude": -95.712891,
//   "respondentCount": 2597
//   }

var url = 'api/stats'

d3.json(url, function(response) {
  console.log('response[0]: ', response[0].population);
  var counter = 0 

  var minPopulation = response.reduce(function(prev, curr) {
    return prev.population < curr.population ? prev : curr;
    }).population;
    console.log('minPopulation.population: ', minPopulation);

 var maxPopulation = response.reduce(function(prev, curr) {
    return prev.population < curr.population ? curr : prev;
    }).population;
    console.log('maxPopulation.population: ', maxPopulation);


  response.forEach(element => {
    Object.entries(element).forEach(([key,value]) => counter += element["respondentCount"]);
    
  });

  var circleMarkers = [];
  var percapitaMarkers = [];

  for (var i = 0; i < response.length; i++) {
    var location = response[i].location;
    if (location) {
    
    // Conditionals for countries points
    var color = "";
    if (response[i].respondentCount > 1000) {
      color = "#b71540";
    }
    else if (response[i].respondentCount > 500) {
      color = "DeepPink";
    }
    else if (response[i].respondentCount > 100) {
      color = "Coral";
    }
    else if (response[i].respondentCount > 20){
      color = "DarkCyan"
    }
    else {
      color = "MediumTurquoise";
    }
  
    // Add circles to map

    var myScale = d3.scaleLinear()
    .domain(d3.extent([1, 2597]))
    .range([150000, 1200000]);

    var percapitaScale = d3.scaleLinear()
    .domain(d3.extent([minPopulation, maxPopulation]))
    // .range([150000, 1200000]);

    // var  colorScale = d3.scaleOrdinal(d3.schemeCategory10)
    //   .domain(d3.extent([(1,2597)]))
    //     // .range([1,10])

    circleMarkers.push(
      L.circle(response[i].location, {
        fillOpacity: 0.4,
        color: 'black',
        fillColor: color,
        weight: 0.4,
        // fillColor: colorScale(response[i].respondentCount/2),
        // Adjust radius
        // radius: (parseInt(response[i].respondentCount) + 150000) * 2
        radius: myScale(response[i].respondentCount)
  
      }).bindPopup("<h4>" + response[i].country + "</h4> <hr> <h5>Responents: " + response[i].respondentCount +  "</h5>")
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
        // radius: myScale(response[i].respondentCount/response[i].population)
        radius: myScale(response[i].respondentCount)

  
      }).bindPopup("<h4>" + response[i].country + "</h4> <hr> <h5>Responents: " + response[i].respondentCount +  "</h5>")
      
      // .bindPopup("<h4>" + response[i].country + "</h4> <hr> <h5>Responents: " + response[i].population +  "</h5>")
    )
    
    // L.circle(response[i].location, {
    //   fillOpacity: 0.4,
    //   color: 'black',
    //   fillColor: color,
    //   weight: 0.4,
    //   // fillColor: colorScale(response[i].respondentCount/2),
    //   // Adjust radius
    //   // radius: (parseInt(response[i].respondentCount) + 150000) * 2
    //   radius: myScale(response[i].respondentCount)

    // }).bindPopup("<h4>" + response[i].country + "</h4> <hr> <h5>Responents: " + response[i].respondentCount +  "</h5>").addTo(myMap);
   }
  }


  var cityLayer = L.layerGroup(circleMarkers);
  var percapitaLayer = L.layerGroup(percapitaMarkers);


  var light = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 5,
    // minZoom: 1.5,
    zomm: 1.5,
    id: "mapbox.light",
    accessToken: API_KEY
  });
  
  var dark = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 5,
    // zominZoomom: 1.5,
    zomm: 1.5,
    id: "mapbox.dark",
    accessToken: API_KEY
  });
  
  // Only one base layer can be shown at a time
  var baseMaps = {
    Light: light,
    Dark: dark
  };

  var overlayMaps = {
    Countries: cityLayer
    // PerCapita: percapitaLayer
  };

  var myMap = L.map("map", {
    center: [15.5994, -28.6731],
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



