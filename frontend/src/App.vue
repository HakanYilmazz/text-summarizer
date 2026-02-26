<template>
  <div class="shell">
    <div class="bg-texture"></div>

    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="brand">
        <svg class="brand-icon" width="28" height="28" viewBox="0 0 28 28" fill="none">
          <rect x="2" y="2" width="24" height="24" rx="6" fill="#c8502a" opacity="0.12"/>
          <rect x="6" y="8" width="16" height="2" rx="1" fill="#c8502a"/>
          <rect x="6" y="13" width="11" height="2" rx="1" fill="#c8502a"/>
          <rect x="6" y="18" width="7" height="2" rx="1" fill="#c8502a"/>
        </svg>
        <span class="brand-name">Précis</span>
      </div>

      <div class="sidebar-content">
        <p class="sidebar-tagline">Condense any text into its clearest, sharpest form.</p>
        <div class="sidebar-meta">
          <div class="meta-item">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
            <span>Instant results</span>
          </div>
          <div class="meta-item">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            <span>Private &amp; secure</span>
          </div>
          <div class="meta-item">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
            <span>AI-powered</span>
          </div>
        </div>
      </div>

      <div class="sidebar-footer">Powered by Claude</div>
    </aside>

    <!-- Main -->
    <main class="main">
      <div class="main-inner">

        <div class="topbar">
          <h1 class="page-title">Text Summarizer</h1>
          <label class="api-toggle" :class="{ active: useKey }">
            <div class="toggle-track" @click="useKey = !useKey">
              <div class="toggle-thumb"></div>
            </div>
            <span>Use my API key</span>
          </label>
        </div>

        <!-- Input panel -->
        <div class="panel input-panel">
          <div class="panel-label-row">
            <span class="panel-label">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
              Input Text
            </span>
            <div class="char-badge" :class="charBadgeClass">
              <span class="char-num">{{ text.length }}</span>
              <span class="char-sep">/</span>
              <span>3000</span>
            </div>
          </div>

          <div class="progress-track">
            <div class="progress-fill" :class="progressClass" :style="{ width: progressWidth }"></div>
          </div>

          <div class="textarea-wrap" :class="{ focused: isFocused, over: isOverLimit }">
            <textarea
              v-model="text"
              :maxlength="3000"
              placeholder="Paste or type your text here…"
              @focus="isFocused = true"
              @blur="isFocused = false"
            ></textarea>
            <button v-if="text.length > 0" class="clear-btn" @click="text = ''" title="Clear">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
          </div>

          <div class="status-row">
            <transition name="hint-fade" mode="out-in">
              <span v-if="remaining === 0" key="limit" class="hint limit">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
                Character limit reached — trim your text to continue
              </span>
              <span v-else-if="remaining <= 200" key="warning" class="hint warning">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                {{ remaining }} characters remaining
              </span>
              <span v-else-if="text.length === 0" key="idle" class="hint idle">Start typing or paste text above</span>
              <span v-else key="good" class="hint good">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                Ready · {{ wordCount }} words · ~{{ readTime }}s read
              </span>
            </transition>
          </div>
        </div>

        <!-- Action -->
        <div class="action-row">
          <button
            class="summarize-btn"
            @click="summarizeText"
            :disabled="loading || text.trim().length === 0 || isOverLimit"
          >
            <span v-if="!loading" class="btn-content">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="21" y1="10" x2="7" y2="10"/><line x1="21" y1="6" x2="3" y2="6"/><line x1="21" y1="14" x2="3" y2="14"/><line x1="21" y1="18" x2="7" y2="18"/></svg>
              Summarize
            </span>
            <span v-else class="btn-content">
              <span class="spinner"></span>
              Summarizing…
            </span>
          </button>
        </div>

        <!-- Output -->
        <transition name="panel-reveal">
          <div v-if="summary || error" class="panel output-panel" :class="{ 'is-error': error }">
            <div class="panel-label-row">
              <span class="panel-label output-label">
                <svg v-if="!error" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
                <svg v-else width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                {{ error ? 'Error' : 'Summary' }}
              </span>
              <button v-if="summary && !error" class="copy-btn" @click="copySummary" :class="{ copied }">
                <svg v-if="!copied" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
                <svg v-else width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                {{ copied ? 'Copied!' : 'Copy' }}
              </button>
            </div>
            <p class="output-text">{{ error || summary }}</p>
          </div>
        </transition>

      </div>
    </main>
  </div>
