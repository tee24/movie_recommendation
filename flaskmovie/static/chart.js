let myChart = document.getElementById('myChart').getContext('2d');
let massPopChart = new Chart(myChart, {
type: 'bar',
data: {
    labels: ['Boston', 'Worcester', 'Providence', 'Springfield', 'Bridgeport', 'New haven'],
    datasets: [{
    label: 'Population',
    data: [
        617594,
        184045,
        178042,
        153060,
        144229,
        129779
    ],
    backgroundColor: 'green'
    }

    ]
},
options: {
    title:{
    display: true,
    text: 'mass pop'
    }
}
});