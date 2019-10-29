eel.expose(consoleLog)
function consoleLog(data) {
    console.log(data); 
}

eel.expose(setCtxt)
function setCtxt(html) {
    console.log("Ctxt:"+html);
    document.querySelector("#ctxt-val").innerHTML = html;
}

eel.expose(setIntr)
function setIntr(html) {
    console.log("Intr:"+html);
    document.querySelector("#intr-val").innerHTML = html;
}

eel.expose(setMemoryTotal)
function setMemoryTotal(html) {
    console.log("Mem Total:"+html);
    document.querySelector("#memoryTotal-val").innerHTML = html;
}

eel.expose(setMemoryAvailable)
function setMemoryAvailable(html) {
    console.log("Mem Avail:"+html);
    document.querySelector("#memoryAvailable-val").innerHTML = html;
}

eel.expose(setMemoryUtilization)
function setMemoryUtilization(html) {
    console.log("Mem Util:"+html);
    document.querySelector("#memoryUtilization-val").innerHTML = html;
}

eel.expose(setDiskStats)
function setDiskStats(data) {
    console.log("Disk Stats:"+data);
    html="<div>"
    for(let i = 0; i<data.length; i++)
    { 
        disk = JSON.parse(data[i])
        html+="<p>"+disk["name"]+"</p>"
        html+="<p>Disk Reads: "+disk["diskReads"]+"/s</p>"
        html+="<p>Disk Writes: "+disk["diskWrites"]+"/s</p>"
        html+="<p>Block Reads: "+disk["blockReads"]+"/s</p>"
        html+="<p>Block Writes: "+disk["blockWrites"]+"/s</p>"
        html+="<hr />"

    }
    html+="</div>"
    
    document.querySelector("#disks-val").innerHTML = html;
}

eel.expose(setCpuStats)
function setCpuStats(data) {
    console.log("Cpu Stats:"+data);
    html=""
    for(let i = 0; i<data.length; i++)
    { 
        cpu = JSON.parse(data[i])
        html+="<p>"+cpu["name"]+"</p>"
        html+="<p>Total Utilization: "+cpu["totalUtil"]+"%</p>" 
        html+="<p>User Mode: "+cpu["userMode"]+"%</p>"
        html+="<p>Sys Mode: "+cpu["sysMode"]+"%</p>"
        html+="<hr />"

    } 
    
    document.querySelector("#cpu-val").innerHTML = html;
}

eel.expose(setNetworkStats)
function setNetworkStats(data) {
    console.log("Network Stats:"+data);
    html="<div>"
    for(let i = 0; i<data.length; i++)
    { 
        device = JSON.parse(data[i])
        html+="<p>"+device["name"]+"</p>"
        html+="<p>Bytes In: "+device["bytesIn"]+"/s</p>"
        html+="<p>Bytes Out: "+device["bytesOut"]+"/s</p>"
        html+="<p>Network Bandwidth: "+device["networkBandwidth"]/125000+" Mb/s</p>"
        html+="<p>Network Utilization: "+device["networkUtilization"]+"% per sec</p>"
        html+="<hr />"

    }
    html+="</div>"
    
    document.querySelector("#network-val").innerHTML = html;
}


eel.expose(setEstTcp)
function setEstTcp(est, active) {
    console.log("Established TCP:"+est);
    html = "Established Connections: "+est+" Active:"+active
    document.querySelector("#tcp-val").innerHTML = html;
}

eel.expose(setTcpConnections)
function setTcpConnections(data) {
    console.log("Tcp Connections:"+data);
    tcpData=[]
    for(let i = 0; i<data.length; i++)
    { 
        conn = JSON.parse(data[i])  

        tcpConn = [
            conn["id"],
            conn["uid"],
            conn["username"],
            conn["program"],
            conn["srcIP"]+":"+conn["srcPort"],
            conn["srcHostname"],
            conn["destIP"]+":"+conn["destPort"],
            conn["destHostname"]
        ] 

       tcpData.push(tcpConn)
    }

    $("#tcp-table").DataTable().clear().draw()
    $("#tcp-table").DataTable().rows.add(tcpData).draw()
}

eel.expose(setUdpConnections)
function setUdpConnections(data) {
    console.log("Udp Connections:"+data);
    udpData=[]
    for(let i = 0; i<data.length; i++)
    { 
        conn = JSON.parse(data[i])  

        udpConn = [
            conn["id"],
            conn["uid"],
            conn["username"],
            conn["program"],
            conn["srcIP"]+":"+conn["srcPort"],
            conn["srcHostname"],
            conn["destIP"]+":"+conn["destPort"],
            conn["destHostname"]
        ] 

       udpData.push(udpConn)
    }

    $("#udp-table").DataTable().clear().draw()
    $("#udp-table").DataTable().rows.add(udpData).draw()
}

eel.expose(setProcesses)
function setProcesses(data) {
    //console.log("Processes:"+data);
    processesData=[]

    for(let i = 0; i<JSON.parse(data).length; i++)
    { 
        process = JSON.parse(data) [i] 
        eachProcess = [
            ""+process["pid"],
            ""+process["name"],
            ""+process["userName"],
            ""+process["inodeNumber"],
            ""+process["userMode"]+"%",
            ""+process["sysMode"]+"%",
            ""+process["total"]+"%",
            ""+process["vMemUtil"]+"%",
            ""+process["phyMemUtil"]+"%" 
        ]  
        console.log(eachProcess)
        processesData.push(eachProcess)
    }

    $("#process-table").DataTable().clear().draw()
    $("#process-table").DataTable().rows.add(processesData).draw()
}
  

$(document).ready(function() {
    
    $("#tcp-table").DataTable();
    $("#udp-table").DataTable();
    $("#process-table").DataTable();
});

function changeTimeInterval(selectObj)
{
    eel.setTimeInterval(selectObj.value)
}
/************************* */
var totalMemory = 0;
var memoryDp = [
    { y: 519960, name: "Used", color: "#E7823A" },
    { y: 363040, name: "Available", color: "#546BC1" }
]
var memoryData = {
	"Used Vs Available Memory": [{
		cursor: "pointer",
		innerRadius: "75%",
		legendMarkerType: "square",
		name: "Used Vs Available Memory",
		radius: "100%",
		showInLegend: true,
		startAngle: 90,
		type: "doughnut",
		dataPoints: memoryDp
	}]
};

var memoryChart = new CanvasJS.Chart("memoryChartContainer",{
    title:{
        text:"Used Vs Available Memory"
    }
});
memoryChart.options.data = visitorsData["New vs Returning Visitors"];
chart.render();
