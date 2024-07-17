const chartProperties = {
  timeScale: {
    timeVisible: true,
    secondsVisible: false,
    fixLeftEdge: true,
    borderVisible: false,
  }
};
const domElement = document.getElementById('tvchart');
const chart = LightweightCharts.createChart(domElement, chartProperties);
const candleSeries = chart.addCandlestickSeries();
const hoverInfo = document.getElementById('hover-info');
const spinner = document.getElementById('spinner');

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

// Show the spinner
function showSpinner() {
  spinner.style.display = 'block';
}

// Hide the spinner
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
    // console.log('Fetched and parsed data:', cdata);
    candleSeries.setData(cdata);
    hideSpinner();
  } catch (error) {
    log(error);
    hideSpinner();
  }
}

// Handle crosshair move event to display hover info
chart.subscribeCrosshairMove(param => {
  if (!param || !param.time) {
    hideHoverInfo();
    return;
  }
  const { seriesData } = param;
  const data = seriesData.get(candleSeries);
  if (data) {
    const hoverInfoContent = `
      <div>Time: ${(new Date(param.time * 1000 - ((5 * 60 * 60 * 1000) + (30 * 60 * 1000)))).toLocaleString([], { dateStyle: 'short', timeStyle: 'short' })}</div>
      <div>Open: ${data.open}</div>
      <div>High: ${data.high}</div>
      <div>Low: ${data.low}</div>
      <div>Close: ${data.close}</div>
    `;
    showHoverInfo(param.point.x, param.point.y, hoverInfoContent);
  } else {
    hideHoverInfo();
  }
});

// Function to show hover info box
function showHoverInfo(x, y, content) {
  hoverInfo.style.display = 'block';
  hoverInfo.style.top = `${y + 20}px`;
  hoverInfo.style.left = `${x + 20}px`;
  hoverInfo.innerHTML = content;
}

// Function to hide hover info box
function hideHoverInfo() {
  hoverInfo.style.display = 'none';
}

function selectStock(row) {
  // Get all rows with the class 'stock-row'
  var rows = document.getElementsByClassName('stock-row');
  
  // Remove the 'selected' class from all rows
  for (var i = 0; i < rows.length; i++) {
      rows[i].classList.remove('selected');
  }
  
  // Add the 'selected' class to the clicked row
  row.classList.add('selected');

  // Get the stock name from the first cell of the selected row
  var stockName = row.getElementsByTagName('td')[0].innerText;
  
  // Update the text content of the span with id 'selected-stock'
  document.getElementById('selected-stock').textContent = stockName;

  // Get the interval from the select element
  const interval = document.getElementById('interval-select').value;
  
  // Get the stock symbol from the data attribute of the selected row
  const symbol = row.getAttribute('data-symbol');
  
  // Fetch data for the selected stock and interval
  fetchData(symbol, interval);
}

// Update the change event listener for the interval select
document.getElementById('interval-select').addEventListener('change', (event) => {
  const interval = event.target.value;

  // Find the selected stock row
  const selectedRow = document.querySelector('.stock-row.selected');
  
  if (selectedRow) {
    const symbol = selectedRow.getAttribute('data-symbol');
    fetchData(symbol, interval);
  }
});

document.addEventListener('DOMContentLoaded', () => {
  const searchButton = document.getElementById('search-button');
  const searchPopup = document.getElementById('search-popup');
  const closeButton = document.querySelector('.close-button');

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

    });
  });

  // Close dropdown when clicking outside
  window.addEventListener('click', (event) => {
    if (!dropdownHeader.contains(event.target) && !dropdownContent.contains(event.target)) {
      dropdownContent.style.display = 'none';
    }
  });
});

document.addEventListener("DOMContentLoaded", function() {
  // Fullscreen button functionality
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



// Initialize fetch data with the default selected row and interval
window.onload = () => {
  const selectedRow = document.querySelector('.stock-row.selected');
  if (selectedRow) {
    const symbol = selectedRow.getAttribute('data-symbol');
    const interval = document.getElementById('interval-select').value;
    fetchData(symbol, interval);
  }
};