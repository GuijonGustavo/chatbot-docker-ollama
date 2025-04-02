async function sendMessage() {
    const userInput = document.getElementById("user-input").value.trim();
    if (!userInput) return;

    const chatbox = document.getElementById("chatbox");
    chatbox.innerHTML += `<div class="user-msg">Tú: ${userInput}</div>`;
    const botMsg = document.createElement('div');
    botMsg.className = 'bot-msg';
    botMsg.innerHTML = 'Bot: <span class="typing">escribiendo...</span>';
    chatbox.appendChild(botMsg);
    chatbox.scrollTop = chatbox.scrollHeight;

    try {
        const response = await fetch("/ollama/api/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                model: "tinyllama",
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
// CSS recomendado para el chat
document.head.insertAdjacentHTML("beforeend", `
<style>
    .user-message { color: #4a86e8; margin: 5px 0; }
    .bot-message { color: #333; margin: 5px 0; }
    .typing { color: #666; font-style: italic; }
    #chatbox { height: 400px; overflow-y: auto; padding: 10px; }
</style>
`);

document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('user-input');
    const chatbox = document.getElementById('chatbox');
    
    // Enviar mensaje al presionar Enter
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;
        
        // Mostrar mensaje del usuario
        const userElement = document.createElement('div');
        userElement.className = 'user-message';
        userElement.textContent = message;
        chatbox.appendChild(userElement);
        
        // Mostrar "escribiendo..."
        const botElement = document.createElement('div');
        botElement.className = 'bot-message';
        botElement.innerHTML = '<span class="typing">Procesando...</span>';
        chatbox.appendChild(botElement);
        
        // Limpiar input
        userInput.value = '';
        
        // Scroll al final
        chatbox.scrollTop = chatbox.scrollHeight;
        
        // Enviar al backend (ajusta tu endpoint)
        fetch('/ollama/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                model: "tinyllama",
                prompt: message,
                stream: false
            })
        })
        .then(response => response.json())
        .then(data => {
            botElement.innerHTML = data.response || "Error: Respuesta no válida";
            chatbox.scrollTop = chatbox.scrollHeight;
        })
        .catch(error => {
            botElement.innerHTML = `Error: ${error.message}`;
            console.error('Error:', error);
        });
    }
    
    // Efecto de cursor intermitente en el input
    setInterval(() => {
        const prompt = document.getElementById('prompt');
        prompt.textContent = prompt.textContent === '>_' ? '> ' : '>_';
    }, 500);
});
