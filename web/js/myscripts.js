/* COPIED FROM: https://stackoverflow.com/questions/15900485/correct-way-to-convert-size-in-bytes-to-kb-mb-gb-in-javascript*/
function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];

    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}


eel.expose(consoleLog)
function consoleLog(data) {
    console.log(data); 
}

eel.expose(setCtxt)
function setCtxt(html) {
    //console.log("Ctxt:"+html);
    document.querySelector("#ctxt-val").innerHTML = html.toFixed(2)+" context switches/s";
}

eel.expose(setIntr)
function setIntr(html) {
    //console.log("Intr:"+html);
    document.querySelector("#intr-val").innerHTML = html.toFixed(2)+" interrupts/s";
}

eel.expose(setMemoryTotal)
function setMemoryTotal(html) {
    //console.log("Mem Total:"+html);
    document.querySelector("#memoryTotal-val").innerHTML = html.toFixed(2);
}

eel.expose(setMemoryAvailable)
function setMemoryAvailable(html) {
    //console.log("Mem Avail:"+html);
    document.querySelector("#memoryAvailable-val").innerHTML = html.toFixed(2);
}

eel.expose(setMemoryUtilization)
function setMemoryUtilization(html) {
    //console.log("Mem Util:"+html);
    document.querySelector("#memoryUtilization-val").innerHTML = html.toFixed(2);
}

eel.expose(setMemoryStats)
function setMemoryStats(data){
    //console.log(data)
    setMemoryTotal(data[0])
    setMemoryAvailable(data[1])
    setMemoryUtilization(data[2])
    updateMemChart(data[0], data[1])
}

eel.expose(setDiskStats)
function setDiskStats(data) {
    //console.log("Disk Stats:"+data);
    let html=""
    for(let i = 0; i<data.length; i++)
    { 
        disk = JSON.parse(data[i])
        html+="<div><div class=\"uk-card uk-card-default uk-card-small uk-card-body\">"
        html+="<h3 class=\"uk-card-title\">"+disk["name"]+"</h3>"
        html+="<p>Disk Reads: "+disk["diskReads"].toFixed(2)+"reads/s</p>"
        html+="<p>Disk Writes: "+disk["diskWrites"].toFixed(2)+"writes/s</p>"
        html+="<p>Block Reads: "+disk["blockReads"].toFixed(2)+"reads/s</p>"
        html+="<p>Block Writes: "+disk["blockWrites"].toFixed(2)+"writes/s</p>"
        html+="</div></div>"
    } 
    
    document.querySelector("#disks-val").innerHTML = html;
}

eel.expose(setCpuStats)
function setCpuStats(data) {
    //console.log("Cpu Stats:"+data);
    

    let html=""
    let utilData = {}
    for(let i = 0; i<data.length; i++)
    { 
        cpu = JSON.parse(data[i])
        html+="<div><div class=\"uk-card uk-card-default uk-card-small uk-card-body\">"
        html+="<h3 class=\"uk-card-title\">"+cpu["name"]+"</h3>"
        html+="<p>Total Utilization: "+cpu["totalUtil"].toFixed(2)+"%</p>" 
        html+="<p>User Mode: "+cpu["userMode"].toFixed(2)+"%</p>"
        html+="<p>Sys Mode: "+cpu["sysMode"].toFixed(2)+"%</p>"
        html+="</div></div>"

        utilData[cpu["name"]]=cpu["totalUtil"].toFixed(2)
    } 
    document.querySelector("#cpu-val").innerHTML = html;
    updateCpuChart(utilData)
}

eel.expose(setNetworkStats)
function setNetworkStats(data) {
    //console.log("Network Stats:"+data);
    
    let html=""
    for(let i = 0; i<data.length; i++)
    { 
        device = JSON.parse(data[i])
        html+="<div><div class=\"uk-card uk-card-default uk-card-body\">"
        html+="<h3 class=\"uk-card-title\">"+device["name"]+"</h3>"
        html+="<p><span uk-icon=\"icon: download\"></span> Receiving: "+formatBytes(device["bytesIn"],2)+"/s</p>"
        html+="<p><span uk-icon=\"icon: upload\"></span> Sending: "+formatBytes(device["bytesOut"],2)+"/s</p>"
        html+="<p>Network Bandwidth: "+device["networkBandwidth"]/125000+" Mb/s</p>"
        html+="<p>Average Utilization: "+formatBytes(device["networkUtilization"],2)+"/s</p>"
        html+="</div></div>"

    }
    html+="</div>"
    
    document.querySelector("#network-val").innerHTML = html;
}


eel.expose(setEstTcp)
function setEstTcp(est, active) {
    //console.log("Established TCP:"+est);
    let html = "<div class=\"uk-column-1-2  \"><p class=\"uk-text-primary\">"+est+" Established Connections</p><p class=\"uk-text-muted\">"+active+" Active Connections</p></div>";
    
    document.querySelector("#tcp-val").innerHTML = html;
}

eel.expose(setTcpConnections)
function setTcpConnections(data) {
    //console.log("Tcp Connections:"+data);
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

    tcpTable.clear().draw()
    tcpTable.rows.add(tcpData).draw()
}

eel.expose(setUdpConnections)
function setUdpConnections(data) {
    //console.log("Udp Connections:"+data);
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

    udpTable.clear().draw()
    udpTable.rows.add(udpData).draw()
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
            ""+process["userMode"].toFixed(2)+"%",
            ""+process["sysMode"].toFixed(2)+"%",
            ""+process["total"].toFixed(2)+"%",
            ""+formatBytes(process["vMemAvg"],2)+"/s",
            ""+process["phyMemUtil"].toFixed(2)+"%" 
        ]  
        //console.log(eachProcess)
        processesData.push(eachProcess)
    }

    processTable.clear().draw()
    processTable.rows.add(processesData).draw()
}
   
