$(document).ready(function () {
$("#usa").on('plotly_click', function(data){
console.log(data)

var fip =data.handleObj.handler.arguments[1].points[0].location

console.log(typeof (fip))
    console.log(fip)
    $.ajax({
      fip: fip,
      dataType: "JSON",
      type: 'POST',
      url:'charts',
    })

      .done(function () {
                  // location.replace('/charts')
      }).fail(function(xhr, text, error) {
    // console.log(text, error)
})
  })
})