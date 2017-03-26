
// var topIds=["homeTag","squareTag","momentsTag","createTalk","logoutTag","loginTag","registerTag"]

// function TopActive(obj){
// 	var elems;
// 	console.log("hehe");
// 	// selector = '.nav-sidebar > li';
// 	elems = document.getElementById("navbarTop").getElementsByTagName("li");
// 	for (var i = 0; i < elems.length; i++)
// 	    	elems[i].setAttribute("class","");
//     obj.setAttribute("class",'active');
// }

function login() {

	// document.getElementById("loginTag").className="active";
	
	var userId=parseInt(document.getElementById("userId").value);
	var password=document.getElementById("password").value;
	// Sending and receiving data in JSON format using POST mothod
	//
	var xhr = new XMLHttpRequest();
	var url ="http://192.168.1.220:5000/api/v1/login";
	// "http://localhost:5000/api/v1/login";
	xhr.open("POST", url, true);
	xhr.setRequestHeader("Content-type", "application/json");
	xhr.onreadystatechange = function () { 
	    if (xhr.readyState == 4 && xhr.status == 200) {
	        var json = JSON.parse(xhr.responseText);
	        console.log(json)
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
	
	// document.getElementById("registerTag").className="active";
	
	var email=document.getElementById("email").value+'';
	var password=document.getElementById("password").value+'';
	// Sending and receiving data in JSON format using POST mothod
	//
	var xhr = new XMLHttpRequest();
	var url ="http://192.168.1.220:5000/api/v1/register"; 
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

// function Play(audioName){
// 	alert("playing audio, the name is: "+audioName);

// }

// function Response(audioName){
// 	alert("Recording audio response to: "+audioName);

// }

function ShowTalk(talkString){
	var elems, currentElement;
	var talk=JSON.parse(talkString);
	// selector = '.nav-sidebar > li';

	elems = document.getElementById("talksSelect").getElementsByTagName("li");
	for (var i = 0; i < elems.length; i++)
			// console.log(elems[i]);
	    	// console.log(elems.length);
	    	elems[i].setAttribute("class","")
	        // elems[i].classList.remove('active');
	// console.log(this);
	currentElement=document.getElementById('talk'+talk['talkId'])
    currentElement.setAttribute("class",'active');
	
	// document.getElementById(talkId).className="active";
	// var html='{%for audio in talk[talkId][\'audios\']%}<tr>'+'<td><button onclick="Play({{audio[\'audioName\']}})">{{audio[\'audioName\']}}</button></td>'+'<td>{{audio[\'tags\']}}</td>'+'<td><button onclick="Response({{audio[\'audioName\']}})">Response</button></td>'+'</tr>{% endfor %}';
	



	html='';
	for(audio in talk['audios']){
		html=html+'<tr><td><input onclick="PlayAudio('+"'"+audio+"'"+')" type="button" value="'+audio+'" /></td><td>'+talk['audios'][audio]['tags']+'</td><td><input onmousedown="StartRecording()" onmouseup="UploadAudio('+"'"+audio+"'"+')" type="button" value="Response"/></td></tr>\n';
	}
	document.getElementById('audioTable').innerHTML=html;
	document.getElementById('talkTitle').innerHTML=talk['title'];
	document.getElementById('talkTags').innerHTML=talk['tags'];
	document.getElementById('talkDescription').innerHTML=talk['description'];


}
function CreateNewTalk(){
		var title=document.getElementById("title").value+'';
		var tags=[document.getElementById("tags").value+''];
		var description=document.getElementById("description").value+'';

		var xhr = new XMLHttpRequest();
		var url ="http://192.168.1.220:5000/api/v1/talk"; 
		// "http://localhost:5000/api/v1/talk";
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
		xhr.send(JSON.stringify({"title":title, "description":description,"tags":tags}));			  
 
}

        // <input onmousedown="startRecording()" onmouseup="uploadAudio()" type="button" value="response" />
        // <input onclick="stopRecording()" type="button" value="停止" />
        // <input onclick="playRecording()" type="button" value="play" />
        // <!-- <input onclick="uploadAudio()" type="button" value="提交" /> -->
 
//                 {%for audio in talk[talkId]['audios']%}
//                   <tr>
//                   <td><button onclick="Play({{audio['audioName']}})">{{audio['audioName']}}</button></td>
//                   <td>{{audio['tags']}}</td>
//                   <td><button onclick="Response({{audio['audioName']}})">Response</button></td>
//                   </tr>
//                 {% endfor %}