import React, { useState, useEffect } from 'react';
import {
  Link,
  useParams,
} from 'react-router-dom';

import {
  List,
  Skeleton,
  Typography,
  Button,
  Space,
  Switch,
  Row,
  Col,
  message,
} from 'antd';
import {
  DownloadOutlined,
} from '@ant-design/icons';

import { get_symbols, get_symbol } from '../javascripts/api';

const { Title, Paragraph } = Typography;

const DownloadList = () => {
  const [initLoading, setInitLoading] = useState(true);
  const [list, setList] = useState([]);

  const _get_symbols = async function () {
    const { status, files } = await get_symbols();

    if (status) {
      setInitLoading(false);
      setList(files);
    }
  };

  useEffect(() => {
    _get_symbols();
  }, []);

  return (
    <List
      className="list"
      loading={initLoading}
      itemLayout="horizontal"
      dataSource={list}
      renderItem={(item) => (
        <List.Item
          actions={[<Link to={"/download/" + item}>view</Link>]}
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

const Download = () => {
  let params = useParams();

  const [checked, setChecked] = useState(false);
  const [ctx, setCtx] = useState([]);

  const [messageApi, contextHolder] = message.useMessage();

  const get_overwrite = function () {
    if (checked) {
      return 1;
    }

    return 0;
  }

  const _get_symbol = async function (_download) {
    const _overwrite = get_overwrite();

    console.log(`download: ${_download}; overwrite: ${_overwrite}`);

    const res = await get_symbol(params.symbol_str, _download, _overwrite);

    setCtx(res);
  };

  const _download = function () {
    messageApi.open({
      type: 'success',
      content: 'Downloading',
      duration: 3,
    });
  };

  const _onClick = function () {
    _get_symbol(1);
    _download();
  };

  useEffect(() => {
    _get_symbol(0);
  }, []);

  return (
    <div>
      {contextHolder}

      <Typography>
        <Row justify="space-between" align="bottom">

          <Col >
            <Title>
              {params.symbol_str}
            </Title>
          </Col>

          <Col >
            <Space direction="horizontal">
              <Switch checkedChildren="overwrite" unCheckedChildren="default" checked={checked} onChange={setChecked} />
              <Button type="primary" shape="round" icon={<DownloadOutlined />} onClick={_onClick}>
                Download
              </Button>
            </Space>
          </Col>

        </Row>

        <Paragraph style={{ whiteSpace: 'pre-line' }}>{ctx}</Paragraph>
      </Typography>
    </div>
  );
};

export {
  DownloadList,
  Download,
};
