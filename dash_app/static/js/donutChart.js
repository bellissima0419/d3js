var dimensions = { height: 500, width: 500, radius: 200 };
var center = { x: (dimensions.width / 2 + 5), y: (dimensions.height / 2 + 5)};

// create svg container
var svg = d3.select('.donut')
  .append('svg')
  .attr('width', dimensions.width + 150)
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
  .innerRadius(dimensions.radius / 2.3);

var  color = d3.scaleOrdinal(d3["schemeCategory10"]);

// legend setup
var legendGroup = svg.append('g')
  .attr('transform', `translate(${dimensions.width + 40}, 10)`)

var legend = d3.legendColor()
  .shape('circle')
  .shapePadding(10)
  .scale(color)

// update function
var update = (data) => {

  // update color scale domain
  color.domain(data.map(d => d.country))

    // update legend
  legendGroup.call(legend);
  legendGroup.selectAll('text').attr('fill', 'black');
  
  // join enhanced (pie) data to path elements
  var paths = graph.selectAll('path')
    .data(pie(data));
      // console.log('pie(data): ',pie(data));
     // console.log('paths: ', paths);
  
  // handle the exit selection
  paths.exit().remove()
    .transition().duration(750)
    .attrTween("d", arcTweenExit)
    .remove();

  // handle the current DOM path updates
  paths.attr('d', arcPath)
    .transition().duration(750)
    .attrTween('d', arcTweenUpdate)

  paths.enter()
    .append('path')
      .attr('class', 'arc')
      // .attr('d', d => arcPath(d)) //  .attr('d', arcPath) //
      .attr('stroke', 'grey')
      .attr('stroke-width', 2)
      .attr('fill', d => color(d.data.country))
      .each(function(d){ this._current = d })
      .transition().duration(750).attrTween("d", arcTweenEnter);
      
      // .transition().duration(750).attrTween("d", arcTweenEnter)

};

// data array to hold the api data
var top10Countries = [];

d3.json('/countries').then( (data) =>  {
  // console.log('data: ', data);
  top10 = data.slice(0, 10)
  // console.log('top10 : ', top10);
  top10.forEach(element => {
    top10Countries.push(element)
  });

  // console.log('top10Countries : ', top10Countries);
  // console.log('top10[0]: ', top10[0]);
  // console.log('top10[0].country: ', top10[0].country);
  
  update(top10Countries)
  console.log('top10Countries1: ', top10Countries);

  // setTimeout(function(){ 
  //   alert("Hello")
  //   let first = top10Countries[0].respondentCount
  //   let second = top10Countries[1].respondentCount
  //   top10Countries[0].respondentCount = second
  //   top10Countries[1].respondentCount = first;

  //   update(top10Countries)
  //   console.log('top10Countries2: ', top10Countries);

  // }, 750);

});

const arcTweenEnter = (d) => {
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