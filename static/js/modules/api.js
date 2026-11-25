/**
 * API communication and authentication module
 */
import { state } from './state.js';

export function apiFetch(url, options = {}) {
  const opts = { ...options };
  opts.headers = { ...(opts.headers || {}) };
  const savedPin = localStorage.getItem("auth_pin");
  if (savedPin && !opts.headers["X-Access-Pin"]) {
    opts.headers["X-Access-Pin"] = savedPin;
  }
  if (!opts.credentials) {
    opts.credentials = "include";
  }
  return fetch(url, opts);
}

export function checkUnauthorized(res) {
  if (res && res.status === 401) {
    localStorage.removeItem("auth_pin");
    const modal = document.getElementById("modal-pin-auth");
    if (modal) {
      const wasHidden = modal.classList.contains("hidden");
      modal.classList.remove("hidden");
      if (wasHidden) {
        setTimeout(() => {
          const inp = document.getElementById("auth-pin-input");
          if (inp) inp.focus();
        }, 100);
      }
    }
    return true;
  }
  return false;
}

export async function submitPinAuth(e, onSuccessCallbacks = {}) {
  if (e) e.preventDefault();
  const pinInput = document.getElementById("auth-pin-input");
  const submitBtn = document.getElementById("btn-auth-pin");
  const pin = pinInput.value.trim();
  const errorEl = document.getElementById("auth-pin-error");
  errorEl.classList.add("hidden");

  if (!pin) {
    errorEl.innerText = "Введи PIN-код";
    errorEl.classList.remove("hidden");
    pinInput.focus();
    return;
  }

  if (submitBtn) submitBtn.disabled = true;
  try {
    const res = await fetch("/api/auth/verify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ pin: pin })
    });
    const data = await res.json().catch(() => ({}));
    if (res.ok && data.success) {
      localStorage.setItem("auth_pin", pin);
      pinInput.value = "";
      document.getElementById("modal-pin-auth").classList.add("hidden");
      if (onSuccessCallbacks.onSuccess) {
        onSuccessCallbacks.onSuccess();
      }
    } else {
      errorEl.innerText = data.error || "Неверный PIN-код доступа";
      errorEl.classList.remove("hidden");
      pinInput.value = "";
      pinInput.focus();
    }
  } catch (err) {
    errorEl.innerText = "Ошибка соединения: " + err.message;
    errorEl.classList.remove("hidden");
  } finally {
    if (submitBtn) submitBtn.disabled = false;
  }
}
