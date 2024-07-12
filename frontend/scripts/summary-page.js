//@ts-check


// donut chart
class DonutChart extends HTMLElement {
    connectedCallback() {

        // pull in data
        /** @type {NodeListOf<HTMLElement>} */
        const items = this.querySelectorAll('chart-item');
        let data = [];
        items.forEach((item) => {
            data.push({
                name: item.dataset.label,
                value: item.dataset.count
            });
        });

        /**
         * Size the chart and chart container
         * @param {boolean} firstTime
         */
        const sizeChart = (firstTime) => {
            this.style.display = 'none';
            this.style.width = `${this.parentElement?.scrollWidth}px`;
            this.style.height = `${this.parentElement?.scrollWidth}px`;
            this.style.display = 'block';
            if (!firstTime) {
                const box = this.getBoundingClientRect();
                chart.resize({
                    height: box.height,
                    width: box.width
                });
            }
        };
        sizeChart(true);

        // setup chart
        // @ts-ignore (echarts global)
        let chart = echarts.init(this, null, {renderer: 'svg'});
        const options = {
            color: [
                '#12436D',
                '#28A197',
                '#801650',
                '#F46A25',
                '#3D3D3D',
                '#A285D1'
            ],
            tooltip: {
                formatter: '{b} ({c}%)',
                trigger: 'item'
            },
            grid: {
                left: 0,
                top: 0,
                right: 0,
                bottom: 0
            },
            series: [
                {
                    type: 'pie',
                    radius: ['40%', '90%'],
                    itemStyle: {
                        borderColor: '#fff',
                        borderWidth: 1
                    },
                    data: data,
                    label: {
                        align: 'left',
                        color: '#fff',
                        fontSize: 14,
                        fontWeight: 'bold',
                        formatter: [
                            //'{b}',
                            //'\n{percent|{c}%}'
                            '{c}%'
                        ].join('\n'),
                        lineHeight: 14,
                        position: 'inside',
                        width: 70,
                        overflow: 'break',
                        rich: {
                            percent: {
                                lineHeight: 18,
                                fontWeight: 'normal'
                            }
                        }
                    }
                }
            ]
        };
        chart.setOption(options);
        window.addEventListener('resize', () => {
            sizeChart(false);
        });

    }
}
customElements.define('donut-chart', DonutChart);



class BarAnimation extends HTMLElement {
    connectedCallback () {

        // check user hasn't requested reduced motion
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            return;
        }

        const bar = this.querySelector('span');
        if (!bar) {
            return;
        }
        const originalWidth = bar.style.width;
        bar.style.width = '0%';
        window.setTimeout(() => {
            bar.classList.add('animate');
            bar.style.width = originalWidth;
        }, 1);

    }
}
customElements.define('bar-animation', BarAnimation);



// scatter chart
class ScatterChart extends HTMLElement {
    connectedCallback() {

        // @ts-ignore (echarts global)
        let chart = echarts.init(this, null, {renderer: 'svg'});

        /**
         * Size the chart and chart container
         */
        const sizeChart = () => {
            this.style.display = 'none';
            const parentWidth = this.parentElement?.scrollWidth || 1;
            this.style.width = `${parentWidth}px`;
            this.style.height = `${parentWidth * 0.5}px`;
            this.style.display = 'block';
            const box = this.getBoundingClientRect();
            chart.resize({
                height: box.height,
                width: box.width
            });
        };
        sizeChart();
        window.addEventListener('resize', sizeChart);

        const data = [
            [10.0, 8.04, -1, "Test item"],
            [8.07, 6.95, -1, "Test item"],
            [13.0, 7.58, 0, "Test item"],
            [9.05, 8.81, 0, "Test item"],
            [11.0, 8.33, 0, "Test item"],
            [14.0, 7.66, 0, "Test item"],
            [13.4, 6.81, 0, "Test item"],
            [10.0, 6.33, 0, "Test item"],
            [14.0, 8.96, 1, "Test item"],
            [12.5, 6.82, 1, "Test item"],
            [9.15, 7.2, 1, "Test item"],
            [11.5, 7.2, 1, "Test item"],
            [3.03, 4.23, 2, "Test item"],
            [12.2, 7.83, 2, "Test item"],
            [2.02, 4.47, 2, "Test item"],
            [1.05, 3.33, 3, "Test item"],
            [4.05, 4.96, 3, "Test item"],
            [6.03, 7.24, 3, "Test item"],
            [12.0, 6.26, 3, "Test item"],
            [12.0, 8.84, 4, "Test item"],
            [7.08, 5.82, 4, "Test item"],
            [5.02, 5.68, 4, "Test item"]
        ];

        const options = {
            xAxis: {},
            yAxis: {},
            series: [
              {
                symbolSize: 10, // size of the dots
                data: data,
                type: 'scatter',
                encode: {
                    tooltip: [0, 1, 2],
                    itemName: 2 // Use Topic ID as item name
                }
              }
            ],
            tooltip: {
                trigger: 'item',
                formatter: function (params) {
                    return `
                        X: ${params.value[0]}<br/>
                        Y: ${params.value[1]}<br/>
                        Topic ID: ${params.value[2]}</br/>
                        Info: ${params.value[3]}<br/>
                        Anything you like can be shown here
                    `;
                }
            },
            visualMap: {
                show: false,
                dimension: 2,
                categories: [-1, 0, 1, 2, 3, 4],
                inRange: {
                    color: ['#60697b', '#C50878', '#0B8478', '#924FB2', '#124581', '#0879C4']
                }
            },
            grid: {
                left: '20px',
                right: '20px',
                top: '10px',
                bottom: '20px'
            }
          };
          chart.setOption(options);

    }
}
customElements.define('scatter-chart', ScatterChart);