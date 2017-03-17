function login() {

	document.getElementById("loginTag").className="active";
	
	var userId=parseInt(document.getElementById("userId").value);
	var password=document.getElementById("password").value;
	// Sending and receiving data in JSON format using POST mothod
	//
	xhr = new XMLHttpRequest();
	var url = {{ url_for('loadLoginPage') }};
	// "http://localhost:5000/api/v1/login";
	xhr.open("POST", url, true);
	xhr.setRequestHeader("Content-type", "application/json");
	xhr.onreadystatechange = function () { 
	    if (xhr.readyState == 4 && xhr.status == 200) {
	        var json = JSON.parse(xhr.responseText);
	        if (json.hasOwnProperty("status")) {
	        	alert(json["status"]);
	        }
	        else{
	        	alert("login success!");
	        }
	        // document.getElementById("statusimage").src=json['status']+".gif"
	        // document.getElementById("speed").innerHTML="Current moving speed: "+json['speed']+"mile/h"
	        
	    }
	}
	xhr.send(JSON.stringify({"userId":userId, "password":password}));			  
	
}

function Register(){
	
	document.getElementById("registerTag").className="active";
	
	var email=document.getElementById("email").value;
	var password=document.getElementById("password").value;
	// Sending and receiving data in JSON format using POST mothod
	//
	xhr = new XMLHttpRequest();
	var url ={{ url_for('loadRegisterPage') }}; 
	// "http://localhost:5000/api/v1/register";
	xhr.open("PUT", url, true);
	xhr.setRequestHeader("Content-type", "application/json");
	xhr.onreadystatechange = function () { 
	    if (xhr.readyState == 4 && xhr.status == 200) {
	        var json = JSON.parse(xhr.responseText);
	        alert("please remember your id: "+json['userId']);
	        // document.getElementById("statusimage").src=json['status']+".gif"
	        // document.getElementById("speed").innerHTML="Current moving speed: "+json['speed']+"mile/h"
	        
	    }
	}
	xhr.send(JSON.stringify({"email":email, "password":password}));			  

}

function Play(audioName){
	alert("playing audio, the name is: "+audioName);

}

function Response(audioName){
	alert("Recording audio response to: "+audioName);

}

function ShowTalk(talkId){
	document.getElementById(talkId).className="active";
	var html='{%for audio in talk[talkId][\'audios\']%}<tr>'+'<td><button onclick="Play({{audio[\'audioName\']}})">{{audio[\'audioName\']}}</button></td>'+'<td>{{audio[\'tags\']}}</td>'+'<td><button onclick="Response({{audio[\'audioName\']}})">Response</button></td>'+'</tr>{% endfor %}';
	document.getElementById('audioTable').innerHTML=html;

}
function CreateNewTalk(){
		xhr = new XMLHttpRequest();
		var url ={{ url_for('createNewTalk') }}; 
		// "http://localhost:5000/api/v1/register";
		xhr.open("PUT", url, true);
		xhr.setRequestHeader("Content-type", "application/json");
		xhr.onreadystatechange = function () { 
		    if (xhr.readyState == 4 && xhr.status == 200) {
		        var json = JSON.parse(xhr.responseText);
		        alert("please remember talk id: "+json['talkId']);
		        // document.getElementById("statusimage").src=json['status']+".gif"
		        // document.getElementById("speed").innerHTML="Current moving speed: "+json['speed']+"mile/h"
		        
		    }
		}
		xhr.send(JSON.stringify({"title":"first talk!!", "description":"heheda this is the first talk for test","tags":["hehe","haha"]}));			  
 
}


//                 {%for audio in talk[talkId]['audios']%}
//                   <tr>
//                   <td><button onclick="Play({{audio['audioName']}})">{{audio['audioName']}}</button></td>
//                   <td>{{audio['tags']}}</td>
//                   <td><button onclick="Response({{audio['audioName']}})">Response</button></td>
//                   </tr>
//                 {% endfor %}