</template>

<script>
const CHAR_LIMIT = 3000;

export default {
  data() {
    return {
      text: "",
      useKey: false,
      summary: "",
      error: "",
      loading: false,
      isFocused: false,
      copied: false,
    };
  },
  computed: {
    remaining() {
      return CHAR_LIMIT - this.text.length;
    },
    isOverLimit() {
      return this.text.length >= CHAR_LIMIT;
    },
    progressWidth() {
      return Math.min((this.text.length / CHAR_LIMIT) * 100, 100) + "%";
    },
    progressClass() {
      const pct = (this.text.length / CHAR_LIMIT) * 100;
      if (pct >= 100) return "fill-limit";
      if (pct >= 80)  return "fill-warning";
      return "fill-ok";
    },
    charBadgeClass() {
      const pct = (this.text.length / CHAR_LIMIT) * 100;
      if (pct >= 100) return "badge-limit";
      if (pct >= 80)  return "badge-warning";
      return "";
    },
    wordCount() {
      return this.text.trim() ? this.text.trim().split(/\s+/).length : 0;
    },
    readTime() {
      return Math.max(1, Math.round((this.wordCount / 238) * 60));
    },
  },
  methods: {
    async summarizeText() {
      this.loading = true;
      this.summary = "";
      this.error = "";
      try {
        const res = await fetch("http://127.0.0.1:8000/summarize", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: this.text, use_key: this.useKey }),
        });
        if (!res.ok) throw new Error(`Server error ${res.status}`);
        const data = await res.json();
        this.summary = data.summary;
      } catch (err) {
        this.error = err.message || "Something went wrong. Please try again.";
      } finally {
        this.loading = false;
      }
    },
    async copySummary() {
      await navigator.clipboard.writeText(this.summary);
      this.copied = true;
      setTimeout(() => (this.copied = false), 2000);
    },
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;1,9..144,300;1,9..144,400&family=Geist:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* ── Tokens ── */
.shell {
  --cream:         #f5f0e8;
  --cream-dark:    #ede7da;
  --warm-white:    #faf8f3;
  --ink:           #1c1a17;
  --ink-muted:     #6b6358;
  --ink-faint:     #aaa195;
  --accent:        #c8502a;
  --accent-soft:   rgba(200,80,42,0.09);
  --green:         #3a7d5b;
  --amber:         #a86e00;
  --border:        rgba(28,26,23,0.09);
  --border-strong: rgba(28,26,23,0.16);

  display: flex;
  min-height: 100vh;
  background: var(--cream);
  font-family: 'Geist', sans-serif;
  color: var(--ink);
  position: relative;
}

/* Linen texture overlay */
.bg-texture {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  background-image: url("data:image/svg+xml,%3Csvg width='80' height='80' viewBox='0 0 80 80' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%231c1a17' fill-opacity='0.022' fill-rule='evenodd'%3E%3Cpath d='M0 0h40v40H0V0zm40 40h40v40H40V40z'/%3E%3C/g%3E%3C/svg%3E");
}

/* ── Sidebar ── */
.sidebar {
  width: 240px;
  flex-shrink: 0;
  background: var(--cream-dark);
  border-right: 1px solid var(--border-strong);
  display: flex;
  flex-direction: column;
  padding: 2rem 1.6rem;
  position: sticky;
  top: 0;
  height: 100vh;
  z-index: 10;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.55rem;
  margin-bottom: 2.75rem;
}

