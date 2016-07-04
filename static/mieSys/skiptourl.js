
$(document).ready(function() {
toflask();
})


function toflask(){
	$(".inventory_class").click( function(){
		//alert($(this).children("src").attr("id"));
		img_id = $(this).children('img').attr("id")
		url = "/click/" + img_id
		phase = 'OK!'
		alert(phase)
		window.location.href = url
	})
}