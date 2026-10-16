
const form = document.getElementById("trafficForm");
const message = document.getElementById("message");
const button = document.getElementById("predictBtn");

const history = {
    labels: [],
    levels: [],
    scores: []
};

let chart;

if (typeof Chart !== "undefined") {
    chart = new Chart(document.getElementById("trafficChart"), {
        type: "bar",
        data: {
            labels: history.labels,
            datasets: [{
                label: "Traffic level (Low=1, Medium=2, High=3)",
                data: history.scores,
                backgroundColor: "#7895ff",
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    min: 0,
                    max: 3,
                    ticks: {
                        stepSize: 1,
                        color: "#a7b3ca",
                        callback: value => ({
                            1: "Low",
                            2: "Medium",
                            3: "High"
                        })[value] || ""
                    },
                    grid: { color: "#293852" }
                },
                x: {
                    ticks: { color: "#a7b3ca" },
                    grid: { display: false }
                }
            },
            plugins: {
                legend: {
                    labels: { color: "#eaf0ff" }
                }
            }
        }
    });
}

form.addEventListener("submit", async event => {
    event.preventDefault();
    message.textContent = "";
    button.disabled = true;
    button.textContent = "Predicting...";

    const input = {
        hour: Number(document.getElementById("hour").value),
        vehicles: Number(document.getElementById("vehicles").value),
        average_speed: Number(document.getElementById("speed").value)
    };

    try {
        const response = await fetch("/api/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(input)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Prediction failed.");
        }

        document.getElementById("vehicleStat").textContent = result.vehicles;
        document.getElementById("speedStat").textContent =
            `${result.average_speed} km/h`;
        document.getElementById("levelStat").textContent =
            result.traffic_level;

        const badge = document.getElementById("resultBadge");
        badge.textContent = `${result.traffic_level} Traffic`;
        badge.className = `result-badge ${result.traffic_level.toLowerCase()}`;

        document.getElementById("resultText").textContent =
            `For ${result.vehicles} vehicles at hour ${result.hour}, ` +
            `the model predicts ${result.traffic_level.toLowerCase()} traffic.`;

        document.getElementById("signalTime").textContent =
            result.recommended_green_seconds;

        message.textContent = result.note;

        history.labels.push(new Date().toLocaleTimeString());
        history.levels.push(result.traffic_level);
        history.scores.push(
            { Low: 1, Medium: 2, High: 3 }[result.traffic_level]
        );

        if (history.labels.length > 10) {
            history.labels.shift();
            history.levels.shift();
            history.scores.shift();
        }

        if (chart) {
            chart.update();
        }
    } catch (error) {
        message.textContent = error.message;
    } finally {
        button.disabled = false;
        button.textContent = "Predict traffic";
    }
});