.brand-name {
  font-family: 'Fraunces', serif;
  font-size: 1.25rem;
  font-weight: 500;
  letter-spacing: -0.02em;
  color: var(--ink);
}

.sidebar-content { flex: 1; }

.sidebar-tagline {
  font-size: 0.84rem;
  line-height: 1.7;
  color: var(--ink-muted);
  font-weight: 300;
  margin-bottom: 2rem;
  padding-left: 0.9rem;
  border-left: 2px solid var(--accent);
}

.sidebar-meta {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.55rem;
  font-size: 0.78rem;
  color: var(--ink-muted);
}

.meta-item svg { color: var(--accent); flex-shrink: 0; }

.sidebar-footer {
  font-size: 0.68rem;
  letter-spacing: 0.05em;
  color: var(--ink-faint);
  border-top: 1px solid var(--border);
  padding-top: 1.25rem;
}

/* ── Main ── */
.main {
  flex: 1;
  padding: 3rem 3.5rem 5rem;
  position: relative;
  z-index: 1;
}

.main-inner {
  max-width: 660px;
  display: flex;
  flex-direction: column;
  gap: 1.4rem;
}

/* ── Topbar ── */
.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 0.25rem;
}

.page-title {
  font-family: 'Fraunces', serif;
  font-size: 2rem;
  font-weight: 400;
  letter-spacing: -0.03em;
  color: var(--ink);
  line-height: 1;
}

/* ── Toggle ── */
.api-toggle {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.78rem;
  color: var(--ink-muted);
  cursor: pointer;
  user-select: none;
}

.toggle-track {
  width: 32px;
  height: 17px;
  border-radius: 9px;
  background: var(--cream);
  border: 1px solid var(--border-strong);
  position: relative;
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s;
  flex-shrink: 0;
}

.api-toggle.active .toggle-track {
  background: var(--accent);
  border-color: var(--accent);
}

.toggle-thumb {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 11px;
  height: 11px;
  border-radius: 50%;
  background: var(--ink-faint);
  transition: transform 0.2s, background 0.2s;
}

.api-toggle.active .toggle-thumb {
  transform: translateX(15px);
  background: #fff;
}

/* ── Panel ── */
.panel {
  background: var(--warm-white);
  border: 1px solid var(--border-strong);
  border-radius: 12px;
  padding: 1.5rem 1.75rem;
  box-shadow: 0 1px 3px rgba(28,26,23,0.06), 0 1px 2px rgba(28,26,23,0.03);
}

.panel-label-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.9rem;
}

.panel-label {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.66rem;
  font-weight: 500;
  letter-spacing: 0.13em;
  text-transform: uppercase;
  color: var(--ink-muted);
}

/* ── Char badge ── */
.char-badge {
  display: flex;
  align-items: center;
  gap: 1px;
  font-size: 0.72rem;
  font-variant-numeric: tabular-nums;
  color: var(--ink-faint);
  transition: color 0.25s;
}
.char-badge.badge-warning { color: var(--amber); }
.char-badge.badge-limit   { color: var(--accent); font-weight: 600; }
.char-num  { font-weight: 500; }
.char-sep  { margin: 0 1px; opacity: 0.45; }

/* ── Progress ── */
.progress-track {
  height: 2px;
  background: var(--border);
  border-radius: 2px;
  margin-bottom: 1rem;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.12s ease, background 0.3s;
}

.fill-ok      { background: var(--green); }
.fill-warning { background: var(--amber); }
.fill-limit   { background: var(--accent); }

/* ── Textarea ── */
.textarea-wrap {
  position: relative;
  border: 1px solid var(--border-strong);
  border-radius: 8px;
  background: #fff;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.textarea-wrap.focused {
  border-color: rgba(200,80,42,0.4);
  box-shadow: 0 0 0 3px var(--accent-soft);
}

