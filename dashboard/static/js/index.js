$(document).ready(function () {
$("#usa").on('plotly_click', function(data){
// console.log(data)

var fip = data.handleObj.handler.arguments[1].points[0].location
console.log(fip)
    $("#back").show()
    var info = {
    fips: fip
    }

    $.ajax({
      data: info,
      dataType: "json",
      type: 'POST',
      url:'/graph',

    })
      .done(function (data) {
        // console.log(info)
        // $("#outer").show()
        //  console.log(data)
        // let pop_line = data[0]
        //   let snap = data[1]
        // let bd = data[2]
        // let bankL = data[3]
        // let county_map = data[4]
        // let hhi = data[5]
        //
        // // console.log(pop)
        // $("#pop").on(Plotly.newPlot('pop', pop_line, pop_line.layout))
        // $("#snap").on(Plotly.newPlot('snap', snap, snap.layout))
        // $("#bd").on(Plotly.newPlot('bd', bd, bd.layout))
        // $("#bankL").on(Plotly.newPlot('bankL', bankL, bankL.layout))
        // $("#county").on(Plotly.newPlot('county', county_map, county_map.layout))
        // $("#hhi").on(Plotly.newPlot('hhi', hhi, hhi.layout))
      })
  })
    $('#back').click( function () {
        location.reload();
    })
})