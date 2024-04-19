import { Column } from '@ant-design/charts';
import { useEffect, useState } from 'react';


interface DataType {
  label: string;
  value: number;
}

const KeywordAndAmountChart = () => {
  const [data, setData] = useState<DataType[]>([]);
  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch('http://localhost:5000/keyword_and_urls/antd/column_chart');
      const data = await response.json();
      setData(data);
    };
    fetchData(); // initialize
    setInterval(() => {
      fetchData();
    }, 1500);
  }, []);

  console.log(data)
  

  const config = {
    data,
    xField: 'label',
    yField: 'value',
    height: window.innerHeight * 0.3,
    color: '#1890ff',
  };

  return <Column {...config} />;
};

export default KeywordAndAmountChart;