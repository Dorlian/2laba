/**
 * Глобальный плеер + очередь: воспроизведение не прерывается при переходах (Turbo Drive).
 * Элемент #ph-global-dock помечен data-turbo-permanent.
 */
(function () {
  var STORAGE_PLAYLIST = "ph_playlist_name";
  var STORAGE_QUEUE = "ph_queue";
  var STORAGE_INDEX = "ph_queue_index";

  function getGlobalAudio() {
    return document.getElementById("ph-global-audio");
  }

  function syncHeader() {
    var el = document.getElementById("header-now-playing");
    if (!el) return;
    var name = sessionStorage.getItem(STORAGE_PLAYLIST);
    var prefix = window.__PH && window.__PH.prefix ? window.__PH.prefix : "";
    if (name) {
      el.textContent = prefix + " " + name;
      el.hidden = false;
    } else {
      el.textContent = "";
      el.hidden = true;
    }
  }

  function updateMiniLabel(text) {
    var el = document.getElementById("mini-player-track");
    if (el) el.textContent = text || "";
  }

  function bindGlobalEndedOnce() {
    var g = getGlobalAudio();
    if (!g || g.dataset.phBound) return;
    g.dataset.phBound = "1";
    g.addEventListener("ended", function () {
      var q = [];
      try {
        q = JSON.parse(sessionStorage.getItem(STORAGE_QUEUE) || "[]");
      } catch (e) {
        return;
      }
      var idx = parseInt(sessionStorage.getItem(STORAGE_INDEX) || "0", 10) + 1;
      if (idx >= q.length || !q[idx]) return;
      sessionStorage.setItem(STORAGE_INDEX, String(idx));
      var item = q[idx];
      g.src = item.src;
      updateMiniLabel(item.label || "");
      g.play().catch(function () {});
    });
  }

  function onPlayCapture(e) {
    var t = e.target;
    if (t.tagName !== "AUDIO") return;
    if (t.id === "ph-global-audio") return;
    if (!t.classList.contains("ph-audio")) return;
    t.pause();
    t.currentTime = 0;
    var g = getGlobalAudio();
    if (!g) return;
    var src = t.currentSrc || t.src;
    if (!src) return;
    var label = t.getAttribute("data-label") || "";
    var one = [{ src: src, label: label }];
    sessionStorage.setItem(STORAGE_QUEUE, JSON.stringify(one));
    sessionStorage.setItem(STORAGE_INDEX, "0");
    if (g.src !== src) {
      g.src = src;
    }
    updateMiniLabel(label);
    if (document.querySelector(".data-table")) {
      var cat = window.__PH && window.__PH.catalogLabel;
      if (cat) sessionStorage.setItem(STORAGE_PLAYLIST, cat);
    }
    syncHeader();
    g.play().catch(function () {});
  }

  document.addEventListener("play", onPlayCapture, true);

  document.addEventListener("click", function (e) {
    var btn = e.target.closest("#js-play-order");
    if (!btn) return;
    e.preventDefault();
    var players = Array.prototype.slice.call(
      document.querySelectorAll(".track-item__player.ph-audio")
    );
    if (!players.length) {
      players = Array.prototype.slice.call(
        document.querySelectorAll(".track-item__player")
      );
    }
    var q = players.map(function (p) {
      return {
        src: p.src || p.currentSrc,
        label: p.getAttribute("data-label") || "",
      };
    }).filter(function (x) { return x.src; });
    if (!q.length) return;
    sessionStorage.setItem(STORAGE_QUEUE, JSON.stringify(q));
    sessionStorage.setItem(STORAGE_INDEX, "0");
    var h1 = document.querySelector(".detail .page-title");
    if (h1) {
      sessionStorage.setItem(STORAGE_PLAYLIST, h1.textContent.trim());
    }
    syncHeader();
    var g = getGlobalAudio();
    if (!g) return;
    g.src = q[0].src;
    updateMiniLabel(q[0].label);
    g.play().catch(function () {});
  });

  function boot() {
    bindGlobalEndedOnce();
    var title = document.querySelector(".detail .page-title");
    if (title) {
      sessionStorage.setItem(STORAGE_PLAYLIST, title.textContent.trim());
    }
    syncHeader();
  }

  if (window.Turbo) {
    document.addEventListener("turbo:load", boot);
  } else {
    document.addEventListener("DOMContentLoaded", boot);
  }
})();
