import { useEffect, useState } from 'react';
import { Input, Table } from 'antd';
import type { TableColumnsType, TableProps } from 'antd';

interface DataType {
  keyword: string;
  url: string;
}

const columns: TableColumnsType<DataType> = [
  {
    title: 'Keyword',
    dataIndex: 'keyword',
    showSorterTooltip: { target: 'full-header' },
    width: '20%',
  },
  {
    title: 'URL',
    dataIndex: 'url',
    render: (url: string) => <a href={url}>{url}</a>,
  }
];


function KeywordAndDeepwebTable({ backend_url }: { backend_url: string }){
  const [data, setData] = useState<DataType[]>([]);
  const [endpoint, setEndpoint] = useState('/keyword_and_urls/antd/table');
  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch(`${backend_url}${endpoint}`);
      const data = await response.json();
      setData(data);
    };
    fetchData(); // initialize

    setInterval(() => {
      fetchData();
    }, 1500);
  }, [backend_url, endpoint]);

  const onChange: TableProps<DataType>['onChange'] = (pagination, filters, sorter, extra) => {
    console.log('params', pagination, filters, sorter, extra);
  };

  return (
      <>
        <Input placeholder='endpoint' onInput={(e) => { setEndpoint(e.currentTarget.value) }} defaultValue={endpoint} />
        <Table
          columns={columns}
          dataSource={data}
          onChange={onChange}
          pagination={false}
          scroll={{ y: "25vh" }}
          showSorterTooltip={{ target: 'sorter-icon' }}
        />
      </>
      
  );
}

export default KeywordAndDeepwebTable;