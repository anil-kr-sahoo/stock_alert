fetch("../stock_data.json")
  .then(res => res.json())
  .then(stock_data => {
    const data = stock_data[stock_data.length -1];
     // Calculate total P/L and total quantity
    let totalReturns = 0;
    let totalQty = 0;

    stock_data.forEach(stock => {
      totalReturns += parseFloat(stock["Total Returns"]);
      totalQty += parseInt(stock["Qty"]);
    });
    document.getElementById("timestamp").textContent = "Last Updated: " + data.Time;
    document.getElementById("message").textContent = "Total Qty: " + totalQty;
    document.getElementById("status").textContent = "Total PL: " + totalReturns.toFixed(2) +"/-";
  })
  .catch(() => {
    document.getElementById("message").textContent = "Error loading status.";
  });