textarea {
  display: block;
  width: 100%;
  min-height: 200px;
  background: transparent;
  border: none;
  outline: none;
  resize: vertical;
  font-family: 'Geist', sans-serif;
  font-size: 0.9rem;
  font-weight: 300;
  line-height: 1.75;
  color: var(--ink);
  padding: 1rem 2.5rem 1rem 1.1rem;
  border-radius: 8px;
}

textarea::placeholder { color: var(--ink-faint); }

.clear-btn {
  position: absolute;
  top: 0.6rem;
  right: 0.6rem;
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: 1px solid transparent;
  border-radius: 5px;
  color: var(--ink-faint);
  cursor: pointer;
  transition: color 0.15s, background 0.15s, border-color 0.15s;
}
.clear-btn:hover {
  color: var(--ink-muted);
  background: var(--cream-dark);
  border-color: var(--border);
}

/* ── Status ── */
.status-row {
  min-height: 1.5rem;
  margin-top: 0.65rem;
}

.hint {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.75rem;
}

.hint.idle    { color: var(--ink-faint); }
.hint.good    { color: var(--green); }
.hint.warning { color: var(--amber); }
.hint.limit   { color: var(--accent); font-weight: 500; }

.hint-fade-enter-active,
.hint-fade-leave-active { transition: opacity 0.18s, transform 0.18s; }
.hint-fade-enter-from   { opacity: 0; transform: translateY(3px); }
.hint-fade-leave-to     { opacity: 0; }

/* ── Action ── */
.action-row { display: flex; align-items: center; gap: 1rem; }

.summarize-btn {
  background: var(--accent);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.72rem 1.6rem;
  font-family: 'Geist', sans-serif;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.15s, transform 0.12s, opacity 0.2s, box-shadow 0.15s;
  box-shadow: 0 1px 4px rgba(200,80,42,0.3);
  letter-spacing: 0.01em;
}

.summarize-btn:hover:not(:disabled) {
  background: #b34422;
  transform: translateY(-1px);
  box-shadow: 0 4px 14px rgba(200,80,42,0.3);
}
.summarize-btn:active:not(:disabled) { transform: translateY(0); }
.summarize-btn:disabled { opacity: 0.38; cursor: not-allowed; }

.btn-content {
  display: flex;
  align-items: center;
  gap: 0.45rem;
}

.spinner {
  width: 13px;
  height: 13px;
  border: 2px solid rgba(255,255,255,0.28);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.65s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ── Output ── */
.output-panel {
  border-left: 3px solid var(--green);
}
.output-panel.is-error { border-left-color: var(--accent); }

.output-label { color: var(--green) !important; }
.output-panel.is-error .output-label { color: var(--accent) !important; }

.copy-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.7rem;
  font-weight: 500;
  font-family: 'Geist', sans-serif;
  background: none;
  border: 1px solid var(--border-strong);
  border-radius: 5px;
  color: var(--ink-muted);
  cursor: pointer;
  padding: 0.22rem 0.6rem;
  transition: color 0.15s, border-color 0.15s, background 0.15s;
}
.copy-btn:hover, .copy-btn.copied {
  color: var(--green);
  border-color: rgba(58,125,91,0.3);
  background: rgba(58,125,91,0.06);
}

.output-text {
  font-size: 0.92rem;
  line-height: 1.82;
  color: var(--ink);
  font-weight: 300;
}

/* ── Transition ── */
.panel-reveal-enter-active {
  transition: opacity 0.32s ease, transform 0.32s ease;
}
.panel-reveal-enter-from {
  opacity: 0;
  transform: translateY(8px);
}

/* ── Responsive ── */
@media (max-width: 720px) {
  .sidebar { display: none; }
  .main { padding: 1.5rem 1.25rem 4rem; }
  .topbar {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.85rem;
  }
}
</style>