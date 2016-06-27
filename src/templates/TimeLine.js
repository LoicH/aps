var margin = {top: 20, right: 30, bottom: 30, left: 40},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

/*var data = [
    [ 17,  4,  2,  7],
    [ 2,  2,  5, 10],
    [ 2, 4, 7,  2],
    [ 1, 7, 8,  2],
    [ 1, 6, 1,  2]];*/



d3.json("timeline.json", function(error, json) {
    if (error) return console.warn(error);
    var data = json.data;



// permute the data
data = data.map(function(d) { return d.map(function(p, i) { return {x:i, y:p, y0:0}; }); });

var colors = d3.scale.category10();

var x = d3.scale.linear()
    .range([0, width])
    .domain([0,3]);

var y = d3.scale.linear()
    .range([height, 0])
    .domain([0,25]);

var z = d3.scale.category20c();

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var stack = d3.layout.stack()
    .offset("zero")

var layers = stack(data);

var area = d3.svg.area()
    .interpolate('cardinal')
    .x(function(d, i) { return x(i); })
    .y0(function(d) { return y(d.y0); })
    .y1(function(d) { return y(d.y0 + d.y); });

svg.selectAll(".layer")
    .data(layers)
    .enter().append("path")
    .attr("class", "layer")
    .attr("d", function(d) { return area(d); })
    .style("fill", function(d, i) { return colors(i); });

});