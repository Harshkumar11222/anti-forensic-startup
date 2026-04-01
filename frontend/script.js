let lastData = null;

async function checkSystem(){
    let res = await fetch("http://127.0.0.1:8000/scan");
    let data = await res.json();

    lastData = data;

    document.getElementById("result").innerText =
        "⚠ Suspicious Files: " + data.total_suspicious +
        "\n🕒 Recent Activity: " + data.recent_activity +
        "\n🔥 Risk Score: " + data.risk_score +
        "\n📊 Status: " + data.status;
}

function downloadReport(){
    if(!lastData){
        alert("Run scan first!");
        return;
    }

    let content =
        "Anti-Forensic Report\n\n" +
        "Suspicious Files: " + lastData.total_suspicious + "\n" +
        "Recent Activity: " + lastData.recent_activity + "\n" +
        "Risk Score: " + lastData.risk_score + "\n" +
        "Status: " + lastData.status;

    let blob = new Blob([content], { type: "text/plain" });
    let a = document.createElement("a");

    a.href = URL.createObjectURL(blob);
    a.download = "report.txt";
    a.click();
}

function login(){
    let user = document.getElementById("username").value;
    let pass = document.getElementById("password").value;

    fetch(`http://127.0.0.1:8000/login?username=${user}&password=${pass}`)
    .then(res => res.json())
    .then(data => {
        if(data.status === "success"){
            window.location.href = "dashboard.html";
        } else {
            document.getElementById("msg").innerText = "❌ Login Failed!";
        }
    });
}

async function checkSystem(){
    let res = await fetch("http://127.0.0.1:8000/scan");
    let data = await res.json();

    document.getElementById("result").innerText =
        "⚠ Suspicious Files: " + data.total_suspicious +
        "\n🕒 Recent Activity: " + data.recent_activity +
        "\n🔥 Risk Score: " + data.risk_score +
        "\n📊 Status: " + data.status +
        "\n🗑 Deleted Traces: " + data.deleted_traces +
        "\n📄 Log Issues: " + data.log_issues;
        "\n🧠 Anomaly: " + data.anomaly
}