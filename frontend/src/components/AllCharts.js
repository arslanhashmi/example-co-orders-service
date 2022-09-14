import { useEffect, useState } from "react";
import LineChart from "./LineChart";
import axios from "axios";
import "./AllCharts.css";

const MONTHS = [
  "JANUARY",
  "FEBRUARY",
  "MARCH",
  "APRIL",
  "MAY",
  "JUNE",
  "JULY",
  "AUGUST",
  "SEPTEMBER",
  "OCTOBER",
  "NOVEMBER",
  "DECEMBER",
];

const WEEK_DAYS = [
  "MONDAY",
  "TUESDAY",
  "WEDNESDAY",
  "THURSDAY",
  "FRIDAY",
  "SATURDAY",
  "SUNDAY",
];

const date = new Date();
const MONTH_DAYS_MAX = new Date(
  date.getFullYear(),
  date.getMonth() + 1,
  0
).getDate();
const MONTH_DAYS = Array.from(Array(MONTH_DAYS_MAX + 1).keys()).slice(
  1,
  MONTH_DAYS_MAX + 1
);

const LABELS = {
  THIS_WEEK: WEEK_DAYS,
  THIS_MONTH: MONTH_DAYS,
  THIS_YEAR: MONTHS,
};

const options = {
  legend: {
    display: false,
    position: "right",
    labels: {
      boxWidth: 50,
      fontSize: 25,
      fontColor: "gray",
        },
    },
    scales: {
        y: {
            beginAtZero: true
        }
    }
};

function AllCharts() {
  const [chartData, setChartData] = useState(null);

  async function fetchData(event) {
    const value = event ? event.target.value : "THIS_YEAR";
    const response = await axios.get(
      `http://localhost:8080/orders?span=${value}`
    );
    const data = response.data;
    let count = [];
    if (value === "THIS_MONTH") {
      count = new Array(MONTH_DAYS_MAX).fill(0);
      data.forEach(
        ({ created_on }) => (count[new Date(created_on).getDay()] += 1)
      );
    } else if (value === "THIS_WEEK") {
      count = new Array(7).fill(0);
      data.forEach(
        ({ created_on }) => (count[new Date(created_on).getDay()] += 1)
      );
    } else {
      count = new Array(12).fill(0);
      data.forEach(
        ({ created_on }) => (count[new Date(created_on).getMonth()] += 1)
      );
    }
    setChartData({
      data: count,
      labels: LABELS[value],
      data_count: response.data.length,
    });
  }

    useEffect(() => {
      fetchData();
    }, []);

  return (
    <div className="all-charts">
      <div style={{ width: 1000 }} className="line-chart">
        <div className="header">
          <h2>New Orders</h2>
          <select id="span" onChange={fetchData}>
            <option value="THIS_YEAR">THIS YEAR</option>
            <option value="THIS_MONTH">THIS MONTH</option>
            <option value="THIS_WEEK">THIS WEEK</option>
          </select>
        </div>

        <h1>{chartData && chartData.data_count}</h1>

        <LineChart
          chartData={{
            labels: chartData ? chartData.labels : [],
            datasets: [
              {
                label: "New Orders",
                data: chartData ? chartData.data : [],
                backgroundColor: [
                  "rgba(75,192,192,1)",
                  "#ecf0f1",
                  "#50AF95",
                  "#f3ba2f",
                  "#2a71d0",
                ],
                borderColor: "black",
                borderWidth: 2,
              },
            ],
          }}
          options={options}
        />
      </div>
    </div>
  );
}

export default AllCharts;
