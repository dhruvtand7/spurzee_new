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
    hideSpinner();
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

function selectStock(row) {
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
  if (selectedOptions.includes('sup-res')) {
    fetchAndDrawSupportResistance(symbol, interval);
  }
}

let priceLines = [];

async function fetchAndDrawSupportResistance(symbol, interval) {
  showSpinner();
  try {
    const response = await fetch(`/support-resistance?symbol=${symbol}&interval=${interval}`);
    const levels = await response.json();
    priceLines.forEach(line => {
      candleSeries.removePriceLine(line);
    });
    priceLines = [];
  
    // Add new price lines
    levels.forEach(level => {
      const line = candleSeries.createPriceLine({
        price: level,
        color: 'black',
        lineWidth: 2,
        lineStyle: LightweightCharts.LineStyle.Solid,
        axisLabelVisible: true,
        title: 'S&R'
      });
      priceLines.push(line);
    });
    hideSpinner();
  } catch (error) {
    console.error(error);
    hideSpinner();
  }
}
// Update the change event listener for the interval select
document.getElementById('interval-select').addEventListener('change', (event) => {
  const interval = event.target.value;

  // Find the selected stock row
  const selectedRow = document.querySelector('.stock-row.selected');
  
  if (selectedRow) {
    const symbol = selectedRow.getAttribute('data-symbol');
    fetchData(symbol, interval);
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
    fetchChange(symbol, interval, row);
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
async function fetchChange(symbol, interval, row) {
  showSpinner();
  try {
    const response = await fetch(`/get-change?symbol=${symbol}&interval=${interval}`);
    const data = await response.json();
    
    if (data.error) {
      console.error(data.error);
    } else {
      // Update table cells with new data
      updateTable(symbol, data.last, data.chg.toFixed(2), data.chgPct, row);
    }

    hideSpinner();
  } catch (error) {
    console.error(error);
    hideSpinner();
  }
}

// Pattern Select Dropdown 
document.addEventListener('DOMContentLoaded', () => {
  const dropdownHeader = document.getElementById('dropdown-header');
  const dropdownContent = document.getElementById('dropdown-content');
  const options = document.querySelectorAll('.option');

  let selectedOptions = [];

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