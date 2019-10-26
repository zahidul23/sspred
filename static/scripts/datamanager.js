//Gets sent data and displays it
		
$(document).ready(function() {

	var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function() {
        socket.emit('beginProcess', post_data); //post_data contained in sent.html
    });
	
	socket.on('seqString', function(msg)
	{
		parse = JSON.parse(msg);
		$('#seq').text(parse.seq);
		if(parse.email != "")
			$('#emaildiv').text("Results will also be sent to " + parse.email);
	});
	
	var j;
	
	socket.on('result', function(msg) {
		j = JSON.parse(msg);
		$('#' + j.pID).text(j.pred);
		$('#' + j.cID).text(j.conf);
		console.log(msg);
		
		if(j != null)
			colorCode(j.pID, j.pred);
	});
	
	socket.on('resulturl', function(msg) {
		$('#resulturl').text("Results");
		$('#resulturl').attr('href','http://'+ document.domain + ':' + location.port + '/output/'+msg);
		$('#resulturl').attr('target','_blank');
		console.log(msg);
		if(j != null)
			colorCode(j.pID, j.pred);
	});
});