const queryEl = document.getElementById('query');
const sendBtn = document.getElementById('send');
const historyBtn = document.getElementById('history');
const statusEl = document.getElementById('status');
const resultEl = document.getElementById('result');
const graphStepEl = document.getElementById('graphStep');
const historyEl = document.getElementById('historyBox');
let stepPoller = null;

async function refreshGraphStatus() {
  const response = await fetch('/graph-status');
  if (!response.ok) {
    return;
  }
  const data = await response.json();
  const timelineText = (data.timeline || []).join('\n');
  graphStepEl.textContent = `Current: ${data.current_step || 'unknown'}\n\nTimeline:\n${timelineText || 'No steps yet.'}`;
}

function startGraphPolling() {
  if (stepPoller) {
    clearInterval(stepPoller);
  }
  stepPoller = setInterval(() => {
    refreshGraphStatus().catch(() => {});
  }, 700);
}

function stopGraphPolling() {
  if (stepPoller) {
    clearInterval(stepPoller);
    stepPoller = null;
  }
}

async function submitQuery() {
  const query = queryEl.value.trim();
  if (!query) {
    statusEl.textContent = 'Please enter a query.';
    return;
  }

  sendBtn.disabled = true;
  statusEl.textContent = 'Running...';
  resultEl.textContent = 'Working on your request...';
  graphStepEl.textContent = 'Initializing graph status...';
  startGraphPolling();

  try {
    const response = await fetch('/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query })
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(errorText || 'Request failed');
    }

    const data = await response.json();
    resultEl.textContent = data.answer;
    await refreshGraphStatus();
    statusEl.textContent = 'Done';
  } catch (err) {
    resultEl.textContent = 'Error: ' + err.message;
    statusEl.textContent = 'Failed';
  } finally {
    stopGraphPolling();
    sendBtn.disabled = false;
  }
}

async function loadHistory() {
  historyBtn.disabled = true;
  statusEl.textContent = 'Loading history...';

  try {
    const response = await fetch('/history?limit=10');
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(errorText || 'Failed to load history');
    }

    const rows = await response.json();
    if (!rows.length) {
      historyEl.textContent = 'No history found yet.';
      statusEl.textContent = 'Done';
      return;
    }

    historyEl.textContent = rows
      .map((row, idx) => `${idx + 1}. Created: ${row.created_at}\nQuery: ${row.query}\nAnswer: ${row.answer}`)
      .join('\n\n');
    statusEl.textContent = 'Done';
  } catch (err) {
    historyEl.textContent = 'Error: ' + err.message;
    statusEl.textContent = 'Failed';
  } finally {
    historyBtn.disabled = false;
  }
}

sendBtn.addEventListener('click', submitQuery);
historyBtn.addEventListener('click', loadHistory);
