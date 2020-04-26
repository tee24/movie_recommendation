let seasonChart = document.getElementById('seasonChart').getContext('2d');
let ratingsChart = new Chart(seasonChart, {
type: 'line',
data: {
    labels: ['1', '2', '3', '4', '5', '6', '7' ],
    datasets: [{
    data: [
        7.9,
        8.2,
        6.4,
        9.8,
        6.7,
        8.1,
        9.2
    ],
    fill: false,
    label: 'Episode Rating',
    borderColor: "#55bae7",
    backgroundColor: "#e755ba",
    pointBackgroundColor: "#000000",
    pointBorderColor: "#000000",
    pointHoverBackgroundColor: "#55bae7",
    pointHoverBorderColor: "#55bae7"
    }

    ]
},
options: {
    title:{
    display: true,
    text: 'Rating Per Episode'
    }
}
});