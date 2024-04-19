import { useEffect, useState } from 'react';
import { Table } from 'antd';
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







function KeywordAndDeepwebTable(){
  
  const [data, setData] = useState<DataType[]>([]);
  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch('http://localhost:5000/keyword_and_urls/antd/table');
      const data = await response.json();
      setData(data);
    };
    fetchData(); // initialize

    setInterval(() => {
      fetchData();
    }, 1500);
  }, []);

  const onChange: TableProps<DataType>['onChange'] = (pagination, filters, sorter, extra) => {
    console.log('params', pagination, filters, sorter, extra);
  };
  // let data:DataType[]=[]; // dummy data
  // for(let i=0;i<100;i++){
  //   data.push({key:i,keyword:"keyword"+i,url:"url"+i});
  // }

  return (
      <Table
        columns={columns}
        dataSource={data}
        onChange={onChange}
        pagination={false}
        scroll={{ y: "25vh" }}
        showSorterTooltip={{ target: 'sorter-icon' }}
      />
  );
}

export default KeywordAndDeepwebTable;