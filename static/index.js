const chartProperties = {
  timeScale: {
    timeVisible: true,
    secondsVisible: false,
    fixLeftEdge: true,
    borderVisible: false,
  }
};
const domElement = document.getElementById('tvchart');
const chart = LightweightCharts.createChart(domElement, {
  width: domElement.clientWidth,
  height: domElement.clientHeight,
  ...chartProperties
});
const candleSeries = chart.addCandlestickSeries();
const hoverInfo = document.getElementById('hover-info');
const spinner = document.getElementById('spinner');

let currentOHLC = {};
// Function to resize the chart
function resizeChart() {
  chart.resize(domElement.clientWidth, domElement.clientHeight);
}

// Resize the chart initially
resizeChart();

// Use ResizeObserver to detect size changes
const resizeObserver = new ResizeObserver(() => {
  resizeChart();
});

// Start observing the container
resizeObserver.observe(domElement);

// Optionally: Handle window resize event as a fallback
window.addEventListener('resize', resizeChart);

// Helper function to parse date-time string to Unix timestamp in seconds
function parseDateTimeToUnix(dateTime) {
  const [datePart, timePart] = dateTime.split(' ');
  const [year, month, day] = datePart.split('-').map(Number);
  const [hour, minute, second] = timePart.split(':').map(Number);
  const date = new Date(year, month - 1, day, hour, minute, second);
  const offset = (5 * 60 * 60 * 1000) + (30 * 60 * 1000);
  const newDate = new Date(date.getTime() + offset);
  return Math.floor(newDate.getTime() / 1000);
}

function showSpinner() {
  spinner.style.display = 'block';
}

function hideSpinner() {
  spinner.style.display = 'none';
}

// Function to fetch and process data from backend
async function fetchData(symbol, interval) {
  showSpinner();
  try {
    const response = await fetch(`/stock-data?symbol=${symbol}&interval=${interval}`);
    const data = await response.json();
    const cdata = data.map(d => ({
      time: parseDateTimeToUnix(d.Date),
      open: parseFloat(d.Open),
      high: parseFloat(d.High),
      low: parseFloat(d.Low),
      close: parseFloat(d.Close)
    }));
    candleSeries.setData(cdata);
    const lastCandle = cdata[cdata.length - 1];
    hideSpinner();
    return lastCandle;
  } catch (error) {
    log(error);
    hideSpinner();
  }
}

// Function to update table cells
function updateTable(symbol, last, chg, chgPct) {
  const table = document.getElementById('stock-table');
  const rows = table.querySelectorAll('.stock-row');
  
  rows.forEach(row => {
    if (row.getAttribute('data-symbol') === symbol) {
      row.querySelector('td:nth-child(2)').textContent = last;
      row.querySelector('td:nth-child(3)').textContent = chg >= 0 ? `+${chg}` : chg;
      row.querySelector('td:nth-child(4)').textContent = `${chgPct}%`;
    }
  });
}

async function selectStock(row) {
  var rows = document.getElementsByClassName('stock-row');
  
  for (var i = 0; i < rows.length; i++) {
      rows[i].classList.remove('selected');
  }
  
  row.classList.add('selected');
  var stockName = row.getElementsByTagName('td')[0].innerText;
  document.getElementById('selected-stock').textContent = stockName;
  const interval = document.getElementById('interval-select').value;
  const symbol = row.getAttribute('data-symbol');
  fetchData(symbol, interval);
  const lastCandle = await fetchData(symbol, interval);
  if (lastCandle) {
    skt.unsubscribe([symbol], false, 1);
    skt.subscribe([symbol], false, 1);
    currentOHLC[lastCandle.time] = lastCandle;
    console.log(currentOHLC[lastCandle.time]);
    console.log(lastCandle);
  }
  if (selectedOptions.includes('sup-res')) {
    fetchAndDrawSupportResistance(symbol, interval);
  }
}

let srLineSeries = [];

// Function to fetch and draw support and resistance lines
async function fetchAndDrawSupportResistance(symbol, interval) {
  showSpinner();
  try {
    const response = await fetch(`/support-resistance?symbol=${symbol}&interval=${interval}`);
    const srGroups = await response.json();
    
    // Clear existing SR line series
    srLineSeries.forEach(series => chart.removeSeries(series));
    srLineSeries = [];
    
    srGroups.forEach((group, index) => {
      const color = ['black', 'blue', 'green'][index];
      const { start_date, end_date, sr_lines } = group;
      const startTime = parseDateTimeToUnix(start_date);
      const endTime = parseDateTimeToUnix(end_date);
      
      sr_lines.forEach(level => {
        const horizontalLineData = [
          { time: startTime, value: level },
          { time: endTime, value: level }
        ];
        
        const lineSeries = chart.addLineSeries({
          color: color,
          lineWidth: 1,
        });
        
        lineSeries.setData(horizontalLineData);
        srLineSeries.push(lineSeries);
      });
    });
    hideSpinner();
  } catch (error) {
    console.error(error);
    hideSpinner();
  }
}

