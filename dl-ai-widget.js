/* ==========================================================================
   D&L AI Sales Assistant widget
   Vanilla JS, no framework, no build step.

   - Floating button bottom-right.
   - Chat box opens on click and auto-opens after 20s.
   - Talks ONLY to /ai-proxy.php (never to DeepSeek directly, no API key here).
   - Sends: message, page_url, page_title, page_context, short history.
   - Uses document.body.dataset.aiContext as page_context when present.
   ========================================================================== */
(function () {
  "use strict";

  // ---- Config ------------------------------------------------------------
  var PROXY_URL = "/ai-proxy.php";
  var AUTO_OPEN_MS = 20000;          // auto-open after 20 seconds
  var HISTORY_LIMIT = 10;            // last N turns forwarded to backend
  var FIRST_MESSAGE =
    "Planning a trip? Are you travelling as a couple, family, or group?";

  var QUICK_BUTTONS = [
    { label: "Family trip", text: "We're planning a family trip." },
    { label: "Couple trip", text: "We're travelling as a couple." },
    { label: "Morocco instead", text: "Actually, can you help with Morocco instead?" },
    { label: "Need custom plan", text: "I'd like a custom travel plan." }
  ];

  // Conversation history: [{ role: 'user'|'assistant', content: '...' }]
  var history = [];
  var isOpen = false;
  var autoOpenTimer = null;
  var hasAutoOpened = false;

  // DOM refs (assigned in build()).
  var els = {};

  // ---- Helpers -----------------------------------------------------------
  function el(tag, className, html) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (html != null) node.innerHTML = html;
    return node;
  }

  function getPageContext() {
    if (document.body && document.body.dataset && document.body.dataset.aiContext) {
      return document.body.dataset.aiContext;
    }
    var meta = document.querySelector('meta[name="description"]');
    return meta ? meta.getAttribute("content") || "" : "";
  }

  function scrollToBottom() {
    els.messages.scrollTop = els.messages.scrollHeight;
  }

  // ---- Rendering messages ------------------------------------------------
  function addMessage(role, text) {
    var cls =
      role === "user"
        ? "dlai-msg dlai-msg-user"
        : role === "error"
        ? "dlai-msg dlai-msg-error"
        : "dlai-msg dlai-msg-assistant";
    var node = el("div", cls);
    node.textContent = text;
    els.messages.appendChild(node);
    scrollToBottom();
    return node;
  }

  function showTyping() {
    var node = el(
      "div",
      "dlai-msg dlai-msg-assistant",
      '<span class="dlai-typing"><span></span><span></span><span></span></span>'
    );
    els.messages.appendChild(node);
    scrollToBottom();
    return node;
  }

  // ---- Networking --------------------------------------------------------
  function sendToBackend(message) {
    var payload = {
      message: message,
      page_url: window.location.href,
      page_title: document.title,
      page_context: getPageContext(),
      history: history.slice(-HISTORY_LIMIT)
    };

    setBusy(true);
    var typing = showTyping();

    fetch(PROXY_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    })
      .then(function (res) {
        return res.json().catch(function () {
          return { error: true, reply: "" };
        });
      })
      .then(function (data) {
        typing.remove();
        var reply = (data && (data.reply || data.message)) || "";
        if (data && data.error && !reply) {
          reply =
            "Sorry, I can't reach the travel assistant right now. Please try again in a moment.";
          addMessage("error", reply);
          return;
        }
        if (!reply) {
          reply = "Thanks! A travel specialist will follow up shortly.";
        }
        history.push({ role: "assistant", content: reply });
        addMessage("assistant", reply);
      })
      .catch(function () {
        typing.remove();
        // Backend not available (expected before upload / offline). Degrade.
        addMessage(
          "error",
          "The AI assistant isn't connected yet on this page. Once it's live, your message will be answered here."
        );
      })
      .finally(function () {
        setBusy(false);
      });
  }

  function handleUserMessage(text) {
    text = (text || "").trim();
    if (!text) return;
    history.push({ role: "user", content: text });
    addMessage("user", text);
    sendToBackend(text);
  }

  // ---- UI state ----------------------------------------------------------
  function setBusy(busy) {
    els.send.disabled = busy;
    els.input.disabled = busy;
  }

  function openPanel() {
    if (isOpen) return;
    isOpen = true;
    els.panel.classList.add("dlai-open");
    els.launcher.classList.add("dlai-hidden");
    if (autoOpenTimer) {
      clearTimeout(autoOpenTimer);
      autoOpenTimer = null;
    }
    // Seed the first assistant message once.
    if (history.length === 0) {
      history.push({ role: "assistant", content: FIRST_MESSAGE });
      addMessage("assistant", FIRST_MESSAGE);
    }
    setTimeout(function () {
      els.input.focus();
    }, 150);
  }

  function closePanel() {
    isOpen = false;
    els.panel.classList.remove("dlai-open");
    els.launcher.classList.remove("dlai-hidden");
  }

  // ---- Build DOM ---------------------------------------------------------
  function build() {
    var root = el("div", "dlai-root");

    // Launcher button
    var launcher = el(
      "button",
      "dlai-launcher",
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg><span>Plan my trip</span>'
    );
    launcher.setAttribute("type", "button");
    launcher.setAttribute("aria-label", "Open travel assistant");

    // Panel
    var panel = el("div", "dlai-panel");
    panel.setAttribute("role", "dialog");
    panel.setAttribute("aria-label", "D&L travel assistant");

    var header = el(
      "div",
      "dlai-header",
      '<span class="dlai-dot"></span>' +
        '<div class="dlai-header-text">' +
        '<div class="dlai-header-title">D&amp;L Travel Assistant</div>' +
        '<div class="dlai-header-sub">Typically replies in a few seconds</div>' +
        "</div>"
    );
    var closeBtn = el("button", "dlai-close", "&times;");
    closeBtn.setAttribute("type", "button");
    closeBtn.setAttribute("aria-label", "Close chat");
    header.appendChild(closeBtn);

    var messages = el("div", "dlai-messages");

    // Quick reply buttons
    var quick = el("div", "dlai-quick");
    QUICK_BUTTONS.forEach(function (b) {
      var btn = el("button", "dlai-quick-btn", null);
      btn.setAttribute("type", "button");
      btn.textContent = b.label;
      btn.addEventListener("click", function () {
        handleUserMessage(b.text);
      });
      quick.appendChild(btn);
    });

    // Composer
    var composer = el("div", "dlai-composer");
    var input = el("textarea", "dlai-input");
    input.setAttribute("rows", "1");
    input.setAttribute("placeholder", "Type your message…");
    input.setAttribute("aria-label", "Message");
    var send = el(
      "button",
      "dlai-send",
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>'
    );
    send.setAttribute("type", "button");
    send.setAttribute("aria-label", "Send message");
    composer.appendChild(input);
    composer.appendChild(send);

    panel.appendChild(header);
    panel.appendChild(messages);
    panel.appendChild(quick);
    panel.appendChild(composer);

    root.appendChild(launcher);
    root.appendChild(panel);
    document.body.appendChild(root);

    els = {
      root: root,
      launcher: launcher,
      panel: panel,
      messages: messages,
      input: input,
      send: send
    };

    // ---- Events ----------------------------------------------------------
    launcher.addEventListener("click", openPanel);
    closeBtn.addEventListener("click", closePanel);

    function submit() {
      var v = input.value;
      input.value = "";
      input.style.height = "auto";
      handleUserMessage(v);
    }

    send.addEventListener("click", submit);

    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        submit();
      }
    });

    // Auto-grow textarea
    input.addEventListener("input", function () {
      input.style.height = "auto";
      input.style.height = Math.min(input.scrollHeight, 96) + "px";
    });

    // Auto-open after 20s (once, only if visitor hasn't opened it already).
    autoOpenTimer = setTimeout(function () {
      if (!isOpen && !hasAutoOpened) {
        hasAutoOpened = true;
        openPanel();
      }
    }, AUTO_OPEN_MS);
  }

  // ---- Init --------------------------------------------------------------
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", build);
  } else {
    build();
  }
})();
