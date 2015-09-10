var width = 960,
    height = 500;

var color = d3.scale.category20();

var force = d3.layout.force()
    .linkDistance(30)
    .charge(-120)
    .size([width, height]);

var svg = d3.select("section.main-section").append("svg")
    .attr("width", width)
    .attr("height", height);

ajaxGet('/api/app-traffic', function(graph){
    console.log(graph)
    force
      .nodes(graph.nodes)
      .links(graph.links)
      .start();

    var link = svg.selectAll(".link")
      .data(graph.links)
      .enter().append("line")
      .attr("class", "link")
      .style("stroke-width", function(d) { return Math.sqrt(d.value); });

    var node = svg.selectAll(".node")
      .data(graph.nodes)
      .enter()
    .append("svg:a")
      .attr("xlink:href", function(d) { return d.url; })
    .append("circle")
      .attr("class", "node")
      .attr("r", 5)
      .style("fill", function(d){ return color(d.group); })
      .call(force.drag);

    node.append("title")
      .text(function(d) { return d.name; });

    force.on("tick", function(){
      link.attr("x1", function(d) { return d.source.x; })
          .attr("y1", function(d) { return d.source.y; })
          .attr("x2", function(d) { return d.target.x; })
          .attr("y2", function(d) { return d.target.y; });

      node.attr("cx", function(d) { return d.x; })
          .attr("cy", function(d) { return d.y; });
    });
});