// Update the change event listener for the interval select
document.getElementById('interval-select').addEventListener('change', async (event) => {
  const interval = event.target.value;

  // Find the selected stock row
  const selectedRow = document.querySelector('.stock-row.selected');
  
  if (selectedRow) {
    const symbol = selectedRow.getAttribute('data-symbol');
    fetchData(symbol, interval);
    const lastCandle = await fetchData(symbol, interval);
    if (lastCandle) {
      currentOHLC[lastCandle.time] = lastCandle;
      console.log(currentOHLC[lastCandle.time]);
      console.log(lastCandle);
    }
    if (selectedOptions.includes('sup-res')) {
      fetchAndDrawSupportResistance(symbol, interval);
    }

  }
});

// Search Button
document.addEventListener('DOMContentLoaded', () => {
  const searchButton = document.getElementById('search-button');
  const searchPopup = document.getElementById('search-popup');
  const closeButton = document.querySelector('.close-button');

  // Get all stock rows and fetch data for each stock
  const rows = document.querySelectorAll('.stock-row');
  rows.forEach(row => {
    const symbol = row.getAttribute('data-symbol');
    const interval = document.getElementById('interval-select').value;
    //fetchChange(symbol, interval, row);
  });

  // Search button click event
  searchButton.addEventListener('click', () => {
    searchPopup.style.display = 'block';
  });

  // Close button click event
  closeButton.addEventListener('click', () => {
    searchPopup.style.display = 'none';
  });

  // Close the popup when clicking outside of it
  window.addEventListener('click', (event) => {
    if (event.target == searchPopup) {
      searchPopup.style.display = 'none';
    }
  });
});

// Function to fetch and process data from the new /get-change endpoint
// async function fetchChange(symbol, interval, row) {
//   showSpinner();
//   try {
//     const response = await fetch(`/get-change?symbol=${symbol}&interval=${interval}`);
//     const data = await response.json();
    
//     if (data.error) {
//       console.error(data.error);
//     } else {
//       // Update table cells with new data
//       updateTable(symbol, data.last, data.chg.toFixed(2), data.chgPct, row);
//     }

//     hideSpinner();
//   } catch (error) {
//     console.error(error);
//     hideSpinner();
//   }
// }
let selectedOptions = [];


// Pattern Select Dropdown 
document.addEventListener('DOMContentLoaded', () => {
  const dropdownHeader = document.getElementById('dropdown-header');
  const dropdownContent = document.getElementById('dropdown-content');
  const options = document.querySelectorAll('.option');

 
  // Toggle dropdown visibility on header click
  dropdownHeader.addEventListener('click', () => {
    dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
  });

  // Handle option click to toggle selection
  options.forEach(option => {
    option.addEventListener('click', () => {
      const value = option.getAttribute('data-value');
      option.classList.toggle('selected');

      if (option.classList.contains('selected')) {
        selectedOptions.push(value);
      } else {
        selectedOptions = selectedOptions.filter(item => item !== value);
      }

      const selectedRow = document.querySelector('.stock-row.selected');
      if (selectedRow) {
        const symbol = selectedRow.getAttribute('data-symbol');
        const interval = document.getElementById('interval-select').value;
        if (selectedOptions.includes('sup-res')) {
          fetchAndDrawSupportResistance(symbol, interval);
        }
        else{
          srLineSeries.forEach(series => chart.removeSeries(series));
          srLineSeries = [];
        }
      }
      
    });
  });

  // Close dropdown when clicking outside
  window.addEventListener('click', (event) => {
    if (!dropdownHeader.contains(event.target) && !dropdownContent.contains(event.target)) {
      dropdownContent.style.display = 'none';
    }
  });
}); 

// Fullscreen button functionality
document.addEventListener("DOMContentLoaded", function() {
  const fullscreenButton = document.getElementById("fullscreen-button");

  fullscreenButton.addEventListener("click", function() {
    if (!document.fullscreenElement &&    // alternative standard method
        !document.mozFullScreenElement && !document.webkitFullscreenElement && !document.msFullscreenElement ) {
      const element = document.documentElement; // Fullscreen the entire document

      if (element.requestFullscreen) {
        element.requestFullscreen();
      } else if (element.mozRequestFullScreen) { /* Firefox */
        element.mozRequestFullScreen();
      } else if (element.webkitRequestFullscreen) { /* Chrome, Safari and Opera */
        element.webkitRequestFullscreen();
      } else if (element.msRequestFullscreen) { /* IE/Edge */
        element.msRequestFullscreen();
      }
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      } else if (document.mozCancelFullScreen) { /* Firefox */
        document.mozCancelFullScreen();
      } else if (document.webkitExitFullscreen) { /* Chrome, Safari and Opera */
        document.webkitExitFullscreen();
      } else if (document.msExitFullscreen) { /* IE/Edge */
        document.msExitFullscreen();
      }
    }
  });
});

