const API_BASE = window.location.origin;

const state = {
  channel: "web",
  accessToken: null,
  refreshToken: null,
  sending: false,
};

const elements = {
  channelTabs: document.getElementById("channel-tabs"),
  channelTitle: document.getElementById("channel-title"),
  channelSubtitle: document.getElementById("channel-subtitle"),
  messages: document.getElementById("messages"),
  chatForm: document.getElementById("chat-form"),
  messageInput: document.getElementById("message-input"),
  sendBtn: document.getElementById("send-btn"),
  newChatBtn: document.getElementById("new-chat-btn"),
  showTrace: document.getElementById("show-trace"),
  connectionStatus: document.getElementById("connection-status"),
  sessionInfo: document.getElementById("session-info"),
  handoffBanner: document.getElementById("handoff-banner"),
};

const channelLabels = {
  web: "Web chat",
  whatsapp: "WhatsApp",
  instagram: "Instagram",
  ads: "Ads lead",
};

function appendMessage(text, role) {
  const node = document.createElement("div");
  node.className = `message ${role}`;
  node.textContent = text;
  elements.messages.appendChild(node);
  elements.messages.scrollTop = elements.messages.scrollHeight;
  return node;
}

function setConnected(online, detail = "") {
  elements.connectionStatus.classList.toggle("online", online);
  elements.connectionStatus.classList.toggle("offline", !online);
  elements.connectionStatus.textContent = online ? "Connected" : "Offline";
  if (detail) {
    elements.sessionInfo.textContent = detail;
  }
}

function stripHandoffMarker(text) {
  return text.replace(/\n\n<!-- HANDOFF:pricing -->/g, "").trim();
}

function detectHandoff(text) {
  if (text.includes("<!-- HANDOFF:pricing -->")) {
    elements.handoffBanner.classList.remove("hidden");
  }
}

async function apiFetch(path, options = {}) {
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };
  if (state.accessToken && !options.skipAuth) {
    headers.Authorization = `Bearer ${state.accessToken}`;
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  if (response.status === 401 && state.refreshToken && !options._retried) {
    const refreshed = await refreshSession();
    if (refreshed) {
      return apiFetch(path, { ...options, _retried: true });
    }
  }

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed (${response.status})`);
  }

  return response;
}

async function refreshSession() {
  const response = await fetch(`${API_BASE}/api/refresh`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${state.refreshToken}`,
    },
  });
  if (!response.ok) {
    return false;
  }
  const data = await response.json();
  state.accessToken = data.access_token;
  state.refreshToken = data.refresh_token;
  return true;
}

async function initializeSession(clearMessages = true) {
  if (clearMessages) {
    elements.messages.innerHTML = "";
    elements.handoffBanner.classList.add("hidden");
  }

  setConnected(false, "Initializing session…");

  const response = await apiFetch("/api/initialize", {
    method: "POST",
    skipAuth: true,
    body: JSON.stringify({
      channel_id: state.channel,
      user_id: `local-${state.channel}`,
      stream_format: "ndjson",
    }),
  });

  const data = await response.json();
  state.accessToken = data.access_token;
  state.refreshToken = data.refresh_token;

  setConnected(true, `Session: ${state.channel}`);
  appendMessage(`Connected to Or-sync agent via ${channelLabels[state.channel]}.`, "system");
}

async function startNewChat() {
  if (state.accessToken) {
    try {
      await apiFetch("/api/new_conversation", { method: "POST" });
    } catch (error) {
      console.warn("Could not persist previous conversation:", error);
    }
  }
  await initializeSession(true);
}

async function sendMessage(message) {
  state.sending = true;
  elements.sendBtn.disabled = true;

  appendMessage(message, "user");

  const response = await apiFetch("/api/chat", {
    method: "POST",
    body: JSON.stringify({ user_query: message, timeout_seconds: 90 }),
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  let finalResponse = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) {
      break;
    }
    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop() || "";

    for (const line of lines) {
      if (!line.trim()) {
        continue;
      }
      let event;
      try {
        event = JSON.parse(line);
      } catch {
        continue;
      }

      if (event.type === "trace" && elements.showTrace.checked) {
        appendMessage(JSON.stringify(event.data, null, 2), "trace");
      }

      if (event.type === "output") {
        const responses = event.data?.command_responses || [];
        finalResponse = responses.map((item) => item.response).join("\n\n");
      }

      if (event.type === "error") {
        throw new Error(event.data?.detail || "Agent error");
      }
    }
  }

  if (finalResponse) {
    detectHandoff(finalResponse);
    appendMessage(stripHandoffMarker(finalResponse), "agent");
  } else {
    appendMessage("No response received from the agent.", "system");
  }

  state.sending = false;
  elements.sendBtn.disabled = false;
}

function setChannel(channel) {
  state.channel = channel;
  elements.channelTitle.textContent = channelLabels[channel] || channel;
  elements.channelSubtitle.textContent =
    channel === "web"
      ? "Simulated website visitor"
      : `Simulated ${channelLabels[channel]} customer`;

  document.querySelectorAll(".channel").forEach((button) => {
    button.classList.toggle("active", button.dataset.channel === channel);
  });
}

elements.channelTabs.addEventListener("click", async (event) => {
  const button = event.target.closest(".channel");
  if (!button || state.sending) {
    return;
  }
  const nextChannel = button.dataset.channel;
  if (nextChannel === state.channel) {
    return;
  }
  setChannel(nextChannel);
  await initializeSession(true);
});

elements.chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = elements.messageInput.value.trim();
  if (!message || state.sending) {
    return;
  }
  elements.messageInput.value = "";
  try {
    await sendMessage(message);
  } catch (error) {
    appendMessage(`Error: ${error.message}`, "system");
    state.sending = false;
    elements.sendBtn.disabled = false;
  }
});

elements.newChatBtn.addEventListener("click", async () => {
  if (state.sending) {
    return;
  }
  try {
    await startNewChat();
  } catch (error) {
    appendMessage(`Error starting new chat: ${error.message}`, "system");
  }
});

window.addEventListener("load", async () => {
  setChannel("web");
  try {
    await initializeSession(true);
  } catch (error) {
    setConnected(false, "FastWorkflow backend unavailable");
    appendMessage(
      `Could not connect to the agent backend. Start it with:\npython -m fastworkflow.run_fastapi_mcp --workflow_path ./orsync_workflow --port 8000\n\n${error.message}`,
      "system"
    );
  }
});