function changeTimeInterval(selectObj)
{
    eel.setTimeInterval(selectObj.value)
}

let tcpTable = ""
let udpTable = ""
let processTable = ""

$(document).ready(function() {
     
    tcpTable = $("#tcp-table").DataTable( {
    language: { search: '', searchPlaceholder: "Search" },paging: false
    });

    udpTable = $("#udp-table").DataTable( {
    language: { search: '', searchPlaceholder: "Search" },paging: false
    });

    processTable = $("#process-table").DataTable({      
    language: { search: '', searchPlaceholder: "Search" },
    paging: false, 
    "order": [[ 6, "desc" ]]});
    
    $('div.dataTables_filter input').addClass('uk-input uk-form-small') 
    $('div.dataTables_filter').css('width', '100%') 
});

/**************************/
/******** Charts **********/
/**************************/
window.chartColors = {
	red: 'rgb(255, 99, 132)',
	green: 'rgb(75, 192, 192)',
	yellow: 'rgb(255, 205, 86)',
	blue: 'rgb(54, 162, 235)',
	orange: 'rgb(255, 159, 64)',
	purple: 'rgb(153, 102, 255)',
	grey: 'rgb(201, 203, 207)'
};

window.transparentColors = {
	red: 'rgba(255, 99, 132,.1)',
	green: 'rgba(75, 192, 192,.1)',
	yellow: 'rgba(255, 205, 86,.1)',
	blue: 'rgba(54, 162, 235,.1)',
	orange: 'rgba(255, 159, 64,.1)',
	purple: 'rgba(153, 102, 255,.1)',
	grey: 'rgba(201, 203, 207,.1)'
};

let memConfig = {
    type: 'doughnut',
    data: {
        datasets: [{
            data: [
                0,
                0
            ],
            backgroundColor: [
                window.chartColors.red,
                window.transparentColors.red,
            ],
            label: 'Memory'
        }],
        labels: [
            'Used',
            'Free',
        ]
    },
    options: {
        responsive: true,
        legend: {
            position: 'bottom',
        },
        title: {
            display: false,
            text: 'Memory'
        },
        animation: {
            animateScale: false,
            animateRotate: false
        },
        circumference : 2*Math.PI,
        rotation : -1*Math.PI
    }
};
 
 
let cpuConfig = {
    type: 'line',
    data: {
        datasets: []
    },
    options: {
        responsive: true,
				title: {
					display: true,
					text: 'CPU UTILIZATION PER SECOND'
				},
				tooltips: {
					mode: 'index',
					intersect: false,
				},
				hover: {
					mode: 'nearest',
					intersect: true
				},
				scales: {
					xAxes: [{
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'Read Count'
						}
					}],
					yAxes: [{
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'Total Utilization Per Second'
                        },
                        ticks: {
                            suggestedMin: 0,
                            suggestedMax: 100
                        }
					}]
                },
                animation: { 
                    duration: 0, 
                },
			}
};


window.onload=function(){
    const memoryCtx = document.getElementById('memoryChart').getContext('2d');
    window.memoryChart = new Chart(memoryCtx,memConfig);


    const cpuCtx = document.getElementById('cpuChart').getContext('2d');
    window.cpuChart = new Chart(cpuCtx,cpuConfig);
}

function updateMemChart(total , avail)
{ 
    //console.log(total+" "+ avail)

    memConfig.data.datasets.forEach(function(dataset) {
        dataset.data.pop() 
        dataset.data.pop() 
    });

    memConfig.data.datasets.forEach(function(dataset) {
        dataset.data.push(avail);
        dataset.data.push((total-avail).toFixed(2));
    });

    window.memoryChart.update();

}

//let cpuChartPausedFlag = false
function updateCpuChart(utilData)
{
    if(cpuConfig.data.datasets.length == 0)    {
        initializeCpuChart(utilData)        
    }
    else
    {
        addToCpuChart(utilData)        
    }

    //if(!cpuChartPausedFlag)
        window.cpuChart.update(); 
}   

/*function toggleCpuChart()
{
    cpuChartPausedFlag = !cpuChartPausedFlag
}*/

function addToCpuChart(utilData)
{  
    let i = 0
    let flag = false
    for (const [key, value] of Object.entries(utilData)) { 

        cpuConfig.data.datasets[i]['data'].push(value)
        if (cpuConfig.data.datasets[i]['data'].length >= 11)
        { 
            cpuConfig.data.datasets[i]['data'].shift()
            flag = true
        } 

        i++
    } 

    if (flag){
        //console.log(cpuConfig.data.labels)
        let x = cpuConfig.data.labels.shift()
        x+=9
        cpuConfig.data.labels.push(x)
    }
}



function initializeCpuChart(utilData)
{
    let colorList = Object.values(window.chartColors)
    let transparentColorList = Object.values(window.transparentColors)
    
    let i=0
    for (const [key, value] of Object.entries(utilData)) {
        var newDataset = {
            label: key, 
            borderColor: colorList[i], 
            backgroundColor: transparentColorList[i], 
            data: [],
            fill: true
        }; 
        
        newDataset.data.push(value);
        cpuConfig.data.datasets.push(newDataset);
 
        cpuConfig.data.labels = [1,2,3,4,5,6,7,8,9,10]; 
        i++  
    }

     
}