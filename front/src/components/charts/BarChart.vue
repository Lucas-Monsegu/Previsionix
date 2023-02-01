<script>
import { Bar } from 'vue-chartjs'

export default {
    extends: Bar,
    props: {
        cdata: {
            type: Object,
            required: true
        },
        options: {
            type: Object,
            default: null
        }
    },
    data () {
        return {
            gradient: null,
            datacollection: {
                labels: this.cdata.labels,
                datasets: this.cdata.datasets
            },
            myoptions: {
                scales: {
                    xAxes: [{ stacked: true }],
                    yAxes: [{ stacked: true }]
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
        // this.chartData is created in the mixin.
        // If you want to pass options please create a local options object
        this.renderChart(this.datacollection, this.options)
    }
}
</script>
