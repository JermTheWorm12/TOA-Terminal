// ----- TOA DATABASE -----

const database = {

"Agent Files":{
"Field Agents":["Finch","Gray","Shard","Stray","Violet","Ward"],
"Researchers":["Glassmind","Restorer","Scribe","Semiotician","Synthetist"]
},

"Compendium of the Archives":{
"Verified Resources":["Object Classifications"]
},

"Entities":{

"Ecliptic":["AE-352"],

"First Discovered":[
"AE-331","AE-332","AE-412-A/B","AE-777","AE-920"
],

"Newly Discovered":[
"AE-175","AE-214","AE-909","AE-911","AE-923"
],

"Shadow":[
"AE-889","AE-913","AE-914","AE-915"
],

"Symbol":[
"AE-072","AE-702"
],

"Kenopses":[
"AE-L0","AE-L1","AE-L2","AE-L4","AE-L7","AE-L10","AE-L15",
"AE-L18","AE-L22","AE-L23","AE-L29","AE-L31","AE-L48"
],

"Triptych":[
"AE-000","AE-601","AE-602","AE-603"
]

},

"Incident Reports":{
"Incident-01":[]
},

"Mission Reports":{
"Mission Report-01":[]
}

};


// ----- BV DATABASE -----

const bv_database = {

"Agent Files":{
"Classified":[
"The Accomplice","The Autist","FearWeaver","The Key",
"The Leader","Nightshade","The Pseudonymist",
"The Seeker","The Thinker","The Watcher","The Wraith"
]
},

"Departure":{
"Records":["THKR-Departure"]
},

"Entity Files":{
"Echo-Walker":["AE-000X","Echo-Walker Dossier"],
"Kenopses":["AE-L[REDACTED]","AE-L96"],
"New":["AE-904"]
},

"Field Reports":{
"Operations":[
"Field Report-01",
"Field Report-02",
"Field Report-03",
"Field Report-04",
"Field Report-05"
]
},

"Incident Reports":{
"Vault Incidents":[
"Incident-BV-01",
"Incident-BV-02",
"Incident-BV-03",
"Incident-BV-04"
]
},

"Interviews":{
"Transcripts":[
"Council Analysis",
"Discussion of I",
"Interview w/Hive Mind",
"Witness Report-01",
"Wraith Debrief"
]
},

"Orientation":{
"Documents":["Archive Orientation"]
}

};


// ----- ADMIN DATABASE -----

const admin_database = {

"SYSTEM CONTROL":{
"Admin Files":[
"The Leader","The Wraith","The Artist"
]
},

"Entity Files":{
"Unlisted":[
"AE-000-1","AE-???","AE-NULL","AE-OBSIDIAN"
]
},

"Monitoring":{
"System Logs":[
"Login Attempts",
"Security Flags",
"Containment Breach Monitor"
]
}

};


// ----- ACCOUNTS -----

const ACCOUNTS = {

"TOA Terminal":{
password:"Paer-X",
message:"Welcome to the TOA Archival Database."
},

"BV Terminal":{
password:" ",
message:"The information you are about to view is highly classified."
},

"ADMIN":{
password:" ",
message:"Administrator privileges granted."
}

};


// ----- FILE CONTENTS -----

const file_contents = {};


// ----- LOGIN -----

function login(){

let user = document.getElementById("username").value
let pw = document.getElementById("password").value

if(ACCOUNTS[user] && ACCOUNTS[user].password === pw){

alert(ACCOUNTS[user].message)

document.getElementById("login").classList.add("hidden")

if(user==="BV Terminal")
openTerminal(bv_database)

else if(user==="ADMIN")
openTerminal(admin_database)

else
openTerminal(database)

}

else{
alert("ACCESS DENIED")
}

}


// ----- TERMINAL -----

function openTerminal(data){

document.getElementById("terminal").classList.remove("hidden")

const tree = document.getElementById("tree")

function build(obj,parent){

for(let key in obj){

let li=document.createElement("li")
li.textContent=key

parent.appendChild(li)

if(Array.isArray(obj[key])){

let ul=document.createElement("ul")

obj[key].forEach(item=>{

let child=document.createElement("li")

child.textContent=item

child.onclick=(e)=>{
e.stopPropagation()
openFile(item)
}

ul.appendChild(child)

})

li.appendChild(ul)

}

else{

let ul=document.createElement("ul")
build(obj[key],ul)
li.appendChild(ul)

}

}

}

build(data,tree)

}


// ----- FILE POPUP -----

function openFile(name){

document.getElementById("popup").classList.remove("hidden")

document.getElementById("fileTitle").textContent=name

document.getElementById("fileText").value =
file_contents[name] || name + "\n\nYou can edit this file."

}


function closePopup(){

document.getElementById("popup").classList.add("hidden")

}        document.getElementById("login-frame").classList.add("hidden");
        openTerminal(database);
    } else {
        alert("ACCESS DENIED: Invalid credentials. Attempt logged.");
    }
}

// ----- TERMINAL -----
function openTerminal(activeDatabase) {
    const container = document.getElementById("tree-container");
    const ul = document.createElement("ul");

    function buildTree(obj, parent) {
        for (let key in obj) {
            const li = document.createElement("li");
            li.textContent = key;
            parent.appendChild(li);
            if (Array.isArray(obj[key])) {
                const subUl = document.createElement("ul");
                obj[key].forEach(item => {
                    const subLi = document.createElement("li");
                    subLi.textContent = item;
                    subLi.onclick = (e) => { e.stopPropagation(); openFilePopup(item); };
                    subUl.appendChild(subLi);
                });
                li.appendChild(subUl);
            } else if (typeof obj[key] === "object") {
                const subUl = document.createElement("ul");
                buildTree(obj[key], subUl);
                li.appendChild(subUl);
            }
        }
    }

    buildTree(activeDatabase, ul);
    container.appendChild(ul);
    document.getElementById("terminal-frame").classList.remove("hidden");
}

// ----- FILE POPUP -----
function openFilePopup(fileName) {
    const popup = document.getElementById("file-popup");
    popup.classList.remove("hidden");
    document.getElementById("file-title").textContent = fileName;
    document.getElementById("file-text").value = file_contents[fileName] || `${fileName}\n\nYou can edit this content.`;
}

document.getElementById("close-popup").onclick = () => {
    document.getElementById("file-popup").classList.add("hidden");
      }
