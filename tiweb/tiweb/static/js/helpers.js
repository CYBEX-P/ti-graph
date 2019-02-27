exportDB = function(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            //var data1 = this.responseText;
            console.log(xhttp.responseText);
            var data1 = JSON.parse(xhttp.responseText);
            document.getElementById("testdiv").innerHTML =
            "<h1>Data Export Successful</h1>";
        }
        xhttp.open("GET", "http://127.0.0.1:5000/neo4j/export", true);
        xhttp.send();
        var nodes = [];
        var edges = [];
        for (i = 0; i < data1.length; i++) {
            edges.push({
                from: data1[i].from,
                to: data1[i].to,
                type: data1[i].type
            }); 
            var nodeItem = {
                id: data1[i].id,
                label: data1[i].label,
                value: data1[i].IP
            };
            nodes.push(nodeItem); 
        }
        var data = {
            nodes: nodes,
            edges: edges
        };

        var options = {};
        var container = document.getElementById("mynetwork");
        var network = new vis.Network(container, data, options);
    }
}

