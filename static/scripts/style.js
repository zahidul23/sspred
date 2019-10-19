//Takes element id and prediction string and color codes the element
function colorCode(id, pred)
{	
	ele = document.getElementById(id);
	
	result = "";
	
	for(i = 0; i < pred.length; i++)
	{
		result += "<span style='color:" + getColor(pred.charAt(i)) + "';>" + pred.charAt(i) + "</span>";
	}
	
	ele.innerHTML = result;
}

//Takes a character and returns a color
function getColor(character)
{
	if (character == 'H')
		return "blue";
	else if (character == 'E')
		return "green";
	else if (character == 'C')
		return "red";
	
	return "black";
}