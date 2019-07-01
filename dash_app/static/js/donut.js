// var dimensions = { height: 500, width: 500, radius: 200 };
// var center = { x: (dimensions.width / 2 + 5), y: (dimensions.height / 2 + 5)}
var dimensions = { height: 300, width: 300, radius: 150 };
var center = { x: (dimensions.width / 2 + 5), y: (dimensions.height / 2 + 5)};

// create svg container
var svg = d3.select('.donut')
  .append('svg')
  .attr('width', dimensions.width + 250)
  .attr('height', dimensions.height + 150);

var graph = svg.append('g')
  .attr("transform", `translate(${center.x}, ${center.y})`);
  // translates the graph group to the middle of the svg container

var pie = d3.pie()
  // .sort(null)
  .value(d => d.respondentCount);
  // the value we are evaluating to create the pie angles

var arcPath = d3.arc()
  .outerRadius(dimensions.radius)
  .innerRadius(dimensions.radius / 1.3);

// ordinal colour scale
var  color = d3.scaleOrdinal(d3["schemeCategory10"]); 
// schemeAccent schemeDark2 schemePaired schemePastel1 schemePastel2
// schemeSet1 schemeSet2 schemeSet3 schemeCategory10

// legend setup
var legendGroup = svg.append('g')
  .attr('transform', `translate(${dimensions.width + 50}, 10)`)

var legend = d3.legendColor()
  // .shape('circle')
  .shape('path', d3.symbol().type(d3.symbolCircle)())
  .shapePadding(10)
  .scale(color)

var tip = d3.tip()
  .attr('class', 'tip card')
  .html(d => {
    let content = `<div class="name">${d.data.country}</div>`;
    content += `<div class="cost">${d.data.percentage} %</div>`;
    content += `<div class="delete">${d.data.respondentCount} Respondents</div>`
    return content;
  });

graph.call(tip);

// update function
var update = (data) => {

  // update color scale domain
  color.domain(data.map(d => d.country))

    // update legend
  legendGroup.call(legend);
  legendGroup.selectAll('text').attr('fill', 'white');
  
  // join enhanced (pie) data to path elements
  var paths = graph.selectAll('path')
    .data(pie(data));
      // console.log('pie(data): ',pie(data));
     // console.log('paths: ', paths);
  
  // handle the exit selection
  paths.exit()
    .transition().duration(750)
    .attrTween("d", arcTweenExit)
    .remove();

  // handle the current DOM path updates
  // paths.attr('d', arcPath)
  //   .transition().duration(750)
  //   .attrTween('d', arcTweenUpdate)

  paths.transition().duration(750)
  .attrTween("d", arcTweenUpdate);
// =======================================
// =======================================
  // USING d3.nest()
  // var countries = d3.nest()
	// .key(d => d.country)
	// .key(d => d.respondentCount)
	// .entries(top10Countries)
// =======================================
// =======================================
  paths.enter()
    .append('path')
      .attr('class', 'arc')
      // .attr('d', d => arcPath(d)) //  .attr('d', arcPath) //
      .attr('stroke', '#ebebeb')
      .attr('stroke-width', 1.1)
      .attr('d', arcPath)
      .attr('fill', d => color(d.data.country))
      .each(function(d){ this._current = d })
      .transition().duration(750).attrTween("d", arcTweenEnter);
      
//     // add events
//   graph.selectAll('path')
//   .on('mouseover', handleMouseOver)
//   .on('mouseout', handleMouseOut)
//   .on('click', handleClick)
// };


  // add events
  graph.selectAll('path')
    .on('mouseover', (d,i,n) => {
      tip.show(d, n[i]);
      handleMouseOver(d, i, n);
    })
    .on('mouseout', (d,i,n) => {
      tip.hide();
      handleMouseOut(d, i, n);
    })
    .on('click', handleClick);

};

// data array to hold the api data
var top10Countries = [];

d3.json('/countries').then( (data) =>  {
    // console.log('data: ', data);
    var total_respondents = 0;
    data.forEach(el => total_respondents += el.respondentCount)
    // console.log("total_respondents: ", total_respondents);
    // console.log("data: ", data);

    data.forEach(el => el["percentage"] = +(el.respondentCount/total_respondents*100).toFixed(2))
    // console.log(data.slice(0,10))

    var top10 = data.slice(0, 10)
    // console.log('top10 : ', top10);

    top10.forEach(element => {
      top10Countries.push(element)
    });
    
    update(top10Countries)
    console.log('top10Countries: ', top10Countries);


});

var arcTweenEnter = (d) => {
  var i = d3.interpolate(d.endAngle-0.1, d.startAngle);

  return function(t) {
    d.startAngle = i(t);
    return arcPath(d);
  };
}

var arcTweenExit = (d) => {
  var i = d3.interpolate(d.startAngle, d.endAngle);

  return function(t) {
    d.startAngle = i(t);
    return arcPath(d);
  };
}

function arcTweenUpdate(d) {
  // console.log('this._current');
  // console.log('d: ', d)
  // interpolate between the two objects
  var i = d3.interpolate(this._current, d);
  // update the current prop with new updated data
  this._current = i(1);

  return function(t) {
    // i(t) returns a value of d (data object) which we pass to arcPath
    return arcPath(i(t));
  };
};


// envent handlers
var handleMouseOver = (d,i,n) => {
  //console.log(n[i]);
  d3.select(n[i])
    .transition('changeSliceFill').duration(300)
      .attr('fill', '#fff');
};

var handleMouseOut = (d,i,n) => {
  // console.log(n[i]);
  d3.select(n[i])
    .transition('changeSliceFill').duration(300)
      .attr('fill', color(d.data.country));
};

var handleClick = d => {
  // console.log('d inside click: ', d) 
  // console.log('top10Countries: ', top10Countries);

  var newData = top10Countries.filter(c => c.country !== d.data.country)

  // console.log('top10Countries', top10Countries);
  // console.log('newData', newData);
  // update(newData)
  update(newData)

}





