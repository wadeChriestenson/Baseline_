$(document).ready(function () {
    // console.log($('#usa'))
    $("#fipsForm").hide()
$("#usa").on('plotly_click', function(data){
console.log(data)
    var location = data.handleObj.handler.arguments[1].points[0].hovertext
var fip =data.handleObj.handler.arguments[1].points[0].location
    $("#location").val(location)
$('#fipsInput').val(fip)
    console.log(typeof (location))
    console.log(location)
console.log(typeof (fip))
    console.log(fip)
    $('#submit').click()

//     $.ajax({
//       fip: fip,
//       dataType: "JSON",
//       type: 'POST',
//       url:'charts',
//     })
//
//       .done(function () {
//                   // location.replace('/charts')
//       }).fail(function(xhr, text, error) {
//     // console.log(text, error)
// })
  })
})