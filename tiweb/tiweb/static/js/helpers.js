exportDB = function(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
    
           var data = JSON.parse(xhttp.responseText);
           UpdateGraph(data)
           
        }
    }
    xhttp.open("GET", "http://localhost:5000/neo4j/export", true);
    xhttp.send();
}

function UpdateGraph(data){
    var dataObject = {
        nodes: data['Neo4j'][0][0]['nodes'],
        edges: data['Neo4j'][1][0]['edges']
    };

    var options = {layout: {improvedLayout: false}};
    var container = document.getElementById("mynetwork");
    var network = new vis.Network(container, dataObject, options);

}

