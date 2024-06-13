// src/components/Finances/Finances.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Line, Bar } from 'react-chartjs-2';
import 'chart.js/auto';
import FilterButtons from '../../helpers/FilterButtons';

const Finances = () => {
  const [topChartData, setTopChartData] = useState(null);
  const [bottomChartData, setBottomChartData] = useState(null);
  const [daysFilter, setDaysFilter] = useState(90);

  const fetchData = async () => {
    try {
      const response = await axios.get('https://evuc3y0h1g.execute-api.eu-north-1.amazonaws.com/PROD/accessTradeLog');
      const data = response.data;

      const sortedData = data.sort((a, b) => new Date(a.dayID) - new Date(b.dayID));

      const days = sortedData.map(entry => entry.dayID);
      const energyBought = sortedData.map(entry => entry.energyBought);
      const energySold = sortedData.map(entry => entry.energySold);
      const earnings = sortedData.map(entry => entry.earnings);

      setTopChartData({
        labels: days,
        datasets: [
          {
            label: 'Energy Bought',
            data: energyBought,
            backgroundColor: 'rgba(75,192,192,0.2)',
            borderColor: 'rgba(75,192,192,1)',
          },
          {
            label: 'Energy Sold',
            data: energySold,
            backgroundColor: 'rgba(153,102,255,0.2)',
            borderColor: 'rgba(153,102,255,1)',
          },
        ],
      });

      setBottomChartData({
        labels: days,
        datasets: [
          {
            label: 'Earnings',
            data: earnings,
            backgroundColor: 'rgba(255, 159, 64, 0.8)',
            borderColor: 'rgba(255, 159, 64, 1)',
            borderWidth: 1,
          },
        ],
      });
    } catch (error) {
      console.error('Error fetching data', error);
    }
  };

  useEffect(() => {
    document.title = 'Finances | Smart Grid';
    fetchData();
  }, []);

  const filterData = (data, days) => {
    const endIndex = data.labels.length;
    const startIndex = Math.max(0, endIndex - days);
    return {
      ...data,
      labels: data.labels.slice(startIndex, endIndex),
      datasets: data.datasets.map(dataset => ({
        ...dataset,
        data: dataset.data.slice(startIndex, endIndex),
      })),
    };
  };

  const handleDaysFilterChange = (days) => {
    setDaysFilter(days);
  };

  const filteredTopChartData = topChartData ? filterData(topChartData, daysFilter) : null;
  const filteredBottomChartData = bottomChartData ? filterData(bottomChartData, daysFilter) : null;

  return (
    <div className="flex flex-col items-center justify-center mt-10">
      <FilterButtons daysFilter={daysFilter} handleDaysFilterChange={handleDaysFilterChange} />
      <div className="flex w-11/12 md:w-3/4">
        <div className="w-1/2">
          {filteredTopChartData ? (
            <div className="chart-container mb-8">
              <Line data={filteredTopChartData} />
            </div>
          ) : (
            <p className="text-white">Loading chart data...</p>
          )}
          {filteredBottomChartData ? (
            <div className="chart-container">
              <Bar data={filteredBottomChartData} />
            </div>
          ) : (
            <p className="text-white">Loading earnings data...</p>
          )}
        </div>
        <div className="w-1/2 text-white ml-8">
          <h2 className="text-xl mb-4">Analysis</h2>
          <p className="mb-4"></p>
        </div>
      </div>
    </div>
  );
};

export default Finances;
