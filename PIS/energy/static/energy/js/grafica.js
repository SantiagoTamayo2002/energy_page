const obtenerOpcionGrafico = async() => {
    try {
        const response = await fetch('http://127.0.0.1:8000/paginaUsuario/proyecciones/grafico');
        return await response.json();
    }catch (ex) {
        alert(ex);
    }
};

const initGrafica = async() => {
  const myChart = echarts.init(document.getElementById('grafica'));
  // let base = +new Date(1988, 9, 3);
  // let oneDay = 24 * 3600 * 1000;
  // let data = [[base, Math.random() * 300]];
  // for (let i = 1; i < 20000; i++) {
  //   let now = new Date((base += oneDay));
  //   data.push([+now, Math.round((Math.random() - 0.5) * 20 + data[i - 1][1])]);
  // }
  //   option = {
  //     tooltip: {
  //       trigger: 'axis',
  //       position: function (pt) {
  //         return [pt[0], '10%'];
  //       }
  //     },
  //     title: {
  //       left: 'center',
  //       text: 'Large Ara Chart'
  //     },
  //     toolbox: {
  //       feature: {
  //         dataZoom: {
  //           yAxisIndex: 'none'
  //         },
  //         restore: {},
  //         saveAsImage: {}
  //       }
  //     },
  //     xAxis: {
  //       type: 'time',
  //       boundaryGap: false
  //     },
  //     yAxis: {
  //       type: 'value',
  //       boundaryGap: [0, '100%']
  //     },
  //     dataZoom: [
  //       {
  //         type: 'inside',
  //         start: 0,
  //         end: 20
  //       },
  //       {
  //         start: 0,
  //         end: 20
  //       }
  //     ],
  //     series: [
  //       {
  //         name: 'Fake Data',
  //         type: 'line',
  //         smooth: true,
  //         symbol: 'none',
  //         areaStyle: {},
  //         data: data
  //       }
  //     ]
  //   };
  myChart.setOption(await obtenerOpcionGrafico());
  myChart.resize();
};
window.addEventListener('load', async () => {
    await initGrafica();
});