fetch("../stock_data.json")
  .then(res => res.json())
  .then(stock_data => {
    const data = stock_data[stock_data.length -1];
    console.log(data,"////")
    document.getElementById("timestamp").textContent = "Last Updated: " + data.Time;
    document.getElementById("message").textContent = data.Name;
    document.getElementById("status").textContent = "URL: " + data.Url;
  })
  .catch(() => {
    document.getElementById("message").textContent = "Error loading status.";
  });
