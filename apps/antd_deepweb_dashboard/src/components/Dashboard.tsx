
import KeywordAndAmountChart from './collapse_content/KeywordAndAmountChart';
import KeywordAndDeepwebTable from './collapse_content/KeywordAndDeepwebTable.tsx';
import ServerStatus from './collapse_content/ServerStatus.tsx';
import { Collapse, Input } from 'antd';
import type { CollapseProps } from 'antd';




function Dashboard() {
  const onChange = (key: string | string[]) => {
    console.log(key);
  }
  const items: CollapseProps['items'] = [
    {
      key: '1',
      label: 'Keyword appearing in deepweb chart',
      children: <KeywordAndAmountChart/>,
    },
    {
      key: '2',
      label: 'Corresponding of keyword and deepweb url',
      children: <KeywordAndDeepwebTable/>,
    },
    {
      key: '3',
      label: 'Server status',
      children: <ServerStatus/>,
    },
  ];

  return (
    <>
      <Input
        placeholder='backend url'
      />
      <Collapse
        items={items}
        onChange={onChange}
        defaultActiveKey={['1', '2', '3']}
        style={{ width: "80vw" }}
      />
    </>
  );
}

export default Dashboard;