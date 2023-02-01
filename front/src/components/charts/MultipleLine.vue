<script>
import { Line } from 'vue-chartjs'

export default {
    extends: Line,
    props: {
        cdata: {
            type: Object,
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
                            beginAtZero: true
                        },
                        gridLines: {
                            display: true
                        },
                        scaleLabel: {
                            display: true
                        }
                    }],
                    xAxes: [{
                        maxBarThickness: 100,
                        gridLines: {
                            display: true
                        },
                        scaleLabel: {
                            display: true
                        }
                    }]
                },
                elements: {
                    point: {
                        radius: 3
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
                this.renderChart(this.datacollection, this.options)
            }
        },

        deep: true
    },
    mounted () {
        this.renderChart(this.datacollection, this.options)
    }
}
</script>