// Add hover info mouse move event listener
chart.subscribeCrosshairMove(function(param) {
  if (!param || !param.time || !param.seriesData.size) {
    hoverInfo.innerHTML = '';
    return;
  }

  const data = param.seriesData.get(candleSeries);
  if (!data) {
    hoverInfo.innerHTML = '';
    return;
  }

  let { open, close, high, low } = data;

  open = open.toFixed(2);
  close = close.toFixed(2);
  high = high.toFixed(2);
  low = low.toFixed(2);

  hoverInfo.innerHTML = `
    Open: ${open}
    Close: ${close}
    High: ${high}
    Low: ${low}
  `;
});

// Initialize fetch data with the default selected row and interval
window.onload = () => {
  const selectedRow = document.querySelector('.stock-row.selected');
  if (selectedRow) {
    const symbol = selectedRow.getAttribute('data-symbol');
    const interval = document.getElementById('interval-select').value;
    fetchData(symbol, interval);
  }
};

const accessTocken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE3MjE2NjgyOTcsImV4cCI6MTcyMTY5NDYzNywibmJmIjoxNzIxNjY4Mjk3LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCbW5wTEpUQWhhY2tYVFZmTlhxS0I0Wks1aDFrNzZDcWVIY0toQ2RadHBVQ0oyM3hab1ZjTmsxM2NhUVZjRVE0ZDJHVW1aek9KTHdQeWswNEF1SE5xSENfZVc3QmVrdVpGNFlDcktSbjBEaE5fcy1zOD0iLCJkaXNwbGF5X25hbWUiOiJMT0tFU0ggVEFMTFVSSSIsIm9tcyI6IksxIiwiaHNtX2tleSI6IjgzZmZjNDBhNDBhNmMzMmVhODEyZmZlNjg4MDg2ZjA2NGE2NTU4OGU5NTEyNjdhOTA4MDQzMjU3IiwiZnlfaWQiOiJZTDAwMTM3IiwiYXBwVHlwZSI6MTAwLCJwb2FfZmxhZyI6Ik4ifQ.DsNDJ6G-OizlaG2Oul94zUX6s2vXQeLe5xs1muwuWhg"

var skt = fyersDataSocket.getInstance(accessTocken);

function roundTimeToInterval(unixTimestamp, intervalMinutes) {
  const date = new Date((unixTimestamp + 5.5 * 60 * 60) * 1000);
  let minutes = date.getMinutes();
  let hours = date.getHours();

  if (intervalMinutes === 30) {
      if (minutes < 15) {
          minutes = 45;
          hours = hours - 1; // previous hour
      } else if (minutes < 45) {
          minutes = 15;
      } else {
          minutes = 45;
      }
  } else if (intervalMinutes === 60) {
      if (minutes < 15) {
          minutes = 15;
          hours =  hours - 1; // previous hour
      } else {
          minutes = 15;
      }
  } else {
      minutes = Math.floor(minutes / intervalMinutes) * intervalMinutes;
  }

  date.setHours(hours);
  date.setMinutes(minutes, 0, 0);
  return Math.floor(date.getTime() / 1000) ;
}





// Function to update OHLC data
function updateOHLC(ltp, time) {
  const interval = document.getElementById('interval-select').value;
  const roundedTime = roundTimeToInterval(time, interval);

  if (!currentOHLC[roundedTime]) {
    currentOHLC[roundedTime] = {
      time: roundedTime,
      open: ltp,
      high: ltp,
      low: ltp,
      close: ltp,
    };
  } else {
    currentOHLC[roundedTime].high = Math.max(currentOHLC[roundedTime].high, ltp);
    currentOHLC[roundedTime].low = Math.min(currentOHLC[roundedTime].low, ltp);
    currentOHLC[roundedTime].close = ltp;
  }

  candleSeries.update(currentOHLC[roundedTime]);
}

// WebSocket message handler
function onmsg(message) {
  const parsedData = message;
  // console.log(message);
  const selectedRow = document.querySelector('.stock-row.selected');
  const symbol = selectedRow.getAttribute('data-symbol');
  if (parsedData.symbol === symbol) {
    const time = parsedData.exch_feed_time;
    const ltp = parsedData.ltp;
    updateOHLC(ltp, time);
  }
}


skt.on("connect", function() {
    const selectedRow = document.querySelector('.stock-row.selected');
    const symbol = selectedRow.getAttribute('data-symbol');
    skt.subscribe([symbol], false, 1);
    skt.mode(skt.FullMode, 1);
    console.log(skt.isConnected());
    skt.autoreconnect();
});

skt.on("message", function(message) {
    onmsg(message);
});

skt.on("error", function(message) {
    console.log("error is", message);
});

skt.on("close", function() {
    console.log("socket closed");
});

skt.connect();
