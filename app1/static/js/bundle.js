(()=>{"use strict";function e(e,...t){var n="";const o=[];for(let i=0;i<e.length-1;i++){let a=t[i];switch(n+=e[i],typeof a){case"number":case"string":n+=`<wbr i${o.push([a,"text"])}>`;break;case"function":n+=`i${o.push([a,"function"])}`;break;default:a instanceof Element||3==a?.nodeType?n+=`<wbr i${o.push([a,"element"])}>`:Array.isArray(a)?n+=`<wbr i${o.push([a,"array"])}>`:n+=`i${o.push([a,"props"])}`}}const i=document.createElement("div");i.innerHTML=n+e.at(-1);for(let e=0;e<o.length;e++){let t=i.querySelector(`[i${e+1}]`);const n=o[e][0];switch(o[e][1]){case"function":n(t);break;case"element":case"text":t.replaceWith(n);break;case"array":for(const e of n)t.before(e);t.remove();break;case"props":for(let e in n)t[e]=n[e]}}const a=i.firstElementChild||i.firstChild;return a.remove(),a}class t{constructor(e=document.createTextNode("...")){this.current=e}put(e){let t=typeof e;"string"!=t&&"number"!=t||(e=document.createTextNode(e)),this.current.replaceWith(e),this.current=e}}let n=null;const o=e`
	<div class="header centered row">
		<img src="https://raw.githubusercontent.com/elcinbayramoff/imagess/main/logo.png" alt="Pasha Insurance">
		<h4 class="text">Pasha Insurance</h4>
		<img class="snap-right menuIcon" ${{onclick:function(t){n?.remove(),n=e`
			<div class="profile">
				<button class="closeButton" ${{onclick:e=>n.remove()}}>X</button>
				<div class="profileContent">
				<div class="col">
				<div class="row"><div class="profinf">Ad:</div> <b>${window.profileData.name}</b></div>
				<div class="row"><div class="profinf">Soyad:</div> <b>${window.profileData.surname}</b></div>
				<div class="row"><div class="profinf">Ata adı:</div> <b>${window.profileData.patrical_name}</b></div>
				<div class="row"><div class="profinf">FİN:</div> <b>${window.profileData.fin_code}</b></div>
					<br>
					<br>
					<div class="box">
						<a href="/login" class="signout">Çıxış et</a>
					</div>
				</div>
				</div>
			</div>`,b.appendChild(n)}}} src="https://raw.githubusercontent.com/elcinbayramoff/imagess/main/menu.png" alt="">
	</div>
`;let i;const a=["Allergist/immunologist","Anesthesiologist","Cardiologist","Dermatologist","Endocrinologist","Family physician","Gastroenterologist","Geneticist","Hematologist","Hospice and palliative medicine specialist","Immunologist","Infectious disease physician","Internal Medicine","Nephrologist","Neurologist","Obstetrician/gynecologist (OBGYNs)","Oncologist","Ophthalmologist","Orthopedist","Otolaryngologist","Osteopath","Pathologist","Pediatrician","Physician executive","Plastic surgeon","Podiatrist","Psychiatrist","Pulmonologist","Radiologist","Rheumatologist ","Sleep medicine specialist ","Surgeon","Urologist"];let s;setTimeout((()=>g.put(f)));const c=e`<div></div>`;c.appendChild(e`<div>






	
Hello! I am your virtual asistant, please, tell me about your symptoms.







	</div>
`);let l=new t;function r(){const e=document.cookie.split(";").find((e=>e.trim().startsWith("csrftoken=")));return e?e.split("=")[1]:null}function u(t){function n(){const e=document.cookie.split(";").find((e=>e.trim().startsWith("csrftoken=")));return e?e.split("=")[1]:null}l.put(e`Ambulans çağırılır`);const o={method:"POST",headers:{"Content-Type":"application/json","X-CSRFToken":n()},body:JSON.stringify({})};let i,a=null;fetch("/call-ambulance/",o).then((e=>e.json())).then((t=>{i=t.fin_code,console.log(i),a=setInterval((()=>{fetch("/check-sent/",{method:"POST",headers:{"Content-Type":"application/json","X-CSRFToken":n()},body:JSON.stringify({fin_code:i})}).then((e=>e.json())).then((t=>{t.sent||(clearInterval(a),l.put(e`Ambulans göndərildi`)),console.log(t.sent)}))}),1e3)})),b.classList.add("callingAmbulance");let s=e`
		<div class="ambulanceCover col box light">
		<div className="fill box">
			<h1 class="fill centered-text vertical-center">${l.current} <br><br>
				<button class="cancel" ${{onclick:e=>{s.remove(),b.classList.remove("callingAmbulance"),clearInterval(a),fetch("/cancel-am/",{method:"POST",headers:{"Content-Type":"application/json","X-CSRFToken":n()},body:JSON.stringify({fin_code:i})})}}}><img src="https://raw.githubusercontent.com/elcinbayramoff/imagess/main/hangup.png" width="90" alt=""></button>
			</h1>
		</div>
			
		</div>
	`;document.body.appendChild(s)}function d(t){function n(){const e=document.cookie.split(";").find((e=>e.trim().startsWith("csrftoken=")));return e?e.split("=")[1]:null}const o={method:"POST",headers:{"Content-Type":"application/json","X-CSRFToken":n()},body:JSON.stringify({})};let i,a=null;fetch("/call-doctor/",o).then((e=>e.json())).then((t=>{i=t.fin_code,console.log(i),a=setInterval((()=>{fetch("/check-sent/",{method:"POST",headers:{"Content-Type":"application/json","X-CSRFToken":n()},body:JSON.stringify({fin_code:i})}).then((e=>e.json())).then((t=>{t.sent||(clearInterval(a),l.put(e`Anında Konsultasiya`)),console.log(t.sent)}))}),1e3)})).catch((()=>{})),l.put(e`Zəng çalınır`),b.classList.add("callingDoctor");let s=e`
		<div class="ambulanceCover col box light doctor">
		<div className="fill box">
			${window.callingDep}
			<h1 class="fill centered-text vertical-center">${l.current} <br><br>
				<button class="cancel" ${{onclick:e=>{s.remove(),b.classList.remove("callingDoctor"),clearInterval(a),fetch("/cancel-am/",{method:"POST",headers:{"Content-Type":"application/json","X-CSRFToken":n()},body:JSON.stringify({fin_code:i})})}}}><img src="https://raw.githubusercontent.com/elcinbayramoff/imagess/main/hangup.png" width="90" alt=""></button>
			</h1>
		</div>
			
		</div>
	`;document.body.appendChild(s)}window.profileData={name:"",surname:"",fin_code:"",patrical_name:""},fetch("/user-profile/").then((e=>e.json())).then((e=>{window.profileData=e}));let h,p=!0;function m(){let t=h.value;fetch("/send-chat/",{method:"POST",headers:{"Content-Type":"application/json","X-CSRFToken":r()},body:JSON.stringify({user_input:t})}).then((e=>e.json())).then((t=>{c.appendChild(e`<div class="botmessage">${t.reply}</div>`),t.doc&&(document.querySelector(".consult").click(),setTimeout((()=>document.querySelector(`a[class~="${t.doc}"]`).click()),20))})),p&&(c.innerHTML="",p=!1),h.value="",c.appendChild(e`<div class="ourmessage">${t}</div>`)}function v(e){fetch("/delete-history/"),c.innerHTML="",window.callingDep=e,d()}const f=e`
	<div class="chatbox col">
		<div class="chatText">
			${c}
		</div>
		<div class="actions col">
		<div class="mainactions row">
			<button class="ambulance" ${{onclick:u}}>Ambulans çağır</button>
			<button class="consult" ${{onclick:t=>g.put(e`
	<div class="consults col">
	<input type="text" placeholder="axtarış" ${e=>s=e} class="filterer" ${{oninput:t=>{i.innerHTML="",i.append(...a.filter((e=>e.toLowerCase().includes(s.value.toLowerCase()))).map((t=>e`
								<button ${{onclick:d}} class="department" ${e=>e.setAttribute("dep",t)} ${{onclick:e=>v(t)}}>${t}</button>`)))}}}>
		<div class="chatText col" ${e=>i=e}>
			${a.map((t=>e`
				<button class="department" ${{onclick:d}} ${e=>e.setAttribute("dep",t)} ${{onclick:e=>v(t)}}>${t}</button>`))}
		</div>
		<div class="actions col">
		<div class="mainactions row">
			<button class="ambulance" ${{onclick:u}}>Ambulans çağır</button>
			<button class="consult">Konsultasiya</button>
		</div>
		<div class="inputContainer">
			<div class="input">
				<input placeholder="Yazınızı bura daxil edin" type="text" ${{onclick:e=>{g.put(f),h.focus(),h.value=""}}}>
				<button class="send" ${{onclick:e=>m()}}>--&gt;</button>
			</div>
		</div>

		</div>
	</div>

	`)}}>Konsultasiya</button>
		</div>
		<div class="inputContainer">
			<div class="input">
				<input placeholder="Yazınızı bura daxil edin" type="text"  ${{onkeydown:e=>13==e.keyCode?m():null}} ${e=>h=e}>
				<button class="send" ${{onclick:e=>m()}}>--&gt;</button>

			</div>
		</div>

		</div>
	</div>
`,g=new t;g.put(f);const b=e`
	<div class="main col">
		${o}

		${g.current}
	</div>
`;document.body.appendChild(b)})();