import React from 'react'
import { Line } from "react-chartjs-2";
import { Chart as ChartJS } from "chart.js/auto";

const options = {
    legend: {
        position: 'left',
        align: 'left',
    }
};

function LineChart ({ chartData}) {
    return <Line data={chartData} options={options}/>
}

export default LineChart;