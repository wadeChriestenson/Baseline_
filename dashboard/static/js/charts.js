$(document).ready(function () {
$("#back_btn").click( function(data){
    location.replace('/index')
console.log(data)
    $.ajax({
      // fip: fip,
      // dataType: "JSON",
      type: 'POST',
      url:'index',
    })
      .done(function () {
          // location.replace('/index')
      }).fail(function(xhr, text, error) {
    console.log(text, error)
})
  })
})