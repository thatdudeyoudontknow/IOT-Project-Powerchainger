document.addEventListener('DOMContentLoaded', function() {
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
  
  function fetchCurrentValues() {
    fetchVerbruik();
    fetchHuidigeWoning();
  }
  

  // Fetch the current values when the page is loaded



  function fetchTotalValue() {
    axios.get('/verbruik_per_dag')
      .then(response => {
        const valueElement = document.getElementById('verbruik_per_dag');
  
        if (response.data.error) {
          valueElement.textContent = response.data.error;
        } else {
          const values = response.data.values;
          const total = values.reduce((acc, entry) => acc + entry.value, 0); // Access the 'value' property of each entry
          valueElement.textContent = `${total} KW`;
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }
  
  function fetchCurrentValues() {
    fetchVerbruik();
    fetchHuidigeWoning();
    fetchTotalValue();
  }

  fetchCurrentValues();

  

  fetch("/data")
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
              datasets: [{
                label: 'Messages',
                data: values,
                fill: true,
                borderColor: 'blue',
                borderWidth: 1,
                pointBorderWidth: 0,

              }]
            },
            // OPTIES AANPASSEN OM DE GRAFIEK AAN TE PASSEN
             options: { 
                scales: {
                  x: {
                    grid: {
                      display: false // Hide the x-axis grid lines
                    }
                  },
                  y: {
                    beginAtZero: true // Start the y-axis from zero
                  }
                },
                plugins: {
                  legend: {
                    display: false // Hide the legend
                  }
              }
            }
          });
        }
      }

      // luisert of er op de knop word gedrukt op de html
      const btnHour = document.getElementById('btnHour');
      const btnDay = document.getElementById('btnDay');
      const btnWeek = document.getElementById('btnWeek');
      const btnMonth = document.getElementById('btnMonth');

      btnHour.addEventListener('click', function() {

        // pak de data en zorg dat alleen het UUR van de huidige dag word gepakt
        const currentDate = new Date().toLocaleDateString();
        const currentHour = new Date().getHours();

        const filteredData = data.filter(item => {
          const itemDate = new Date(item.timestamp).toLocaleDateString();
          const itemHour = new Date(item.timestamp).getHours();
          return itemDate === currentDate && itemHour === currentHour;
        });

        const labels = filteredData.map(item => new Date(item.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));
        const values = filteredData.map(item => item.message);

        createOrUpdateChart(labels, values);

        // zorg dat deze knop een geselecteerd vinkje krijgt en de abdere knoppen niet 
        btnHour.classList.add('selected');
        btnDay.classList.remove('selected');
        btnWeek.classList.remove('selected');
        btnMonth.classList.remove('selected');
      });

      btnDay.addEventListener('click', function() {
        // pak de data en zorg dat alleen de DAG word gepakt
        const currentDate = new Date().getDate();

        const filteredDataDay = data.filter(item => {
          const itemDate = new Date(item.timestamp).getDate();
          return itemDate === currentDate;
        });

        const labels = filteredDataDay.map(item => new Date(item.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));
        const values = filteredDataDay.map(item => item.message);

        createOrUpdateChart(labels, values);

        // zorg dat deze knop een geselecteerd vinkje krijgt en de abdere knoppen niet 
        btnHour.classList.remove('selected');
        btnDay.classList.add('selected');
        btnWeek.classList.remove('selected');
        btnMonth.classList.remove('selected');

        // Update the other buttons (btn3, btn4, btn5) as needed
      });

      btnWeek.addEventListener('click', function() {
        // pak de data en zorg dat alleen de WEEK word gepakt
        const currentWeek = moment().week();

        const filteredDataWeek = data.filter(item => {
          const itemWeek = moment(item.timestamp).week();
          return itemWeek === currentWeek;
        });

        const labels = filteredDataWeek.map(item => moment(item.timestamp).format('ll'));
        const values = filteredDataWeek.map(item => item.message);

        createOrUpdateChart(labels, values);


        // zorg dat deze knop een geselecteerd vinkje krijgt en de abdere knoppen niet 
        btnHour.classList.remove('selected');
        btnDay.classList.remove('selected');
        btnWeek.classList.add('selected');
        btnMonth.classList.remove('selected');
      });

      btnMonth.addEventListener('click', function() {
        // pak de data en zorg dat alleen de MAAND word gepakt
        const currentMonth = new Date().getMonth();

        const filteredDataMonth = data.filter(item => {
          const itemMonth = new Date(item.timestamp).getMonth();
          return itemMonth === currentMonth;
        });

        const labels = filteredDataMonth.map(item => moment(item.timestamp).format('ll'));
        const values = filteredDataMonth.map(item => item.message);

        createOrUpdateChart(labels, values);

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
