const TaiwanMap = new Vue({
  el: '#app',
  data: {
    city: "尚無圖片"
  },
  methods: {
    async getTaiwanMap() {
      const width = (this.$refs.map.offsetWidth).toFixed(),
          height = Number((this.$refs.map.offsetHeight).toFixed())+Number(135);

      // const width = 700,
        // height = 750;

      // 判斷螢幕寬度，給不同放大值
      let mercatorScale, w = window.screen.width;
      if(w > 1366) {
        mercatorScale = 11000;
      }
      else if(w <= 1366 && w > 480) {
        mercatorScale = 9000;
      }
      else {
        mercatorScale = 6000;
      }

      // d3：svg path 產生器
      var path = await d3.geo.path().projection(
        // !important 座標變換函式
        d3.geo
          .mercator()
          .center([121,24])
          .scale(mercatorScale)
          .translate([width/2, height/2.5])
      );
      
      // 讓d3抓svg，並寫入寬高
      var svg = await d3.select('#svg')
          .attr('width', width)
          .attr('height', height)
          .attr('viewBox', `0 0 ${width} ${height}`);

      // 讓d3抓GeoJSON檔，並寫入path的路徑
      var url = 'static/src/taiwan.geojson';
      var myModal = new bootstrap.Modal(document.getElementById('modal'), {
        keyboard: false
      })
      await d3.json(url, (error, geometry) => {
        if (error) throw error;

        svg
          .selectAll('path')
          .data(geometry.features)
          .enter().append('path')
          .attr('d', path)
          .attr({
            // 設定id，為了click時加class用
            id: (d) => 'city' + d.properties.COUNTYCODE
          })
          .on('click', d => {
            myModal.show()
            document.getElementById('modalLabel').innerHTML = d.properties.COUNTYNAME;
            cityName = d.properties.COUNTYNAME;
            // console.log(cityName)

            // var Obj = document.getElementById('modal-body')
            var str = document.getElementById('no-img').innerHTML
            var num = parseInt(document.getElementById('num').innerHTML)+1
            var tag = 0
            // console.log(num)
            // var str = document.getElementById('img').innerHTML
            for (i = 1; i < num; i++) {
              // console.log(document.getElementById('name'+step).innerHTML)
              if(document.getElementById('name'+i).innerHTML == cityName){
                if(tag != 0){
                  str = str + document.getElementById('img'+i).innerHTML
                }
                else{
                  str = document.getElementById('img'+i).innerHTML
                }
                tag++
              }
            }
            
            document.getElementById('modal-body').innerHTML = str


          });
      });
      return svg;
    },
  },
  mounted() {

    this.getTaiwanMap();

  }
})