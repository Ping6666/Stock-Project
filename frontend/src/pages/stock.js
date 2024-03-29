import React, { useState, useEffect } from 'react';
import {
  Link,
  useParams,
} from 'react-router-dom';

import { List, Skeleton, Table, Input, Space } from 'antd';

// import Highcharts from 'highcharts';
import * as Highcharts from 'highcharts/highstock';
import HighchartsReact from 'highcharts-react-official';

import 'highcharts/css/stocktools/gui.css';
import 'highcharts/css/annotations/popup.css';

import { get_dates, get_date_result, get_date_csv } from '../javascripts/api';

require("highcharts/modules/hollowcandlestick")(Highcharts);
require("highcharts/indicators/indicators")(Highcharts);
require("highcharts/indicators/indicators-all")(Highcharts);

require("highcharts/modules/drag-panes")(Highcharts);
require("highcharts/modules/annotations-advanced")(Highcharts);
require("highcharts/modules/price-indicator")(Highcharts);
require("highcharts/modules/full-screen")(Highcharts);
require("highcharts/modules/stock-tools")(Highcharts);

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

  const [searchValue, setSearchValue] = useState(null);

  const columns = [
    {
      // title: 'Name',
      title: () => {
        return (
          <>
            <Space>
              Name

              <Input
                placeholder={'Search Name'}
                value={searchValue}
                onChange={(e) => {
                  setSearchValue(e.target.value);
                }}
                onClick={(e) => e.stopPropagation()}
              />
            </Space>
          </>
        );
      },
      dataIndex: 'Name',
      fixed: 'left',
      width: '15%',
      showSorterTooltip: false,
      sorter: (a, b) => a.Name.localeCompare(b.Name),
      render: (text) => <Link to={"/stock/" + params.date_str + "/" + text}>{text}</Link>,
      filteredValue: searchValue ? [searchValue] : [],
      onFilter: (value, record) => {
        return record['Name'].toString().includes(value);
      },
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
  const [showLegend, setShowLegend] = useState({ 'enabled': false, 'text': 'Show Legend' });
  const [visibles, setVisibles] = useState({
    'ohlc': true,
    'volume': true,
    'sma-5': true,
    'sma-10': true,
    'sma-20': true,
    'sma-60': true,
    'sma-120': false,
    'sma-240': false,
    'kc': false,
    'bb': false,
    'vbp': false,
    'ikh': false,
    'rsi': false,
    'kd': false,
    'k_rsi': true,
    'd_rsi': true,
  });

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
    exporting: {
      buttons: {
        contextButton: {
          menuItems: [
            {
              text: showLegend['text'],
              onclick: function () {
                setShowLegend((value) => {
                  if (value['enabled']) {
                    return { 'enabled': false, 'text': 'Show Legend' };
                  } else {
                    return { 'enabled': true, 'text': 'Hide Legend' };
                  }
                });
              },
            },
            "separator",
            "viewFullscreen",
            "printChart",
            "separator",
            "downloadPNG",
            "downloadJPEG",
            "downloadPDF",
            "downloadSVG",
          ],
        }
      },
    },
    legend: {
      enabled: showLegend['enabled'],
      align: 'right',
      verticalAlign: 'top',
      layout: 'vertical',
    },
    rangeSelector: {
      selected: 3,
    },
    plotOptions: {
      series: {
        showInLegend: true,
        events: {
          legendItemClick(e) {
            const _key = e.target.name;
            const _value = !e.target.visible;

            setVisibles({ ...visibles, [_key]: _value });
          },
        },
      },
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
        type: 'hollowcandlestick',
        id: 'OHLC',
        name: 'ohlc',
        data: data['ohlc'],
        visible: visibles['ohlc'],
      },
      {
        type: 'column',
        id: 'volume',
        name: 'volume',
        data: data['volume'],
        visible: visibles['volume'],
        yAxis: 1,
      },
      //
      {
        type: 'sma',
        name: 'sma-5',
        linkedTo: 'OHLC',
        visible: visibles['sma-5'],
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
        visible: visibles['sma-10'],
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
        visible: visibles['sma-20'],
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
        visible: visibles['sma-60'],
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
        visible: visibles['sma-120'],
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
        visible: visibles['sma-240'],
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
        name: 'kc',
        linkedTo: 'OHLC',
        visible: visibles['kc'],
      },
      {
        type: 'bb',
        name: 'bb',
        linkedTo: 'OHLC',
        visible: visibles['bb'],
      },
      {
        type: 'vbp',
        name: 'vbp',
        linkedTo: 'OHLC',
        visible: visibles['vbp'],
      },
      //
      {
        type: 'ikh',
        name: 'ikh',
        linkedTo: 'OHLC',
        visible: visibles['ikh'],
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
        name: 'rsi',
        linkedTo: 'OHLC',
        visible: visibles['rsi'],
        marker: {
          radius: 0
        },
        yAxis: 2,
      },
      {
        type: 'stochastic',
        name: 'kd',
        linkedTo: 'OHLC',
        visible: visibles['kd'],
        yAxis: 2,
      },
      {
        name: 'k_rsi',
        data: data['k_rsi'],
        visible: visibles['k_rsi'],
        yAxis: 2,
      },
      {
        name: 'd_rsi',
        data: data['d_rsi'],
        visible: visibles['d_rsi'],
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
