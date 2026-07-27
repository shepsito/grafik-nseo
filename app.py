<!DOCTYPE html>
<html lang="bg">
<head>
  <meta charset="UTF-8">
  <title>График НСЕО</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { background:#0b0b13; color:#eee; font-family:system-ui; margin:0; padding:10px; }
    h2 { margin-top:20px; color: #aaa; font-size: 1.2em; letter-spacing: 2px; }
    .card { background:#1a1a24; padding:10px; margin:8px 0; border-radius:8px; border-left: 3px solid #444; }
    .card:hover { background:#222233; }
    .title { font-weight:bold; color: #fff; }
    .small { color:#aaa; font-size:0.9em; }
    .shift-1 { border-left-color: #ff6b6b; background: #1a1a2e; }
    .shift-1 .title { color: #ff6b6b; }
    .shift-2 { border-left-color: #4ecdc4; background: #1a2a2a; }
    .shift-2 .title { color: #4ecdc4; }
    .shift-3 { border-left-color: #ffe66d; background: #2a2a1a; }
    .shift-3 .title { color: #ffe66d; }
    .empty { color: #555; font-style: italic; padding: 15px 10px; }
  </style>
</head>
<body>

  <h2>📅 МИНАЛИ</h2>
  <div id="past"></div>

  <h2>📅 ДНЕС</h2>
  <div id="today"></div>

  <h2>📅 СЛЕДВАЩИ</h2>
  <div id="next"></div>

  <script>
    const API_BASE = '';

    function parseBBCode(text) {
      if (!text) return '';
      return text.replace(/\[color=([0-9a-fA-F]{6})\](.*?)\[\/color\]/g, function(match, color, content) {
        return `<span style="color: #${color}">${content}</span>`;
      });
    }

    function formatBG(dateString) {
      const d = new Date(dateString);
      const day = d.getDate();
      const months = ["януари","февруари","март","април","май","юни","юли","август","септември","октомври","ноември","декември"];
      const month = months[d.getMonth()];
      const hours = String(d.getHours()).padStart(2, "0");
      const minutes = String(d.getMinutes()).padStart(2, "0");
      return `${day} ${month}, ${hours}:${minutes}`;
    }

    function getShiftClass(shift) {
      if (shift.includes('Смяна 1')) return 'shift-1';
      if (shift.includes('Смяна 2')) return 'shift-2';
      if (shift.includes('Смяна 3')) return 'shift-3';
      return '';
    }

    function renderEvent(ev) {
      const div = document.createElement("div");
      const shiftClass = getShiftClass(ev.shift);
      div.className = `card ${shiftClass}`;
      
      const titleHtml = parseBBCode(ev.title);
      const descHtml = parseBBCode(ev.description || '');
      const timeDisplay = ev.formatted_time || formatBG(ev.datetime);
      
      div.innerHTML = `
        <div class="title">${titleHtml}</div>
        <div class="small">${timeDisplay} | ${ev.shift} | ${ev.facility}</div>
        <div class="small">${descHtml}</div>
      `;
      return div;
    }

    async function loadToday() {
      try {
        const res = await fetch(`${API_BASE}/api/events/today`);
        const data = await res.json();
        const box = document.getElementById("today");
        box.innerHTML = "";
        if (!data || !data.length) {
          box.innerHTML = "<div class='empty'>✅ Няма събития за днес</div>";
          return;
        }
        data.forEach(ev => {
          box.appendChild(renderEvent(ev));
        });
      } catch (error) {
        console.error('Грешка:', error);
        document.getElementById("today").innerHTML = "<div class='empty'>❌ Грешка при зареждане</div>";
      }
    }

    async function loadNext() {
      try {
        const res = await fetch(`${API_BASE}/api/events/next`);
        const data = await res.json();
        const box = document.getElementById("next");
        box.innerHTML = "";
        if (!data || !data.length) {
          box.innerHTML = "<div class='empty'>Няма предстоящи събития</div>";
          return;
        }
        data.forEach(ev => {
          box.appendChild(renderEvent(ev));
        });
      } catch (error) {
        console.error('Грешка:', error);
        document.getElementById("next").innerHTML = "<div class='empty'>Грешка при зареждане</div>";
      }
    }

    async function loadPast() {
      try {
        const res = await fetch(`${API_BASE}/api/events/past`);
        const data = await res.json();
        const box = document.getElementById("past");
        box.innerHTML = "";
        if (!data || !data.length) {
          box.innerHTML = "<div class='empty'>Няма минали събития</div>";
          return;
        }
        data.forEach(ev => {
          box.appendChild(renderEvent(ev));
        });
      } catch (error) {
        console.error('Грешка:', error);
        document.getElementById("past").innerHTML = "<div class='empty'>Грешка при зареждане</div>";
      }
    }

    loadPast();
    loadToday();
    loadNext();

    setInterval(() => {
      loadPast();
      loadToday();
      loadNext();
    }, 60000);
  </script>
</body>
</html>
