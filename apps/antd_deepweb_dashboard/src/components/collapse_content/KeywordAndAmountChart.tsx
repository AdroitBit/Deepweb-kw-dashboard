import { Column } from '@ant-design/charts';
import { Input } from 'antd';
import { useEffect, useState } from 'react';


interface DataType {
  label: string;
  value: number;
}

const KeywordAndAmountChart = ({ backend_url }: { backend_url: string }) => {
    const [data, setData] = useState<DataType[]>([]);
    const [endpoint, setEndpoint] = useState('/keyword_and_urls/antd/column_chart');
    useEffect(() => {
        const fetchData = async () => {
          try {
            const response = await fetch(`${backend_url}${endpoint}`);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const result = await response.json();
            setData(result);
          } catch (error) {
            console.error('Error fetching data:', error);
          }
        };
        fetchData();
        const intervalId = setInterval(fetchData, 1500);
        return () => clearInterval(intervalId);
    }, [backend_url, endpoint]);

    // console.log(data)
    

    const config = {
      data,
      xField: 'label',
      yField: 'value',
      height: window.innerHeight * 0.3,
      color: '#1890ff',
    };

    
    return (
        <>
            <Input placeholder='endpoint' onInput={(e) => { setEndpoint(e.currentTarget.value) }} defaultValue={endpoint} />
            <Column {...config} />
        </>
    )
};

export default KeywordAndAmountChart;