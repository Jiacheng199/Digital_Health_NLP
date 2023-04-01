const csvUrl = "https://github.com/COMP90082-2023-SM1/DI-RedBack/blob/sprint2/src/example.csv";

fetch(csvUrl)
  .then(response => response.text())
  .then(data => {
    const lines = data.split("\n");
    const counts = {
      matched: 0,
      unable: 0,
      notsure: 0
    };

    lines.forEach(line => {
      const thisline = line.trim().split(",");;
      if (thisline[1] == "Non-Match") {
        counts.notsure++;
      }
      else{
        counts.matched++;
      }
    });

    const total = counts.matched + counts.unable + counts.notsure;
    const matchedPercentage = (counts.matched / total) * 100;

    document.getElementById("matched-percentage").textContent = `matched:${matchedPercentage.toFixed(2)}%`;

    const chartCanvas = document.getElementById("chart");
    const chartData = {
      labels: ["matched", "unable", "not sure"],
      datasets: [
        {
          label: "matched",
          data: [counts.matched, counts.unable, counts.notsure],
          backgroundColor: ['rgba(75, 192, 192, 0.8)',
      'rgba(54, 162, 235, 0.8)',
      'rgba(153, 102, 255, 0.8)']
        }
      ]
    };
    const chartOptions = {
      responsive: true,
      maintainAspectRatio: true,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    };

    new Chart(chartCanvas, {
      type: "bar",
      data: chartData,
      options: chartOptions
    });
  })
  .catch(error => {
    console.error(error);
  });