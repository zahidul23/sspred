//Manages sending and receiving data
$(document).ready(function() {
	var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function() {
        socket.emit('connected');
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
	
	$('#submitbtn').on('click', function() {
		socket.emit('sendSeq',{
			'data': $('#seqtext').val(),
			'targets':targets
		});
		$('#seq').text($('#seqtext').val());
		console.log('Button Clicked!!!!!');
		$('#submitbtn').attr('disabled','disabled');
		$('#clearbtn').attr('disabled','disabled');	
	});
	
	$('#clearbtn').on('click', function() {
		$('#seqtext').val("")
	});
	
	/*
		Array containing which sites to send to.
		0-Jpred 1-Psipred 2-Psspred	3-Raptorx 4-Sable 5-Yaspin 6-SSPro
	*/
	var targets = new Array(7);
	targets.fill(true, 0, 7);
	
	$('#0checkbox').change(function() {toggleSite(0);});
	$('#1checkbox').change(function() {toggleSite(1);});
	$('#2checkbox').change(function() {toggleSite(2);});
	$('#3checkbox').change(function() {toggleSite(3);});
	$('#4checkbox').change(function() {toggleSite(4);});
	$('#5checkbox').change(function() {toggleSite(5);});
	$('#6checkbox').change(function() {toggleSite(6);});
	function toggleSite(num){targets[num] = !targets[num];}
});
/*
var targets = new Array(7);
	targets.fill(true, 0, 7);
	for(i = 0; i < targets.length; i++)
	{
		$('#icheckbox').on('change',toggleSite(i));
	}

	$('#0checkbox').change(toggleSite(0));
	$('#1checkbox').change(toggleSite(1));
	$('#2checkbox').change(toggleSite(2));
	$('#3checkbox').change(toggleSite(3));
	$('#4checkbox').change(toggleSite(4));
	$('#5checkbox').change(toggleSite(5));
	$('#6checkbox').change(toggleSite(6));

	function toggleSite(num)
	{
		return function() {
			console.log("fr+" + targets[num]);
			targets[num] = !targets[num];
			console.log("fr+11124344" + targets[num]);
		}
	}
*/