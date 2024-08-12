// Sales by Customers (bar graph)
const ctxPurchases = document.getElementById("purchases").getContext("2d");
const names = document.getElementById('data').innerText.split(",");
// integer list of prices recieved as string by JS by default, so we need to convert it into object(array) using Json.parse
const prices = JSON.parse(document.getElementById('price').innerText)

const purchasesChart = new Chart(ctxPurchases, {
    type: "bar",
    data: {
        labels: names,
        datasets: [{
            label: "Sales by Customers",
            data: prices,
            backgroundColor: "#6c757d", // muted gray
            borderColor: "#343a40",
            borderWidth: 1,
        }],
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: "#e9ecef",
                },
                ticks: {
                    color: "#495057",
                    
                }
            },
            x: {
                grid: {
                    color: "#e9ecef",
                },
                ticks: {
                    color: "#495057",
                    callback: function(value) {
                        return value.toLocaleString();
                    }
                }
            }
        },
        plugins: {
            legend: {
                labels: {
                    color: "#495057",
                }
            },
            tooltip: {
                callbacks: {
                    label: function(tooltipItem) {
                        // Format numbers with commas in tooltips
                        return tooltipItem.raw.toLocaleString();
                    }
                }
            }

        }
    }
});


// Monthly Sales (line graph)
const lineChartCanvas = document.getElementById('monthly-sales');
const postData = { 'key': 'montlySalesGraph' };

$.ajax({
    url: '/',
    type: 'POST',
    data: JSON.stringify(postData),
    contentType: 'application/json',
    success: function (data) {
        const monthly_sale = data['monthly_sale'].reverse();
        const months = data['months'].map(month => {
            return ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][month - 1];
        }).reverse();

        const lineChart = new Chart(lineChartCanvas, {
            type: 'line',
            data: {
                labels: months,
                datasets: [{
                    label: 'Monthly Sales',
                    data: monthly_sale,
                    borderColor: '#007bff', // Bootstrap primary color
                    borderWidth: 2,
                    fill: false,
                }],
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: "#e9ecef",
                        },
                        ticks: {
                            color: "#495057",
                        }
                    },
                    x: {
                        grid: {
                            color: "#e9ecef",
                        },
                        ticks: {
                            color: "#495057",
                        }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: "#495057",
                        }
                    }
                }
            }
        });
    },
    error: function (error) {
        console.log(error);
    }
});

// Weather update
navigator.geolocation.getCurrentPosition(function(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;
    const Key = '7e59d57620d34e8b511755055014fe3c';
    const apiUrl = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${Key}&units=metric`;

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            const temp = data.main.temp;
            const description = data.weather[0].description;
            document.querySelector('.temperature').textContent = `${temp}°C`;
            document.querySelector('.description').textContent = description;
            document.querySelector('.weather-icon').classList.remove('fa-cog');
            document.querySelector('.weather-icon').classList.add('fa-cloud-sun');
        })
        .catch(error => console.error('Error fetching weather data:', error));
});

// Calculator functionality
function appendToDisplay(value) {
    const display = document.getElementById('display');
    display.value += value;
}

function clearDisplay() {
    const display = document.getElementById('display');
    display.value = '';
}

function calculateResult() {
    const display = document.getElementById('display');
    try {
        display.value = eval(display.value);
    } catch (e) {
        display.value = 'Error';
    }
}

// Clock
function updateClock() {
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const seconds = now.getSeconds().toString().padStart(2, '0');
    document.querySelector('.clock').textContent = `${hours}:${minutes}:${seconds}`;
}

setInterval(updateClock, 1000);
updateClock();


// Top Icon Bar: Top Icon container div, Icons setup and working
var monthlySales = document.getElementById('div1');
var SalesByCustomer = document.getElementById('div2');
var Calculator = document.getElementById('div3');
var linegraph = document.getElementById('graphElem');
var bargraph = document.getElementById('bargraphElem');
var calcElem = document.getElementById('calcElem');

//line graph on click show/hide + styling
linegraph.addEventListener('click', function(){
  if (monthlySales.style.display === "none" ){
    monthlySales.style.display = "";
  }else{monthlySales.style.display = "none"}
});  

//bar graph on click show/hide + styling
bargraph.addEventListener('click', function(){
  if (SalesByCustomer.style.display === "none" ){
    SalesByCustomer.style.display = "";
  }else{SalesByCustomer.style.display = "none"}
});  

//calculator on click show/hide + styling
calcElem.addEventListener('click', function(){
if (Calculator.style.display === "none" ){
  Calculator.style.display = "";
}else{Calculator.style.display = "none"}
});  
