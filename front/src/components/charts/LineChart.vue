<script>
import { Line } from 'vue-chartjs'

export default {
    extends: Line,
    props: {
        cdata: {
            type: Object,
            required: true
        },
        yLabel: {
            type: String,
            required: true
        },
        xLabel: {
            type: String,
            required: true
        }
    },
    data () {
        return {
            gradient: null,
            datacollection: {
                labels: this.cdata.labels,
                datasets: this.cdata.datasets
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true,
                            suggestedMax: 30

                        },
                        gridLines: {
                            display: true
                        },
                        scaleLabel: {
                            display: true,
                            labelString: this.yLabel
                        }
                    }],
                    xAxes: [{
                        maxBarThickness: 100,
                        gridLines: {
                            display: true
                        },
                        scaleLabel: {
                            display: true,
                            labelString: this.xLabel
                        }
                    }]
                },
                elements: {
                    point: {
                        radius: 2
                    }
                },
                legend: {
                    display: true
                },
                responsive: true,
                maintainAspectRatio: false
            }
        }
    },
    watch: {
        cdata: {
            handler: function (val) {
                this.datacollection = val
                for (let i = 0; i < this.datacollection.datasets.length; ++i) {
                    this.datacollection.datasets[i]['backgroundColor'] = this.gradient
                }
                this.renderChart(this.datacollection, this.options)
            }
        },
        deep: true
    },
    mounted () {
        this.gradient = this.$refs.canvas.getContext('2d').createLinearGradient(0, 0, 0, 400)
        this.gradient.addColorStop(0, 'rgba(255, 160,0, 0.2)')
        this.gradient.addColorStop(1, 'rgba(255, 160,0, 0.0)')

        this.renderChart(this.datacollection, this.options)
    }
}
</script>
