// DONUT CHART: PROGRAMING key POPULARITY BY GENDER
$( document ).ready(function(){
  // $(".dropdown-button").dropdown();
  $(".dropdown-trigger").dropdown();

})

// $(".dropdown-trigger").dropdown();


function buildDonut(url, selector) {
  var dimensions = { height: 800, width: 500, radius: 200 };
  var center = { x: (dimensions.width / 2 + 5), y: (dimensions.height / 2 + 5)}
  // ==================================================
  // var dimensions = { height: 300, width: 300, radius: 150 };
  // var center = { x: (dimensions.width / 2 + 5), y: (dimensions.height / 2 + 5)};
  // create svg container
  var svg = d3.select(selector)
    .append('svg')
    .attr('width', dimensions.width + 550)
    .attr('height', dimensions.height - 200);
    
    // translate(255, 405)

  var graph = svg.append('g')
    .attr("transform", `translate(${center.x - 50}, ${center.y - 200})`);
    // translates the graph group to the middle of the svg container
  
  var pie = d3.pie()
    .sort(null)
    .value(d => d.value);
    // the value we are evaluating to create the pie angles
  
  var arcPath = d3.arc()
    .outerRadius(dimensions.radius)
    .innerRadius(dimensions.radius / 1.3);
  
  // ordinal colour scale
  var  color = d3.scaleOrdinal(d3["schemeCategory10"]); 
  
  // legend setup
  var legendGroup = svg.append('g')
    .attr('transform', `translate(${dimensions.width - 50}, 10)`)
  
  var legend = d3.legendColor()
    // .shape('circle')
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
  
  // update function
  var update = (data) => {
  
    // update color scale domain
    color.domain(data.map(d => d.key))
  
      // update legend
    legendGroup.call(legend);
    legendGroup.selectAll('text').attr('fill', 'white');
    
    // join modified (pie) data to path elements
    var paths = graph.selectAll('path')
      .data(pie(data));
        // console.log('pie(data): ',pie(data));
       // console.log('paths: ', paths);
    
    // handle the exit selection
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
  var data_array = [];
  
  // visit the api to retrieve the data
  d3.json(url).then( data =>  {
      // console.log('data: ', data);
      var counter = 0;
  
      data.forEach(obj => {
      Object.values(obj).forEach(val => counter += val);
    });
      // console.log(counter)
      
      data.forEach(obj => {
        Object.entries(obj).forEach(([key,value]) => {
          tempDict = {}
          tempDict['key'] = String(key)
          tempDict['value'] = +value
          tempDict['percentage'] = +(value/counter*100).toFixed(2)
          data_array.push(tempDict)
        } );
      });
  
      // console.log('data_array: ', data_array);
  
      data_array.sort(function(a, b){
        return b.value-a.value
      })

      // data_array.forEach(el => console.log(el.value))
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
        .attr('fill', color(d.data.key));
  };
  
  var handleClick = d => {
    // console.log('d inside click: ', d) 
    // console.log('top10Countries: ', top10Countries);
  
    // var newData = data_array.filter(c => c.key !== d.data.key)
  
    // console.log('top10Countries', top10Countries);
    // console.log('newData', newData);
    // update(newData)
    update(newData)
  
  }
}

buildDonut('/api/socialmedia', '#socialmedia')

buildDonut('/api/gender', '#gender')
buildDonut('/api/trans', '#trans')
buildDonut('/api/dependents', '#dependents')
buildDonut('/api/edlevel', '#edlevel')
buildDonut('/api/employment', '#employment')
buildDonut('/api/careersat', '#careersat')
buildDonut('/api/jobsat', '#jobsat')
buildDonut('/api/jobseek', '#jobseek')
buildDonut('/api/mgrmoney', '#mgrmoney')
buildDonut('/api/mgrwant', '#mgrwant')
buildDonut('/api/workplan', '#workplan')
buildDonut('/api/workloc', '#workloc')
buildDonut('/api/sojobs', '#sojobs')
buildDonut('/api/soaccount', '#soaccount')
buildDonut('/api/extraversion', '#extraversion')
// buildDonut('/api/socialmedia', '#socialmedia')
buildDonut('/api/opsys', '#opsys')
buildDonut('/api/blockchainis', '#blockchainis')
buildDonut('/api/impsyn', '#impsyn')
buildDonut('/api/fizzbuzz', '#fizzbuzz')
buildDonut('/api/offon', '#offon')
buildDonut('/api/betterlife', '#betterlife')
buildDonut('/api/undergradmajor', '#undergradmajor')
buildDonut('/api/mgridiot', '#mgridiot')

buildDonut('/api/socialmedia', '#socialmedia')




// var apiRoutes = ['gender','trans', 'dependents', 'edlevel','employment',
// 'careersat', 'jobsat', 'jobseek', 'mgrmoney', 'mgrwant', 'workplan',
// 'workloc', 'sojobs', 'soaccount', 'extraversion', 'socialmedia',
// 'opsys', 'blockchainis', 'impsyn','fizzbuzz', 'offon','betterlife'
// ]

// for (let index = 0; index < apiRoutes.length; index++) {
//   const element = apiRoutes[index];
//   const params = `"/api/${element}", "#${element}"`
//   buildDonut(params)
  
// }

// apiRoutes.forEach(route => {
//     var params = `/api/${route}, #${route}`
//     buildDonut(params)
// })
