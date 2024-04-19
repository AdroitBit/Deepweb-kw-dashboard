
import { useEffect, useState } from 'react';


import {Gauge} from '@ant-design/charts';


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







function ServerStatus(){
    const [data, setData] = useState([]);
    useEffect(() => {
        const fetchData = async () => {
            const response = await fetch('http://localhost:5000/server_health/antd/gauge');
            const data = await response.json();
            setData(data);
        };
        fetchData(); // initialize

        setInterval(() => {
            fetchData();
        }, 1500);

    }, []);

    return (
        <div style={{ display: 'flex', justifyContent: 'space-around' }}>
            {
              data.map((d: DataType) => (
                <MonitorGauge data={d} />
              ))
            }
        </div>
    );
}
export default ServerStatus;