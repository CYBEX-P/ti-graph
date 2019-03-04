exportDB = function(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
    
           var data = JSON.parse(xhttp.responseText);
           UpdateGraph(data);
           
        }
    }
    xhttp.open("GET", "http://localhost:5000/neo4j/export", true);
    xhttp.setRequestHeader("Access-Control-Allow-Origin", '*');
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

wipeDB = function(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        
            var data = JSON.parse(xhttp.responseText);
            exportDB();
        }
    }
    xhttp.open("GET", "http://localhost:5000/neo4j/wipe", true);
    xhttp.setRequestHeader("Access-Control-Allow-Origin", '*');
    xhttp.send();
}

insertIP = function(IP) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        
            var data = JSON.parse(xhttp.responseText);
            exportDB();
        }
    }
    xhttp.open("GET", `http://localhost:5000/neo4j/insert/IP/${IP}`, true);
    xhttp.setRequestHeader("Access-Control-Allow-Origin", '*');
    xhttp.send();
}

ASN = function(IP){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        
            var data = JSON.parse(xhttp.responseText);
            exportDB();
        }
    }
    xhttp.open("GET", `http://localhost:5000/enrich/asn/${IP}`, true);
    xhttp.setRequestHeader("Access-Control-Allow-Origin", '*');
    xhttp.send();
}

GIP = function(IP){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        
            var data = JSON.parse(xhttp.responseText);
            if(data["GIP insert status"] != 0){
                exportDB();
            }
            else{
                alert("Geoip lookup returned nothing.");
            }
        }
    }
    xhttp.open("GET", `http://localhost:5000/enrich/gip/${IP}`, true);
    xhttp.setRequestHeader("Access-Control-Allow-Origin", '*');
    xhttp.send();
}

whois = function(IP){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        
            var data = JSON.parse(xhttp.responseText);
            if(data["Whois insert status"] != 0){
                exportDB();
            }
            else{
                alert("Whois lookup returned nothing.");
            }

        }
    }
    xhttp.open("GET", `http://localhost:5000/enrich/whois/${IP}`, true);
    xhttp.setRequestHeader("Access-Control-Allow-Origin", '*');
    xhttp.send();
}

host = function(IP){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        
            var data = JSON.parse(xhttp.responseText);
            if(data["Hostname insert status"] != 0){
                exportDB();
            }
            else{
                alert("Hostname lookup returned nothing.");
            }
            
        }
    }
    xhttp.open("GET", `http://localhost:5000/enrich/hostname/${IP}`, true);
    xhttp.setRequestHeader("Access-Control-Allow-Origin", '*');
    xhttp.send();
}