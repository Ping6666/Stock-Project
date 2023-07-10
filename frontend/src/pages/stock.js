import React, { useState, useEffect } from 'react';
import {
  Link,
  useParams,
} from 'react-router-dom';

import { List, Skeleton, Table } from 'antd';

// import Highcharts from 'highcharts';
import * as Highcharts from 'highcharts/highstock';
import HighchartsReact from 'highcharts-react-official';

import { get_dates, get_date_result, get_date_csv } from '../javascripts/api';

require("highcharts/indicators/indicators")(Highcharts);
require("highcharts/indicators/bollinger-bands")(Highcharts);
require("highcharts/indicators/atr")(Highcharts);
require("highcharts/indicators/ema")(Highcharts);
require("highcharts/indicators/keltner-channels")(Highcharts);
require("highcharts/indicators/volume-by-price")(Highcharts);
require("highcharts/indicators/ichimoku-kinko-hyo")(Highcharts);
require("highcharts/indicators/rsi")(Highcharts);
require("highcharts/indicators/stochastic")(Highcharts);

require("highcharts/modules/exporting")(Highcharts);
require("highcharts/modules/accessibility")(Highcharts);

const StockDateList = () => {
  const [initLoading, setInitLoading] = useState(true);
  const [list, setList] = useState([]);

  const _get_dates = async function () {
    const { status, files } = await get_dates();

    if (status) {
      setInitLoading(false);
      setList(files);
    }
  };

  useEffect(() => {
    _get_dates();
  }, []);

  return (
    <List
      className="list"
      loading={initLoading}
      itemLayout="horizontal"
      dataSource={list}
      renderItem={(item) => (
        <List.Item
          actions={[<Link to={"/stock/" + item}>view</Link>]}
        >
          <Skeleton title={false} loading={item.loading} active>
            <List.Item.Meta
              title={item}
            />
          </Skeleton>
        </List.Item>
      )}
    />
  );
};

