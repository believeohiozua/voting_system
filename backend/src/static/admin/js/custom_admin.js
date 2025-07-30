// Custom JavaScript for Feature Voting System Admin

document.addEventListener("DOMContentLoaded", function () {
  // Add vote functionality
  window.addVote = function (featureId) {
    if (confirm("Add one vote to this feature?")) {
      // In a real implementation, this would make an AJAX call
      // For now, we'll show a message
      alert("Vote added! Please refresh the page to see changes.");

      // You could implement actual AJAX here:
      /*
            fetch(`/admin/features/feature/${featureId}/add-vote/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                }
            });
            */
    }
  };

  // Get CSRF token helper
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  // Enhanced tooltips
  const tooltipElements = document.querySelectorAll("[title]");
  tooltipElements.forEach((element) => {
    element.addEventListener("mouseenter", function () {
      this.style.cursor = "help";
    });
  });

  // Smooth animations for vote badges
  const voteBadges = document.querySelectorAll(".votes-badge");
  voteBadges.forEach((badge) => {
    badge.addEventListener("mouseenter", function () {
      this.style.transform = "scale(1.1)";
      this.style.transition = "transform 0.2s ease";
    });

    badge.addEventListener("mouseleave", function () {
      this.style.transform = "scale(1)";
    });
  });

  // Auto-refresh functionality (optional)
  if (window.location.pathname.includes("/features/feature/")) {
    // Add auto-refresh button to changelist
    const toolbar = document.querySelector(".object-tools");
    if (toolbar) {
      const refreshBtn = document.createElement("li");
      refreshBtn.innerHTML =
        '<a href="#" onclick="location.reload(); return false;" class="addlink">Refresh Data</a>';
      toolbar.appendChild(refreshBtn);
    }
  }

  // Dashboard enhancements
  if (window.location.pathname === "/admin/") {
    // Add custom dashboard widgets
    addDashboardStats();
  }
});

function addDashboardStats() {
  // This would typically fetch real stats from an API
  const dashboardContent = document.querySelector("#content-main");
  if (dashboardContent) {
    const statsHTML = `
            <div class="dashboard-card">
                <h3>📊 Feature Voting Statistics</h3>
                <p>Welcome to the Feature Voting System administration panel.</p>
                <ul>
                    <li>Manage feature requests and their votes</li>
                    <li>View detailed analytics and trends</li>
                    <li>Moderate content and user submissions</li>
                </ul>
            </div>
        `;

    dashboardContent.insertAdjacentHTML("afterbegin", statsHTML);
  }
}
