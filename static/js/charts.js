// Ticket Priority Pie Chart

// Make an AJAX call to retrieve data
  // Make an AJAX call to retrieve data
  $.ajax({
    url: '/ticket_data/',
    success: function(data) {
      var ctx = document.getElementById('priority-pie-chart').getContext('2d');
      var myChart = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: ['High', 'Medium', 'Low', 'None'],
          datasets: [{
            data: data.values,
            backgroundColor: [
              'rgba(255, 99, 132, 0.8)',
              'rgba(54, 162, 235, 0.8)',
              'rgba(255, 206, 86, 0.8)',
              'rgba(75, 192, 192, 0.8)'
            ]
          }]
        },
        options: {
          title: {
            display: true,
            text: 'Tickets by Priority'
          }
        }
      });
    }
  });


// Ticket Type Doughnut chart

$.ajax({
    url: '/type_data/',
    success: function(data) {
      var ctx = document.getElementById('donut-chart').getContext('2d');
      var myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: ['Misc', 'Bug', 'Help Needed', 'Concern', 'Question'],
          datasets: [{
            data: data.values,
            backgroundColor: [
              'rgba(255, 99, 132, 0.8)',
              'rgba(54, 162, 235, 0.8)',
              'rgba(255, 206, 86, 0.8)',
              'rgba(75, 192, 192, 0.8)',
              'rgba(102, 0, 255, 0.8)'
            ]
          }]
        },
        options: {
          title: {
            display: true,
            text: 'Tickets by Type'
          }
        }
      });
    }
  });


// Ticket Status Pie Chart
$.ajax({
    url: '/status_data/',
    success: function(data) {
      var ctx = document.getElementById('status-pie-chart').getContext('2d');
      var myChart = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: ['Open', 'Closed'],
          datasets: [{
            data: data.values,
            backgroundColor: [
              'rgba(54, 162, 235, 0.8)',
              'rgba(255, 99, 132, 0.8)',
            ]
          }]
        },
        options: {
          title: {
            display: true,
            text: 'Tickets by Status'
          }
        }
      });
    }
  });

// User Doughnut Chart

var ctx = document.getElementById('user-donut-chart').getContext('2d');
    var myChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['High', 'Medium', 'Low'],
        datasets: [{
          data: [12, 19, 3],
          backgroundColor: [
            'rgba(255, 99, 132, 0.8)',
            'rgba(54, 162, 235, 0.8)',
            'rgba(255, 206, 86, 0.8)'
          ]
        }]
      },
      options: {
        title: {
          display: true,
          text: 'Tickets by User'
        }
      }
    });
