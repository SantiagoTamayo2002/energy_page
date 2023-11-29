// Función genérica para inicializar gráficos
const initChart = async (chartId, fetchDataFunction) => {
    try {
        const myChart = echarts.init(document.getElementById(chartId));
        const data = await fetchDataFunction();

        if (!data) {
            console.error(`No se recibieron datos para el gráfico ${chartId}`);
            return;
        }
        myChart.setOption(data);
        myChart.resize();
    } catch (error) {
        console.error(`Error al inicializar el gráfico ${chartId}:`, error);
    }
};

const graficoConsumoActual = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/paginaUsuario/proyecciones/graficoConsumoActual');
        const data = await response.json();
        console.log(data);  // Añade esto para depurar
        return data;
    } catch (ex) {
        alert(ex);
    }
};
const graficoProyeccionSemanal = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/paginaUsuario/proyecciones/graficoProyeccionSemanal');
        const data = await response.json();
        console.log(data);  // Añade esto para depurar
        return data;
    } catch (ex) {
        alert(ex);
    }
}
const graficoProyeccionMensual = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/paginaUsuario/proyecciones/graficoProyeccionMensual');
        const data = await response.json();
        console.log(data);  // Añade esto para depurar
        return data;
    } catch (ex) {
        alert(ex);
    }
}
const graficoArtefactoMasUsado = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/paginaUsuario/proyecciones/graficoArtefactoMasUsado');
        const data = await response.json();
        console.log(data);  // Añade esto para depurar
        return data;
    } catch (ex) {
        alert(ex);
    }
}
// Inicializar gráficas al cargar la página en el navegador
window.addEventListener('load', async () => {
    await initChart('graficoConsumoActual', graficoConsumoActual);
    await initChart('graficoProyeccionSemanal', graficoProyeccionSemanal);
    await initChart('graficoProyeccionMensual', graficoProyeccionMensual);
    await initChart('graficoArtefactoMasUsado', graficoArtefactoMasUsado);
});
