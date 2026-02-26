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
    })
    .catch(() => {
        loader.classList.add("hidden");
        alert("Server error");
    });
}