document.addEventListener("DOMContentLoaded", () => {
    const chatContainer = document.getElementById("chat-container");
    const userInput = document.getElementById("user-input");
    const chatModal = document.getElementById("chat-modal");
    const closeModal = document.getElementById("close-modal");
    const getRecommendations = document.getElementById("get-recommendations");
    const userId = "user_" + Math.random().toString(36).substr(2, 9); // Unique user ID

    // Show modal when "Get Started" is clicked
    getRecommendations.addEventListener("click", () => {
        chatModal.classList.remove("hidden");
    });

    // Close modal
    closeModal.addEventListener("click", () => {
        chatModal.classList.add("hidden");
    });

    // Chat input handling
    userInput.addEventListener("keypress", async (e) => {
        if (e.key === "Enter" && userInput.value.trim() && !chatModal.classList.contains("hidden")) {
            const message = userInput.value.trim();

            // Display user message
            const userMessage = document.createElement("div");
            userMessage.className = "user-message";
            userMessage.textContent = message;
            chatContainer.appendChild(userMessage);
            userInput.value = "";
            chatContainer.scrollTop = chatContainer.scrollHeight;

            // Send message to backend
            console.log("Sending message to /chat with user_id:", userId, "message:", message);
            try {
                const response = await fetch("/chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ user_id: userId, message })
                });
                console.log("Response status:", response.status);
                const result = await response.json();
                console.log("Full response data:", JSON.stringify(result, null, 2));

                const botMessage = document.createElement("div");
                botMessage.className = "bot-message";

                if (result && typeof result === 'object') {
                    if (Array.isArray(result.recommendations)) {
                        result.recommendations.forEach(recommendation => {
                            const movieLine = document.createElement("div");
                            movieLine.className = "mb-4"; // Margin-bottom for gap
                            movieLine.textContent = recommendation || "No title available";
                            botMessage.appendChild(movieLine);
                        });
                        if (result.check_availability) {
                            const linkDiv = document.createElement("div");
                            linkDiv.className = "mb-4";
                            const link = document.createElement("a");
                            link.href = result.check_availability;
                            link.textContent = "Check Availability";
                            link.target = "_blank"; // Open in new tab
                            link.className = "text-blue-500 underline";
                            linkDiv.appendChild(link);
                            botMessage.appendChild(linkDiv);
                        }
                    } else if (result.response) {
                        botMessage.textContent = result.response;
                    } else {
                        botMessage.textContent = "Unexpected response format.";
                        console.warn("Unexpected response structure:", result);
                    }
                } else {
                    botMessage.textContent = "Error: Invalid response from server.";
                    console.error("Invalid response:", result);
                }
                chatContainer.appendChild(botMessage);
                chatContainer.scrollTop = chatContainer.scrollHeight;
            } catch (error) {
                console.error("Fetch or parsing error:", error);
                const errorMessage = document.createElement("div");
                errorMessage.className = "bot-message";
                errorMessage.textContent = "Sorry, something went wrong. Try again!";
                chatContainer.appendChild(errorMessage);
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
        }
    });
});