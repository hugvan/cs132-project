/* ==========================================================================
   FYI — Public Dossier Interactive Controller
   All metrics sourced strictly from scripts/analysis.py and notebooks 01–03.
   ========================================================================== */

(() => {
  'use strict';

  const GROUPS = [
    {
      id: 'WATER-DISTRICT',
      code: 'WD',
      shortName: 'Water districts',
      fullName: 'Water districts (WATER-DISTRICT)',
      serial: 'TKT-WD-0287',
      frame: 287,
      sample: 287,
      replied: 212,
      noReplyCount: 75,
      noReplyPct: 26.1,
      wMedian: 1.12,
      p25: 0.76,
      p75: 6.56,
      succ: 32.1,
      part: 1.0,
      unsuc: 43.6,
      open: 22.6,
      ref: 0.7,
      allSucc: 33.1,
      allSuccCount: 95,
      closedSucc: 43.2,
      closedSuccShare: 41.8,
      closedPartShare: 1.4,
      closedUnsucShare: 56.8,
      mwSuccMed: 1.07,
      mwUnsuccMed: 1.13,
      mwP: 0.674,
      closedNoReply: 20,
      mwPWith: 0.0164,
      stamp: 'FAST REPLY, 26.1% SILENCE',
      stampTone: 'alert',
      note: 'Fast first responders when they reply (1.12 d weighted median), yet 75 of 287 requests never received a public agency message—and all 20 closed silent requests ended unsuccessful.'
    },
    {
      id: 'LEA',
      code: 'LEA',
      shortName: 'Law enforcement',
      fullName: 'Law enforcement (LEA)',
      serial: 'TKT-LEA-0359',
      frame: 359,
      sample: 280,
      replied: 278,
      noReplyCount: 2,
      noReplyPct: 0.7,
      wMedian: 0.56,
      p25: 0.15,
      p75: 0.99,
      succ: 61.3,
      part: 2.2,
      unsuc: 35.4,
      open: 1.1,
      ref: 0.0,
      allSucc: 63.5,
      allSuccCount: 228,
      closedSucc: 64.2,
      closedSuccShare: 62.0,
      closedPartShare: 2.3,
      closedUnsucShare: 35.8,
      mwSuccMed: 0.53,
      mwUnsuccMed: 0.65,
      mwP: 0.108,
      closedNoReply: 0,
      mwPWith: 0.108,
      stamp: 'FASTEST REPLY, 0.7% SILENCE',
      stampTone: 'neutral',
      note: 'Quickest initial reply across all six groups (0.56 d weighted median, 99.3% replied), though 20 Q1 sampled pages had vanished from public view before collection day.'
    },
    {
      id: 'NGA',
      code: 'NGA',
      shortName: 'National agencies',
      fullName: 'National government agencies (NGA)',
      serial: 'TKT-NGA-12219',
      frame: 12219,
      sample: 298,
      replied: 281,
      noReplyCount: 17,
      noReplyPct: 5.7,
      wMedian: 1.16,
      p25: 0.56,
      p75: 3.72,
      succ: 47.4,
      part: 15.7,
      unsuc: 25.8,
      open: 6.0,
      ref: 5.1,
      allSucc: 63.0,
      allSuccCount: 7703,
      closedSucc: 71.0,
      closedSuccShare: 53.3,
      closedPartShare: 17.6,
      closedUnsucShare: 29.0,
      mwSuccMed: 1.42,
      mwUnsuccMed: 0.93,
      mwP: 0.949,
      closedNoReply: 0,
      mwPWith: 0.949,
      stamp: '83.3% OF VOLUME, p = 0.949',
      stampTone: 'neutral',
      note: 'Handles 12,219 of 14,668 public 2025 filings (83.3%), posts a 1.16 d weighted median first reply, and shows no evidence that faster replies help closed requests succeed (p = 0.949).'
    },
    {
      id: 'GOCC',
      code: 'GOCC',
      shortName: 'Government corps',
      fullName: 'Government corporations (GOCC)',
      serial: 'TKT-GOCC-1284',
      frame: 1284,
      sample: 300,
      replied: 260,
      noReplyCount: 40,
      noReplyPct: 13.3,
      wMedian: 2.65,
      p25: 0.65,
      p75: 11.04,
      succ: 55.1,
      part: 9.5,
      unsuc: 22.8,
      open: 10.4,
      ref: 2.3,
      allSucc: 64.6,
      allSuccCount: 829,
      closedSucc: 73.9,
      closedSuccShare: 63.0,
      closedPartShare: 10.9,
      closedUnsucShare: 26.1,
      mwSuccMed: 2.65,
      mwUnsuccMed: 3.04,
      mwP: 0.911,
      closedNoReply: 2,
      mwPWith: 0.608,
      stamp: '2.65 D MEDIAN, 73.9% CLOSED',
      stampTone: 'neutral',
      note: 'Second-largest 2025 group (1,284 filings). Weighted median reply arrives in 2.65 calendar days, with 73.9% success among closed requests and 13.3% without recorded replies.'
    },
    {
      id: 'SUC',
      code: 'SUC',
      shortName: 'State universities',
      fullName: 'State universities and colleges (SUC)',
      serial: 'TKT-SUC-0344',
      frame: 344,
      sample: 301,
      replied: 260,
      noReplyCount: 41,
      noReplyPct: 13.6,
      wMedian: 3.24,
      p25: 0.94,
      p75: 15.57,
      succ: 52.3,
      part: 0.6,
      unsuc: 26.2,
      open: 17.2,
      ref: 3.8,
      allSucc: 52.9,
      allSuccCount: 182,
      closedSucc: 66.9,
      closedSuccShare: 66.2,
      closedPartShare: 0.7,
      closedUnsucShare: 33.1,
      mwSuccMed: 2.99,
      mwUnsuccMed: 3.72,
      mwP: 0.366,
      closedNoReply: 0,
      mwPWith: 0.366,
      stamp: '3.24 D MEDIAN, 17.2% OPEN',
      stampTone: 'neutral',
      note: 'Weighted median reply takes 3.24 calendar days (upper quartile reaches 15.57 days), and 17.2% of 2025 filings remained open on collection day.'
    },
    {
      id: 'LGU',
      code: 'LGU',
      shortName: 'Local governments',
      fullName: 'Local governments (LGU, voluntary EO 2)',
      serial: 'TKT-LGU-0175',
      frame: 175,
      sample: 175,
      replied: 145,
      noReplyCount: 30,
      noReplyPct: 17.1,
      wMedian: 4.68,
      p25: 1.67,
      p75: 21.93,
      succ: 70.3,
      part: 4.6,
      unsuc: 7.4,
      open: 16.6,
      ref: 1.1,
      allSucc: 74.9,
      allSuccCount: 131,
      closedSucc: 91.0,
      closedSuccShare: 85.4,
      closedPartShare: 5.6,
      closedUnsucShare: 9.0,
      mwSuccMed: 4.38,
      mwUnsuccMed: 7.74,
      mwP: 0.401,
      closedNoReply: 0,
      mwPWith: 0.401,
      stamp: 'SLOWEST (4.68 D), 91.0% CLOSED',
      stampTone: 'neutral',
      note: 'Only encouraged (not mandated) under EO No. 2. Slowest median first reply (4.68 d, 17.1% silent) yet posts the highest full-frame (74.9%) and closed-only (91.0%) success shares.'
    }
  ];

  const GROUP_MAP = Object.fromEntries(GROUPS.map((g) => [g.id, g]));

  /* Unweighted sample counts for the "Now serving" queue exhibit.
     succ / unsucc: closed requests with a recorded reply (Exhibit 03 within-group table).
     notClosed: replied requests that were not closed (replied − succ − unsucc).
     silentClosed: closed requests with no recorded reply (all unsuccessful; Exhibit 03 table).
     silentOpen: remaining requests with no recorded reply (noReplyCount − silentClosed). */
  const QUEUE_COUNTS = {
    LEA: { succ: 186, unsucc: 92, notClosed: 0, silentClosed: 0, silentOpen: 2 },
    'WATER-DISTRICT': { succ: 95, unsucc: 105, notClosed: 12, silentClosed: 20, silentOpen: 55 },
    NGA: { succ: 196, unsucc: 80, notClosed: 5, silentClosed: 0, silentOpen: 17 },
    GOCC: { succ: 195, unsucc: 55, notClosed: 10, silentClosed: 2, silentOpen: 38 },
    SUC: { succ: 165, unsucc: 74, notClosed: 21, silentClosed: 0, silentOpen: 41 },
    LGU: { succ: 131, unsucc: 13, notClosed: 1, silentClosed: 0, silentOpen: 30 }
  };

  const RQ3_BANDS = [
    { label: '0.0 – 0.6 d', n: 362, pct: 71.9 },
    { label: '0.6 – 1.3 d', n: 314, pct: 67.7 },
    { label: '1.3 – 3.9 d', n: 275, pct: 78.3 },
    { label: '3.9 – 527.0 d', n: 436, pct: 67.1 }
  ];

  const prefersReducedMotion = () =>
    window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const formatInt = (num) => Number(num).toLocaleString('en-US');

  /* --------------------------------------------------------------------------
     1. Scrollytelling Routing Diagram (#intro)
     -------------------------------------------------------------------------- */
  function initScrollytelling() {
    const steps = Array.from(document.querySelectorAll('#intro .step'));
    const path = document.getElementById('routing-path');
    const nodes = Array.from(document.querySelectorAll('#paper-trail-svg .route-node'));
    const progressLabel = document.getElementById('routing-progress-label');
    if (!steps.length || !path) return;

    const totalLen = path.getTotalLength ? path.getTotalLength() : 620;
    path.style.strokeDasharray = `${totalLen}`;

    const STAGE_FRACTIONS = [0.06, 0.28, 0.54, 0.78, 1.0];
    let currentStage = 0;

    function applyStage(idx) {
      currentStage = Math.max(0, Math.min(steps.length - 1, idx));
      steps.forEach((step, i) => {
        step.classList.toggle('is-active', i === currentStage);
      });
      nodes.forEach((node, i) => {
        node.classList.toggle('is-reached', i <= currentStage);
      });
      if (progressLabel) {
        progressLabel.textContent = `Stage ${currentStage + 1} of 5`;
      }
      if (prefersReducedMotion()) {
        path.style.strokeDashoffset = '0';
      } else {
        const frac = STAGE_FRACTIONS[currentStage] ?? 1;
        path.style.strokeDashoffset = `${(1 - frac) * totalLen}`;
      }
    }

    applyStage(0);

    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver(
        (entries) => {
          let best = null;
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              if (!best || entry.intersectionRatio > best.intersectionRatio) {
                best = entry;
              }
            }
          });
          if (best) {
            const idx = Number(best.target.dataset.step || 0);
            applyStage(idx);
          }
        },
        {
          rootMargin: '-28% 0px -42% 0px',
          threshold: [0.15, 0.45, 0.75]
        }
      );

      steps.forEach((step) => observer.observe(step));
    }

    steps.forEach((step, idx) => {
      step.addEventListener('click', () => applyStage(idx));
    });

    return {
      lockComplete: () => {
        steps.forEach((s) => s.classList.add('is-active'));
        nodes.forEach((n) => n.classList.add('is-reached'));
        if (progressLabel) progressLabel.textContent = 'Stage 5 of 5';
        path.style.strokeDashoffset = '0';
      },
      restoreStage: () => applyStage(currentStage)
    };
  }

  /* --------------------------------------------------------------------------
     2. Queue Ticket Simulator (#pick) & Completion Tracker (#dashboard)
     -------------------------------------------------------------------------- */
  const state = {
    selectedId: 'WATER-DISTRICT',
    inspected: new Set(['WATER-DISTRICT']),
    sortBy: 'median-asc',
    rq1View: 'both',
    rq2View: 'all',
    rq3View: 'bands',
    rq1FocusId: 'WATER-DISTRICT',
    clockRaf: null,
    ticketAnims: null
  };

  function updateTrackerBar() {
    const countEl = document.getElementById('tracker-count');
    if (countEl) {
      const count = state.inspected.size;
      countEl.textContent =
        count === GROUPS.length
          ? `Inspected ${count} / ${GROUPS.length} agency groups. Full audit complete`
          : `Inspected ${count} / ${GROUPS.length} agency groups`;
    }
    const cards = document.querySelectorAll('.group-card');
    cards.forEach((card) => {
      const id = card.dataset.group;
      const done = state.inspected.has(id);
      card.classList.toggle('is-inspected', done);
      const pill = card.querySelector('.audit-pill');
      if (pill) pill.textContent = done ? 'Audited' : 'Pending';
    });
  }

  function renderTicket(groupId, animate = true) {
    const g = GROUP_MAP[groupId];
    if (!g) return;

    state.selectedId = g.id;
    state.inspected.add(g.id);
    updateTrackerBar();

    document.querySelectorAll('.group-btn').forEach((btn) => {
      const active = btn.dataset.group === g.id;
      btn.classList.toggle('is-selected', active);
      btn.setAttribute('aria-pressed', active ? 'true' : 'false');
    });

    const stub = document.getElementById('ticket-stub');
    const serial = document.getElementById('ticket-serial');
    const nameEl = document.getElementById('ticket-group-name');
    const stampEl = document.getElementById('ticket-stamp');
    const noteEl = document.getElementById('ticket-note');
    const clockNum = document.getElementById('ticket-clock-num');
    const iqrEl = document.getElementById('ticket-iqr');
    const fillEl = document.getElementById('ticket-clock-fill');
    const noReplyEl = document.getElementById('ticket-noreply');
    const noReplyCountEl = document.getElementById('ticket-noreply-count');
    const succAllEl = document.getElementById('ticket-success-all');
    const frameCountEl = document.getElementById('ticket-frame-count');
    const succClosedEl = document.getElementById('ticket-success-closed');
    const openShareEl = document.getElementById('ticket-open-share');

    if (!stub || !clockNum || !fillEl) return;

    const body = stub.querySelector('.ticket-body');
    if (state.ticketAnims) {
      state.ticketAnims.forEach((a) => a.cancel());
      state.ticketAnims = null;
    }
    if (state.clockRaf) {
      cancelAnimationFrame(state.clockRaf);
      state.clockRaf = null;
    }

    const targetWidth = Math.min(100, (g.wMedian / 15) * 100);
    const canAnimate = animate && !prefersReducedMotion() && body && typeof body.animate === 'function';

    // Tear the current stub off along the perforation, then print the new one out of the slot.
    if (canAnimate && stub.dataset.rendered === 'true') {
      stub.classList.remove('is-stamped');
      const tear = body.animate(
        [
          { transform: 'none', opacity: 1 },
          { transform: 'translateY(22px) rotate(1.2deg)', opacity: 0 }
        ],
        { duration: 180, easing: 'cubic-bezier(0.55, 0, 1, 0.45)', fill: 'forwards' }
      );
      state.ticketAnims = [tear];
      tear.onfinish = () => {
        tear.cancel();
        fillTicket();
        const printOut = body.animate(
          [
            { clipPath: 'inset(0 0 100% 0)', transform: 'translateY(-14px)' },
            { clipPath: 'inset(0 0 0% 0)', transform: 'none' }
          ],
          { duration: 460, easing: 'cubic-bezier(0.16, 1, 0.3, 1)' }
        );
        state.ticketAnims = [printOut];
        runCountUp();
      };
      return;
    }

    fillTicket();
    stub.dataset.rendered = 'true';
    if (canAnimate) {
      runCountUp();
    } else {
      finishStatic();
    }

    function fillTicket() {
      serial.textContent = g.serial;
      nameEl.textContent = g.fullName;
      noteEl.textContent = g.note;
      iqrEl.textContent = `${g.p25.toFixed(2)} – ${g.p75.toFixed(2)} d`;
      noReplyEl.textContent = `${g.noReplyPct.toFixed(1)}%`;
      noReplyCountEl.textContent = `${g.noReplyCount} of ${g.sample} sampled`;
      succAllEl.textContent = `${g.allSucc.toFixed(1)}%`;
      frameCountEl.textContent = `${formatInt(g.allSuccCount)} of ${formatInt(g.frame)} in frame`;
      succClosedEl.textContent = `${g.closedSucc.toFixed(1)}%`;
      openShareEl.textContent = `${g.open.toFixed(1)}% still open on Sept 29`;

      stampEl.textContent = g.stamp;
      stampEl.className = `stamp ${g.stampTone === 'alert' ? 'stamp-alert' : 'stamp-neutral'}`;
    }

    function finishStatic() {
      clockNum.textContent = g.wMedian.toFixed(2);
      fillEl.style.transform = `scaleX(${(targetWidth / 100).toFixed(4)})`;
      stub.classList.add('is-stamped');
    }

    function runCountUp() {
      stub.classList.remove('is-stamped');
      const duration = 700;
      const start = performance.now();

      function step(now) {
        const t = Math.min(1, (now - start) / duration);
        const eased = t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
        clockNum.textContent = (g.wMedian * eased).toFixed(2);
        fillEl.style.transform = `scaleX(${((targetWidth / 100) * eased).toFixed(4)})`;

        if (t < 1) {
          state.clockRaf = requestAnimationFrame(step);
        } else {
          finishStatic();
          state.clockRaf = null;
        }
      }

      state.clockRaf = requestAnimationFrame(step);
    }
  }

  function renderGroupGrid() {
    const grid = document.getElementById('group-grid');
    if (!grid) return;

    const sorted = [...GROUPS].sort((a, b) => {
      switch (state.sortBy) {
        case 'noreply-desc':
          return b.noReplyPct - a.noReplyPct;
        case 'success-desc':
          return b.allSucc - a.allSucc;
        case 'frame-desc':
          return b.frame - a.frame;
        case 'median-asc':
        default:
          return a.wMedian - b.wMedian;
      }
    });

    grid.innerHTML = sorted
      .map((g) => {
        const inspected = state.inspected.has(g.id);
        const noReplyAlert = g.noReplyPct >= 20 ? ' is-alert' : '';
        return `
          <article class="group-card${inspected ? ' is-inspected' : ''}" data-group="${g.id}" tabindex="0" role="button" aria-label="Inspect ${g.shortName} in the Agency Explorer">
            <div>
              <div class="group-card-head">
                <div>
                  <span class="group-card-code">${g.code} (N = ${formatInt(g.frame)})</span>
                  <h3>${g.shortName}</h3>
                </div>
                <span class="audit-pill">${inspected ? 'Audited' : 'Pending'}</span>
              </div>
            </div>
            <div class="group-card-metrics">
              <div>
                <span class="gc-stat-label">Median reply</span>
                <span class="gc-stat-val">${g.wMedian.toFixed(2)} d</span>
              </div>
              <div>
                <span class="gc-stat-label">No reply</span>
                <span class="gc-stat-val${noReplyAlert}">${g.noReplyPct.toFixed(1)}%</span>
              </div>
              <div>
                <span class="gc-stat-label">Success (all)</span>
                <span class="gc-stat-val">${g.allSucc.toFixed(1)}%</span>
              </div>
            </div>
            <div class="group-card-foot">
              <span>Closed: ${g.closedSucc.toFixed(1)}%</span>
              <span class="group-card-action">Inspect ↑</span>
            </div>
          </article>
        `;
      })
      .join('');

    grid.querySelectorAll('.group-card').forEach((card) => {
      const activate = () => {
        const id = card.dataset.group;
        renderTicket(id, true);
        const pickEl = document.getElementById('pick');
        if (pickEl) pickEl.scrollIntoView({ behavior: prefersReducedMotion() ? 'auto' : 'smooth', block: 'start' });
      };
      card.addEventListener('click', activate);
      card.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          activate();
        }
      });
    });
  }

  function initQueueAndDashboard() {
    document.querySelectorAll('.group-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        renderTicket(btn.dataset.group, true);
      });
    });

    const replayBtn = document.getElementById('replay-ticket-btn');
    if (replayBtn) {
      replayBtn.addEventListener('click', () => {
        renderTicket(state.selectedId, true);
      });
    }

    const sortSel = document.getElementById('sort-groups');
    if (sortSel) {
      sortSel.addEventListener('change', () => {
        state.sortBy = sortSel.value;
        renderGroupGrid();
      });
    }

    const jumpSel = document.getElementById('jump-group');
    if (jumpSel) {
      jumpSel.addEventListener('change', () => {
        if (!jumpSel.value) return;
        renderTicket(jumpSel.value, true);
        const pickEl = document.getElementById('pick');
        if (pickEl) pickEl.scrollIntoView({ behavior: prefersReducedMotion() ? 'auto' : 'smooth', block: 'start' });
      });
    }

    renderTicket('WATER-DISTRICT', false);
    renderGroupGrid();
  }

  /* --------------------------------------------------------------------------
     2b. "Now Serving" Queue Exhibit (#queue-board)
     Final (completed) frame is the base DOM state; motion plays from .is-queued.
     -------------------------------------------------------------------------- */
  const QUEUE_TICKETS = 20;
  const QUEUE_WAIT_SLOTS = 5;
  const QUEUE_CLOCK = { offset: 0.3, scale: 0.62 }; // seconds = offset + scale * log2(1 + days)
  const QUEUE_STAGGER = 0.028;
  const QUEUE_TRAVEL = 0.45;
  const QUEUE_STAMP_LAG = 0.3;

  const MARK_SVG = {
    succ: '<svg class="q-mark" viewBox="0 0 16 16" aria-hidden="true"><path d="M3.2 8.6l3 3 6.6-7"/></svg>',
    unsucc: '<svg class="q-mark" viewBox="0 0 16 16" aria-hidden="true"><path d="M4 4l8 8M12 4l-8 8"/></svg>',
    open: '<svg class="q-mark" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="3.4"/></svg>'
  };

  const laneOpenAt = (days) => QUEUE_CLOCK.offset + QUEUE_CLOCK.scale * Math.log2(1 + days);

  // Largest-remainder rounding so every lane shows exactly QUEUE_TICKETS tickets.
  function allocateTickets(counts, total) {
    const keys = Object.keys(counts);
    const n = keys.reduce((s, k) => s + counts[k], 0);
    const raw = keys.map((k) => (counts[k] * total) / n);
    const out = raw.map(Math.floor);
    let left = total - out.reduce((s, v) => s + v, 0);
    raw
      .map((v, i) => ({ i, rem: v - Math.floor(v) }))
      .sort((a, b) => b.rem - a.rem || a.i - b.i)
      .forEach(({ i }) => {
        if (left > 0) {
          out[i] += 1;
          left -= 1;
        }
      });
    return Object.fromEntries(keys.map((k, i) => [k, out[i]]));
  }

  function initQueueExhibit() {
    const board = document.getElementById('queue-board');
    const clockEl = document.getElementById('queue-clock-val');
    const replayBtn = document.getElementById('queue-replay-btn');
    if (!board) return null;

    const lanes = [...GROUPS].sort((a, b) => a.wMedian - b.wMedian);
    const lastOpen = laneOpenAt(lanes[lanes.length - 1].wMedian);
    const maxMedian = lanes[lanes.length - 1].wMedian;
    let silenceAt = 0;

    const laneHtml = lanes.map((g) => {
      const c = QUEUE_COUNTS[g.id];
      if (c.succ + c.unsucc + c.notClosed !== g.replied || c.silentClosed + c.silentOpen !== g.noReplyCount) {
        console.warn(`Queue counts for ${g.id} do not reconcile with GROUP_MAP.`);
      }
      const t = allocateTickets(c, QUEUE_TICKETS);
      const open = laneOpenAt(g.wMedian);

      const served = [
        ...Array(t.succ).fill('succ'),
        ...Array(t.unsucc).fill('unsucc'),
        ...Array(t.notClosed).fill('open')
      ];
      const servedHtml = served
        .map((kind, i) => {
          const d = open + i * QUEUE_STAGGER;
          silenceAt = Math.max(silenceAt, d + QUEUE_TRAVEL + QUEUE_STAMP_LAG);
          return `<span class="q-ticket q-${kind}" style="--i:${i};--d:${d.toFixed(3)};--s:${(d + QUEUE_STAMP_LAG).toFixed(3)}">${MARK_SVG[kind]}</span>`;
        })
        .join('');

      const waiting = [...Array(t.silentClosed).fill(true), ...Array(t.silentOpen).fill(false)];
      const waitHtml = waiting
        .map((closed, j) => {
          const col = QUEUE_WAIT_SLOTS - waiting.length + j + 1;
          return `<span class="q-ticket q-wait${closed ? ' q-silent-closed' : ''}" style="grid-column:${col}">${closed ? MARK_SVG.unsucc : ''}</span>`;
        })
        .join('');

      const label =
        `${g.shortName}: weighted median first reply ${g.wMedian.toFixed(2)} days. ` +
        `Of ${g.sample} sampled requests, ${c.succ} closed successful and ${c.unsucc} closed unsuccessful after a reply, ` +
        `${c.notClosed} replied but not closed, and ${g.noReplyCount} never received a recorded reply` +
        (c.silentClosed ? ` (${c.silentClosed} of them closed unsuccessful).` : '.') +
        ` Shown as ${t.succ} successful, ${t.unsucc} unsuccessful, ${t.notClosed} not closed and ${t.silentClosed + t.silentOpen} no-reply tickets out of 20.`;

      return `
        <div class="queue-lane" role="img" aria-label="${label}">
          <div class="lane-label">
            <span class="lane-code">${g.code}</span>
            <span class="lane-name">${g.shortName}</span>
            <span class="lane-median">median ${g.wMedian.toFixed(2)} d</span>
          </div>
          <div class="lane-track" aria-hidden="true">
            <div class="lane-wait">${waitHtml}</div>
            <div class="lane-window"></div>
            <div class="lane-served">${servedHtml}</div>
          </div>
          <div class="lane-count" aria-hidden="true">
            <span>n = ${g.sample}</span>
            <span>${g.noReplyCount} no reply</span>
          </div>
        </div>`;
    });

    board.innerHTML = `
      <div class="queue-board-head" aria-hidden="true">
        <span></span>
        <div class="lane-track">
          <span class="qb-wait">Awaiting first reply</span>
          <span class="lane-window"></span>
          <span class="qb-served">Replied and stamped with outcome</span>
        </div>
        <span class="qb-count">Sample</span>
      </div>
      ${laneHtml.join('')}`;
    board.style.setProperty('--silence', silenceAt.toFixed(3));

    let clockRaf = null;
    let observer = null;
    const finalClock = `${maxMedian.toFixed(2)} d`;

    const stopClock = () => {
      if (clockRaf) cancelAnimationFrame(clockRaf);
      clockRaf = null;
    };

    const runClock = () => {
      stopClock();
      if (!clockEl) return;
      const start = performance.now();
      const tick = (now) => {
        const t = (now - start) / 1000;
        if (t >= lastOpen) {
          clockEl.textContent = finalClock;
          clockRaf = null;
          return;
        }
        const days = Math.max(0, Math.pow(2, (t - QUEUE_CLOCK.offset) / QUEUE_CLOCK.scale) - 1);
        clockEl.textContent = `${days.toFixed(2)} d`;
        clockRaf = requestAnimationFrame(tick);
      };
      clockRaf = requestAnimationFrame(tick);
    };

    const reset = () => {
      stopClock();
      board.classList.add('no-anim', 'is-queued');
      if (clockEl) clockEl.textContent = '0.00 d';
      requestAnimationFrame(() => board.classList.remove('no-anim'));
    };

    const play = () => {
      // Let the queued state commit for one frame instead of forcing a sync reflow.
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          board.classList.remove('is-queued');
          runClock();
        });
      });
    };

    const lockComplete = () => {
      if (observer) observer.disconnect();
      observer = null;
      stopClock();
      board.classList.add('no-anim');
      board.classList.remove('is-queued');
      if (clockEl) clockEl.textContent = finalClock;
    };

    if (prefersReducedMotion() || !('IntersectionObserver' in window)) {
      lockComplete();
      return { lockComplete };
    }

    reset();
    observer = new IntersectionObserver(
      (entries) => {
        if (entries.some((e) => e.isIntersecting)) {
          observer.disconnect();
          observer = null;
          play();
        }
      },
      { threshold: 0.35 }
    );
    observer.observe(board);

    if (replayBtn) {
      replayBtn.addEventListener('click', () => {
        if (observer) {
          observer.disconnect();
          observer = null;
        }
        reset();
        play();
      });
    }

    return { lockComplete };
  }

  /* --------------------------------------------------------------------------
     3. Scroll-Triggered Verdict Rubber Stamps (#research)
     -------------------------------------------------------------------------- */
  function initStampObserver() {
    const cards = Array.from(document.querySelectorAll('[data-stamp-target]'));
    if (!cards.length) return;

    const revealAll = () => {
      cards.forEach((c) => {
        const st = c.querySelector('.scroll-stamp');
        if (st) st.classList.add('is-stamped');
      });
    };

    if (prefersReducedMotion() || !('IntersectionObserver' in window)) {
      revealAll();
      return { lockComplete: revealAll };
    }

    const obs = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const st = entry.target.querySelector('.scroll-stamp');
            if (st) st.classList.add('is-stamped');
            obs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.3 }
    );

    cards.forEach((c) => obs.observe(c));
    return { lockComplete: revealAll };
  }

  /* --------------------------------------------------------------------------
     4. Interactive SVG Exhibits (RQ1, RQ2, RQ3)
     -------------------------------------------------------------------------- */
  function renderRQ1() {
    const stage = document.getElementById('chart-rq1');
    if (!stage) return;

    const mode = state.rq1View;
    const rows =
      mode === 'noreply'
        ? [...GROUPS].sort((a, b) => b.noReplyPct - a.noReplyPct)
        : [...GROUPS].sort((a, b) => a.wMedian - b.wMedian);

    const W = 820;
    const rowH = 44;
    const topPad = mode === 'noreply' ? 32 : 58;
    const H = topPad + rows.length * rowH + 30;
    const labelX = 152;
    const medBarMax = mode === 'both' ? 255 : 530;
    const nrStart = mode === 'both' ? 500 : 168;
    const nrBarMax = mode === 'both' ? 235 : 530;

    const eo15x = labelX + (15 / 15) * medBarMax;
    const medSvgBars = (g, y) => {
      if (mode === 'noreply') return '';
      const barW = Math.max(4, (g.wMedian / 15) * medBarMax);
      return `
        <rect x="${labelX}" y="${y + 10}" width="${medBarMax}" height="18" fill="#F7F7F5" />
        <rect x="${labelX}" y="${y + 10}" width="${barW.toFixed(1)}" height="18" fill="#1c1246" />
        <text x="${(labelX + barW + 8).toFixed(1)}" y="${y + 23}" font-family="Public Sans, sans-serif" font-size="11.5" font-weight="700" fill="#1c1246">${g.wMedian.toFixed(2)} d</text>
      `;
    };

    const nrSvgBars = (g, y) => {
      if (mode === 'median') return '';
      const barW = Math.max(3, (g.noReplyPct / 30) * nrBarMax);
      const isAlert = g.noReplyPct >= 20;
      const fill = isAlert ? '#F46201' : '#4F4A6B';
      return `
        <rect x="${nrStart}" y="${y + 10}" width="${nrBarMax}" height="18" fill="#F7F7F5" />
        <rect x="${nrStart}" y="${y + 10}" width="${barW.toFixed(1)}" height="18" fill="${fill}" />
        <text x="${(nrStart + barW + 8).toFixed(1)}" y="${y + 23}" font-family="Public Sans, sans-serif" font-size="11.5" font-weight="700" fill="${fill}">${g.noReplyPct.toFixed(1)}%</text>
      `;
    };

    const headers = [];
    if (mode !== 'noreply') {
      headers.push(`<text x="${labelX}" y="18" font-family="Public Sans, sans-serif" font-size="10.5" font-weight="700" fill="#4F4A6B">Weighted median first reply (0–15 days)</text>`);
      headers.push(`<text x="${eo15x}" y="${H - 6}" text-anchor="end" font-family="Public Sans, sans-serif" font-size="10" fill="#4F4A6B">EO No. 2 allows 15 working days; bars show calendar days</text>`);
    }
    if (mode !== 'median') {
      headers.push(`<text x="${nrStart}" y="18" font-family="Public Sans, sans-serif" font-size="10.5" font-weight="700" fill="#4F4A6B">No recorded reply (0–30%)</text>`);
    }

    const rowEls = rows
      .map((g, idx) => {
        const y = topPad + idx * rowH;
        return `
          <g class="rq1-row" data-group="${g.id}" tabindex="0" role="button" aria-label="${g.shortName}: median ${g.wMedian.toFixed(2)} days, no reply ${g.noReplyPct.toFixed(1)}%">
            <rect class="row-bg" x="0" y="${y}" width="${W}" height="${rowH - 4}" fill="transparent" />
            <text x="8" y="${y + 23}" font-family="'Public Sans', sans-serif" font-size="13" font-weight="700" fill="#1c1246">${g.shortName}</text>
            ${medSvgBars(g, y)}
            ${nrSvgBars(g, y)}
            <line x1="0" y1="${y + rowH - 2}" x2="${W}" y2="${y + rowH - 2}" stroke="#D2D4CF" stroke-width="1" />
          </g>
        `;
      })
      .join('');

    const focused = GROUP_MAP[state.rq1FocusId] || rows[0];
    stage.innerHTML = `
      <svg class="chart-svg" viewBox="0 0 ${W} ${H}" role="img" aria-label="First response times and no-reply percentages across the six agency groups">
        ${headers.join('')}
        ${rowEls}
        ${mode === 'noreply' ? '' : `
        <g class="eo15-ref" aria-hidden="true">
          <rect x="${eo15x - 7}" y="${topPad - 4}" width="14" height="${H - topPad - 26}" fill="#F46201" fill-opacity="0.08" />
          <line x1="${eo15x}" y1="${topPad - 6}" x2="${eo15x}" y2="${H - 22}" stroke="#F46201" stroke-width="2.5" />
          <rect x="${eo15x - 58}" y="26" width="116" height="22" rx="3" fill="#FFF4EC" stroke="#F46201" stroke-width="1.5" />
          <text x="${eo15x}" y="41" text-anchor="middle" font-family="Public Sans, sans-serif" font-size="11.5" font-weight="700" fill="#1c1246">EO No. 2: 15 days</text>
        </g>`}
      </svg>
      <div id="rq1-readout" class="chart-readout">
        <strong>${focused.code} (${focused.shortName}):</strong> weighted median ${focused.wMedian.toFixed(2)} cal. days; unweighted IQR ${focused.p25.toFixed(2)}–${focused.p75.toFixed(2)} d (${focused.replied}/${focused.sample} replied; ${focused.noReplyCount} blank = ${focused.noReplyPct.toFixed(1)}% weighted no-reply).
      </div>
    `;

    const readout = document.getElementById('rq1-readout');
    stage.querySelectorAll('.rq1-row').forEach((row) => {
      const updateReadout = () => {
        const g = GROUP_MAP[row.dataset.group];
        if (!g || !readout) return;
        state.rq1FocusId = g.id;
        readout.innerHTML = `<strong>${g.code} (${g.shortName}):</strong> weighted median ${g.wMedian.toFixed(2)} cal. days; unweighted IQR ${g.p25.toFixed(2)}–${g.p75.toFixed(2)} d (${g.replied}/${g.sample} replied; ${g.noReplyCount} blank = ${g.noReplyPct.toFixed(1)}% weighted no-reply).`;
      };
      row.addEventListener('mouseenter', updateReadout);
      row.addEventListener('focus', updateReadout);
      row.addEventListener('click', updateReadout);
    });
  }

  function renderRQ2() {
    const stage = document.getElementById('chart-rq2');
    if (!stage) return;

    const mode = state.rq2View;
    const rows =
      mode === 'closed'
        ? [...GROUPS].sort((a, b) => b.closedSucc - a.closedSucc)
        : [...GROUPS].sort((a, b) => b.allSucc - a.allSucc);

    const legendItems =
      mode === 'closed'
        ? [
            { label: 'Successful', color: '#155E63' },
            { label: 'Partially successful', color: '#3B82A6' },
            { label: 'Unsuccessful', color: '#F46201' }
          ]
        : [
            { label: 'Successful', color: '#155E63' },
            { label: 'Partially successful', color: '#3B82A6' },
            { label: 'Unsuccessful', color: '#F46201' },
            { label: 'Open', color: '#6B7280' },
            { label: 'Referred', color: '#D49B2A' }
          ];

    const W = 820;
    const barX = 165;
    const barW = 515;
    const rowH = 42;
    const topPad = 14;
    const H = topPad + rows.length * rowH + 22;

    const rowEls = rows
      .map((g, idx) => {
        const y = topPad + idx * rowH;
        const segments =
          mode === 'closed'
            ? [
                { val: g.closedSuccShare, color: '#155E63' },
                { val: g.closedPartShare, color: '#3B82A6' },
                { val: g.closedUnsucShare, color: '#F46201' }
              ]
            : [
                { val: g.succ, color: '#155E63' },
                { val: g.part, color: '#3B82A6' },
                { val: g.unsuc, color: '#F46201' },
                { val: g.open, color: '#6B7280' },
                { val: g.ref, color: '#D49B2A' }
              ];

        let curX = barX;
        const rects = segments
          .map((seg) => {
            const w = (seg.val / 100) * barW;
            const rect = `<rect x="${curX.toFixed(1)}" y="${y + 8}" width="${w.toFixed(1)}" height="20" fill="${seg.color}" />`;
            curX += w;
            return rect;
          })
          .join('');

        const totalSucc = mode === 'closed' ? g.closedSucc : g.allSucc;
        const nLabel = mode === 'closed' ? `closed ${g.closedSucc.toFixed(1)}%` : `${g.allSucc.toFixed(1)}% succ.`;

        return `
          <g>
            <text x="8" y="${y + 22}" font-family="'Public Sans', sans-serif" font-size="13" font-weight="700" fill="#1c1246">${g.shortName}</text>
            ${rects}
            <rect x="${barX}" y="${y + 8}" width="${barW}" height="20" fill="none" stroke="#1c1246" stroke-width="0.9" />
            <text x="${barX + barW + 10}" y="${y + 22}" font-family="Public Sans, sans-serif" font-size="11.5" font-weight="700" fill="#1c1246">${nLabel}</text>
            <title>${g.shortName}: combined success ${totalSucc.toFixed(1)}%</title>
          </g>
        `;
      })
      .join('');

    const legendHtml = legendItems
      .map(
        (item) =>
          `<span class="legend-item"><span class="legend-swatch" style="background:${item.color}"></span><span>${item.label}</span></span>`
      )
      .join('');

    stage.innerHTML = `
      <div class="chart-legend">${legendHtml}</div>
      <svg class="chart-svg" viewBox="0 0 ${W} ${H}" role="img" aria-label="100 percent stacked horizontal bar chart of observed outcomes across the six agency groups">
        ${rowEls}
      </svg>
    `;
  }

  function renderRQ3() {
    const stage = document.getElementById('chart-rq3');
    if (!stage) return;

    if (state.rq3View === 'bands') {
      const W = 820;
      const H = 265;
      const plotL = 72;
      const plotR = 790;
      const plotT = 30;
      const plotB = 212;
      const plotW = plotR - plotL;
      const plotH = plotB - plotT;
      const colW = plotW / RQ3_BANDS.length;
      const refY = plotB - (71.3 / 100) * plotH;

      const gridLines = [0, 25, 50, 75, 100]
        .map((tick) => {
          const y = plotB - (tick / 100) * plotH;
          return `
            <line x1="${plotL}" y1="${y.toFixed(1)}" x2="${plotR}" y2="${y.toFixed(1)}" stroke="#D2D4CF" stroke-width="1" />
            <text x="${plotL - 10}" y="${(y + 4).toFixed(1)}" text-anchor="end" font-family="Public Sans, sans-serif" font-size="10.5" fill="#4F4A6B">${tick}%</text>
          `;
        })
        .join('');

      const bars = RQ3_BANDS.map((b, idx) => {
        const bw = 92;
        const cx = plotL + idx * colW + colW / 2;
        const bx = cx - bw / 2;
        const bh = (b.pct / 100) * plotH;
        const by = plotB - bh;
        return `
          <g>
            <rect x="${bx.toFixed(1)}" y="${by.toFixed(1)}" width="${bw}" height="${bh.toFixed(1)}" fill="#155E63" stroke="#1c1246" stroke-width="1.25" />
            <text x="${cx.toFixed(1)}" y="${(by - 8).toFixed(1)}" text-anchor="middle" font-family="Public Sans, sans-serif" font-size="12" font-weight="700" fill="#1c1246">${b.pct.toFixed(1)}%</text>
            <text x="${cx.toFixed(1)}" y="${plotB + 19}" text-anchor="middle" font-family="Public Sans, sans-serif" font-size="11" font-weight="700" fill="#1c1246">${b.label}</text>
            <text x="${cx.toFixed(1)}" y="${plotB + 35}" text-anchor="middle" font-family="Public Sans, sans-serif" font-size="10" fill="#4F4A6B">n = ${b.n}</text>
          </g>
        `;
      }).join('');

      stage.innerHTML = `
        <div class="chart-legend">
          <span class="legend-item"><span class="legend-swatch" style="background:#155E63"></span><span>Closed success rate (%)</span></span>
          <span class="legend-item"><span class="legend-swatch" style="background:#F46201"></span><span>71.3% overall weighted success (dashed reference)</span></span>
        </div>
        <svg class="chart-svg" viewBox="0 0 ${W} ${H}" role="img" aria-label="Success proportions across four weighted quartile response-time bands">
          ${gridLines}
          ${bars}
          <line x1="${plotL}" y1="${plotB}" x2="${plotR}" y2="${plotB}" stroke="#1c1246" stroke-width="1.5" />
          <line x1="${plotL}" y1="${refY.toFixed(1)}" x2="${plotR}" y2="${refY.toFixed(1)}" stroke="#F46201" stroke-width="1.75" stroke-dasharray="5 4" />
        </svg>
      `;
      return;
    }

    // Mode: within-group medians & no-reply sensitivity
    const W = 820;
    const rowH = 42;
    const topPad = 28;
    const H = topPad + GROUPS.length * rowH + 16;
    const scaleL = 165;
    const scaleW = 410;
    const maxDays = 8.5;

    const rows = [...GROUPS]
      .sort((a, b) => a.mwSuccMed - b.mwSuccMed)
      .map((g, idx) => {
        const y = topPad + idx * rowH;
        const sx = scaleL + (g.mwSuccMed / maxDays) * scaleW;
        const ux = scaleL + (g.mwUnsuccMed / maxDays) * scaleW;
        const pColor = g.mwPWith < 0.05 ? '#F46201' : '#4F4A6B';
        const pNote =
          g.closedNoReply > 0
            ? `p = ${g.mwP} → ${g.mwPWith} (${g.closedNoReply} silent)`
            : `p = ${g.mwP}`;
        return `
          <g>
            <text x="8" y="${y + 22}" font-family="'Public Sans', sans-serif" font-size="13" font-weight="700" fill="#1c1246">${g.shortName}</text>
            <line x1="${scaleL}" y1="${y + 18}" x2="${scaleL + scaleW}" y2="${y + 18}" stroke="#D2D4CF" stroke-width="1" />
            <line x1="${Math.min(sx, ux).toFixed(1)}" y1="${y + 18}" x2="${Math.max(sx, ux).toFixed(1)}" y2="${y + 18}" stroke="#1c1246" stroke-width="2" />
            <circle cx="${sx.toFixed(1)}" cy="${y + 18}" r="5.5" fill="#155E63" stroke="#1c1246" stroke-width="1" />
            <rect x="${(ux - 5).toFixed(1)}" y="${y + 13}" width="10" height="10" fill="#F46201" stroke="#1c1246" stroke-width="1" />
            <text x="${scaleL + scaleW + 14}" y="${y + 22}" font-family="Public Sans, sans-serif" font-size="10.8" font-weight="700" fill="${pColor}">${pNote}</text>
            <title>${g.shortName}: median successful ${g.mwSuccMed.toFixed(2)} d vs unsuccessful ${g.mwUnsuccMed.toFixed(2)} d</title>
          </g>
        `;
      })
      .join('');

    stage.innerHTML = `
      <div class="chart-legend">
        <span class="legend-item"><span class="legend-swatch" style="background:#155E63"></span><span>Median: successful (closed replied)</span></span>
        <span class="legend-item"><span class="legend-swatch" style="background:#F46201"></span><span>Median: unsuccessful (closed replied)</span></span>
      </div>
      <svg class="chart-svg" viewBox="0 0 ${W} ${H}" role="img" aria-label="Within-group unweighted medians for closed successful versus unsuccessful requests and no-reply sensitivity">
        <text x="${scaleL}" y="16" font-family="Public Sans, sans-serif" font-size="10.5" font-weight="700" fill="#4F4A6B">Unweighted group medians (0–8.5 calendar days)</text>
        <text x="${scaleL + scaleW + 14}" y="16" font-family="Public Sans, sans-serif" font-size="10.5" font-weight="700" fill="#4F4A6B">Mann–Whitney p (replied / +no-reply)</text>
        ${rows}
      </svg>
    `;
  }

  function initCharts() {
    document.querySelectorAll('[data-rq1-view]').forEach((btn) => {
      btn.addEventListener('click', () => {
        state.rq1View = btn.dataset.rq1View;
        document.querySelectorAll('[data-rq1-view]').forEach((b) => b.classList.toggle('is-active', b === btn));
        renderRQ1();
      });
    });

    document.querySelectorAll('[data-rq2-view]').forEach((btn) => {
      btn.addEventListener('click', () => {
        state.rq2View = btn.dataset.rq2View;
        document.querySelectorAll('[data-rq2-view]').forEach((b) => b.classList.toggle('is-active', b === btn));
        renderRQ2();
      });
    });

    document.querySelectorAll('[data-rq3-view]').forEach((btn) => {
      btn.addEventListener('click', () => {
        state.rq3View = btn.dataset.rq3View;
        document.querySelectorAll('[data-rq3-view]').forEach((b) => b.classList.toggle('is-active', b === btn));
        renderRQ3();
      });
    });

    renderRQ1();
    renderRQ2();
    renderRQ3();
  }

  /* --------------------------------------------------------------------------
     5. A4 Print Preparation
     -------------------------------------------------------------------------- */
  function initPrintControls(scrollyCtrl, stampCtrl, queueCtrl) {
    const printBtn = document.getElementById('print-btn');
    if (printBtn) {
      printBtn.addEventListener('click', () => window.print());
    }

    const detailsList = Array.from(document.querySelectorAll('details.analysis-details'));
    let prevOpen = [];
    let prevViews = null;

    window.addEventListener('beforeprint', () => {
      prevOpen = detailsList.map((d) => d.open);
      detailsList.forEach((d) => {
        d.open = true;
      });
      prevViews = { rq1: state.rq1View, rq2: state.rq2View, rq3: state.rq3View };
      state.rq1View = 'both';
      state.rq2View = 'all';
      state.rq3View = 'bands';
      renderRQ1();
      renderRQ2();
      renderRQ3();
      if (scrollyCtrl) scrollyCtrl.lockComplete();
      if (stampCtrl) stampCtrl.lockComplete();
      if (queueCtrl) queueCtrl.lockComplete();
      renderTicket(state.selectedId, false);
    });

    window.addEventListener('afterprint', () => {
      detailsList.forEach((d, i) => {
        d.open = Boolean(prevOpen[i]);
      });
      if (prevViews) {
        state.rq1View = prevViews.rq1;
        state.rq2View = prevViews.rq2;
        state.rq3View = prevViews.rq3;
        renderRQ1();
        renderRQ2();
        renderRQ3();
      }
      if (scrollyCtrl) scrollyCtrl.restoreStage();
    });
  }

  /* --------------------------------------------------------------------------
     Boot
     -------------------------------------------------------------------------- */
  document.addEventListener('DOMContentLoaded', () => {
    const scrollyCtrl = initScrollytelling();
    initQueueAndDashboard();
    const stampCtrl = initStampObserver();
    const queueCtrl = initQueueExhibit();
    initCharts();
    initPrintControls(scrollyCtrl, stampCtrl, queueCtrl);
  });
})();
