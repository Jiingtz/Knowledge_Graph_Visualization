function radar(user, data) {
    var chartDom = document.getElementById('radar');
    var myChart = echarts.init(chartDom);
    var option;

    option = {
        title: {
            text: '错误知识点雷达图' + '\n\n用户：' + user
        },
        tooltip: {},
        legend: {
            x: 'left',
            y: 'center',
            data: ['错误知识点']
        },
        radar: {
            // shape: 'circle',
            name: {
                textStyle: {
                    color: '#fff',
                    backgroundColor: '#999',
                    borderRadius: 3,
                    padding: [3, 5]
                }
            },
            indicator: [
                {name: data[0][0], max: 15},
                {name: data[1][0], max: 15},
                {name: data[2][0], max: 15},
                {name: data[3][0], max: 15},
                {name: data[4][0], max: 15},
                {name: data[5][0], max: 15}
            ]
        },
        series: [{
            name: '错误知识点',
            type: 'radar',
            // areaStyle: {normal: {}},
            data: [
                {
                    value: [data[0][1], data[1][1], data[2][1], data[3][1], data[4][1], data[5][1]],
                    name: '错误知识点',
                    areaStyle: {
                        normal: {
                            color: 'rgb(210,7,34)' // 选择区域颜色
                        }
                    }

                },
            ]
        }]
    };

    option && myChart.setOption(option);
}