var apiRoutes = ['gender','trans', 'dependents', 'edlevel','employment',
'careersat', 'jobsat', 'jobseek', 'mgrmoney', 'mgrwant', 'workplan',
'workloc', 'sojobs', 'soaccount', 'extraversion', 'socialmedia',
'opsys', 'blockchainis', 'impsyn','fizzbuzz', 'offon','betterlife'
]

for (let index = 0; index < apiRoutes.length; index++) {
  var url = apiRoutes[index];
  var  selector = `#${url}"`
  buildDonut(url, selector)
}


function buildDonut(url, selector) {
  var dimensions = { height: 800, width: 500, radius: 200 };
  var center = { x: (dimensions.width / 2 + 5), y: (dimensions.height / 2 + 5)}

  var svg = d3.select(selector)
    .append('svg')
    .attr('width', dimensions.width + 550)
    .attr('height', dimensions.height - 200);

  var graph = svg.append('g')
    .attr("transform", `translate(${center.x - 50}, ${center.y - 200})`);
  
  var pie = d3.pie()
    .sort(null)
    .value(d => d.value);
  
  var arcPath = d3.arc()
    .outerRadius(dimensions.radius)
    .innerRadius(dimensions.radius / 1.7);
  
  var  color = d3.scaleOrdinal(d3["schemeCategory10"]); 
  
  var legendGroup = svg.append('g')
    .attr('transform', `translate(${dimensions.width - 50}, 10)`)
  
  var legend = d3.legendColor()
    .shape('path', d3.symbol().type(d3.symbolCircle)())
    .shapePadding(10)
    .scale(color)
  
  var tip = d3.tip()
    .attr('class', 'tip card')
    .html(d => {
      let content = `<div class="key">${d.data.key}</div>`;
      content += `<div class="percentage">${d.data.percentage} %</div>`;
      content += `<div class="respondents">${d.data.value} Respondents</div>`
      return content;
    });
  
  graph.call(tip);
  
  var update = (data) => {
  
    color.domain(data.map(d => d.key))
  
    legendGroup.call(legend);
    legendGroup.selectAll('text').attr('fill', 'white');
    
    var paths = graph.selectAll('path')
      .data(pie(data));
    paths.exit()
      .transition().duration(750)
      .attrTween("d", arcTweenExit)
      .remove();
  
    paths.transition().duration(750)
    .attrTween("d", arcTweenUpdate);
  
    paths.enter()
      .append('path')
        .attr('class', 'arc')
        .attr('stroke', '#ebebeb')
        .attr('stroke-width', 1.1)
        .attr('d', arcPath)
        .attr('fill', d => color(d.data.key))
        .each(function(d){ this._current = d })
        .transition().duration(750).attrTween("d", arcTweenEnter);
        
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
  
  var data_array = [];
  
  d3.json(url).then( data =>  {
      var counter = 0;
  
      data.forEach(obj => {
      Object.values(obj).forEach(val => counter += val);
    });
      
      data.forEach(obj => {
        Object.entries(obj).forEach(([key,value]) => {
          tempDict = {}
          tempDict['key'] = String(key)
          tempDict['value'] = +value
          tempDict['percentage'] = +(value/counter*100).toFixed(2)
          data_array.push(tempDict)
        } );
      });
  
      data_array.sort(function(a, b){
        return b.value-a.value
      })

      console.log('sorted data_array: ', data_array);
  
      update(data_array)
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
    var i = d3.interpolate(this._current, d);
    this._current = i(1);
    return function(t) {
      return arcPath(i(t));
    };
  };

  var handleMouseOver = (d,i,n) => {
    d3.select(n[i])
      .transition('changeSliceFill').duration(300)
        .attr('fill', 'black');
  };
  
  var handleMouseOut = (d,i,n) => {
    d3.select(n[i])
      .transition('changeSliceFill').duration(300)
        .attr('fill', color(d.data.key));
  };
  
}


