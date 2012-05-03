 // Load the Visualization API and the piechart package.
      google.load("visualization", "1", {packages:["corechart","geochart"]});
      google.setOnLoadCallback(drawCharts);

      //class Set
      var Set = function(){}
      Set.prototype.add = function(o) { this[o] = true; }
      Set.prototype.remove = function(o) { delete this[o]; }
      Set.prototype.get_list = function(o){ 
        return Object.keys(this)
      }
      //-- end set

      //returns a set with keys of both dicts. 
      function getKeys(dict1,dict2){
        var s = new Set()
        for (var key in dict1){ s.add(key); }
        for (var key in dict2){ s.add(key); }
        return s
      }

      function drawCharts(){
        drawChart1()
        drawChart2()
        drawChart3()
        drawChart4()
      };

      function createData(data){
        datas = []
        keys = getKeys(data['pos'],data['neg']); 
        header = ['Feature','Positives','Negatives']
        datas.push(header);
       
        $.each(keys.get_list(),function(index,feature) {
          datas.push([ feature, data['pos'][feature], data['neg'][feature] ]);
        });

        console.log(datas)
        var data = google.visualization.arrayToDataTable(datas)
        return data
      }

      function drawChart1() {

        $.getJSON("http://localhost:8080/stats/freqfeature",function(datos){

          data = createData(datos)
          var options = {
            title: 'Features stats',
            vAxis: {title: 'Features',  titleTextStyle: {color: 'green'}}
          };

          var chart1 = new google.visualization.ColumnChart(document.getElementById('chart_div1'));
          chart1.draw(data, options);
        });
      };

      function drawChart2() {
        var data = google.visualization.arrayToDataTable([
          ['Feature', 'Positives', 'Negatives'],
          ['view',      70,       30],
          ['location',  80,       18],
          ['staff',     20,       60],
          ['comfort',   24,       70],
          ['clean',     28,       30],
          ['facilities',40,       35],
          ['services',  37,       64],
        ]);

        var options = {
          title: 'Features stats',
          vAxis: {title: 'Features',  titleTextStyle: {color: 'green'}}
        };

        var chart2 = new google.visualization.BarChart(document.getElementById('chart_div2'));
        chart2.draw(data, options);
      };

      function drawChart3() {
        
        $.getJSON("http://localhost:8080/stats/totalposneg",function(datos){
        
          console.log(datos)
          var data = google.visualization.arrayToDataTable([
            ['Feature', 'Positives'],
            ['pos',      datos['pos']],
            ['neg',      datos['neg']],
            
          ]);

          var options = {
            title: 'Total Positives, Negatives',
            vAxis: {title: 'Features',  titleTextStyle: {color: 'green'}}
          };

          var chart3 = new google.visualization.PieChart(document.getElementById('chart_div3'));
          chart3.draw(data, options);
        });
      }

      function drawChart4() {

        var data = google.visualization.arrayToDataTable([
          ['Country', 'Popularity'],
          ['Germany', 200],
          ['United States', 300],
          ['Brazil', 400],
          ['Canada', 500],
          ['France', 600],
          ['RU', 700]
        ]);

        var options = {
          title: 'Features stats'
        };

        var chart4 = new google.visualization.GeoChart(document.getElementById('chart_div4'));
        chart4.draw(data, options);
      };
      