// ----- DATABASES -----
const database = {
    "Agent Files": {
        "Field Agents": ["Finch", "Gray", "Shard", "Stray", "Violet", "Ward"],
        "Researchers": ["Glassmind", "Restorer", "Scribe", "Semiotician", "Synthetist"]
    },
    "Compendium of the Archives": {
        "Verified Resources": ["Object Classifications"]
    },
    "Entities": {
        "Ecliptic": ["AE-352"],
        "First Discovered": ["AE-331", "AE-332", "AE-412-A/B", "AE-777", "AE-920"]
        // truncated for brevity
    }
};

// User accounts
const ACCOUNTS = {
    "TOA Terminal": {password:"Paer-X", message:"Welcome to the TOA Archival Database."},
    "BV Terminal": {password:" ", message:"The information you are about to view is highly classified."},
    "ADMIN": {password:" ", message:"Administrator privileges granted."}
};

// File contents (example for brevity)
const file_contents = {
    "Finch": "File content for Finch",
    "Gray": "File content for Gray",
    "Shard": "File content for Shard"
};

// ----- LOGIN -----
document.getElementById("login-btn").onclick = () => {
    const user = document.getElementById("username").value;
    const pw = document.getElementById("password").value;
    if (ACCOUNTS[user] && ACCOUNTS[user].password === pw) {
        alert(ACCOUNTS[user].message);
        document.getElementById("login-frame").classList.add("hidden");
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
