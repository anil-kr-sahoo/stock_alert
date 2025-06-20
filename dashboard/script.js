fetch("../stock_data.json")
  .then(res => res.json())
  .then(stock_data => {
    const latest = stock_data[stock_data.length - 1];

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

    document.getElementById("timestamp").textContent = "🕒 Last Time Fetched: " + formatReadableDateTime(latest.Time);
    document.getElementById("message").textContent = "📦 Total Quantity Bought: " + totalQty;

    const statusElem = document.getElementById("status");
    const plText = "💰 Total Profit/Loss: ₹" + totalReturns.toFixed(2);
    statusElem.textContent = plText;

    if (totalReturns >= 0) {
      statusElem.classList.add("positive");
    } else {
      statusElem.classList.add("negative");
    }
  })
  .catch(() => {
    document.getElementById("timestamp").textContent = "⛔ Error loading data.";
    document.getElementById("message").textContent = "";
    document.getElementById("status").textContent = "";
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
