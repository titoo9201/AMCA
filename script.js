document.addEventListener("DOMContentLoaded", function () {

    // Select Elements
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const messages = document.getElementById('messages');
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('toggle-btn');
    const main = document.getElementById("main");
    const cameraBtn = document.getElementById('camera-btn');
    const imagePromptInput = document.getElementById('image-prompt');
    const micbtn=document.getElementById('mic-btn');
  
    // yha user ka message hai
    function addUserMessage(message) {
      const messageDiv = document.createElement('div');
      messageDiv.className = 'user-message';
      messageDiv.textContent = message;
      messages.appendChild(messageDiv);
      messages.scrollTop = messages.scrollHeight; // Auto-scroll 
    }
  
    // yha par amca ka reply hoga 
    function addAMCAReply(reply) {
      const replyDiv = document.createElement('div');
      replyDiv.className = 'reply-message';
      replyDiv.textContent = reply;
      messages.appendChild(replyDiv);
      messages.scrollTop = messages.scrollHeight; // Auto-scroll 
    }
  
    // Sending Messages
    function sendMessage() {
      const message = userInput.value.trim();
      if (message) {
        addUserMessage(message); // Add user message to chat
        userInput.value = ''; // Clear input field
  
        // Simulate AMCA Reply
        setTimeout(() => {
          addAMCAReply('This is a response from AMCA!');
        }, 500); // Delay for realism
      }
    }
  
    // Event Listener for Send Button
    sendBtn.addEventListener('click', sendMessage);
  
    // Event Listener for Enter Key
    userInput.addEventListener('keydown', (event) => {
      if (event.key === 'Enter') {
        sendMessage();
      }
    });
  
    // Sidebar Toggle Functionality
    toggleBtn.addEventListener("click", function () {
        if (sidebar.classList.contains('hidden')) {
            sidebar.classList.remove('hidden');
            document.getElementById('main').classList.remove('expanded');
        } else {
            sidebar.classList.add('hidden');
            document.getElementById('main').classList.add('expanded');
        }
    });
   // camera button 
   cameraBtn.addEventListener('click', function () {
    const imagePrompt = imagePromptInput.value.trim();// user se input lo 
    
    if (!imagePrompt) {
        alert("Please describe the image you want to generate!");
        return;
    }

   // api ko fetch karenge backend se 
    fetch('http://127.0.0.1:5000/generate-image', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt: imagePrompt }) // prompt jaye backend mein kya generate karni hai is ke liye
    })
        .then(response => response.json())
        .then(data => {
            // sahi se chale
            alert(data.message); 
        })
        .catch(error => {
            // error ko dekhna
            alert('Failed to generate image: ' + error.message);
        });
});


 

  });
  