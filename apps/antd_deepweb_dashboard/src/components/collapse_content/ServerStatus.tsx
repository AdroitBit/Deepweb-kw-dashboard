
import { useEffect, useState } from 'react';


import {Gauge} from '@ant-design/charts';
import { Input } from 'antd';


interface DataType {
  label: string;
  value: number;
  display_label: string;
  highest_value: number;
}


const MonitorGauge = ({ data }: { data:DataType }) => {
    const thresholds = [data.highest_value*0.5, data.highest_value*0.8, data.highest_value];
    const config = {
        width: window.innerWidth*0.35,
        height: window.innerWidth*0.35,
        autoFit: false,
        data: {
            target: data.value,
            total: data.highest_value,

            thresholds: thresholds,
        },
        legend: false,
        scale: {
            color: {
                range: ['lime','orange','red'],
            },
        },
        style: {
            textContent: function(){
                //target:number,total:number
                // console.log(args);
                return `${data.label} : ${data.display_label}`
            },
            color: 'blue',
        },
    };
    return <Gauge {...config} />;
};







function ServerStatus({ backend_url }: { backend_url: string }){
    const [data, setData] = useState([]);
    const [endpoint, setEndpoint] = useState('/server_health/antd/gauge');
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

    return (
        <>
            <Input placeholder='endpoint' onInput={(e) => { setEndpoint(e.currentTarget.value) }} defaultValue={endpoint} />
            <div style={{ display: 'flex', justifyContent: 'space-around' }}>
                {
                data.map((d: DataType) => (
                    <MonitorGauge data={d} />
                ))
                }
            </div>
        </>
    );
}
export default ServerStatus;