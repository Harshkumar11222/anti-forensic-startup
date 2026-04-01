let lastData = null;

function downloadReport() {
    if (!lastData) {
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

let token = null;

function login() {
    let user = document.getElementById("admin").value;
    let pass = document.getElementById("1234").value;

    fetch(`https://anti-forensic-startup.onrender.com/login?username=${user}&password=${pass}`)
        .then(res => res.json())
        .then(data => {
            console.log("Login response:", data);

            if (data.token) {
                token = data.token;

                // token store karna (important)
                localStorage.setItem("token", token);

                window.location.href = "dashboard.html";
            } else {
                document.getElementById("msg").innerText = "❌ Login Failed!";
            }
        })
        .catch(err => {
            console.log("ERROR:", err);
            document.getElementById("msg").innerText = "⚠ Server Error!";
        });
}

async function checkSystem(){
    let token = localStorage.getItem("token");

    let res = await fetch(`https://anti-forensic-startup.onrender.com/scan?token=${token}`);
    let data = await res.json();

    console.log("Scan response:", data);

    document.getElementById("result").innerText =
        "⚠ Suspicious Files: " + data.total_suspicious +
        "\n🕒 Recent Activity: " + data.recent_activity +
        "\n🔥 Risk Score: " + data.risk_score +
        "\n📊 Status: " + data.status +
        "\n🗑 Deleted Traces: " + data.deleted_traces +
        "\n📄 Log Issues: " + data.log_issues +
        "\n🧠 Anomaly: " + data.anomaly;
}






