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
          valueElement.textContent = 'No data available';
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
    })
    .catch(error => {
      console.error('Error:', error);
    });
});
