export const regionData = [
  {
    value: '11',
    label: '北京市',
    children: [
      {
        value: '1101',
        label: '北京市',
        children: [
          {
            value: '110101',
            label: '东城区',
            children: [
              {
                value: '110101001',
                label: '东华门街道',
                children: [
                  {
                    value: '110101001001',
                    label: '多福巷社区'
                  },
                  {
                    value: '110101001002',
                    label: '银闸社区'
                  }
                ]
              },
              {
                value: '110101002',
                label: '景山街道',
                children: [
                  {
                    value: '110101002001',
                    label: '隆福寺社区'
                  }
                ]
              }
            ]
          },
          {
            value: '110102',
            label: '西城区',
            children: [
              {
                value: '110102001',
                label: '西长安街街道',
                children: [
                  {
                    value: '110102001001',
                    label: '天安门社区'
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  {
    value: '44',
    label: '广东省',
    children: [
      {
        value: '4401',
        label: '广州市',
        children: [
          {
            value: '440103',
            label: '荔湾区',
            children: [
              {
                value: '440103001',
                label: '沙面街道',
                children: [
                  {
                    value: '440103001001',
                    label: '沙面社区'
                  }
                ]
              }
            ]
          },
          {
            value: '440104',
            label: '越秀区',
            children: [
              {
                value: '440104001',
                label: '建设街道',
                children: [
                  {
                    value: '440104001001',
                    label: '建设社区'
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        value: '4403',
        label: '深圳市',
        children: [
          {
            value: '440303',
            label: '罗湖区',
            children: [
              {
                value: '440303001',
                label: '桂园街道',
                children: [
                  {
                    value: '440303001001',
                    label: '红桂社区'
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  }
  // ... 这里只展示了部分数据
  // 完整的数据建议通过后端API获取
  // 或者使用专门的行政区划数据库
] 