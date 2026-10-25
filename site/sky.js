/**
 * ARTIFICIAL CIVILIZATION LABORATORY (ACL)
 * Cinematic Atmosphere & Living Sky Engine
 * 
 * "Night sky, a single light, a lone figure on a horizon."
 */

(function () {
  "use strict";

  var reducedMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // PRNG for consistent, beautiful starfield across refreshes
  function createSeededRNG(seed) {
    var s = seed;
    return function () {
      s = (s * 16807) % 2147483647;
      return s / 2147483647;
    };
  }

  // Smooth easing helpers
  function easeInOutCubic(x) {
    return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
  }
  function clamp(val, min, max) {
    return Math.max(min, Math.min(max, val));
  }

  // Global mouse state for interactive parallax & constellations
  var mouse = {
    x: -9999,
    y: -9999,
    targetX: 0,
    targetY: 0,
    currentX: 0,
    currentY: 0,
    active: false,
    lastMoved: 0
  };

  window.addEventListener("mousemove", function (e) {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
    // Normalized [-1, 1] relative to viewport center
    mouse.targetX = (e.clientX / window.innerWidth) * 2 - 1;
    mouse.targetY = (e.clientY / window.innerHeight) * 2 - 1;
    mouse.active = true;
    mouse.lastMoved = performance.now();
  }, { passive: true });

  window.addEventListener("mouseleave", function () {
    mouse.active = false;
    mouse.targetX = 0;
    mouse.targetY = 0;
  });

  // =========================================================================
  // 1. GLOBAL NIGHT SKY (#sky)
  // =========================================================================
  var skyCanvas = document.createElement("canvas");
  skyCanvas.id = "sky";
  document.body.prepend(skyCanvas);

  var sCtx = skyCanvas.getContext("2d");
  var sW = 0, sH = 0, sDPR = 1;
  var stars = [];
  var nebulae = [];
  var meteors = [];
  var lastMeteorTime = performance.now();
  var nebulaLayer = null;

  function initSky() {
    sDPR = 1;                                   // smoothness: a full-screen sky at 1x is enough for soft stars
    sW = window.innerWidth;
    sH = window.innerHeight;
    skyCanvas.width = sW * sDPR;
    skyCanvas.height = sH * sDPR;
    sCtx.setTransform(sDPR, 0, 0, sDPR, 0, 0);

    var rng = createSeededRNG(20261022);
    var starCount = Math.round((sW * sH) / 6500);
    starCount = Math.max(120, Math.min(320, starCount));

    stars = [];
    for (var i = 0; i < starCount; i++) {
      var depth = rng(); // 0 = far, 1 = near
      var typeRoll = rng();
      var colorType = "white"; // default
      if (typeRoll < 0.22) colorType = "gold";
      else if (typeRoll < 0.50) colorType = "cyan";

      stars.push({
        x: rng() * sW,
        y: rng() * sH,
        baseX: 0,
        baseY: 0,
        radius: depth > 0.8 ? (rng() * 1.2 + 0.9) : (rng() * 0.9 + 0.35),
        depth: depth * 0.8 + 0.2, // parallax weight
        twinkleSpeed: rng() * 0.0018 + 0.0006,
        twinklePhase: rng() * Math.PI * 2,
        baseAlpha: rng() * 0.45 + 0.25,
        colorType: colorType
      });
    }

    // Soft celestial atmospheric clouds (nebulae)
    nebulae = [
      { x: sW * 0.25, y: sH * 0.2, r: Math.max(sW, sH) * 0.35, color: "rgba(18, 32, 64, 0.12)" },
      { x: sW * 0.75, y: sH * 0.4, r: Math.max(sW, sH) * 0.42, color: "rgba(28, 20, 52, 0.09)" },
      { x: sW * 0.5, y: sH * 0.85, r: Math.max(sW, sH) * 0.38, color: "rgba(14, 28, 56, 0.14)" }
    ];
    // The clouds never move: paint them once, then copy the picture each frame (much cheaper than 3 big gradients).
    nebulaLayer = document.createElement("canvas");
    nebulaLayer.width = sW;
    nebulaLayer.height = sH;
    var nCtx = nebulaLayer.getContext("2d");
    for (var n = 0; n < nebulae.length; n++) {
      var neb = nebulae[n];
      var g = nCtx.createRadialGradient(neb.x, neb.y, 0, neb.x, neb.y, neb.r);
      g.addColorStop(0, neb.color);
      g.addColorStop(1, "rgba(3, 5, 9, 0)");
      nCtx.fillStyle = g;
      nCtx.beginPath();
      nCtx.arc(neb.x, neb.y, neb.r, 0, Math.PI * 2);
      nCtx.fill();
    }
  }

  function spawnMeteor(now) {
    if (reducedMotion) return;
    var startX = Math.random() * sW * 0.8 + sW * 0.1;
    var startY = Math.random() * sH * 0.35;
    var angle = Math.PI * (0.18 + Math.random() * 0.08); // downward gentle streak
    var speed = 900 + Math.random() * 500;
    var length = 110 + Math.random() * 90;

    meteors.push({
      x: startX,
      y: startY,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed,
      len: length,
      alpha: 1,
      decay: 0.8 + Math.random() * 0.4,
      born: now
    });
  }

  function drawSky(time) {
    if (!sW || !sH) initSky();
    sCtx.clearRect(0, 0, sW, sH);

    var scrollY = window.pageYOffset || document.documentElement.scrollTop || 0;

    // 1. Atmospheric nebulae (painted once in initSky)
    if (nebulaLayer) sCtx.drawImage(nebulaLayer, 0, 0, sW, sH);

    // 2. Stars rendering with parallax & twinkling
    var pX = mouse.currentX * 14;
    var pY = mouse.currentY * 10;

    for (var i = 0; i < stars.length; i++) {
      var s = stars[i];
      // Parallax offset based on depth & scroll
      var sx = s.x + pX * s.depth;
      var sy = (s.y - scrollY * (s.depth * 0.22) + pY * s.depth) % sH;
      if (sy < 0) sy += sH;

      // Twinkle calculation
      var twinkle = reducedMotion ? 1 : 0.5 + 0.5 * Math.sin(time * s.twinkleSpeed + s.twinklePhase);
      var alpha = clamp(s.baseAlpha * twinkle, 0.08, 0.98);

      var fillCol;
      if (s.colorType === "gold") {
        fillCol = "rgba(255, 218, 160, " + alpha.toFixed(3) + ")";
      } else if (s.colorType === "cyan") {
        fillCol = "rgba(180, 220, 255, " + alpha.toFixed(3) + ")";
      } else {
        fillCol = "rgba(235, 244, 255, " + alpha.toFixed(3) + ")";
      }

      sCtx.fillStyle = fillCol;
      sCtx.beginPath();
      sCtx.arc(sx, sy, s.radius, 0, Math.PI * 2);
      sCtx.fill();

      // Subtle diamond star halo on bright near stars
      if (s.radius > 1.2 && alpha > 0.65) {
        sCtx.strokeStyle = "rgba(180, 215, 255, " + (alpha * 0.35).toFixed(3) + ")";
        sCtx.lineWidth = 0.75;
        sCtx.beginPath();
        sCtx.moveTo(sx - 3.5, sy);
        sCtx.lineTo(sx + 3.5, sy);
        sCtx.moveTo(sx, sy - 3.5);
        sCtx.lineTo(sx, sy + 3.5);
        sCtx.stroke();
      }
    }

    // 3. Interactive Constellation Web (emergent connection around mouse)
    if (mouse.active && !reducedMotion) {
      var maxDist = 135;
      var closeStars = [];

      for (var k = 0; k < stars.length; k++) {
        var st = stars[k];
        var cx = st.x + pX * st.depth;
        var cy = (st.y - scrollY * (st.depth * 0.22) + pY * st.depth) % sH;
        if (cy < 0) cy += sH;

        var dx = cx - mouse.x;
        var dy = cy - mouse.y;
        var d2 = dx * dx + dy * dy;

        if (d2 < maxDist * maxDist) {
          var dist = Math.sqrt(d2);
          closeStars.push({ x: cx, y: cy, dist: dist });
          // Line from star to cursor
          var cAlpha = (1 - dist / maxDist) * 0.38;
          sCtx.strokeStyle = "rgba(165, 205, 255, " + cAlpha.toFixed(3) + ")";
          sCtx.lineWidth = 0.75;
          sCtx.beginPath();
          sCtx.moveTo(cx, cy);
          sCtx.lineTo(mouse.x, mouse.y);
          sCtx.stroke();
        }
      }

      // Connect neighbor stars in cluster
      for (var a = 0; a < closeStars.length; a++) {
        for (var b = a + 1; b < closeStars.length; b++) {
          var ndx = closeStars[a].x - closeStars[b].x;
          var ndy = closeStars[a].y - closeStars[b].y;
          var nd = Math.sqrt(ndx * ndx + ndy * ndy);
          if (nd < 95) {
            var nAlpha = (1 - nd / 95) * 0.22;
            sCtx.strokeStyle = "rgba(255, 215, 160, " + nAlpha.toFixed(3) + ")";
            sCtx.lineWidth = 0.6;
            sCtx.beginPath();
            sCtx.moveTo(closeStars[a].x, closeStars[a].y);
            sCtx.lineTo(closeStars[b].x, closeStars[b].y);
            sCtx.stroke();
          }
        }
      }
    }

    // 4. Meteors / Shooting Stars
    if (!reducedMotion) {
      if (time - lastMeteorTime > 7500 + Math.random() * 5500) {
        spawnMeteor(time);
        lastMeteorTime = time;
      }

      for (var m = meteors.length - 1; m >= 0; m--) {
        var met = meteors[m];
        var age = (time - met.born) / 1000;
        met.alpha = 1 - age * met.decay;

        if (met.alpha <= 0) {
          meteors.splice(m, 1);
          continue;
        }

        var speedDt = 0.016; // approximate dt
        met.x += met.vx * speedDt;
        met.y += met.vy * speedDt;

        var headX = met.x;
        var headY = met.y;
        var tailX = met.x - (met.vx / 1000) * met.len;
        var tailY = met.y - (met.vy / 1000) * met.len;

        var mg = sCtx.createLinearGradient(headX, headY, tailX, tailY);
        mg.addColorStop(0, "rgba(255, 255, 255, " + (met.alpha * 0.95).toFixed(3) + ")");
        mg.addColorStop(0.3, "rgba(180, 220, 255, " + (met.alpha * 0.6).toFixed(3) + ")");
        mg.addColorStop(1, "rgba(180, 220, 255, 0)");

        sCtx.strokeStyle = mg;
        sCtx.lineWidth = 1.4;
        sCtx.beginPath();
        sCtx.moveTo(headX, headY);
        sCtx.lineTo(tailX, tailY);
        sCtx.stroke();
      }
    }
  }

  // =========================================================================
  // 2. CINEMATIC HERO SCENE (Home Page Canvas)
  // "Night sky, a single light, a lone figure on a horizon"
  // =========================================================================
  var heroCanvas = document.querySelector(".hero .scene canvas");
  var hCtx = null;
  var hW = 0, hH = 0, hDPR = 1;
  var heroStartTime = null;

  // Particle System: Rising Campfire Sparks & Embers
  var embers = [];
  var MAX_EMBERS = 42;

  function initEmbers(originX, originY) {
    embers = [];
    for (var i = 0; i < MAX_EMBERS; i++) {
      embers.push(createEmber(originX, originY, true));
    }
  }

  function createEmber(originX, originY, prewarm) {
    var pAge = prewarm ? Math.random() : 0;
    return {
      x: originX + (Math.random() - 0.5) * 12,
      y: originY + (Math.random() - 0.5) * 4,
      vx: (Math.random() - 0.35) * 18, // gentle drift rightward
      vy: -(Math.random() * 32 + 22),  // buoyant upward
      size: Math.random() * 1.8 + 0.8,
      life: Math.random() * 2.2 + 1.2,
      age: pAge * 2,
      phase: Math.random() * Math.PI * 2
    };
  }

  function initHero() {
    if (!heroCanvas) return;
    hDPR = Math.min(window.devicePixelRatio || 1, 1.5);
    hW = heroCanvas.clientWidth;
    hH = heroCanvas.clientHeight;
    heroCanvas.width = hW * hDPR;
    heroCanvas.height = hH * hDPR;
    hCtx = heroCanvas.getContext("2d");
    hCtx.setTransform(hDPR, 0, 0, hDPR, 0, 0);

    var fireX = hW * 0.42;
    var fireY = hH * 0.84;
    initEmbers(fireX, fireY);
  }

  function drawHero(now) {
    if (!heroCanvas || !hCtx) return;
    if (!hW || !hH) initHero();

    hCtx.clearRect(0, 0, hW, hH);

    if (heroStartTime === null) heroStartTime = now;
    var elapsed = reducedMotion ? 99 : (now - heroStartTime) / 1000;

    // Smooth entry phases
    var pAwaken = easeInOutCubic(clamp(elapsed / 1.0, 0, 1));
    var pHorizon = easeInOutCubic(clamp((elapsed - 0.7) / 1.5, 0, 1));
    var pLandscape = easeInOutCubic(clamp((elapsed - 1.5) / 1.6, 0, 1));
    var pFigure = easeInOutCubic(clamp((elapsed - 2.5) / 1.4, 0, 1));

    // Interactive camera / parallax
    var camX = mouse.currentX * 18;
    var camY = mouse.currentY * 8;

    var cy = hH * 0.81; // Base horizon line (low, so the title sits in the sky above)
    var fireX = hW * 0.43 + camX * 0.8;
    var fireY = cy - 2;

    // -----------------------------------------------------------------------
    // A. The Sky & Distant Atmosphere
    // -----------------------------------------------------------------------
    var skyGrad = hCtx.createLinearGradient(0, 0, 0, hH);
    skyGrad.addColorStop(0, "rgba(4, 7, 16, 0)");       // open at the top: the page's stars show through
    skyGrad.addColorStop(0.55, "rgba(10, 18, 38, 0.45)");
    skyGrad.addColorStop(0.75, "rgba(18, 32, 62, 0.85)");
    skyGrad.addColorStop(1, "rgba(5, 8, 15, 1)");
    hCtx.fillStyle = skyGrad;
    hCtx.fillRect(0, 0, hW, hH);

    // -----------------------------------------------------------------------
    // B. Distant Mountain Headlands (Mid-Horizon Layer)
    // -----------------------------------------------------------------------
    if (pLandscape > 0) {
      hCtx.save();
      var mAlpha = 0.55 * pLandscape;
      hCtx.fillStyle = "rgba(14, 24, 46, " + mAlpha.toFixed(3) + ")";
      hCtx.beginPath();
      hCtx.moveTo(0, cy + 2);
      for (var x = 0; x <= hW; x += 12) {
        var mNorm = x / hW;
        var my = cy - 22 * Math.sin(mNorm * 3.4 + 0.4) - 10 * Math.sin(mNorm * 8.2);
        hCtx.lineTo(x + camX * 0.3, my);
      }
      hCtx.lineTo(hW, hH);
      hCtx.lineTo(0, hH);
      hCtx.closePath();
      hCtx.fill();
      hCtx.restore();
    }

    // -----------------------------------------------------------------------
    // C. The Infinite Ocean & Horizon Seam
    // -----------------------------------------------------------------------
    if (pHorizon > 0) {
      hCtx.save();
      // The ocean plane
      var oceanGrad = hCtx.createLinearGradient(0, cy, 0, hH);
      oceanGrad.addColorStop(0, "rgba(6, 12, 24, " + (0.9 * pHorizon).toFixed(3) + ")");
      oceanGrad.addColorStop(0.4, "rgba(4, 8, 16, 0.96)");
      oceanGrad.addColorStop(1, "rgba(2, 4, 8, 1)");
      hCtx.fillStyle = oceanGrad;
      hCtx.fillRect(0, cy, hW, hH - cy);

      // Shimmering horizon light beam
      var horizSpan = pHorizon * hW * 0.52;
      var cx = hW * 0.5 + camX * 0.2;
      var hBeam = hCtx.createLinearGradient(cx - horizSpan, 0, cx + horizSpan, 0);
      hBeam.addColorStop(0, "rgba(155, 194, 255, 0)");
      hBeam.addColorStop(0.35, "rgba(155, 194, 255, 0.45)");
      hBeam.addColorStop(0.5, "rgba(235, 245, 255, 0.85)");
      hBeam.addColorStop(0.65, "rgba(155, 194, 255, 0.45)");
      hBeam.addColorStop(1, "rgba(155, 194, 255, 0)");

      hCtx.strokeStyle = hBeam;
      hCtx.lineWidth = 1.2;
      hCtx.shadowColor = "#9bc2ff";
      hCtx.shadowBlur = 12 * pHorizon;
      hCtx.beginPath();
      hCtx.moveTo(cx - horizSpan, cy);
      hCtx.lineTo(cx + horizSpan, cy);
      hCtx.stroke();
      hCtx.shadowBlur = 0;

      // Faint water shimmer streaks below horizon
      var waterFlicker = reducedMotion ? 0.3 : (0.25 + 0.1 * Math.sin(now * 0.002));
      hCtx.strokeStyle = "rgba(155, 194, 255, " + (waterFlicker * pHorizon).toFixed(3) + ")";
      hCtx.lineWidth = 0.8;
      for (var w = 1; w <= 4; w++) {
        var wy = cy + w * 6;
        var wLen = horizSpan * (0.8 - w * 0.15);
        hCtx.beginPath();
        hCtx.moveTo(cx - wLen, wy);
        hCtx.lineTo(cx + wLen, wy);
        hCtx.stroke();
      }
      hCtx.restore();
    }

    // -----------------------------------------------------------------------
    // D. Foreground Rocky Island Bluff
    // -----------------------------------------------------------------------
    if (pLandscape > 0) {
      hCtx.save();
      var fAlpha = pLandscape;
      var rockGrad = hCtx.createLinearGradient(0, cy - 30, 0, hH);
      rockGrad.addColorStop(0, "rgba(10, 16, 28, " + fAlpha + ")");
      rockGrad.addColorStop(0.5, "rgba(6, 10, 18, " + fAlpha + ")");
      rockGrad.addColorStop(1, "rgba(2, 4, 8, " + fAlpha + ")");

      hCtx.fillStyle = rockGrad;
      hCtx.beginPath();
      hCtx.moveTo(0, hH);
      // Left crag descending into sea
      hCtx.lineTo(0, cy + 8);
      for (var rx = 0; rx <= hW * 0.65; rx += 8) {
        var rNorm = rx / (hW * 0.65);
        // Island bluff profile: rises to a rocky promontory where fire & person are
        var ry = cy + 6 - 28 * Math.sin(rNorm * Math.PI * 0.85) - 4 * Math.sin(rNorm * 18);
        hCtx.lineTo(rx + camX * 0.7, ry);
      }
      hCtx.lineTo(hW * 0.68 + camX * 0.7, cy + 24);
      hCtx.lineTo(hW * 0.75 + camX * 0.7, hH);
      hCtx.closePath();
      hCtx.fill();
      hCtx.restore();
    }

    // -----------------------------------------------------------------------
    // E. The First Fire ("The Single Light in the Dark")
    // -----------------------------------------------------------------------
    if (pAwaken > 0) {
      hCtx.save();
      var flicker = reducedMotion ? 1 : 1 + 0.12 * Math.sin(now * 0.009) + 0.08 * Math.sin(now * 0.023);
      var fireScale = pAwaken * flicker;

      // 1. Broad atmospheric illumination on the island and ground
      var castRad = 110 * fireScale;
      var castGlow = hCtx.createRadialGradient(fireX, fireY, 0, fireX, fireY, castRad);
      castGlow.addColorStop(0, "rgba(255, 190, 83, 0.45)");
      castGlow.addColorStop(0.3, "rgba(255, 142, 36, 0.2)");
      castGlow.addColorStop(0.7, "rgba(255, 82, 26, 0.06)");
      castGlow.addColorStop(1, "rgba(255, 82, 26, 0)");
      hCtx.fillStyle = castGlow;
      hCtx.beginPath();
      hCtx.arc(fireX, fireY, castRad, 0, Math.PI * 2);
      hCtx.fill();

      // 2. Intense radiant fire core
      var coreGlow = hCtx.createRadialGradient(fireX, fireY - 3, 0, fireX, fireY - 3, 26 * fireScale);
      coreGlow.addColorStop(0, "rgba(255, 255, 240, 1)");
      coreGlow.addColorStop(0.25, "rgba(255, 218, 140, 0.95)");
      coreGlow.addColorStop(0.55, "rgba(255, 142, 36, 0.6)");
      coreGlow.addColorStop(1, "rgba(255, 82, 26, 0)");

      hCtx.fillStyle = coreGlow;
      hCtx.beginPath();
      hCtx.arc(fireX, fireY - 3, 26 * fireScale, 0, Math.PI * 2);
      hCtx.fill();

      // 3. Small flame tongues dancing
      if (!reducedMotion) {
        hCtx.fillStyle = "rgba(255, 245, 215, 0.95)";
        var flameH = 9 * fireScale;
        hCtx.beginPath();
        hCtx.moveTo(fireX - 4, fireY);
        hCtx.quadraticCurveTo(fireX + Math.sin(now * 0.02) * 3, fireY - flameH, fireX + 1, fireY - flameH - 4);
        hCtx.quadraticCurveTo(fireX + 3, fireY - flameH * 0.6, fireX + 4, fireY);
        hCtx.closePath();
        hCtx.fill();
      }
      hCtx.restore();

      // ---------------------------------------------------------------------
      // F. Rising Sparks & Embers Particle Engine
      // ---------------------------------------------------------------------
      if (!reducedMotion) {
        hCtx.save();
        var dt = 0.016; // approximate frame dt
        for (var eIdx = 0; eIdx < embers.length; eIdx++) {
          var emb = embers[eIdx];
          emb.age += dt;

          if (emb.age >= emb.life) {
            embers[eIdx] = createEmber(fireX, fireY, false);
            continue;
          }

          var progress = emb.age / emb.life;
          // Wind turbulence
          var sway = Math.sin(now * 0.003 + emb.phase) * 6;
          emb.x += (emb.vx + sway) * dt;
          emb.y += emb.vy * dt;

          var eAlpha = (1 - progress) * pAwaken;
          var curSize = emb.size * (1 - progress * 0.4);

          // Color transition: White-gold -> Orange -> Ember Red -> Fade
          var eCol;
          if (progress < 0.25) {
            eCol = "rgba(255, 240, 200, " + eAlpha.toFixed(3) + ")";
          } else if (progress < 0.6) {
            eCol = "rgba(255, 175, 60, " + eAlpha.toFixed(3) + ")";
          } else {
            eCol = "rgba(255, 85, 30, " + (eAlpha * 0.8).toFixed(3) + ")";
          }

          // A faint halo, then the ember (cheaper than a shadow blur on every particle)
          hCtx.fillStyle = "rgba(255, 190, 83, " + (0.18 * eAlpha).toFixed(3) + ")";
          hCtx.beginPath();
          hCtx.arc(emb.x, emb.y, curSize * 2.6, 0, Math.PI * 2);
          hCtx.fill();
          hCtx.fillStyle = eCol;
          hCtx.beginPath();
          hCtx.arc(emb.x, emb.y, curSize, 0, Math.PI * 2);
          hCtx.fill();
        }
        hCtx.shadowBlur = 0;
        hCtx.restore();
      }
    }

    // -----------------------------------------------------------------------
    // G. The Lone Figure on the Horizon (Standing Contemplatively)
    // -----------------------------------------------------------------------
    if (pFigure > 0) {
      hCtx.save();
      var figX = hW * 0.49 + camX * 0.72; // Standing to the right of the campfire
      var figY = cy - 10;                // Standing on the rocky crest
      var figH = hH * 0.13;              // Figure height
      var windSway = reducedMotion ? 0 : Math.sin(now * 0.0032) * 1.8;

      var figAlpha = pFigure;

      // Figure Silhouette Drawing
      hCtx.fillStyle = "rgba(6, 10, 18, " + figAlpha + ")";
      hCtx.strokeStyle = "rgba(155, 194, 255, " + (0.35 * figAlpha).toFixed(3) + ")";
      hCtx.lineWidth = 1;

      // 1. Cloak & Body Silhouette
      hCtx.beginPath();
      // Head
      var headRadius = figH * 0.09;
      var headCY = figY - figH + headRadius;
      hCtx.arc(figX, headCY, headRadius, 0, Math.PI * 2);
      hCtx.fill();

      // Shoulders & Flowing Cloak
      hCtx.beginPath();
      hCtx.moveTo(figX - headRadius * 1.3, headCY + headRadius * 0.8);
      // Left shoulder (facing fire)
      hCtx.lineTo(figX - figH * 0.16, figY - figH * 0.75);
      // Left cloak drape down to ground
      hCtx.lineTo(figX - figH * 0.18, figY);
      // Bottom of cloak (gently billowing in wind)
      hCtx.lineTo(figX + figH * 0.18 + windSway, figY);
      // Right cloak drape (facing ocean)
      hCtx.lineTo(figX + figH * 0.15, figY - figH * 0.75);
      hCtx.lineTo(figX + headRadius * 1.3, headCY + headRadius * 0.8);
      hCtx.closePath();
      hCtx.fill();

      // 2. Dual Rim Lighting (Warm Fire Gold on left, Cool Starlight Ice on right)
      // Firelight edge
      var fireRimAlpha = (0.75 * pFigure * (reducedMotion ? 1 : 0.9 + 0.1 * Math.sin(now * 0.01))).toFixed(3);
      hCtx.strokeStyle = "rgba(255, 190, 83, " + fireRimAlpha + ")";
      hCtx.lineWidth = 1.3;
      hCtx.beginPath();
      hCtx.moveTo(figX - headRadius * 0.9, headCY);
      hCtx.lineTo(figX - figH * 0.16, figY - figH * 0.75);
      hCtx.lineTo(figX - figH * 0.18, figY);
      hCtx.stroke();

      // Starlight edge
      var starRimAlpha = (0.55 * pFigure).toFixed(3);
      hCtx.strokeStyle = "rgba(180, 215, 255, " + starRimAlpha + ")";
      hCtx.lineWidth = 1.1;
      hCtx.beginPath();
      hCtx.moveTo(figX + headRadius * 0.9, headCY);
      hCtx.lineTo(figX + figH * 0.15, figY - figH * 0.75);
      hCtx.lineTo(figX + figH * 0.18 + windSway, figY);
      hCtx.stroke();

      hCtx.restore();
    }

    // -----------------------------------------------------------------------
    // H. Soft Horizon Edge Vignette (Seamless Bleed)
    // -----------------------------------------------------------------------
    hCtx.save();
    hCtx.globalCompositeOperation = "destination-in";
    var mask = hCtx.createLinearGradient(0, 0, hW, 0);
    mask.addColorStop(0, "rgba(0, 0, 0, 0)");
    mask.addColorStop(0.12, "rgba(0, 0, 0, 1)");
    mask.addColorStop(0.88, "rgba(0, 0, 0, 1)");
    mask.addColorStop(1, "rgba(0, 0, 0, 0)");
    hCtx.fillStyle = mask;
    hCtx.fillRect(0, 0, hW, hH);

    // Top & bottom soft fade
    var vertMask = hCtx.createLinearGradient(0, 0, 0, hH);
    vertMask.addColorStop(0, "rgba(0, 0, 0, 0.4)");
    vertMask.addColorStop(0.15, "rgba(0, 0, 0, 1)");
    vertMask.addColorStop(0.88, "rgba(0, 0, 0, 1)");
    vertMask.addColorStop(1, "rgba(0, 0, 0, 0.2)");
    hCtx.fillStyle = vertMask;
    hCtx.fillRect(0, 0, hW, hH);
    hCtx.restore();
  }

  // =========================================================================
  // 3. ANIMATION MAIN LOOP
  // =========================================================================
  function render(time) {
    // Smooth camera inertia
    mouse.currentX += (mouse.targetX - mouse.currentX) * 0.055;
    mouse.currentY += (mouse.targetY - mouse.currentY) * 0.055;

    drawSky(time);
    if (heroVisible) drawHero(time);           // nothing to draw once the hero has scrolled away

    if (!reducedMotion) {
      requestAnimationFrame(render);
    }
  }

  function handleResize() {
    initSky();
    initHero();
    if (reducedMotion) {
      drawSky(performance.now());
      drawHero(performance.now());
    }
  }

  window.addEventListener("resize", handleResize);
  var heroVisible = true;
  if (heroCanvas && "IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) {
      heroVisible = entries[0].isIntersecting;
    }).observe(heroCanvas);
  }
  initSky();
  initHero();
  requestAnimationFrame(render);

  // =========================================================================
  // 4. SCROLL REVEAL (IntersectionObserver with graceful fallback)
  // =========================================================================
  var targetElements = document.querySelectorAll(
    "main > h2, main > p, main > .cards, main > figure, main > .bookrow, " +
    "main > .btns, main > ul, main > .scroll, main > table, main > .note"
  );

  if (!reducedMotion && "IntersectionObserver" in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          observer.unobserve(entry.target);
        }
      });
    }, {
      rootMargin: "0px 0px -8% 0px",
      threshold: 0.05
    });

    targetElements.forEach(function (el) {
      el.classList.add("reveal");
      observer.observe(el);
    });
  } else {
    // Immediate display if reduced motion or older browser
    targetElements.forEach(function (el) {
      el.classList.add("in");
    });
  }

})();

// Looping film clips stay still for readers who ask for less motion.
if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  document.querySelectorAll("figure.loop video").forEach(function (v) { v.removeAttribute("autoplay"); v.pause(); });
}
