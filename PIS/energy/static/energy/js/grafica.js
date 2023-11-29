const graficoConsumoDiario = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/paginaUsuario/proyecciones/graficoConsumoDiario');
        return await response.json();
    } catch (ex) {
        alert(ex);
    }
};

const proyeccion = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/paginaUsuario/proyecciones/graficoProyeccion');
        return await response.json();
    } catch (ex) {
        alert(ex);
    }
}
const graficaArtefactoMasUsado = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/paginaUsuario/proyecciones/gArtefactoMasUsado');
        return await response.json();
    } catch (ex) {
        alert(ex);
    }
}
const initGraficaConsumoDiario = async () => {
    const myChart = echarts.init(document.getElementById('graficaConsumoDiario'));
    myChart.setOption(await graficoConsumoDiario());
    myChart.resize();
};

const initGraficaProyeccion = async () => {
    const myChart = echarts.init(document.getElementById('graficaProyeccion'));
    myChart.setOption(await proyeccion());
    myChart.resize();
};
const initGraficaArtefactoMasUsado = async () => {
    const myChart = echarts.init(document.getElementById('gArtefactoMasUsado'));
    myChart.setOption(await graficaArtefactoMasUsado());
    myChart.resize();
}

window.addEventListener('load', async () => {
    await initGraficaConsumoDiario();
    await initGraficaProyeccion();
    await initGraficaArtefactoMasUsado();
});
