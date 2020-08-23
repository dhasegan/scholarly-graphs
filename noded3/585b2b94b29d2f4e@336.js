import define1 from "./a33468b95d0b15b0@695.js";

export default function define(runtime, observer) {
  const main = runtime.module();
  const fileAttachments = new Map([["table.tsv",new URL("./files/aab4366cc0cae2b2289c37e5c86d719086bfbad5d3c52f1219750697d6f61bc0123e0a254381a3f6bb31bbfb4c5289b17bed44582df035c4e0e58e2bcfe96757",import.meta.url)]]);
  main.builtin("FileAttachment", runtime.fileAttachments(name => fileAttachments.get(name)));
  main.variable(observer()).define(["md"], function(md){return(
md`# Graph of Neuroscientists

Downloaded and created from google scholar`
)});
  main.variable(observer()).define(["swatches","color2"], function(swatches,color2){return(
swatches({color:color2})
)});
  main.variable(observer()).define(["swatches","color"], function(swatches,color){return(
swatches({color})
)});
  main.variable(observer("chart")).define("chart", ["data","d3","width","height","types","color","titles","color2","location","drag","titlesMap","linkArc","invalidation"], function(data,d3,width,height,types,color,titles,color2,location,drag,titlesMap,linkArc,invalidation)
{
  const links = data.links.map(d => Object.create(d));
  const nodes = data.nodes.map(d => Object.create(d));

  const simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).id(d => d.id))
      .force("charge", d3.forceManyBody().strength(-100))
      .force("x", d3.forceX())
      .force("y", d3.forceY());

  const svg = d3.create("svg")
      .attr("viewBox", [-width / 2, -height , width, height*2])
      .style("font", "12px sans-serif");

  // Per-type markers, as they don't inherit styles.
  svg.append("defs").selectAll("marker")
    .data(types)
    .join("marker")
      .attr("id", d => `arrow-${d}`)
      .attr("viewBox", "0 -5 10 10")
      .attr("refX", 15)
      .attr("refY", -0.5)
      .attr("markerWidth", 0)
      .attr("markerHeight", 0)
      .attr("orient", "auto")
    .append("path")
      .attr("fill", color)
      .attr("d", "M0,-5L10,0L0,5");
  
  // Per-type markers, as they don't inherit styles.
  svg.append("defs").selectAll("marker")
    .data(titles)
    .join("marker")
      .attr("id", d => `title-${d}`)
      .attr("viewBox", "0 -5 10 10")
      .attr("refX", 15)
      .attr("refY", -0.5)
      .attr("markerWidth", 0)
      .attr("markerHeight", 0)
      .attr("orient", "auto")
    .append("path")
      .attr("fill", color2)
      .attr("d", "M0,-5L10,0L0,5");

  const link = svg.append("g")
      .attr("fill", "none")
      .attr("stroke-width", 1)
    .selectAll("path")
    .data(links)
    .join("path")
      .attr("stroke", d => color(d.type))
      .attr("marker-end", d => `url(${new URL(`#arrow-${d.type}`, location)})`);

  const node = svg.append("g")
      .attr("fill", "currentColor")
      .attr("stroke-linecap", "round")
      .attr("stroke-linejoin", "round")
    .selectAll("g")
    .data(nodes)
    .join("g")
      .call(drag(simulation));

  node.append("circle")
      .attr("stroke", "white")
      .attr("stroke-width", 1.5)
      .attr("fill", d => color2(titlesMap[d.id]))
      .attr("r", 6);

  node.append("text")
      .attr("x", 8)
      .attr("y", "0.31em")
      .text(d => d.id)
    .clone(true).lower()
      .attr("fill", "none")
      .attr("stroke", "white")
      .attr("stroke-width", 3);

  simulation.on("tick", () => {
    link.attr("d", linkArc);
    node.attr("transform", d => `translate(${d.x},${d.y})`);
  });

  invalidation.then(() => simulation.stop());

  return svg.node();
}
);
  main.variable(observer("links")).define("links", ["d3","FileAttachment"], async function(d3,FileAttachment){return(
d3.tsvParse(await FileAttachment("table.tsv").text())
)});
  main.variable(observer()).define(["links"], function(links){return(
links
)});
  main.variable(observer("types")).define("types", ["links"], function(links){return(
Array.from(new Set(links.map(d => d.type)))
)});
  main.variable(observer("data")).define("data", ["links"], function(links){return(
{nodes: Array.from(new Set(links.flatMap(l => [l.source, l.target])), id => ({id})), links}
)});
  main.variable(observer()).define(["data"], function(data){return(
data.nodes
)});
  main.variable(observer("titlesMap")).define("titlesMap", ["links"], function(links)
{
  const res = {}
  links.forEach(l => {
    res[l.source] = l.sourceTitle
    res[l.target] = l.targetTitle
  })
  return res
}
);
  main.variable(observer("titles")).define("titles", ["titlesMap"], function(titlesMap){return(
Array.from(new Set(Object.values(titlesMap)))
)});
  main.variable(observer("height")).define("height", function(){return(
600
)});
  main.variable(observer("color")).define("color", ["d3","types"], function(d3,types){return(
d3.scaleOrdinal(types, d3.schemeCategory10)
)});
  main.variable(observer("color2")).define("color2", ["d3","titles"], function(d3,titles){return(
d3.scaleOrdinal(titles, d3.schemeCategory10)
)});
  main.variable(observer("linkArc")).define("linkArc", function(){return(
function linkArc(d) {
  const r = Math.hypot(d.target.x - d.source.x, d.target.y - d.source.y);
  return `
    M${d.source.x},${d.source.y}
    S${d.target.x},${d.target.y}
     ${d.target.x},${d.target.y}
  `;
}
)});
  main.variable(observer("drag")).define("drag", ["d3"], function(d3){return(
simulation => {
  
  function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
  }
  
  function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
  }
  
  function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
  }
  
  return d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended);
}
)});
  main.variable(observer("d3")).define("d3", ["require"], function(require){return(
require("d3@5")
)});
  const child1 = runtime.module(define1);
  main.import("swatches", child1);
  return main;
}
