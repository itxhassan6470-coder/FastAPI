const API_URL = "http://127.0.0.1:8000/predict";

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("predict-form");
  const predictBtn = document.getElementById("predict-btn");
  const btnLabel = predictBtn.querySelector("[data-btn-label]");

  const resultBox = document.getElementById("result-box");
  const successPanel = document.getElementById("result-success");
  const errorPanel = document.getElementById("result-error");
  const categoryValue = document.getElementById("result-category-value");
  const statusText = document.getElementById("result-status-text");
  const errorText = document.getElementById("result-error-text");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const age = parseInt(document.getElementById("age").value, 10);
    const income_lpa = parseFloat(document.getElementById("income_lpa").value);
    const weight = parseFloat(document.getElementById("weight").value);
    const height = parseFloat(document.getElementById("height").value);
    const smoker = document.getElementById("smoker").value === "true";
    const city = document.getElementById("city").value.trim();
    const occupation = document.getElementById("occupation").value;

    const payload = { age, income_lpa, weight, height, smoker, city, occupation };

    setLoading(true);
    hideResult();

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          (data && (data.detail || data.message)) ||
          `Server returned ${response.status}`
        );
      }

      const category = data.predicted_category;
      showSuccess(category, city, occupation);

    } catch (err) {
      showError(
        err.message === "Failed to fetch"
          ? "Could not reach the server. Make sure your FastAPI app is running on http://127.0.0.1:8000."
          : err.message
      );
    } finally {
      setLoading(false);
      resultBox.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
  });

  function showSuccess(category, city, occupation) {
    const tier = (category || "").toString().toLowerCase();
    successPanel.classList.remove("tier-low", "tier-medium", "tier-high");
    if (tier.includes("low")) successPanel.classList.add("tier-low");
    else if (tier.includes("medium") || tier.includes("mid")) successPanel.classList.add("tier-medium");
    else if (tier.includes("high")) successPanel.classList.add("tier-high");

    categoryValue.textContent = category ?? "Unknown";
    statusText.textContent = `Assessed for ${city} • ${occupation.replace(/_/g, " ")}`;

    errorPanel.classList.add("hidden");
    errorPanel.classList.remove("flex");
    successPanel.classList.remove("hidden");
    successPanel.classList.add("flex");
    resultBox.classList.remove("hidden");
  }

  function showError(message) {
    errorText.textContent = message;

    successPanel.classList.add("hidden");
    successPanel.classList.remove("flex");
    errorPanel.classList.remove("hidden");
    errorPanel.classList.add("flex");
    resultBox.classList.remove("hidden");
  }

  function hideResult() {
    resultBox.classList.add("hidden");
    successPanel.classList.add("hidden");
    errorPanel.classList.add("hidden");
  }

  function setLoading(isLoading) {
    predictBtn.disabled = isLoading;
    btnLabel.textContent = isLoading ? "Computing..." : "Calculate Premium";
    predictBtn.querySelector('[data-spinner]')?.remove();
    if (isLoading) {
      const spinner = document.createElement("span");
      spinner.className = "spinner";
      spinner.setAttribute("data-spinner", "");
      btnLabel.before(spinner);
    }
  }
});
