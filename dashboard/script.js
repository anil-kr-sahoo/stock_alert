fetch("../stock_data.json")
  .then(res => res.json())
  .then(stock_data => {
    const data = stock_data[stock_data.length - 1];

    // Calculate total profit/loss and total quantity
    let totalReturns = 0;
    let totalQty = 0;

    stock_data.forEach(stock => {
      const qty = parseInt(stock["Qty"]);
      const avg = parseFloat(stock["Stock Average Value"]);
      const current = parseFloat(stock["Current Price"]);

      if (!isNaN(qty) && qty > 0) {
        const profit = (current - avg) * qty;
        totalReturns += profit;
        totalQty += qty;
      }
    });

    document.getElementById("timestamp").textContent = "Last Time Fetched: " + formatReadableDateTime(data.Time);
    document.getElementById("message").textContent = "🧾 Total Quantity Bought: " + totalQty;
    document.getElementById("status").textContent = "💰 Total Profit/Loss: ₹" + totalReturns.toFixed(2);
  })
  .catch(() => {
    document.getElementById("message").textContent = "Error loading stock data.";
    document.getElementById("status").textContent = "";
    document.getElementById("timestamp").textContent = "";
  });

function formatReadableDateTime(dateString) {
  const date = new Date(dateString.replace(" ", "T"));
  const options = {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
  };
  return date.toLocaleString("en-GB", options).replace(",", "");
}
