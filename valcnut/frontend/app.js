const API_BASE = "/api/v1";
let token = localStorage.getItem("token");
let character = null;
let ws = null;

async function apiRequest(endpoint, method = "GET", body = null) {
    const headers = {
        "Content-Type": "application/json"
    };
    if (token) headers["Authorization"] = `Bearer ${token}`;

    const config = { method, headers };
    if (body) config.body = JSON.stringify(body);

    const response = await fetch(`${API_BASE}${endpoint}`, config);
    return response.json();
}

function showScreen(screenId) {
    document.querySelectorAll("main > section").forEach(s => s.classList.add("hidden"));
    document.getElementById(`${screenId}-screen`).classList.remove("hidden");
}

async function init() {
    if (token) {
        const res = await apiRequest("/character/me");
        if (res.id) {
            character = res;
            document.getElementById("main-nav").classList.remove("hidden");
            document.getElementById("chat-box").classList.remove("hidden");
            showScreen("arena");
            connectWS();
        } else {
            showScreen("char-create");
        }
    }
}

function connectWS() {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    ws = new WebSocket(`${protocol}//${window.location.host}/ws/${character.id}`);

    ws.onmessage = (event) => {
        const msg = JSON.parse(event.data);
        if (msg.type === "chat") {
            const chatLog = document.getElementById("chat-messages");
            chatLog.innerHTML += `<div><strong>${msg.from_id}:</strong> ${msg.text}</div>`;
            chatLog.scrollTop = chatLog.scrollHeight;
        }
    };
}

async function submitTurn(zone) {
    const res = await apiRequest(`/battle/1/turn?attack_zone=${zone}`, "POST", [1, 2]); // Block head & body
    if (res.turn_logs) {
        const log = document.getElementById("combat-log");
        res.turn_logs.forEach(l => {
            log.innerHTML += `<div>Character ${l.attacker_id} hit Character ${l.defender_id} in zone ${l.hit_zone} for ${l.damage} damage (${l.type})</div>`;
        });
        log.scrollTop = log.scrollHeight;
    }
}

// Event Listeners
document.getElementById("login-btn")?.addEventListener("click", async () => {
    // simplified login
    token = "mock-token"; // normally from /auth/login
    localStorage.setItem("token", token);
    init();
});

init();
