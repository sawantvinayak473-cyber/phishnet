function scan() {
    const url = document.getElementById("urlInput").value;
    const loader = document.getElementById("loader");
    const result = document.getElementById("result");

    loader.classList.remove("hidden");
    result.classList.add("hidden");

    fetch("/scan", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({url: url})
    })
    .then(res => res.json())
    .then(data => {
        loader.classList.add("hidden");
        result.classList.remove("hidden");

        const conf = data.confidence || 0;
        const percent = Math.round(conf * 100);

        document.getElementById("percent").innerText = percent + "%";
        document.getElementById("confidence").innerText = "Confidence: " + conf;

        const needle = document.getElementById("needle");
        const angle = percent * 1.8;
        needle.style.transform = "rotate(" + angle + "deg)";

        const label = document.getElementById("label");

        if (data.prediction === 1) {
            label.innerText = "Phishing ⚠";
            label.style.color = "red";
        } else {
            label.innerText = "Legitimate ✓";
            label.style.color = "lime";
        }

        if (data.analysis) {
            const domainEl = document.getElementById("domain");
            const httpsEl = document.getElementById("https");
            const indicatorsEl = document.getElementById("indicators");

            if (domainEl) {
                domainEl.innerText = "Domain: " + (data.analysis.domain || "N/A");
            }

            if (httpsEl) {
                httpsEl.innerText = "HTTPS: " + (data.analysis.https ? "Yes" : "No");
            }

            if (indicatorsEl) {
                indicatorsEl.innerHTML = "";
                if (data.analysis.indicators && data.analysis.indicators.length > 0) {
                    data.analysis.indicators.forEach(i => {
                        const li = document.createElement("li");
                        li.innerText = i;
                        indicatorsEl.appendChild(li);
                    });
                } else {
                    const li = document.createElement("li");
                    li.innerText = "No phishing indicators detected";
                    indicatorsEl.appendChild(li);
                }
            }
        }

        loadHistory();
    })
    .catch(() => {
        loader.classList.add("hidden");
        alert("Server error");
    });
}

function loadHistory() {
    const table = document.getElementById("historyTable");
    if (!table) return;

    fetch("/history")
    .then(res => res.json())
    .then(rows => {
        table.innerHTML = "<tr><th>Input</th><th>Score</th><th>Time</th></tr>";
        rows.forEach(r => {
            const score = Math.round(r[2] * 100);
            table.innerHTML += `<tr><td>${r[0]}</td><td>${score}%</td><td>${r[3]}</td></tr>`;
        });
    });
}