async function sendMessage() {
    const userInput = document.getElementById("user-input").value.trim();
    if (!userInput) return;

    const chatbox = document.getElementById("chatbox");
    chatbox.innerHTML += `<div class="user-msg">Tú: ${userInput}</div>`;
    const botMsg = document.createElement('div');
    botMsg.className = 'bot-msg';
    botMsg.innerHTML = '<span class="typing">Bot: escribiendo...</span>';
    chatbox.appendChild(botMsg);
    chatbox.scrollTop = chatbox.scrollHeight;
const spanishPrompt = `Responde exclusivamente en español, de forma clara y concisa: ${userInput}`;
    try {
        const response = await fetch("/ollama/api/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                model: "tinyllama",
                prompt: spanishPrompt,  // Usa el prompt modificado
                prompt: userInput,
                stream: false
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Error en el servidor");
        }

        const data = await response.json();
        botMsg.querySelector('.typing').textContent = data.response || data.message;

    } catch (error) {
        console.error("Error:", error);
        botMsg.querySelector('.typing').textContent = `Error: ${error.message}`;
    } finally {
        document.getElementById("user-input").value = "";
    }
}

// 👇 Añade este Event Listener para el Enter
document.getElementById("user-input").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault(); // Evita el comportamiento por defecto (como un salto de línea)
        sendMessage();
    }
});

// CSS recomendado para el chat
document.head.insertAdjacentHTML("beforeend", `
<style>
    .user-msg { color: #4a86e8; margin: 5px 0; }
    .bot-msg { color: #333; margin: 5px 0; }
    .typing { color: #666; font-style: italic; }
    #chatbox { height: 400px; overflow-y: auto; padding: 10px; }
    #user-input { 
        width: 100%; 
        padding: 8px; 
        box-sizing: border-box; 
    }
</style>
`);

// Efecto "lluvia de código" Matrix (corregido)
document.addEventListener('DOMContentLoaded', () => {
    const chars = "01アイウエオカキクケコ";
    const canvas = document.createElement('canvas');
    document.body.prepend(canvas);
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.zIndex = '-1';
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    const ctx = canvas.getContext('2d');
    const columns = Math.floor(canvas.width / 15);
    const drops = Array(columns).fill(1);

    function drawMatrix() {  // 👈 Corregí el typo "functio" por "function"
        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#00ff41';
        ctx.font = '15px monospace';
        
        drops.forEach((y, i) => {
            const text = chars[Math.floor(Math.random() * chars.length)];
            ctx.fillText(text, i * 15, y * 15);
            drops[i] = y > canvas.height / 15 || Math.random() > 0.98 ? 0 : y + 1;
        });
    }
    
    setInterval(drawMatrix, 50);
});
