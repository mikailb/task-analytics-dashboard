/**
 * charts.js - Felles funksjonalitet for diagrammer i Task Analytics Dashboard
 */

// Globale konfigurasjoner for Plotly diagrammer
const DEFAULT_PLOTLY_CONFIG = {
    responsive: true,
    displayModeBar: false,
    locale: 'no'
};

// Fargepalett for diagrammer
const CHART_COLORS = {
    primary: 'rgb(49, 130, 189)',
    secondary: 'rgb(204, 204, 0)',
    success: 'rgb(75, 192, 92)',
    danger: 'rgb(255, 99, 132)',
    warning: 'rgb(255, 159, 64)',
    info: 'rgb(54, 162, 235)',
    dark: 'rgb(55, 83, 109)'
};

// Hjelpefunksjon for å formatere datoer
function formatDate(dateStr) {
    if (!dateStr) return '-';
    const date = new Date(dateStr);
    return date.toLocaleDateString('no-NO');
}

// Hjelpefunksjon for å beregne forskjell mellom datoer i dager
function daysBetween(date1, date2) {
    const d1 = new Date(date1);
    const d2 = new Date(date2);
    const diffTime = Math.abs(d2 - d1);
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
}

// Hjelpefunksjon for å gruppere data etter en nøkkel
function groupBy(array, key) {
    return array.reduce((result, item) => {
        (result[item[key]] = result[item[key]] || []).push(item);
        return result;
    }, {});
}

// Hjelpefunksjon for å kalkulere gjennomsnitt av en egenskap i et array
function average(array, prop) {
    if (array.length === 0) return 0;
    const sum = array.reduce((total, item) => {
        return total + (prop ? item[prop] || 0 : item || 0);
    }, 0);
    return sum / array.length;
}

// Metode for å resette og tegne et diagram på nytt ved vindusstørrelseendring
function resizeChart(chartId, dataFn, layoutFn, configOverride = {}) {
    const el = document.getElementById(chartId);
    if (!el) return;
    
    Plotly.purge(el);
    Plotly.newPlot(
        chartId, 
        dataFn(), 
        layoutFn(), 
        {...DEFAULT_PLOTLY_CONFIG, ...configOverride}
    );
}

// Metode for å oppdatere responsivt diagram ved vindusstørrelseendring
window.addEventListener('resize', function() {
    const chartElements = document.querySelectorAll('div[id$="-chart"]');
    chartElements.forEach(el => {
        if (el._fullLayout) {
            Plotly.relayout(el.id, {
                'xaxis.autorange': true,
                'yaxis.autorange': true
            });
        }
    });
});

// Hjelpefunksjon for å eksportere diagrammer som bilder
function exportChartAsImage(chartId, filename) {
    const el = document.getElementById(chartId);
    if (!el) return;
    
    Plotly.downloadImage(el, {
        format: 'png',
        width: 800,
        height: 450,
        filename: filename || 'chart-export'
    });
}

// Fargefunksjoner for tilpassede diagrammer
function getStatusColor(status) {
    switch(status) {
        case 'Fullført':
            return CHART_COLORS.success;
        case 'Pågående':
            return CHART_COLORS.info;
        case 'Ikke påbegynt':
            return CHART_COLORS.secondary;
        default:
            return CHART_COLORS.dark;
    }
}

function getPriorityColor(priority) {
    switch(priority) {
        case 'Høy':
            return CHART_COLORS.danger;
        case 'Medium':
            return CHART_COLORS.warning;
        case 'Lav':
            return CHART_COLORS.info;
        default:
            return CHART_COLORS.dark;
    }
}

// Eksporter til globalt omfang for å være tilgjengelig i HTML
window.chartUtils = {
    formatDate,
    daysBetween,
    groupBy,
    average,
    resizeChart,
    exportChartAsImage,
    getStatusColor,
    getPriorityColor,
    CHART_COLORS
};