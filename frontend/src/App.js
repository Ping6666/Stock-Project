import React from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
} from 'react-router-dom';

import { Layout, Menu } from 'antd';
import {
  HomeOutlined,
  DatabaseOutlined,
  CloudDownloadOutlined,
} from '@ant-design/icons';

import { Home } from './pages/home';
import { StockDateList, StockList, Stock } from './pages/stock';
import { DownloadList, Download } from './pages/download';

// TODO Breadcrumb

const {
  // Header,
  Content,
  Footer,
  Sider,
} = Layout;

const menuItems = [
  {
    key: '1',
    icon: <HomeOutlined />,
    label: <Link to="/">Home</Link>,
  },
  {
    key: '2',
    icon: <DatabaseOutlined />,
    label: <Link to="/stock">Stock</Link>,
  },
  {
    key: '3',
    icon: <CloudDownloadOutlined />,
    label: <Link to="/download">Download</Link>,
  },
];

function App() {
  return (
    <Router>
      <Layout style={{ minHeight: '100vh' }}>

        <Sider>
          <Menu theme="dark" mode="inline" defaultSelectedKeys={['1']} items={menuItems}>
          </Menu>
        </Sider>

        <Layout
          style={{ height: "100vh" }}
        >

          {/* 
          <Header>
          </Header>
           */}

          <Content style={{ padding: '0 50px', overflow: "auto" }}>

            <div style={{ background: '#fff', padding: 24 }}>
              <Routes>

                <Route path='/' element={<Home />} />
                <Route path='/stock' element={<StockDateList />} />
                <Route path='/stock/:date_str' element={<StockList />} />
                <Route path='/stock/:date_str/:csv_str' element={<Stock />} />
                <Route path='/download' element={<DownloadList />} />
                <Route path='/download/:symbol_str' element={<Download />} />

              </Routes>
            </div>

          </Content>

          {/* 
          <Footer style={{ textAlign: 'center' }}>
            Stock © {new Date().getFullYear()} Created by Ping
          </Footer>
           */}

        </Layout>

      </Layout>
    </Router>
  );
}

export default App;