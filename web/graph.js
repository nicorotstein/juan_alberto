function init() {
    /**
     * sigma.js instance 1 (banner) :
     */
    s1 = sigma.init(document.getElementById('sigma-1')).configProperties({
      drawHoverNodes: false
    }).mouseProperties({
      mouseEnabled: true,
    }).graphProperties({
      scalingMode: 'inside'
    }).drawingProperties({
      defaultLabelColor: '#fff',
      defaultLabelSize: 14,
      defaultLabelBGColor: '#fff',
      defaultLabelHoverColor: '#000',
      labelThreshold: 6,
      defaultEdgeType: 'curve'
    }).graphProperties({
      minNodeSize: 0.5,
      maxNodeSize: 5,
      minEdgeSize: 1,
      maxEdgeSize: 1
    }).mouseProperties({
      maxRatio: 32
    });
       // Bind events :
    s1.bind('overnodes',function(event){
      var nodes = event.content;
      var neighbors = {};
      s1.iterEdges(function(e){
        if(nodes.indexOf(e.source)>=0 || nodes.indexOf(e.target)>=0){
          neighbors[e.source] = 1;
          neighbors[e.target] = 1;
        }
      }).iterNodes(function(n){
        if(!neighbors[n.id]){
          n.hidden = 1;
        }else{
          n.hidden = 0;
        }
      }).draw(2,2,2);
    }).bind('outnodes',function(){
      s1.iterEdges(function(e){
        e.hidden = 0;
      }).iterNodes(function(n){
        n.hidden = 0;
      }).draw(2,2,2);
    });
    
    s1.parseGexf('../data/les_miserables.gexf');
    console.log(s1)

    s1.draw();
  
    var newParent = document.getElementById('mouselayer-sigma-1');
    var mouseLayer = document.getElementById('sigma_mouse_1');

    newParent.appendChild(mouseLayer);

    mouseLayer.addEventListener('mouseover', function() {
      s1.activateFishEye();
    }, true);
    mouseLayer.addEventListener('mouseout', function() {
      s1.desactivateFishEye().draw(2,2,2);
    }, true);

    /**
     * Resize every instances on window resizing, and
     * some divs :
     */
    function resize(event){
      for(var key in sigma.instances) {
        sigma.instances[key].resize();
      }
    };

    window.onresize = resize;
    resize();
  }

  /**
   * Wait for the DOM to be ready to start :
   */
  if (document.addEventListener) {
    document.addEventListener("DOMContentLoaded", init, false);
  } else {
    window.onload = init;
  }