var margin = {top: 20, right: 30, bottom: 30, left: 40},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

/*var data2 = [
    {label:"Marcel", values:[ 17,  4,  2,  7]},
    {label:"Jean", values:[ 2,  2,  5, 10]},
    {label:"Jacques", values:[ 2, 4, 7,  2]},
    {label:"Rene", values:[ 1, 7, 8,  2]},
    {label:"balbla", values:[ 1, 6, 1,  2]}];*/





d3.json("/static/timeline.json", function(error, json) {
    if (error) return console.warn(error);
    var data2 = json.toto;



// permute the data
data = data2.map(function(d) { return d.values.map(function(p, i) { return {x:i, y:p, y0:0}; }); });

var colors = d3.scale.category20();

var x = d3.scale.linear()
    .range([0, width])
    .domain([0,data2[0].values.length-1]);

var y = d3.scale.linear()
    .range([height, 0])
    .domain([0,22]);


var z = d3.scale.category20c();

var svg = d3.select("#tl").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")")


var stack = d3.layout.stack()
    .offset("zero");

var layers = stack(data);

var area = d3.svg.area()
    .interpolate('cardinal')
    .x(function(d, i) { return x(i); })
    .y0(function(d) { return y(d.y0); })
    .y1(function(d) { return y(d.y0 + d.y); });

svg.selectAll(".layer")
    .data(layers)
    .enter().append('g')
        .attr("class", "layer")
        .append("path")
            .attr("d", function(d) { return area(d); })
            .style("fill", function(d, i) { return colors(i); });

svg.selectAll(".layer")
    .append('text')
    .attr("x", function(d,i) {
        var maxi = Math.max.apply(null, data2[i].values);
        var indice = data2[i].values.indexOf(maxi);
        if (indice===0) {return x(indice)+10; }
        else if (indice===(data2[i].values.length-1)) {return x(indice)-10; }
        else {return x(indice);}
    })
    .attr("y", function(d,i) {
        var maxi = Math.max.apply(null, data2[i].values);
        var indice = data2[i].values.indexOf(maxi);
        return y(d[indice].y0 + d[indice].y/2);
    })
    .attr("text-anchor", function(d,i) {
        var maxi = Math.max.apply(null, data2[i].values);
        var indice = data2[i].values.indexOf(maxi);
        if (indice === (d.length-1)) {return "end";}
        else if (indice===0) {return "start"; }
        else {return "middle";}
    })
    .text(function(d,i) {
        return data2[i].label;
    })
    .attr("font-family", "impact")
    .attr("fill", "white")
    .attr("font-size","25px");

});
