document.addEventListener('DOMContentLoaded', function () {
  let currentChart = null; // Variable to keep track of the current chart

  function fetchVerbruik() {
    axios.get('/huidig_verbruik')
      .then(response => {
        const verbruikElement = document.getElementById('huidig_verbruik');

        if (response.data.error) {
          verbruikElement.textContent = response.data.error;
        } else {
          const verbruik = response.data.value;
          verbruikElement.textContent = `${verbruik} KW`;
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }

  function fetchHuidigeWoning() {
    axios.get('/huidige_woning')
      .then(response => {
        const woningElement = document.getElementById('huidige_woning');

        if (response.data.error) {
          woningElement.textContent = response.data.error;
        } else {
          const woningValue = response.data.value;
          woningElement.textContent = woningValue;
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }

  function fetchTotalValue() {
    axios.get('/verbruik_per_dag')
      .then(response => {
        const valueElement = document.getElementById('verbruik_per_dag');
  
        if (response.data.error) {
          valueElement.textContent = response.data.error;
        } else if (response.data.value !== undefined) {
          const total = response.data.value;
          valueElement.textContent = `${total} KW`;
        } else {
          valueElement.textContent = 'geen verbruik beschikbaar';
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }
  

  if (document.getElementById('huidige_woning')) {
    fetchHuidigeWoning();
  }

  if (document.getElementById('verbruik_per_dag')) {
    fetchTotalValue();
  }

  if (document.getElementById('huidig_verbruik')) {
    fetchVerbruik();
  }





  fetch('/data')
    .then(response => response.json())
    .then(data => {
      // maakt of update de grafiek
      function createOrUpdateChart(labels, values) {
        const ctx = document.getElementById('Grafieken').getContext('2d');

        // controleert of de grafiek al bestaat
        if (currentChart) {
          // Update de grafiek
          currentChart.data.labels = labels;
          currentChart.data.datasets[0].data = values;
          currentChart.update();
        } else {
          // maak een nieuwe grafiek
          currentChart = new Chart(ctx, {
            type: 'line',
            data: {
              labels: labels,
              datasets: [
                {
                  label: 'verbruiks',
                  data: values,
                  fill: true,
                  borderColor: 'blue',
                  borderWidth: 1,
                  pointBorderWidth: 0,
                },
              ],
            },
            // OPTIES AANPASSEN OM DE GRAFIEK AAN TE PASSEN
            options: {
              scales: {
                x: {
                  grid: {
                    display: false, // Hide the x-axis grid lines
                  },
                },
                y: {
                  beginAtZero: true, // Start the y-axis from zero
                },
              },
              plugins: {
                legend: {
                  display: false, // Hide the legend
                },
              },
            },
          });
        }
      }

      // luisert of er op de knop word gedrukt op de html
      const btnHour = document.getElementById('btnHour');
      const btnDay = document.getElementById('btnDay');
      const btnWeek = document.getElementById('btnWeek');
      const btnMonth = document.getElementById('btnMonth');

      function filterDataByHour(data) {
        const currentDate = new Date().toLocaleDateString();
        const currentHour = new Date().getHours();

        return data.filter(item => {
          const itemDate = new Date(item.datetime).toLocaleDateString();
          const itemHour = new Date(item.datetime).getHours();
          return itemDate === currentDate && itemHour === currentHour;
        });
      }

      function filterDataByDay(data) {
        const currentDate = new Date().toLocaleDateString();

        return data.filter(item => {
          const itemDate = new Date(item.datetime).toLocaleDateString();
          return itemDate === currentDate;
        });
      }

      function filterDataByWeek(data) {
        const currentWeek = moment().week();

        return data.filter(item => {
          const itemWeek = moment(item.datetime).week();
          return itemWeek === currentWeek;
        });
      }

      function filterDataByMonth(data) {
        const currentMonth = new Date().getMonth();

        return data.filter(item => {
          const itemMonth = new Date(item.datetime).getMonth();
          return itemMonth === currentMonth;
        });
      }

      function updateChartWithFilteredData(filteredData) {
        const labels = filteredData.map(item =>
          new Date(item.datetime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        );
        const values = filteredData.map(item => item.verbruik);

        createOrUpdateChart(labels, values);
      }
      if (document.getElementById('Grafieken')) {
      btnHour.addEventListener('click', function () {
        const filteredData = filterDataByHour(data);
        updateChartWithFilteredData(filteredData);

        // zorg dat deze knop een geselecteerd vinkje krijgt en de abdere knoppen niet
        btnHour.classList.add('selected');
        btnDay.classList.remove('selected');
        btnWeek.classList.remove('selected');
        btnMonth.classList.remove('selected');
      });

      btnDay.addEventListener('click', function () {
        const filteredData = filterDataByDay(data);
        updateChartWithFilteredData(filteredData);

        // zorg dat deze knop een geselecteerd vinkje krijgt en de abdere knoppen niet
        btnHour.classList.remove('selected');
        btnDay.classList.add('selected');
        btnWeek.classList.remove('selected');
        btnMonth.classList.remove('selected');
      });

      btnWeek.addEventListener('click', function () {
        const filteredData = filterDataByWeek(data);
        updateChartWithFilteredData(filteredData);

        // zorg dat deze knop een geselecteerd vinkje krijgt en de abdere knoppen niet
        btnHour.classList.remove('selected');
        btnDay.classList.remove('selected');
        btnWeek.classList.add('selected');
        btnMonth.classList.remove('selected');
      });

      btnMonth.addEventListener('click', function () {
        const filteredData = filterDataByMonth(data);
        updateChartWithFilteredData(filteredData);

        // zorg dat deze knop een geselecteerd vinkje krijgt en de abdere knoppen niet
        btnHour.classList.remove('selected');
        btnDay.classList.remove('selected');
        btnWeek.classList.remove('selected');
        btnMonth.classList.add('selected');
      });

      btnHour.click();
    }})
    .catch(error => {
      console.error('Error:', error);
    });




    var openPopupButton = document.getElementById('openPopup');
    var popup = document.getElementById('popup');
    var searchForm = document.getElementById('searchForm');
    var searchResults = document.getElementById('searchResults');
  
    if (openPopupButton && popup && searchForm && searchResults) {
      openPopupButton.addEventListener('click', function() {
        popup.style.display = 'block';
      });
  
      searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        var searchQuery = document.getElementsByName('search_query')[0].value;
  
        // Perform AJAX request to send search query to the server
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/search', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.onreadystatechange = function() {
          if (xhr.readyState === 4 && xhr.status === 200) {
            searchResults.innerHTML = xhr.responseText;
          }
        };
        xhr.send('search_query=' + encodeURIComponent(searchQuery));
      });
    } 
    console.log("AJAX request to /vrienden_verbruik_per_dag");
  
    $.ajax({
      url: "/vrienden_verbruik_per_dag",
      method: "GET",
      
      success: function(response) {
        // Update the HTML content with the received data
        var tableHtml = "<table>";
        tableHtml += "<tr><th>naam</th><th>dagverbruik</th></tr>";
        $.each(response, function(gebruikersnaam, totalVerbruik) {
          tableHtml += "<tr><td>" + gebruikersnaam + "</td><td>" + totalVerbruik + "</td></tr>";
        });
        tableHtml += "</table>";
        $("#verbruikTable").html(tableHtml);
      },
      error: function(xhr, status, error) {
        console.log("Error:", error);
      }
    });

    $.ajax({
      url: "/vrienden_verbruik_per_dag",
      method: "GET",
    
      success: function(response) {
        // Update the HTML content with the received data
        var tableHtml = "<table>";
        tableHtml += "<tr><th>naam</th><th>dagverbruik</th><th></th></tr>"; // Add an empty header for the delete button
        $.each(response, function(vriendID, gebruikersnaam, totalVerbruik) {
          tableHtml += "<tr><td>" + gebruikersnaam + "</td><td>" + totalVerbruik + "</td><td><button class='delete-btn' data-vriend-id='" + vriendID + "'>Delete</button></td></tr>";
        });
        tableHtml += "</table>";
        $("#verbruikTableDelete").html(tableHtml);
    
        // Attach event handlers to the delete buttons
        $(".delete-btn").click(function() {
          var vriendID = $(this).data("vriend-id");
          // Perform the delete operation using the vriendID variable
          $.ajax({
            url: "/remove_vriend",
            method: "POST",
            data: { vriend_id: vriendID },
            success: function(response) {
              // Handle the success response, if needed
              console.log("Friend removed successfully.");
              // You can update the table or perform any other actions as required
              // ...
            },
            error: function(xhr, status, error) {
              // Handle the error response, if needed
              console.log("Error:", error);
            }
          });
        });
      },
      error: function(xhr, status, error) {
        console.log("Error:", error);
      }
    });
    
});
