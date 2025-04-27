// Function to handle countdown and redirect after password reset
function handlePasswordResetRedirect(redirectUrl, seconds) {
  // Hide the form
  const form = document.querySelector('form');
  if (form) {
      form.style.display = 'none';
  }
  
  // Create a message div for countdown
  const messageDiv = document.createElement('div');
  messageDiv.className = 'redirect-message';
  messageDiv.style.textAlign = 'center';
  messageDiv.style.marginTop = '20px';
  messageDiv.innerHTML = '<p>Redirecting to login page in <span id="countdown">' + seconds + '</span> seconds...</p>';
  
  // Find messages container and insert after it
  const messagesContainer = document.querySelector('.messages');
  if (messagesContainer) {
      messagesContainer.after(messageDiv);
  } else {
      // If no messages container, insert at the beginning of body
      document.body.prepend(messageDiv);
  }
  
  // Countdown function
  let remainingSeconds = seconds;
  const countdownElement = document.getElementById('countdown');
  const countdownInterval = setInterval(function() {
      remainingSeconds--;
      if (countdownElement) {
          countdownElement.textContent = remainingSeconds;
      }
      if (remainingSeconds <= 0) {
          clearInterval(countdownInterval);
      }
  }, 1000);
  
  // Redirect after delay
  setTimeout(function() {
      window.location.href = redirectUrl;
  }, seconds * 1000);
}