// measure.js: run inside slides.html by render.py. Returns {fonts, slides[]} describing what the browser
// actually laid out, so lint can check the house rules without anyone's opinion.
//
// Contract (assets/slide-base.html): .slide (1080x1350), one .headline, a .visual, .foot with .site (+ .cue),
// .decor for decoration only. Everything else is free.
(async () => {
  const W = 1080, H = 1350;
  const slides = [...document.querySelectorAll('.slide')];
  const SYSTEM = new Set(['georgia', 'times new roman', 'times', 'arial', 'helvetica', 'helvetica neue', 'courier new', 'courier',
    'menlo', 'monaco', 'impact', 'arial black', 'verdana', 'trebuchet ms', 'segoe ui']);
  const GENERIC = new Set(['serif', 'sans-serif', 'monospace', 'system-ui', 'cursive', 'fantasy', 'ui-monospace', 'ui-sans-serif',
    'ui-serif', '-apple-system', 'blinkmacsystemfont']);
  const SKIP = 'script,style,title,head,noscript';

  function textNodes(root) {
    const out = [], w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    for (let n; (n = w.nextNode());) if (n.textContent.trim() && n.parentElement && !n.parentElement.closest(SKIP)) out.push(n);
    return out;
  }
  const first = ff => ff.split(',')[0].trim().replace(/^["']|["']$/g, '');

  // 1. load every font face the slides use, then wait for layout to settle
  const combos = new Map();
  for (const s of slides) for (const n of textNodes(s)) {
    const cs = getComputedStyle(n.parentElement);
    combos.set(cs.fontFamily + '|' + cs.fontWeight + '|' + cs.fontStyle, [cs.fontFamily, cs.fontWeight, cs.fontStyle]);
  }
  await Promise.all([...combos.values()].map(([f, w, st]) => document.fonts.load(`${st} ${w} 40px ${f}`, 'Aa1').catch(() => {})));
  await document.fonts.ready;
  await Promise.all([...document.images].map(i => i.decode().catch(() => {})));
  await new Promise(r => setTimeout(r, 150));

  const faces = [...document.fonts].map(f => ({ family: f.family.replace(/^["']|["']$/g, ''), status: f.status }));
  const fonts = [];
  const seen = new Set();
  for (const [ff, w] of combos.values()) {
    const fam = first(ff);
    if (seen.has(fam) || GENERIC.has(fam.toLowerCase())) continue;
    seen.add(fam);
    const mine = faces.filter(x => x.family === fam);
    let status;
    if (mine.some(x => x.status === 'loaded')) status = 'loaded';
    else if (mine.length) status = 'failed';
    else if (SYSTEM.has(fam.toLowerCase())) status = 'system';
    else status = 'missing';
    fonts.push({ family: fam, status });
  }

  // colour helpers (for contrast against whatever is painted underneath)
  const rgba = str => { const m = str.match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 }; };
  const lum = c => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b); };
  const mixc = (fg, bg) => ({ r: fg.r * fg.a + bg.r * (1 - fg.a), g: fg.g * fg.a + bg.g * (1 - fg.a), b: fg.b * fg.a + bg.b * (1 - fg.a), a: 1 });
  const opac = el => { let o = 1; for (let a = el; a; a = a.parentElement) o *= parseFloat(getComputedStyle(a).opacity); return o; };
  function bgUnder(el, x, y) {
    for (const u of document.elementsFromPoint(x, y)) {
      if (u === el || el.contains(u)) continue;
      const us = getComputedStyle(u);
      if (us.backgroundImage && us.backgroundImage !== 'none') return null;   // gradient or image: can't measure
      const b = rgba(us.backgroundColor);
      if (b && b.a >= 0.6) return b;
    }
    return null;
  }

  const inter = (a, b) => Math.max(0, Math.min(a.r, b.r) - Math.max(a.l, b.l)) > 0 && Math.max(0, Math.min(a.b, b.b) - Math.max(a.t, b.t)) > 0
    ? { w: Math.min(a.r, b.r) - Math.max(a.l, b.l), h: Math.min(a.b, b.b) - Math.max(a.t, b.t) } : null;

  const report = [];
  for (let si = 0; si < slides.length; si++) {
    const s = slides[si];
    s.scrollIntoView();
    const sr = s.getBoundingClientRect();
    const docX = Math.round(sr.left + scrollX), docY = Math.round(sr.top + scrollY);
    const rel = r => ({ l: r.left - sr.left, t: r.top - sr.top, r: r.right - sr.left, b: r.bottom - sr.top });
    const box = r => ({ x: +r.l.toFixed(1), y: +r.t.toFixed(1), w: +(r.r - r.l).toFixed(1), h: +(r.b - r.t).toFixed(1) });

    // 2. every readable text run
    const texts = [];
    for (const n of textNodes(s)) {
      const el = n.parentElement, cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden' || opac(el) < 0.05) continue;
      const range = document.createRange(); range.selectNodeContents(n);
      const rr = range.getBoundingClientRect();
      if (!rr.width || !rr.height) continue;
      const lines = [...range.getClientRects()].filter(q => q.width > 1 && q.height > 1).map(rel);
      let px = parseFloat(cs.fontSize);
      if (el instanceof SVGElement) { const m = el.getScreenCTM && el.getScreenCTM(); if (m) px *= Math.abs(m.a); }
      texts.push({
        el, n, r: rel(rr), lines, px: +px.toFixed(1), weight: parseInt(cs.fontWeight, 10), family: first(cs.fontFamily),
        text: n.textContent.trim().replace(/\s+/g, ' ').slice(0, 60),
        decor: !!el.closest('.decor'), visual: !!el.closest('.visual'), headline: !!el.closest('.headline'),
        foot: !!el.closest('.foot'), svg: el instanceof SVGElement,
      });
    }

    // 3. structure
    const headlines = [...s.querySelectorAll('.headline')];
    const hl = headlines[0];
    const hlr = hl ? rel(hl.getBoundingClientRect()) : null;
    const visuals = [...s.querySelectorAll('.visual')];
    const visArea = visuals.reduce((a, v) => { const r = v.getBoundingClientRect(); return a + r.width * r.height; }, 0);
    let svgScale = null;   // how much the browser shrank the drawing; text drawn at 34 in the viewBox is under 34px when this is below 1
    for (const v of s.querySelectorAll('.visual svg')) {
      const vb = v.viewBox && v.viewBox.baseVal, r = v.getBoundingClientRect();
      if (vb && vb.width && r.width) { const sc = Math.min(r.width / vb.width, r.height / vb.height || 99); svgScale = svgScale === null ? sc : Math.min(svgScale, sc); }
    }
    if (svgScale !== null) svgScale = +svgScale.toFixed(2);
    const siteEl = s.querySelector('.foot .site') || [...s.querySelectorAll('.foot *, .foot')].find(e => /BUILDABLELABS\.COM/.test(e.textContent || ''));
    const siteR = siteEl ? rel(siteEl.getBoundingClientRect()) : null;
    const cueEl = s.querySelector('.foot .cue');
    const above = hlr ? texts.filter(t => !t.headline && (t.r.t + t.r.b) / 2 < hlr.t + 2 && t.r.b <= hlr.t + (hlr.b - hlr.t) * 0.5).map(t => t.text) : [];

    // 4. clipping and bounds
    const clipped = [];
    for (const t of texts) {
      if (t.decor) continue;
      let why = null;
      if (t.r.l < -1 || t.r.t < -1 || t.r.r > W + 1 || t.r.b > H + 1) why = 'off the slide';
      for (let a = t.el.parentElement; a && !why && a !== document.body; a = a.parentElement) {
        const cs = getComputedStyle(a);
        if (cs.overflow !== 'visible' && a !== s) {
          const ar = a.getBoundingClientRect(), tr = { left: sr.left + t.r.l, right: sr.left + t.r.r, top: sr.top + t.r.t, bottom: sr.top + t.r.b };
          if (tr.right > ar.right + 2 || tr.left < ar.left - 2 || tr.bottom > ar.bottom + 2 || tr.top < ar.top - 2) why = 'cut off by a box';
        }
      }
      if (why) clipped.push({ text: t.text, why });
    }
    for (const e of s.querySelectorAll('*')) {
      if (e.closest('.decor')) continue;
      const cs = getComputedStyle(e);
      if ((cs.overflow === 'hidden' || cs.overflow === 'auto') && (e.scrollHeight > e.clientHeight + 2 || e.scrollWidth > e.clientWidth + 2) && e.clientHeight > 0 && e !== s) {
        if (e.querySelector('.headline') || e.classList.contains('visual') || e.classList.contains('frame')) clipped.push({ text: '(' + (e.className || e.tagName) + ')', why: 'content taller or wider than its box' });
      }
    }

    // 5. overlaps between text runs (inner 60% of each line box, so tight leading isn't a false alarm)
    const shrink = r => { const h = r.b - r.t; return { l: r.l, r: r.r, t: r.t + h * 0.2, b: r.b - h * 0.2 }; };
    const overlaps = [];
    for (let i = 0; i < texts.length && overlaps.length < 10; i++) for (let j = i + 1; j < texts.length; j++) {
      const a = texts[i], b = texts[j];
      if (a.el === b.el || (a.headline && b.headline) || a.el.contains(b.el) || b.el.contains(a.el)) continue;
      const x = inter(shrink(a.r), shrink(b.r));
      if (x && x.w > 6 && x.h > 4) overlaps.push({ a: a.text, b: b.text, w: +x.w.toFixed(0), h: +x.h.toFixed(0) });
    }
    const overVisual = [];
    for (const t of texts) {
      if (t.decor || t.visual) continue;
      for (const v of visuals) { const x = inter(shrink(t.r), rel(v.getBoundingClientRect())); if (x && x.w > 8 && x.h > 6) overVisual.push(t.text); }
    }

    // 6. highlight blocks must not touch the lines around them
    const highlightTouch = [];
    if (hl) for (const e of hl.querySelectorAll('*')) {
      const cs = getComputedStyle(e), bg = rgba(cs.backgroundColor);
      const painted = (bg && bg.a > 0.5) || (cs.backgroundImage && cs.backgroundImage !== 'none');
      if (!painted) continue;
      for (const r of e.getClientRects()) {
        const hr = rel(r);
        for (const t of texts) {
          if (!t.headline || e.contains(t.el)) continue;
          for (const ln of t.lines) {   // one rect per wrapped line, shrunk to a glyph-ish area (the font box overlaps at tight leading)
            const tr = shrink(ln);
            const o = Math.min(hr.r, tr.r) - Math.max(hr.l, tr.l);
            if (o > 4) { const gap = tr.t >= hr.b - 1 ? tr.t - hr.b : hr.t - tr.b;
              if (gap < 4 && gap > -(hr.b - hr.t) * 0.2) highlightTouch.push({ block: (e.textContent || '').trim().slice(0, 30), other: t.text, gap: +gap.toFixed(1) }); }
          }
        }
      }
    }

    // 7. dead space: largest empty rectangle once text, svg, images and painted boxes are accounted for
    const CELL = 30, cols = Math.ceil(W / CELL), rows = Math.ceil(H / CELL);
    const occ = Array.from({ length: rows }, () => new Uint8Array(cols));
    const mark = r => { for (let y = Math.max(0, Math.floor(r.t / CELL)); y <= Math.min(rows - 1, Math.floor((r.b - 0.01) / CELL)); y++)
      for (let x = Math.max(0, Math.floor(r.l / CELL)); x <= Math.min(cols - 1, Math.floor((r.r - 0.01) / CELL)); x++) occ[y][x] = 1; };
    for (const t of texts) mark({ l: t.r.l - 8, r: t.r.r + 8, t: t.r.t - 8, b: t.r.b + 8 });
    for (const e of s.querySelectorAll('*')) {
      if (e === s) continue;
      const tag = e.tagName.toLowerCase();
      if (['script', 'style'].includes(tag)) continue;
      const rr = rel(e.getBoundingClientRect()), area = (rr.r - rr.l) * (rr.b - rr.t);
      if (area <= 0 || area > 0.7 * W * H) continue;
      if (e.closest('.decor') && e.classList.contains('decor')) continue;
      const cs = getComputedStyle(e), bg = rgba(cs.backgroundColor);
      const paintedBg = (bg && bg.a > 0.15) || (cs.backgroundImage && cs.backgroundImage !== 'none');
      const border = ['Top', 'Right', 'Bottom', 'Left'].some(k => parseFloat(cs['border' + k + 'Width']) > 0 && cs['border' + k + 'Style'] !== 'none');
      if (['svg', 'img', 'canvas', 'video'].includes(tag) || (paintedBg && area > 400) || (border && area > 400)) mark(rr);
    }
    const heights = new Array(cols).fill(0); let best = { a: 0, x: 0, y: 0, w: 0, h: 0 };
    for (let y = 0; y < rows; y++) {
      for (let x = 0; x < cols; x++) heights[x] = occ[y][x] ? 0 : heights[x] + 1;
      const st = [];
      for (let x = 0; x <= cols; x++) {
        const h = x === cols ? 0 : heights[x]; let start = x;
        while (st.length && st[st.length - 1].h >= h) { const p = st.pop(); const a = p.h * (x - p.x);
          if (a > best.a) best = { a, x: p.x, y: y - p.h + 1, w: x - p.x, h: p.h }; start = p.x; }
        st.push({ x: start, h });
      }
    }
    const empty = { pct: +(best.a / (cols * rows) * 100).toFixed(1), x: best.x * CELL, y: best.y * CELL, w: best.w * CELL, h: best.h * CELL };

    // 8. contrast of every text run against what is painted under it; light weights; type sizes
    let worst = null;
    for (const t of texts) {
      const cs = getComputedStyle(t.el); let fg = rgba(cs.color); if (!fg || fg.a === 0) continue;
      const r = t.el.getBoundingClientRect(); if (!r.width || !r.height) continue;
      const ob = rgba(cs.backgroundColor);
      const bg = (ob && ob.a >= 0.6 && (!cs.backgroundImage || cs.backgroundImage === 'none')) ? ob : bgUnder(t.el, r.left + r.width / 2, r.top + r.height / 2);
      if (!bg) continue;
      fg = mixc({ ...fg, a: fg.a * opac(t.el) }, bg);
      const l1 = lum(fg), l2 = lum(bg), ratio = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
      if (!worst || ratio < worst.ratio) worst = { ratio: +ratio.toFixed(2), px: Math.round(t.px), text: t.text };
    }
    const light = texts.filter(t => t.weight < 400).sort((a, b) => a.weight - b.weight)[0];
    const sizes = texts.filter(t => !t.decor).map(t => t.px);
    const smallest = texts.filter(t => !t.decor && t.px < 34).sort((a, b) => a.px - b.px).slice(0, 4).map(t => ({ text: t.text, px: t.px, family: t.family }));
    const digits = texts.filter(t => /^\s*\d{1,2}\s*$/.test(t.text) && t.px >= 100 && !t.headline).map(t => ({ text: t.text, px: t.px }));

    report.push({
      n: si + 1, type: s.dataset.type || '', size: { w: +sr.width.toFixed(1), h: +sr.height.toFixed(1) }, doc: { x: docX, y: docY },
      headline: hl ? { text: (hl.innerText || hl.textContent).trim().replace(/\s+/g, ' '), count: headlines.length, box: box(hlr) } : { count: 0 },
      visual: { count: visuals.length, pct: +(visArea / (W * H) * 100).toFixed(1), box: visuals[0] ? (r => ({ w: Math.round(r.width), h: Math.round(r.height) }))(visuals[0].getBoundingClientRect()) : null, svg_scale: svgScale },
      footer: { site: siteEl ? siteEl.textContent.trim() : null, site_box: siteR ? box(siteR) : null, cue: !!cueEl },
      above_headline: above, clipped, overlaps, text_over_visual: [...new Set(overVisual)].slice(0, 6), highlight_touch: highlightTouch.slice(0, 6),
      empty, min_px: sizes.length ? Math.min(...sizes) : null, small_text: smallest, min_contrast: worst,
      light_weight: light ? { weight: light.weight, family: light.family, text: light.text } : null,
      big_digits: digits, images: [...s.querySelectorAll('img')].map(i => (i.getAttribute('src') || '').slice(0, 80)),
      text_count: texts.length,
      texts: texts.slice(0, 120).map(t => ({ t: t.text, px: t.px, w: t.weight, y: +t.r.t.toFixed(0), x: +t.r.l.toFixed(0),
        decor: t.decor, visual: t.visual, headline: t.headline, foot: t.foot })),
    });
  }
  window.scrollTo(0, 0);
  return { fonts, slides: report };
})()
