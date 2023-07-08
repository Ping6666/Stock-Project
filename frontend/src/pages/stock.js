import React, { useState, useEffect } from 'react';
import {
  Link,
  useParams,
} from 'react-router-dom';

import { List, Skeleton, Table } from 'antd';

import { get_dates, get_date, get_date_result } from '../javascripts/api';

const StockList = () => {
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

const columns = [
  {
    title: 'Name',
    dataIndex: 'Name',
    sorter: (a, b) => a.Name.localeCompare(b.Name),
    fixed: 'left',
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

const Stock = () => {
  let params = useParams();

  const [list, setList] = useState([]);

  const _get_date_result = async function () {
    const { status, files } = await get_date_result(params.date_str);

    if (status) {
      for (var i = 0; i < files.length; i++) {
        files[i].key = i;

        const keys = Object.keys(files[i]);

        for (var j = 0; j < keys.length; j++) {
          if (keys[j] != 'key' && keys[j] != 'Name') {

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

export {
  StockList,
  Stock,
};
