<<<<<<< HEAD
async function scan() {
  const text = document.getElementById("inputText").value;
  const resultDiv = document.getElementById("result");
  const loader = document.getElementById("loader");
  const risk = document.getElementById("riskScore");
  const details = document.getElementById("details");
  const gaugeFill = document.getElementById("gaugeFill");
  const riskPercent = document.getElementById("riskPercent");

  if (!text) {
    alert("Please enter text to scan");
    return;
  }

  resultDiv.classList.add("hidden");
  loader.classList.remove("hidden");

  const response = await fetch("/scan", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ text: text })
  });

  const data = await response.json();

  await new Promise(r => setTimeout(r, 1200));

  loader.classList.add("hidden");
  resultDiv.classList.remove("hidden");

  let score = Math.round(data.confidence * 100);

  if (data.prediction === 1) {
    score = Math.max(score, 60);
  }

  riskPercent.textContent = score + "%";

  const rotation = score * 1.8;
  gaugeFill.style.transform = `rotate(${rotation}deg)`;

  if (score > 70) gaugeFill.style.background = "#ff4d4d";
  else if (score > 40) gaugeFill.style.background = "#ffb84d";
  else gaugeFill.style.background = "#00ff9c";

  let level = "Low Risk";
  if (score > 75) level = "Critical";
  else if (score > 55) level = "High";
  else if (score > 35) level = "Medium";

  if (data.prediction === 1) {
    risk.textContent = "⚠️ Phishing Detected";
    risk.className = "risk phishing typing";
  } else {
    risk.textContent = "✅ Legitimate";
    risk.className = "risk safe typing";
  }

  setTimeout(() => {
    risk.classList.remove("typing");
  }, 1200);

  details.textContent =
    "Threat Level: " + level + " | Confidence: " + data.confidence.toFixed(2);
=======
async function scan() {
  const text = document.getElementById("inputText").value;
  const resultDiv = document.getElementById("result");
  const loader = document.getElementById("loader");
  const risk = document.getElementById("riskScore");
  const details = document.getElementById("details");
  const gaugeFill = document.getElementById("gaugeFill");
  const riskPercent = document.getElementById("riskPercent");

  if (!text) {
    alert("Please enter text to scan");
    return;
  }

  resultDiv.classList.add("hidden");
  loader.classList.remove("hidden");

  const response = await fetch("/scan", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ text: text })
  });

  const data = await response.json();

  await new Promise(r => setTimeout(r, 1200));

  loader.classList.add("hidden");
  resultDiv.classList.remove("hidden");

  let score = Math.round(data.confidence * 100);

  if (data.prediction === 1) {
    score = Math.max(score, 60);
  }

  riskPercent.textContent = score + "%";

  const rotation = score * 1.8;
  gaugeFill.style.transform = `rotate(${rotation}deg)`;

  if (score > 70) gaugeFill.style.background = "#ff4d4d";
  else if (score > 40) gaugeFill.style.background = "#ffb84d";
  else gaugeFill.style.background = "#00ff9c";

  let level = "Low Risk";
  if (score > 75) level = "Critical";
  else if (score > 55) level = "High";
  else if (score > 35) level = "Medium";

  if (data.prediction === 1) {
    risk.textContent = "⚠️ Phishing Detected";
    risk.className = "risk phishing typing";
  } else {
    risk.textContent = "✅ Legitimate";
    risk.className = "risk safe typing";
  }

  setTimeout(() => {
    risk.classList.remove("typing");
  }, 1200);

  details.textContent =
    "Threat Level: " + level + " | Confidence: " + data.confidence.toFixed(2);
>>>>>>> 356acd049ea2f22d119ffb982b647351fa584b32
}