const StockList = () => {
  let params = useParams();

  const columns = [
    {
      title: 'Name',
      dataIndex: 'Name',
      fixed: 'left',
      sorter: (a, b) => a.Name.localeCompare(b.Name),
      render: (text) => <Link to={"/stock/" + params.date_str + "/" + text}>{text}</Link>
    },
    //
    {
      title: 'Open',
      dataIndex: 'Open',
      sorter: (a, b) => a.Open - b.Open,
    },
    {
      title: 'High',
      dataIndex: 'High',
      sorter: (a, b) => a.High - b.High,
    },
    {
      title: 'Low',
      dataIndex: 'Low',
      sorter: (a, b) => a.Low - b.Low,
    },
    {
      title: 'Close',
      dataIndex: 'Close',
      sorter: (a, b) => a.Close - b.Close,
    },
    //
    {
      title: 'Volume',
      dataIndex: 'Volume',
      sorter: (a, b) => a.Volume - b.Volume,
    },
    //
    {
      title: 'K',
      dataIndex: 'K',
      sorter: (a, b) => a.K - b.K,
    },
    {
      title: 'D',
      dataIndex: 'D',
      sorter: (a, b) => a.D - b.D,
    },
    //
    {
      title: 'RSI',
      dataIndex: 'RSI',
      sorter: (a, b) => a.RSI - b.RSI,
    },
    //
    {
      title: 'K_RSI',
      dataIndex: 'K_RSI',
      sorter: (a, b) => a.K_RSI - b.K_RSI,
    },
    {
      title: 'D_RSI',
      dataIndex: 'D_RSI',
      sorter: (a, b) => a.D_RSI - b.D_RSI,
    },
    //
    {
      title: 'KC_high',
      dataIndex: 'KC_high',
      sorter: (a, b) => a.KC_high - b.KC_high,
    },
    {
      title: 'KC_middle',
      dataIndex: 'KC_middle',
      sorter: (a, b) => a.KC_middle - b.KC_middle,
    },
    {
      title: 'KC_low',
      dataIndex: 'KC_low',
      sorter: (a, b) => a.KC_low - b.KC_low,
    },
    //
    {
      title: 'ICH_plot_1',
      dataIndex: 'ICH_plot_1',
      sorter: (a, b) => a.ICH_plot_1 - b.ICH_plot_1,
    },
    {
      title: 'ICH_plot_2',
      dataIndex: 'ICH_plot_2',
      sorter: (a, b) => a.ICH_plot_2 - b.ICH_plot_2,
    },
    {
      title: 'ICH_plot_3',
      dataIndex: 'ICH_plot_3',
      sorter: (a, b) => a.ICH_plot_3 - b.ICH_plot_3,
    },
    //
    {
      title: 'SMA_5',
      dataIndex: 'SMA_5',
      sorter: (a, b) => a.SMA_5 - b.SMA_5,
    },
    {
      title: 'SMA_10',
      dataIndex: 'SMA_10',
      sorter: (a, b) => a.SMA_10 - b.SMA_10,
    },
    {
      title: 'SMA_20',
      dataIndex: 'SMA_20',
      sorter: (a, b) => a.SMA_20 - b.SMA_20,
    },
    {
      title: 'SMA_60',
      dataIndex: 'SMA_60',
      sorter: (a, b) => a.SMA_60 - b.SMA_60,
    },
    {
      title: 'SMA_120',
      dataIndex: 'SMA_120',
      sorter: (a, b) => a.SMA_120 - b.SMA_120,
    },
    {
      title: 'SMA_240',
      dataIndex: 'SMA_240',
      sorter: (a, b) => a.SMA_240 - b.SMA_240,
    },
  ];

  const onChange = (pagination, filters, sorter, extra) => {
    console.log('params', pagination, filters, sorter, extra);
  };

  const [list, setList] = useState([]);

  const _get_date_result = async function () {
    const { status, files } = await get_date_result(params.date_str);

    if (status) {
      for (var i = 0; i < files.length; i++) {
        files[i].key = i;

        const keys = Object.keys(files[i]);

        for (var j = 0; j < keys.length; j++) {
          if (keys[j] !== 'key' && keys[j] !== 'Name') {

            files[i][keys[j]] = Number.parseFloat(files[i][keys[j]]).toFixed(1);
            // keys[j] = Math.round10(keys[j], -1);
          }
        }

      }

      setList(files);
    }
  };

  useEffect(() => {
    _get_date_result();

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <Table
      columns={columns}
      dataSource={list}
      onChange={onChange}
      scroll={{
        x: 1500,
        // y: 600,
      }}
      tableLayout='auto'
    />
  );
};

const Stock = () => {
  let params = useParams();

  const [data, setData] = useState({});

  const options = {
    chart: {
      height: window.innerHeight - 50,
    },
    title: {
      text: params.csv_str,
    },
    accessibility: {
      enabled: false,
    },
    legend: {
      enabled: true,
    },
    rangeSelector: {
      selected: 3,
    },
    plotOptions: {
      series: {
        showInLegend: true
      }
    },
    xAxis: {
    },
    yAxis: [
      {
        height: '80%',
      },
      {
        top: '90%',
        height: '10%',
      },
      {
        top: '80%',
        height: '10%',
        plotLines: [
          {
            color: '#FF0000',
            width: 2,
            value: 10
          },
          {
            color: '#FF0000',
            width: 2,
            value: 70
          },
        ],
      },
    ],
    series: [
      {
        type: 'candlestick',
        id: 'OHLC',
        name: 'ohlc',
        data: data['ohlc'],
      },
      {
        type: 'column',
        id: 'volume',
        name: 'volume',
        data: data['volume'],
        yAxis: 1,
      },
      //
      {
        type: 'sma',
        name: 'sma-5',
        linkedTo: 'OHLC',
        marker: {
          radius: 0
        },
        params: {
          period: 5,
        },
      },
      {
        type: 'sma',
        name: 'sma-10',
        linkedTo: 'OHLC',
        marker: {
          radius: 0
        },
        params: {
          period: 10,
        },
      },
      {
        type: 'sma',
        name: 'sma-20',
        linkedTo: 'OHLC',
        marker: {
          radius: 0
        },
        params: {
          period: 20,
        },
      },
      {
        type: 'sma',
        name: 'sma-60',
        linkedTo: 'OHLC',
        marker: {
          radius: 0
        },
        params: {
          period: 60,
        },
      },
      {
        type: 'sma',
        name: 'sma-120',
        linkedTo: 'OHLC',
        visible: false,
        marker: {
          radius: 0
        },
        params: {
          period: 120,
        },
      },
      {
        type: 'sma',
        name: 'sma-240',
        linkedTo: 'OHLC',
        visible: false,
        marker: {
          radius: 0
        },
        params: {
          period: 240,
        },
      },
      //
      {
        type: 'keltnerchannels',
        linkedTo: 'OHLC',
        visible: false,
      },
      {
        type: 'bb',
        linkedTo: 'OHLC',
        visible: false,
      },
      {
        type: 'vbp',
        linkedTo: 'OHLC',
        visible: false,
      },
      //
      {
        type: 'ikh',
        linkedTo: 'OHLC',
        visible: false,
        tenkanLine: {
          styles: {
            lineColor: 'lightblue',
          },
        },
        kijunLine: {
          styles: {
            lineColor: 'darkred',
          },
        },
        chikouLine: {
          styles: {
            lineColor: 'lightgreen',
          },
        },
        senkouSpanA: {
          styles: {
            lineColor: 'green',
          },
        },
        senkouSpanB: {
          styles: {
            lineColor: 'red',
          },
        },
        senkouSpan: {
          color: 'rgba(0, 255, 0, 0.3)',
          styles: {
            fill: 'rgba(0, 0, 255, 0.1)',
          },
        },
      },
      //
      {
        type: 'rsi',
        linkedTo: 'OHLC',
        visible: false,
        marker: {
          radius: 0
        },
        yAxis: 2,
      },
      {
        type: 'stochastic',
        linkedTo: 'OHLC',
        visible: false,
        yAxis: 2,
      },
      {
        name: 'K * RSI',
        data: data['k_rsi'],
        yAxis: 2,
      },
      {
        name: 'D * RSI',
        data: data['d_rsi'],
        yAxis: 2,
      },
    ],
  };

  const _date_str_2_ms = (str) => {
    const [year, month, day] = String(str).split('/');
    return Date.UTC(+year, +month - 1, +day);
  };

  const _get_date_csv = async function () {
    const { status, files } = await get_date_csv(params.date_str, params.csv_str);

    if (status) {
      const ohlc = [];
      const volume = [];
      const k_rsi = [];
      const d_rsi = [];

      for (var i = 0; i < files.length; i += 1) {
        const c_item = files[i];
        const _date_ms = _date_str_2_ms(c_item['Date']);

        ohlc.push([
          _date_ms,
          c_item['Open'],
          c_item['High'],
          c_item['Low'],
          c_item['Close'],
        ]);

        volume.push([
          _date_ms,
          c_item['Volume'],
        ]);

        k_rsi.push([
          _date_ms,
          c_item['K_RSI'],
        ]);
        d_rsi.push([
          _date_ms,
          c_item['D_RSI'],
        ]);
      }

      const _data = {
        'ohlc': ohlc,
        'volume': volume,
        'k_rsi': k_rsi,
        'd_rsi': d_rsi,
      };

      setData(_data);
    }
  };

  useEffect(() => {
    _get_date_csv();

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (

    <HighchartsReact
      constructorType={'stockChart'}
      highcharts={Highcharts}
      options={options}
    />
  );
};

export {
  StockDateList,
  StockList,
  Stock,
};
