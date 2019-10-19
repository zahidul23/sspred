//Gets sent data and displays it
		
$(document).ready(function() {

	var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function() {
		console.log("sent results");
        socket.emit('beginProcess');
    });
	
	socket.on('seqString', function(msg)
	{
		$('#seq').text(JSON.parse(msg).seq);
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