function history(user, data) {
    var chartDom = document.getElementById('c');
    var myChart = echarts.init(chartDom);
    var option;
    setTimeout(function () {
        option = {
            title: {
                text: user,
                left: '10%',
            },
            legend: {},
            tooltip: {
                trigger: 'axis',
                showContent: false
            },
            toolbox: {
                show: true,
                feature: {
                    dataView: {show: true, readOnly: false},
                    restore: {show: true},
                    saveAsImage: {show: true}
                }
            },
            dataZoom: [
                {
                    id: 'dataZoomX',
                    type: 'slider',
                    xAxisIndex: [0],
                    filterMode: 'filter', // 设定为 'filter' 从而 X 的窗口变化会影响 Y 的范围。
                    start: 0,
                    end: 100
                },
                {
                    id: 'dataZoomY',
                    type: 'slider',
                    yAxisIndex: [0],
                    filterMode: 'empty',
                    start: 0,
                    end: 100
                }
            ],

            dataset: {
                source: data
            },
            xAxis: {type: 'category'},
            yAxis: {gridIndex: 0},
            grid: {top: '55%'},
            series: [
                {type: 'line', smooth: true, seriesLayoutBy: 'row', emphasis: {focus: 'series'}},
                {type: 'line', smooth: true, seriesLayoutBy: 'row', emphasis: {focus: 'series'}},
                {type: 'line', smooth: true, seriesLayoutBy: 'row', emphasis: {focus: 'series'}},
                {
                    type: 'pie',
                    id: 'pie',
                    radius: '30%',
                    center: ['50%', '25%'],
                    emphasis: {focus: 'data'},
                    label: {
                        formatter: '{b}: {@[1]} ({d}%)'
                    },
                    encode: {
                        itemName: '答题时间',
                        value: data[0][1],
                        tooltip: data[0][1]
                    }
                }
            ]
        };

        myChart.on('updateAxisPointer', function (event) {
            var xAxisInfo = event.axesInfo[0];
            if (xAxisInfo) {
                var dimension = xAxisInfo.value + 1;
                console.log(dimension)
                myChart.setOption({
                    series: {
                        id: 'pie',
                        label: {
                            formatter: '{b}: {@[' + dimension + ']} ({d}%)'
                        },
                        encode: {
                            value: dimension,
                            tooltip: dimension
                        }
                    }
                });
            }
        });

        myChart.setOption(option);

    });

    option && myChart.setOption(option);
}