<template>
  <div>
    <h2>Text Summarizer</h2>
    <textarea v-model="text" rows="10" cols="50" placeholder="Paste text here..."></textarea>
    <br>
    <label>
      Use my API key: <input type="checkbox" v-model="useKey" />
    </label>
    <br>
    <button @click="summarizeText">Summarize</button>
    <h3>Summary:</h3>
    <p>{{ summary }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      text: "",
      useKey: false,
      summary: ""
    };
  },
  methods: {
    async summarizeText() {
      const res = await fetch("http://127.0.0.1:8000/summarize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: this.text, use_key: this.useKey })
      });
      const data = await res.json();
      this.summary = data.summary;
    }
  }
};
</script>