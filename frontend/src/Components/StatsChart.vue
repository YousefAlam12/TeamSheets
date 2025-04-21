<template>
    <canvas class="p-3" id="statsRadarChart"></canvas>
</template>


<script>
import Chart from 'chart.js/auto'

export default {
    props: {
        stats: {
            required: true
        }
    },
    data() {
        return {
        }
    },
    // displays graph of users stats
    async mounted() {
        const ctx = document.getElementById('statsRadarChart')
        new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['Attack', 'Defence', 'Strength', 'Speed', 'Technique'],
                datasets: [{
                    label: 'Rating',
                    data: [
                        this.stats.attack,
                        this.stats.defence,
                        this.stats.strength,
                        this.stats.speed,
                        this.stats.technique,
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                elements: {
                    line: {
                        borderWidth: 3
                    }
                },
                scales: {
                    r: {
                        min: 0,
                        max: 10,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        })
    },
    methods: {

    }
}
</script>