#!/usr/bin/env python3
"""
render.py - turn a carousel folder into 1080x1350 PNG slides and a review board.

Reads   <carousel>/vision.json     the look (theme + colours, type, layout overrides)
        <skill>/assets/themes/<theme>/  theme.json (defaults, fill_types) + theme.css (layout styling)
        <carousel>/script.json     the slides (type + copy per slide)
        <skill>/assets/brand/brand.json  the brand limits (palette, fonts, handle); a project's own brand/ above the carousel wins

Writes  <carousel>/slides.html          every slide in one HTML file; open it to tweak
        <carousel>/slides/01.png ...     one PNG per slide, exactly 1080x1350
        <carousel>/render_report.json    what the browser measured: overflow, shrink-to-fit,
                                         smallest type, which fonts actually loaded
        <carousel>/board.html + .png     references, vision panel, decisions, every slide at phone size
        <carousel>/status.json           stage -> "vision_draft" (vision not locked) or "rendered" (locked)

Needs Google Chrome or Chromium. No Python packages required (Pillow, if installed,
is used to double-check output sizes). Set CHROME_PATH to point at a specific binary.

Usage
  python3 render.py carousels/<slug>
  python3 render.py carousels/<slug> --only 2,5     # re-shoot just these slides (fix rounds)
  python3 render.py carousels/<slug> --html-only    # write slides.html, skip the browser
  python3 render.py carousels/<slug> --no-board
"""

import argparse
import base64
import copy
import datetime as dt
import fcntl
import glob
import html
import json
import math
import os
import re
import select
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.parse

W, H = 1080, 1350

DEFAULT_VISION = {
    "name": "untitled",
    "theme": "foundation",
    "status": "draft",
    "mode": "dark",
    "mood": [],
    "colors": {
        "bg": "#0A0B0E",
        "text": "#F5F6F8",
        "muted": "#7A8296",
        "accent": "#6789EC",
        "fill": "#0B3FDE",
        "on_fill": "#FFFFFF",
    },
    "type": {
        "display": "Instrument Serif",
        "body": "Manrope",
        "mono": "JetBrains Mono",
        "display_case": "upper",
        "scale": {"cover": 132, "headline": 84, "body": 40, "label": 34, "number": 280},
    },
    "layout": {
        "align": "left",
        "margin": 96,
        "texture": "none",
        "counter": False,      # house rule: no slide or page numbers (gate G7)
        "kicker": False,       # house rule: the headline is the first thing on a slide (no eyebrow above it)
        "min_text_px": 34,     # house rule: nothing under 34px (gate G4); render.js floors smaller text to this
        "last_cue": "",        # optional cue on the last slide instead of the swipe cue, e.g. "YOUR TAKE ↓"
        "handle": True,
        "progress": True,
        "swipe_cue": True,
        "cta_fill": False,
    },
    "custom_css": "",
}

ICONS = {
    "save": '<path d="M6 3h12v18l-6-4.5L6 21z"/>',
    "follow": '<path d="M12 5v14M5 12h14"/>',
    "comment": '<path d="M4 5h16v11H10l-6 4z"/>',
    "read": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "share": '<path d="M21 3 3 10.5l7.5 3L13.5 21z"/>',
    "dm": '<path d="M21 3 3 10.5l7.5 3L13.5 21z"/>',
}

CSS = r"""
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#111}
body{width:1080px}
.slide{position:relative;width:1080px;height:1350px;overflow:hidden;background:var(--bg);color:var(--text);
  font-family:var(--f-body);display:none;--fit:1}
body.all .slide{display:block}
.slide.on{display:block}
.slide.fill{background-color:var(--fill);color:var(--on-fill);--accent:var(--on-fill);--muted:var(--on-fill-muted);--line:var(--on-fill-line);--grid:var(--on-fill-grid)}
.tex-grid{background-image:linear-gradient(var(--grid) 2px,transparent 2px),linear-gradient(90deg,var(--grid) 2px,transparent 2px);
  background-size:108px 108px;background-position:-1px -1px}
.tex-dots{background-image:radial-gradient(var(--grid) 3px,transparent 3.5px);background-size:54px 54px}
.tex-weave{background-image:repeating-linear-gradient(45deg,var(--pattern) 0 2px,transparent 2px 72px),
  repeating-linear-gradient(-45deg,var(--pattern) 0 2px,transparent 2px 72px)}
.tex-ascent{background-image:repeating-linear-gradient(-62deg,transparent 0 46px,var(--pattern-blue) 46px 48px);
  -webkit-mask-image:linear-gradient(200deg,#000 0%,transparent 55%);mask-image:linear-gradient(200deg,#000 0%,transparent 55%)}
.tex-loop{background-image:radial-gradient(circle at 82% 18%,transparent 118px,var(--pattern) 119px 121px,transparent 122px),
  radial-gradient(circle at 92% 30%,transparent 58px,var(--pattern) 59px 61px,transparent 62px),
  radial-gradient(circle at 12% 88%,transparent 168px,var(--pattern) 169px 171px,transparent 172px),
  radial-gradient(circle at 70% 78%,transparent 28px,var(--pattern) 29px 31px,transparent 32px)}
.frame{position:absolute;inset:var(--m);display:flex;flex-direction:column;z-index:2}
.decor,.decor2{position:absolute;inset:0;pointer-events:none;z-index:1}
.top,.foot{display:flex;justify-content:space-between;align-items:center;gap:24px;flex:none;
  font-family:var(--f-mono);font-size:var(--s-label);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);line-height:1.2}
.top .kicker{color:var(--accent)}
.foot .cue{color:var(--accent)}
.content{flex:1;min-height:0;display:flex;flex-direction:column;justify-content:center;
  gap:calc(40px*var(--fit));overflow:hidden;padding:28px 0}
.align-center .content{align-items:center;text-align:center}
.display{font-family:var(--f-display);font-weight:400;line-height:.98;letter-spacing:-.005em;text-transform:var(--display-case);text-wrap:balance}
.h-cover{font-size:calc(var(--s-cover)*var(--fit))}
.h{font-size:calc(var(--s-headline)*var(--fit))}
.h-sm{font-size:calc(var(--s-headline)*.78*var(--fit))}
.h-cta{font-size:calc(var(--s-headline)*1.18*var(--fit))}
.body{font-size:calc(var(--s-body)*var(--fit));line-height:1.38;max-width:880px}
.sub{font-size:calc(var(--s-body)*1.08*var(--fit));line-height:1.3;color:var(--muted);max-width:860px}
.num{font-family:var(--f-display);font-size:calc(var(--s-number)*var(--fit));line-height:.82;color:var(--accent);letter-spacing:-.02em}
.source{font-family:var(--f-mono);font-size:var(--s-label);color:var(--muted);letter-spacing:.03em;line-height:1.35}
em{font-style:italic;color:var(--accent)}
.body em,.sub em,.list em{font-style:normal;font-weight:700}
.rule{width:132px;height:8px;background:var(--fill);flex:none}
.slide.fill .rule{background:var(--on-fill)}
.list{list-style:none;display:flex;flex-direction:column;gap:calc(24px*var(--fit));width:100%}
.list li{display:flex;gap:30px;align-items:baseline;text-align:left;font-size:calc(var(--s-body)*1.1*var(--fit));line-height:1.28;
  padding-top:calc(24px*var(--fit));border-top:2px solid var(--line)}
.list .ix{font-family:var(--f-mono);font-size:calc(var(--s-label)*1.2*var(--fit));color:var(--accent);flex:none;min-width:58px}
.quote-mark{font-family:var(--f-display);font-size:240px;line-height:.62;height:118px;color:var(--accent)}
.quote{text-wrap:balance;font-family:var(--f-display);font-style:italic;font-size:calc(var(--s-headline)*.86*var(--fit));line-height:1.1}
.pill{display:inline-flex;align-items:center;gap:20px;align-self:flex-start;border:3px solid currentColor;border-radius:999px;
  padding:24px 42px;font-family:var(--f-mono);font-size:calc(var(--s-label)*1.3);letter-spacing:.1em;text-transform:uppercase}
.align-center .pill{align-self:center}
.pill svg{width:36px;height:36px;fill:none;stroke:currentColor;stroke-width:2;stroke-linejoin:round;stroke-linecap:round}
.img{width:100%;height:calc(600px*var(--fit));object-fit:cover;border-radius:20px;flex:none}
.progress{position:absolute;left:0;bottom:0;height:10px;background:var(--fill)}
.slide.fill .progress{background:var(--on-fill)}
/* ---- visuals (slide "visual" field): UI mockups and diagrams in brand colours. Themes can restyle them
   or override the --ui-* colours. */
/* 24px side clearance: a tilt or an overhanging sticker would otherwise count as overflow and trigger shrink-to-fit */
.visual{flex:none;width:calc(100% - 48px);margin-inline:auto;position:relative;margin-block:auto;transform:rotate(var(--tilt,0deg));font-family:var(--f-mono);
  --ui-bg:#0A0B0E;--ui-panel:#12141A;--ui-line:#2C3444;--ui-text:#F5F6F8;--ui-dim:#7A8296;--ui-accent:#6789EC;--ui-fill:#0B3FDE;--ui-on-fill:#FFFFFF;
  --ui-shadow:0 34px 70px rgba(10,11,14,.38)}
.visual .ic{width:1em;height:1em;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;flex:none}
.win,.hud,.dialog{background:var(--ui-bg);color:var(--ui-text);border:2px solid var(--ui-line);border-radius:4px;box-shadow:var(--ui-shadow);overflow:hidden}
.win-bar{display:flex;align-items:center;gap:12px;padding:14px 24px;background:var(--ui-panel);border-bottom:2px solid var(--ui-line);
  font-size:34px;letter-spacing:.04em;text-transform:lowercase;color:var(--ui-dim)}
.win-bar i{width:18px;height:18px;border-radius:50%;background:var(--ui-line)}
.win-bar span{margin-left:12px}
.win-hud{padding:calc(24px*var(--fit)) 28px;display:flex;flex-direction:column;gap:calc(18px*var(--fit))}
.win-hud:not(:last-child){border-bottom:2px dashed var(--ui-line)}
.win-body{padding:calc(24px*var(--fit)) 28px;display:flex;flex-direction:column;gap:calc(12px*var(--fit))}
.ln{display:flex;gap:16px;font-size:34px;line-height:1.3;color:var(--ui-text);white-space:pre-wrap}
.ln .pr{color:var(--ui-accent);font-weight:700;flex:none}
.ln-dim{color:#B8BECC}
.ln-hl span{background:var(--ui-fill);color:var(--ui-on-fill);padding:0 .3em}
.toast{position:absolute;right:-14px;top:-30px;display:flex;align-items:center;gap:12px;background:var(--ui-fill);color:var(--ui-on-fill);
  font-size:34px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;padding:12px 22px;border-radius:4px;
  transform:rotate(4deg);box-shadow:0 14px 30px rgba(10,11,14,.4);border:2px solid var(--ui-on-fill)}
.toast .ic{font-size:38px;stroke-width:2}
.hud{padding:calc(32px*var(--fit)) 34px;display:flex;flex-direction:column;gap:calc(30px*var(--fit))}
.hud-row{display:flex;flex-direction:column;gap:calc(14px*var(--fit))}
.hud-head{display:flex;justify-content:space-between;align-items:center;gap:20px}
.hud-label{font-size:34px;letter-spacing:.06em;text-transform:uppercase;color:var(--ui-dim)}
.hud-tag{font-size:34px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--ui-accent)}
.hearts{display:flex;gap:calc(10px*var(--fit))}
.px-heart{width:calc(52px*var(--fit));height:auto;fill:var(--ui-accent)}
.v-hud .px-heart{width:calc(66px*var(--fit))}
.v-hud .seg-bar{height:calc(44px*var(--fit))}
.v-hud .hud-label,.v-hud .hud-tag{font-size:36px}
.px-heart.off{fill:var(--ui-line)}
.seg-bar{display:flex;gap:6px;height:calc(34px*var(--fit));padding:5px;border:2px solid var(--ui-line);border-radius:2px}
.seg-bar i{flex:1;background:var(--ui-panel)}
.seg-bar i.on{background:var(--ui-accent)}
/* flow: input on top, your thing in the middle, outcomes in a row below (stacked so 34px labels fit) */
.flow{display:flex;flex-direction:column;align-items:center;color:var(--text)}
.fl-chip{display:flex;align-items:center;gap:12px;border:3px solid currentColor;border-radius:4px;padding:14px 18px;font-size:34px;font-weight:700;
  letter-spacing:.02em;text-transform:uppercase;white-space:nowrap;background:var(--bg)}
.fl-chip .ic{font-size:38px}
.fl-via{background:var(--ui-bg);color:var(--ui-text);border-color:var(--ui-bg);padding:22px 30px;box-shadow:var(--ui-shadow)}
.fl-via .ic{color:var(--ui-accent)}
.fl-arrow{width:3px;height:calc(46px*var(--fit));background:currentColor;position:relative;flex:none;margin-bottom:12px}
.fl-arrow::after{content:"";position:absolute;left:-8px;bottom:-12px;border-style:solid;border-width:13px 9.5px 0 9.5px;border-color:currentColor transparent transparent transparent}
.fl-outs{display:flex;flex-wrap:wrap;justify-content:center;gap:16px}
.slots{display:grid;grid-template-columns:repeat(2,1fr);gap:20px}
.slots.n3{grid-template-columns:repeat(3,1fr)}
.slot{position:relative;min-height:calc(200px*var(--fit));background:var(--ui-bg);color:var(--ui-text);border:3px solid var(--ui-line);border-radius:4px;
  box-shadow:inset 0 0 0 6px var(--ui-panel),var(--ui-shadow);display:flex;flex-direction:column;justify-content:flex-end;gap:16px;padding:28px}
.slot .ic{font-size:calc(60px*var(--fit));color:var(--ui-accent);stroke-width:1.6}
.slot-label{font-family:var(--f-body);font-weight:700;font-size:34px;line-height:1.12;letter-spacing:-.01em}
.slot .key{position:absolute;top:12px;right:20px;font-size:34px;color:var(--ui-dim)}
.slot.on{background:var(--ui-fill);border-color:var(--ui-on-fill);box-shadow:inset 0 0 0 6px rgba(255,255,255,.12),var(--ui-shadow)}
.slot.on .ic,.slot.on .key{color:var(--ui-on-fill)}
.slot.on::after{content:"Equipped";position:absolute;top:-26px;left:24px;background:var(--ui-on-fill);color:var(--ui-fill);font-size:34px;font-weight:700;
  letter-spacing:.06em;text-transform:uppercase;padding:2px 12px;border-radius:2px}
.slots-cap{margin-top:18px;font-size:34px;line-height:1.2;color:var(--text)}
.dl-title{display:flex;align-items:center;gap:16px;padding:20px 28px;background:var(--ui-panel);border-bottom:2px solid var(--ui-line);
  font-family:var(--f-body);font-weight:700;font-size:36px}
.dl-title .ic{color:var(--ui-accent);font-size:36px}
.dl-rows{padding:calc(26px*var(--fit)) 28px;display:flex;flex-direction:column;gap:calc(18px*var(--fit))}
.dl-row{display:flex;align-items:center;gap:18px;font-family:var(--f-body);font-size:34px;font-weight:500;line-height:1.2}
.dl-row .ic{color:var(--ui-accent);font-size:34px;stroke-width:2.4}
.dl-btns{display:flex;justify-content:flex-end;gap:14px;padding:0 28px 26px}
.dl-btn{font-family:var(--f-body);font-weight:600;font-size:34px;padding:12px 30px;border:2px solid var(--ui-line);border-radius:4px;color:var(--ui-text)}
.dl-btn.primary{background:var(--ui-fill);border-color:var(--ui-fill);color:var(--ui-on-fill)}
/* funnel: stages narrowing to one outcome */
.funnel{display:flex;flex-direction:column;align-items:center;gap:calc(16px*var(--fit))}
.fn-stage{width:var(--w);display:flex;align-items:center;justify-content:center;gap:14px;background:var(--ui-bg);color:var(--ui-text);
  border:2px solid var(--ui-line);border-radius:4px;padding:calc(30px*var(--fit)) 28px;font-family:var(--f-body);font-weight:700;font-size:42px;
  line-height:1.1;text-align:center;box-shadow:var(--ui-shadow)}
.fn-stage .ic{font-size:44px;color:var(--ui-accent)}
.fn-arrow{width:3px;height:calc(40px*var(--fit));background:var(--text);position:relative;margin-bottom:12px}
.fn-arrow::after{content:"";position:absolute;left:-8px;bottom:-12px;border-style:solid;border-width:13px 9.5px 0 9.5px;border-color:var(--text) transparent transparent transparent}
.fn-out{display:flex;align-items:center;gap:14px;background:var(--ui-fill);color:var(--ui-on-fill);border-radius:4px;padding:28px 40px;
  font-family:var(--f-body);font-weight:800;font-size:46px;line-height:1.1;box-shadow:var(--ui-shadow)}
.fn-out .ic{font-size:42px;stroke-width:2.4}
/* tags: a cloud of pills, one or two filled */
.tags{display:flex;flex-wrap:wrap;justify-content:center;gap:30px 22px;padding:14px 0}
.tag{display:inline-block;transform:rotate(var(--tt));font-family:var(--f-body);font-weight:700;font-size:46px;line-height:1;padding:24px 36px;
  border-radius:999px;border:3px solid currentColor;color:var(--text)}
.tag.on{background:var(--ui-fill);border-color:var(--ui-fill);color:var(--ui-on-fill)}
.tags-cap{margin-top:36px;text-align:center;font-size:38px;line-height:1.2;color:var(--text)}
/* compare: before | after */
.compare{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.cp-col{background:var(--ui-bg);color:var(--ui-text);border:2px solid var(--ui-line);border-radius:4px;overflow:hidden;box-shadow:var(--ui-shadow)}
.cp-title{padding:22px 26px;background:var(--ui-panel);border-bottom:2px solid var(--ui-line);font-size:34px;font-weight:700;letter-spacing:.04em;
  text-transform:uppercase;color:var(--ui-dim)}
.cp-after .cp-title{background:var(--ui-fill);border-color:var(--ui-fill);color:var(--ui-on-fill)}
.cp-rows{padding:calc(34px*var(--fit)) 26px calc(40px*var(--fit));display:flex;flex-direction:column;gap:calc(28px*var(--fit))}
.cp-row{display:flex;gap:14px;align-items:flex-start;font-family:var(--f-body);font-size:38px;font-weight:600;line-height:1.15}
.cp-row .ic{font-size:38px;margin-top:2px;stroke-width:2.6}
.cp-before .cp-row{color:var(--ui-dim)}
.cp-after .cp-row .ic{color:var(--ui-accent)}
/* chart: horizontal bars; values are drawn, a printed figure goes in "display" (and must be sourced) */
.chart{background:var(--ui-bg);color:var(--ui-text);border:2px solid var(--ui-line);border-radius:4px;padding:calc(40px*var(--fit)) 38px calc(46px*var(--fit));
  display:flex;flex-direction:column;gap:calc(36px*var(--fit));box-shadow:var(--ui-shadow)}
.ch-title{font-size:34px;letter-spacing:.06em;text-transform:uppercase;color:var(--ui-dim)}
.ch-row{display:flex;flex-direction:column;gap:16px}
.ch-head{display:flex;justify-content:space-between;align-items:baseline;gap:16px;font-family:var(--f-body);font-size:42px;font-weight:600;line-height:1.1}
.ch-val{font-family:var(--f-mono);font-weight:700;color:var(--ui-accent)}
.ch-track{height:calc(48px*var(--fit));background:var(--ui-panel);border-radius:2px;overflow:hidden}
.ch-track i{display:block;height:100%;background:var(--ui-dim)}
.ch-row.on .ch-track i{background:var(--ui-accent)}
/* timeline: steps down a rail, one current */
.timeline{display:flex;flex-direction:column;position:relative;gap:calc(44px*var(--fit))}
.timeline::before{content:"";position:absolute;left:42px;top:24px;bottom:24px;width:3px;background:var(--text);opacity:.35}
.tl-step{display:flex;align-items:center;gap:32px;position:relative}
.tl-node{flex:none;width:88px;height:88px;border-radius:50%;display:grid;place-items:center;background:var(--ui-bg);color:var(--ui-accent);
  border:3px solid var(--ui-line);font-size:42px}
.tl-step.on .tl-node{background:var(--ui-fill);color:var(--ui-on-fill);border-color:var(--ui-fill)}
.tl-text{display:flex;flex-direction:column;gap:4px}
.tl-when{font-size:34px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.tl-t{font-family:var(--f-body);font-size:46px;font-weight:700;line-height:1.15;color:var(--text)}
"""

JS = r"""
const slides = [...document.querySelectorAll('.slide')];
const fams = JSON.parse(document.getElementById('fams').textContent);
document.body.classList.add('all');
window.show = n => { document.body.classList.remove('all'); slides.forEach((s, i) => s.classList.toggle('on', i === n - 1)); };

const over = c => c.scrollHeight > c.clientHeight + 1 || c.scrollWidth > c.clientWidth + 1;
function fit(slide) {
  const c = slide.querySelector('.content');
  let f = 1;
  while (over(c) && f > 0.7) { f = +(f - 0.03).toFixed(2); slide.style.setProperty('--fit', f); }
  return f;
}
// Labels (.top, .foot, .source, .ix, .pill, .visual) are meta text; everything else in .content is reading text.
const META = '.source, .ix, .pill, .pill *, .visual, .visual *';
function textSizes(root, meta) {
  const out = [];
  if (!root) return out;
  for (const el of root.querySelectorAll('*')) {
    const own = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (!own) continue;
    if (meta === undefined || el.matches(META) === meta) out.push(parseFloat(getComputedStyle(el).fontSize));
  }
  return out;
}
// Contrast and weight of every rendered text run. The background is whatever is painted under the middle of the
// text (elementsFromPoint, so decoration layers count); text over a gradient or image is skipped because it can't
// be measured reliably, and the judge looks at those by eye.
function rgbaOf(str) {
  const m = str.match(/rgba?\(([^)]+)\)/); if (!m) return null;
  const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number);
  return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
}
function lum(c) { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
  return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b); }
function mix(fg, bg) { const a = fg.a; return { r: fg.r * a + bg.r * (1 - a), g: fg.g * a + bg.g * (1 - a), b: fg.b * a + bg.b * (1 - a), a: 1 }; }
function opacityOf(el) { let o = 1; for (let a = el; a; a = a.parentElement) o *= parseFloat(getComputedStyle(a).opacity); return o; }
function bgUnder(el, x, y) {
  for (const u of document.elementsFromPoint(x, y)) {
    if (u === el || el.contains(u)) continue;
    const us = getComputedStyle(u);
    if (us.backgroundImage && us.backgroundImage !== 'none') return null;   // gradient/image: can't measure
    const b = rgbaOf(us.backgroundColor);
    if (b && b.a >= 0.6) return b;
  }
  return null;
}
function textAudit(slide) {
  let worst = null, light = null;
  slide.scrollIntoView();
  for (const el of slide.querySelectorAll('*')) {
    const own = [...el.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim());
    if (!own.length) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden') continue;
    const r = el.getBoundingClientRect(); if (!r.width || !r.height) continue;
    const txt = own.map(n => n.textContent.trim()).join(' ').slice(0, 40);
    const w = parseInt(cs.fontWeight, 10);
    if (w < 400 && (!light || w < light.weight)) light = { weight: w, family: cs.fontFamily.split(',')[0].replace(/["']/g, ''), text: txt };
    let fg = rgbaOf(cs.color); if (!fg || fg.a === 0) continue;
    const own_bg = rgbaOf(cs.backgroundColor);
    const bg = (own_bg && own_bg.a >= 0.6 && (!cs.backgroundImage || cs.backgroundImage === 'none')) ? own_bg
             : bgUnder(el, r.left + r.width / 2, r.top + r.height / 2);
    if (!bg) continue;
    fg = mix({ ...fg, a: fg.a * opacityOf(el) }, bg);
    const l1 = lum(fg), l2 = lum(bg), ratio = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
    if (!worst || ratio < worst.ratio) worst = { ratio: +ratio.toFixed(2), px: Math.round(parseFloat(cs.fontSize)), text: txt };
  }
  return { worst, light };
}
(async () => {
  try { await Promise.all(fams.map(f => document.fonts.load('40px "' + f + '"', 'Aa1'))); } catch (e) {}
  await document.fonts.ready;
  await Promise.all([...document.images].map(i => i.decode().catch(() => {})));
  // House rule: nothing under the minimum text size. Lift any smaller text to the floor before fitting.
  const FLOOR = +(document.body.dataset.minText || 0);
  if (FLOOR) for (const s of slides) for (const el of s.querySelectorAll('*')) {
    const own = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (own && parseFloat(getComputedStyle(el).fontSize) < FLOOR) el.style.fontSize = FLOOR + 'px';
  }
  const fits = new Map(slides.map(s => [s, fit(s)]));
  const loaded = {};
  for (const fam of fams) loaded[fam] = [...document.fonts].some(ff => ff.family.replace(/["']/g, '') === fam && ff.status === 'loaded');
  const hit = document.createElement('style'); hit.textContent = '*{pointer-events:auto!important}'; document.head.appendChild(hit);
  const rep = slides.map((s, i) => {
    const c = s.querySelector('.content');
    const audit = textAudit(s);
    const content = textSizes(c, false), meta = [...textSizes(s.querySelector('.top')), ...textSizes(s.querySelector('.foot')), ...textSizes(c, true)];
    return { n: i + 1, type: s.dataset.type, fit: fits.get(s), overflow: over(c),
             min_content_px: content.length ? Math.min(...content) : null,
             min_meta_px: meta.length ? Math.min(...meta) : null,
             min_contrast: audit.worst, light_weight: audit.light };
  });
  hit.remove(); window.scrollTo(0, 0);
  window.REPORT = { fonts_loaded: loaded, slides: rep };
  document.body.dataset.ready = '1';
})();
"""


# ---------------------------------------------------------------- helpers

def deep_merge(base, over):
    out = copy.deepcopy(base)
    for k, v in (over or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def hex_rgb(h):
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgba(h, a):
    r, g, b = hex_rgb(h)
    return f"rgba({r},{g},{b},{a})"


def luminance(h):
    def ch(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = hex_rgb(h)
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def fmt(text):
    """Escape copy; *word* -> accent emphasis; newlines -> <br>."""
    if text is None:
        return ""
    t = html.escape(str(text))
    t = re.sub(r"\*(.+?)\*", r"<em>\1</em>", t)
    return t.replace("\n", "<br>")


# Brand kit and themes: a brand/brand.json above the carousel (a project's own kit) wins; otherwise this
# skill's bundled assets/ (assets/brand, assets/themes). Carousels themselves live in the working folder.
ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")


def find_root(start):
    d = os.path.abspath(start)
    while True:
        if os.path.isfile(os.path.join(d, "brand", "brand.json")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return ASSETS if os.path.isfile(os.path.join(ASSETS, "brand", "brand.json")) else None


def load_json(path, default=None):
    if not os.path.isfile(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def now():
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


# ---------------------------------------------------------------- fonts

def font_entry(brand, family):
    for role in ("display", "body", "mono"):
        e = (brand.get("fonts") or {}).get(role) or {}
        if e.get("family") == family:
            return e
    for e in (brand.get("fonts") or {}).get("extra", []) or []:
        if e.get("family") == family:
            return e
    return {"family": family, "google": family.replace(" ", "+"), "fallback": "sans-serif"}


def font_head(brand, families, brand_dir):
    """<link> for Google-hosted families and @font-face for local files."""
    google, faces = [], []
    for fam in families:
        e = font_entry(brand, fam)
        if e.get("files"):
            for fl in e["files"]:
                p = os.path.abspath(os.path.join(brand_dir, fl["path"]))
                faces.append(
                    "@font-face{font-family:'%s';src:url('%s');font-weight:%s;font-style:%s;font-display:block}"
                    % (fam, "file://" + urllib.parse.quote(p), fl.get("weight", 400), fl.get("style", "normal")))
        elif e.get("google"):
            google.append("family=" + e["google"])
    head = ""
    if google:
        url = "https://fonts.googleapis.com/css2?" + "&".join(dict.fromkeys(google)) + "&display=block"
        head += f'<link rel="stylesheet" href="{html.escape(url)}">\n'
    if faces:
        head += "<style>" + "".join(faces) + "</style>\n"
    return head


def stack(brand, fam):
    e = font_entry(brand, fam)
    return f"'{fam}', {e.get('fallback', 'sans-serif')}"


# ---------------------------------------------------------------- slides

def root_vars(v, brand):
    c, t, L = v["colors"], v["type"], v["layout"]
    s = t["scale"]
    return (
        ":root{"
        f"--bg:{c['bg']};--text:{c['text']};--muted:{c['muted']};--accent:{c['accent']};"
        f"--fill:{c['fill']};--on-fill:{c['on_fill']};--on-fill-muted:{rgba(c['on_fill'], .78)};"
        f"--on-fill-line:{rgba(c['on_fill'], .3)};--on-fill-grid:{rgba(c['on_fill'], .1)};"
        f"--line:{rgba(c['text'], .16)};--grid:{rgba(c['text'], .05)};"
        f"--pattern:{rgba(c['text'], .08)};--pattern-blue:{rgba(c['fill'], .35)};"
        f"--f-display:{stack(brand, t['display'])};--f-body:{stack(brand, t['body'])};--f-mono:{stack(brand, t['mono'])};"
        f"--display-case:{'uppercase' if t.get('display_case') == 'upper' else 'none'};"
        f"--s-cover:{s['cover']}px;--s-headline:{s['headline']}px;--s-body:{s['body']}px;"
        f"--s-label:{s['label']}px;--s-number:{s['number']}px;--m:{L['margin']}px"
        "}"
    )


def pill(s):
    action = (s.get("action") or "save").lower()
    label = s.get("button") or {
        "save": "Save this", "follow": "Follow for the next one", "comment": "Comment below",
        "read": "Read the full post", "share": "Send to a founder", "dm": "DM us",
    }.get(action, action)
    icon = ICONS.get(action, ICONS["read"])
    return f'<div class="pill"><svg viewBox="0 0 24 24">{icon}</svg><span>{fmt(label)}</span></div>'


def items_html(items, numbered=True):
    lis = []
    for k, it in enumerate(items or [], 1):
        ix = f"{k:02d}" if numbered else "&#10003;"
        lis.append(f'<li><span class="ix">{ix}</span><span>{fmt(it)}</span></li>')
    return f'<ul class="list">{"".join(lis)}</ul>'


# ---------------------------------------------------------------- visuals
# A slide can carry one "visual": a UI mockup or diagram drawn in HTML/CSS in brand colours, so a
# carousel isn't a run of text-only slides. No photos (the brand bans them); these are product-style
# illustrations. Kinds: window, hud, flow, slots, dialog, funnel, tags, compare, chart, timeline. Format: references/visuals.md.

VIS_ICONS = {  # outline icons on a 24 grid, Lucide-style (1.5-2px stroke, round caps), drawn for this skill
    "layout": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/>',
    "shield": '<path d="M12 3l7 3v5c0 5-3.5 8.5-7 10-3.5-1.5-7-5-7-10V6z"/><path d="M9 12l2 2 4-4"/>',
    "slash": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M10.5 16l3-8"/>',
    "gamepad": '<path d="M7 8h10a5 5 0 0 1 5 5v1.5a2.5 2.5 0 0 1-4.6 1.4L16 14H8l-1.4 1.9A2.5 2.5 0 0 1 2 14.5V13a5 5 0 0 1 5-5z"/><path d="M7.5 10.5v3M6 12h3"/><path d="M15.5 11.5h.01M18 12.5h.01"/>',
    "terminal": '<path d="M4 17l6-6-6-6"/><path d="M12 19h8"/>',
    "eye": '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "alert": '<path d="M12 3l10 18H2z"/><path d="M12 10v4M12 17.5v.01"/>',
    "zap": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    "play": '<path d="M7 4l13 8-13 8z"/>',
    "heart": '<path d="M12 20s-8-4.6-8-10.5A4.5 4.5 0 0 1 12 7a4.5 4.5 0 0 1 8 2.5C20 15.4 12 20 12 20z"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
    "plug": '<path d="M9 2v5M15 2v5M6 7h12v4a6 6 0 0 1-12 0z"/><path d="M12 17v5"/>',
    "sparkle": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/>',
    "bookmark": '<path d="M6 3h12v18l-6-4.5L6 21z"/>',
    "code": '<path d="M8 7l-5 5 5 5M16 7l5 5-5 5"/>',
}
# pixel heart, 7x6 cells
_HEART = ["0110110", "1111111", "1111111", "0111110", "0011100", "0001000"]
_HEART_RECTS = "".join(f'<rect x="{x}" y="{y}" width="1" height="1"/>'
                       for y, row in enumerate(_HEART) for x, c in enumerate(row) if c == "1")


def _e(t):
    return html.escape(str(t if t is not None else ""))


def _icon(name):
    p = VIS_ICONS.get(str(name or ""), VIS_ICONS["sparkle"])
    return f'<svg class="ic" viewBox="0 0 24 24">{p}</svg>'


def _hearts(full, total=10):
    full, total = int(full), int(total)
    return "".join(f'<svg class="px-heart{"" if k < full else " off"}" viewBox="0 0 7 6" shape-rendering="crispEdges">{_HEART_RECTS}</svg>'
                   for k in range(total))


def _bar(value, segs=20):
    on = round(max(0.0, min(1.0, float(value))) * segs)
    return '<div class="seg-bar">' + "".join(f'<i class="{"on" if k < on else ""}"></i>' for k in range(segs)) + '</div>'


def _hud_rows(rows):
    out = []
    for r in rows or []:
        if "hearts" in r:
            h = r["hearts"] if isinstance(r["hearts"], list) else [r["hearts"], 10]
            meter = f'<div class="hearts">{_hearts(*h)}</div>'
        else:
            meter = _bar(r.get("bar", 0.5))
        tag = f'<span class="hud-tag">{_e(r["tag"])}</span>' if r.get("tag") else ""
        out.append(f'<div class="hud-row"><div class="hud-head"><span class="hud-label">{_e(r.get("label"))}</span>{tag}</div>{meter}</div>')
    return "".join(out)


def _lines(lines):
    out = []
    for ln in lines or []:
        if isinstance(ln, str):
            ln = {"t": ln}
        style = ln.get("s", "out")
        prefix = {"cmd": '<b class="pr">&gt;</b>', "shell": '<b class="pr">$</b>', "ok": '<b class="pr">&#10003;</b>'}.get(style, "")
        out.append(f'<div class="ln ln-{_e(style)}">{prefix}<span>{_e(ln.get("t"))}</span></div>')
    return "".join(out)


def visual_html(vis):
    if not vis:
        return ""
    k = vis.get("kind")
    tilt = f' style="--tilt:{float(vis["tilt"])}deg"' if vis.get("tilt") is not None else ""
    if k == "window":
        hud = f'<div class="win-hud">{_hud_rows(vis["hud"])}</div>' if vis.get("hud") else ""
        body = f'<div class="win-body">{_lines(vis["lines"])}</div>' if vis.get("lines") else ""
        toast = f'<div class="toast">{_icon(vis.get("toast_icon", "zap"))}<span>{_e(vis["toast"])}</span></div>' if vis.get("toast") else ""
        inner = (f'<div class="win"><div class="win-bar"><i></i><i></i><i></i><span>{_e(vis.get("title", ""))}</span></div>'
                 f'{hud}{body}</div>{toast}')
    elif k == "hud":
        inner = f'<div class="hud">{_hud_rows(vis.get("rows"))}</div>'
    elif k == "flow":
        outs = "".join(f'<div class="fl-chip fl-out">{_icon(o.get("icon")) if isinstance(o, dict) else ""}'
                       f'<span>{_e(o.get("t") if isinstance(o, dict) else o)}</span></div>' for o in vis.get("to") or [])
        inner = (f'<div class="flow"><div class="fl-chip fl-in">{_icon(vis.get("from_icon", "terminal"))}<span>{_e(vis.get("from"))}</span></div>'
                 f'<div class="fl-arrow"></div><div class="fl-chip fl-via">{_icon(vis.get("via_icon", "plug"))}<span>{_e(vis.get("via"))}</span></div>'
                 f'<div class="fl-arrow"></div><div class="fl-outs">{outs}</div></div>')  # stacked top to bottom
    elif k == "slots":
        act = vis.get("active")
        cells = []
        for n, it in enumerate(vis.get("items") or [], 1):
            on = " on" if act == n else ""
            cells.append(f'<div class="slot{on}"><span class="key">{n}</span>{_icon(it.get("icon"))}<span class="slot-label">{_e(it.get("label"))}</span></div>')
        cap = f'<div class="slots-cap">{_e(vis["caption"])}</div>' if vis.get("caption") else ""
        inner = f'<div class="slots n{len(cells)}">{"".join(cells)}</div>{cap}'
    elif k == "dialog":
        rows = "".join(f'<div class="dl-row">{_icon(r.get("icon", "check")) if isinstance(r, dict) else _icon("check")}'
                       f'<span>{_e(r.get("t") if isinstance(r, dict) else r)}</span></div>' for r in vis.get("rows") or [])
        btns = vis.get("buttons") or []
        prim = vis.get("primary", True)  # false on a CTA slide, so the CTA button is the only solid one
        bh = "".join(f'<span class="dl-btn{" primary" if prim and j == len(btns) - 1 else ""}">{_e(b)}</span>' for j, b in enumerate(btns))
        inner = (f'<div class="dialog"><div class="dl-title">{_icon(vis.get("icon", "shield"))}<span>{_e(vis.get("title"))}</span></div>'
                 f'<div class="dl-rows">{rows}</div>{f"<div class=dl-btns>{bh}</div>" if bh else ""}</div>')
    elif k == "funnel":
        st = vis.get("stages") or []
        n = len(st)
        rows = "".join(f'<div class="fn-stage" style="--w:{100 - j * (40 / max(n - 1, 1)):.0f}%">'
                       f'{_icon(x.get("icon")) if isinstance(x, dict) and x.get("icon") else ""}'
                       f'<span>{_e(x.get("t") if isinstance(x, dict) else x)}</span></div>' for j, x in enumerate(st))
        o = vis.get("out")
        out = (f'<div class="fn-arrow"></div><div class="fn-out">{_icon(o.get("icon", "check")) if isinstance(o, dict) else _icon("check")}'
               f'<span>{_e(o.get("t") if isinstance(o, dict) else o)}</span></div>') if o else ""
        inner = f'<div class="funnel">{rows}{out}</div>'
    elif k == "tags":
        act = vis.get("active") or []
        act = act if isinstance(act, list) else [act]
        tilts = (-3, 2, -1.5, 3, -2.5, 1.5, -1, 2.5)
        pills = "".join(f'<span class="tag{" on" if j in act else ""}" style="--tt:{tilts[(j - 1) % len(tilts)]}deg">{_e(t)}</span>'
                        for j, t in enumerate(vis.get("tags") or [], 1))
        cap = f'<div class="tags-cap">{_e(vis["caption"])}</div>' if vis.get("caption") else ""
        inner = f'<div class="tags">{pills}</div>{cap}'
    elif k == "compare":
        def col(c, cls, icon):
            c = c or {}
            rows = "".join(f'<div class="cp-row">{_icon(icon)}<span>{_e(r)}</span></div>' for r in c.get("rows") or [])
            return f'<div class="cp-col {cls}"><div class="cp-title">{_e(c.get("title", ""))}</div><div class="cp-rows">{rows}</div></div>'
        inner = f'<div class="compare">{col(vis.get("left"), "cp-before", "x")}{col(vis.get("right"), "cp-after", "check")}</div>'
    elif k == "chart":
        bars = vis.get("bars") or []
        top = max([float(b.get("value") or 0) for b in bars] or [1]) or 1
        rows = []
        for j, b in enumerate(bars, 1):
            val = f'<span class="ch-val">{_e(b["display"])}</span>' if b.get("display") else ""
            width = max(float(b.get("value") or 0) / top * 100, 3)
            rows.append(f'<div class="ch-row{" on" if vis.get("highlight") == j else ""}"><div class="ch-head">'
                        f'<span class="ch-label">{_e(b.get("label"))}</span>{val}</div>'
                        f'<div class="ch-track"><i style="width:{width:.1f}%"></i></div></div>')
        title = f'<div class="ch-title">{_e(vis["title"])}</div>' if vis.get("title") else ""
        inner = f'<div class="chart">{title}{"".join(rows)}</div>'
    elif k == "timeline":
        rows = []
        for j, x in enumerate(vis.get("steps") or [], 1):
            x = x if isinstance(x, dict) else {"t": x}
            when = f'<span class="tl-when">{_e(x["when"])}</span>' if x.get("when") else ""
            rows.append(f'<div class="tl-step{" on" if vis.get("active") == j else ""}"><div class="tl-node">{_icon(x.get("icon", "check"))}</div>'
                        f'<div class="tl-text">{when}<span class="tl-t">{_e(x.get("t"))}</span></div></div>')
        inner = f'<div class="timeline">{"".join(rows)}</div>'
    else:
        raise SystemExit(f"unknown visual kind '{k}' (window, hud, flow, slots, dialog, funnel, tags, compare, chart, timeline)")
    return f'<div class="visual v-{_e(k)}"{tilt}>{inner}</div>'


def content_html(s, v, carousel_dir):
    t = s.get("type", "point")
    hl, body = s.get("headline"), s.get("body")
    parts = []
    if t == "cover":
        if s.get("number"):
            parts.append(f'<div class="num">{fmt(s["number"])}</div>')
        parts.append(f'<h1 class="display h-cover">{fmt(hl)}</h1>')
        if s.get("sub"):
            parts.append(f'<p class="sub">{fmt(s["sub"])}</p>')
    elif t in ("stake", "point"):
        if v["layout"]["align"] != "center":
            parts.append('<div class="rule"></div>')
        parts.append(f'<h2 class="display h">{fmt(hl)}</h2>')
        if body:
            parts.append(f'<p class="body">{fmt(body)}</p>')
    elif t == "stat":
        parts.append(f'<div class="num">{fmt(s.get("number"))}</div>')
        if hl:
            parts.append(f'<h2 class="display h-sm">{fmt(hl)}</h2>')
        if body:
            parts.append(f'<p class="body">{fmt(body)}</p>')
        if s.get("source"):
            parts.append(f'<p class="source">Source: {fmt(s["source"])}</p>')
    elif t in ("steps", "recap"):
        if hl:
            parts.append(f'<h2 class="display h">{fmt(hl)}</h2>')
        parts.append(items_html(s.get("items"), numbered=(t == "steps" or s.get("numbered", False))))
        if body:
            parts.append(f'<p class="body">{fmt(body)}</p>')
    elif t == "quote":
        parts.append('<div class="quote-mark">&ldquo;</div>')
        parts.append(f'<p class="quote">{fmt(s.get("quote"))}</p>')
        if s.get("attribution"):
            parts.append(f'<p class="source">{fmt(s["attribution"])}</p>')
    elif t == "cta":
        parts.append(f'<h2 class="display h-cta">{fmt(hl)}</h2>')
        if body:
            parts.append(f'<p class="body">{fmt(body)}</p>')
        parts.append(pill(s))
    elif t == "image":
        src = s.get("image") or ""
        if src and not re.match(r"^[a-z]+:", src):
            src = os.path.relpath(os.path.join(carousel_dir, src), carousel_dir)
        parts.append(f'<img class="img" src="{html.escape(src)}" alt="">')
        if hl:
            parts.append(f'<h2 class="display h-sm">{fmt(hl)}</h2>')
        if body:
            parts.append(f'<p class="body">{fmt(body)}</p>')
    else:
        raise SystemExit(f"slide {s.get('n')}: unknown type '{t}'")
    vis = visual_html(s.get("visual"))
    if vis:  # after the headline (after the sub line on a cover), before body copy and buttons
        at = len(parts) if t == "cover" else next(
            (j + 1 for j, p in enumerate(parts) if 'class="display' in p or 'class="quote"' in p), len(parts))
        parts.insert(at, vis)
    return "\n".join(parts)


def slide_html(s, i, total, v, brand, carousel_dir):
    L = v["layout"]
    t = s.get("type", "point")
    cls = ["slide", f"t-{t}", f"align-{s.get('align') or L['align']}"]
    tex = s.get("texture", L.get("texture"))
    if tex in ("grid", "dots", "weave", "loop", "ascent"):
        cls.append(f"tex-{tex}")
    fill = s.get("fill")
    if fill is None:
        fill = (t == "cta" and L.get("cta_fill")) or t in (v.get("_fill_types") or [])
    if fill:
        cls.append("fill")
    if s.get("visual"):
        cls.append("has-visual")  # themes can step their own decoration aside for it
    kicker = s.get("kicker") if L.get("kicker") else None
    if kicker is None and t == "cover" and L.get("kicker"):
        kicker = brand.get("name", "")
    counter = f"{i:02d} / {total:02d}" if L.get("counter") else ""
    top = (f'<div class="top"><span class="kicker">{fmt(kicker or "")}</span><span>{counter}</span></div>'
           if (kicker or counter) else "")
    # footer: the site address bottom-left (brand.json "footer", else the handle), swipe cue bottom-right
    handle = fmt(brand.get("footer") or brand.get("handle", "")) if L.get("handle", True) else ""
    if i < total and L.get("swipe_cue", True):
        right = '<span class="cue">Swipe &rarr;</span>'
    elif i == total and L.get("last_cue"):
        right = f'<span class="cue">{fmt(L["last_cue"])}</span>'
    else:
        right = "<span></span>"
    foot = f'<div class="foot"><span>{handle}</span>{right}</div>'
    prog = f'<div class="progress" style="width:{i / total * 100:.2f}%"></div>' if L.get("progress", True) else ""
    # Hooks for themes: two empty decoration layers for shapes, and data attributes that theme CSS
    # can print with content: attr(...) (a big background word, a circular badge, the slide position).
    ghost = html.escape(str(s.get("ghost") or ""), quote=True)
    badge = html.escape(str(s.get("badge") or ""), quote=True)
    pos = "first" if i == 1 else ("last" if i == total else "mid")
    return (f'<section class="{" ".join(cls)}" data-type="{t}" data-n="{i}" data-total="{total}" data-pos="{pos}" '
            f'data-ghost="{ghost}" data-badge="{badge}" data-kicker="{html.escape(str(kicker or ""), quote=True)}">'
            f'<div class="decor"></div><div class="decor2"></div>'
            f'<div class="frame">{top}<div class="content">{content_html(s, v, carousel_dir)}</div>{foot}</div>{prog}</section>')


def theme_dirs(start, root):
    """Where themes are looked up, first match wins: a themes/ folder in the working project (walking up from
    the carousel), then the brand root's themes/, then the skill's bundled assets/themes."""
    out, d = [], os.path.abspath(start or ".")
    while True:
        if os.path.isdir(os.path.join(d, "themes")):
            out.append(os.path.join(d, "themes"))
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    for extra in (os.path.join(root, "themes"), os.path.join(ASSETS, "themes")):
        if extra not in out:
            out.append(extra)
    return out


THEME_START = None  # set by main() to the carousel folder, so project themes are found


def load_theme(root, name, _seen=None):
    """themes/<name>/theme.json (+ theme.css). Unknown theme -> error, so a typo can't silently fall back.
    "extends": "<parent>" reuses the parent's CSS and defaults (own CSS loads after, own defaults win);
    variants, fonts, palette and the brand mode are the child's own."""
    dirs = theme_dirs(THEME_START, root)
    d = next((os.path.join(t, name or "editorial") for t in dirs if os.path.isfile(os.path.join(t, name or "editorial", "theme.json"))),
             os.path.join(dirs[-1], name or "editorial"))
    meta = load_json(os.path.join(d, "theme.json"))
    if meta is None:
        if (name or "editorial") == "editorial":
            return {"name": "editorial", "defaults": {}}, ""
        avail = sorted({x for t in dirs if os.path.isdir(t) for x in os.listdir(t) if not x.startswith(("_", "."))
                        and os.path.isfile(os.path.join(t, x, "theme.json"))})
        raise SystemExit(f"Theme '{name}' not found in themes/. Available: {', '.join(avail) or 'none'}")
    css = ""
    if os.path.isfile(os.path.join(d, meta.get("css", "theme.css"))):
        with open(os.path.join(d, meta.get("css", "theme.css")), encoding="utf-8") as f:
            css = f.read()
    parent = meta.get("extends")
    if parent:
        seen = (_seen or set()) | {name}
        if parent in seen:
            raise SystemExit(f"Theme '{name}' extends '{parent}', which extends it back.")
        pmeta, pcss = load_theme(root, parent, seen)
        merged = deep_merge(pmeta, {k: v for k, v in meta.items() if k != "extends"})
        for k in ("variants", "fonts", "palette", "brand"):
            merged[k] = meta.get(k) if k in meta else ({} if k in ("variants", "palette") else [] if k == "fonts" else "locked")
        merged["fill_types"] = meta.get("fill_types", pmeta.get("fill_types") or [])
        meta, css = merged, pcss + "\n/* ---- " + str(name) + " (extends " + parent + ") ---- */\n" + css
    return meta, css


def with_theme_fonts(brand, v):
    """brand.json plus the fonts a free theme declares, so font_head/stack can load and name them."""
    tf = v.get("_theme_fonts") or []
    if not tf:
        return brand
    b = copy.deepcopy(brand)
    fonts = b.setdefault("fonts", {})
    fonts["extra"] = list(fonts.get("extra") or []) + list(tf)
    return b


def resolve_vision(root, vraw):
    """renderer defaults <- theme defaults <- theme variant <- this carousel's vision.json"""
    vraw = dict(vraw or {})
    if vraw.get("theme") in ("dark", "light"):  # older vision files used "theme" for the mode
        vraw["mode"] = vraw.pop("theme")
    meta, css = load_theme(root, vraw.get("theme") or DEFAULT_VISION["theme"])
    base = deep_merge(DEFAULT_VISION, meta.get("defaults") or {})
    variant = vraw.get("variant") or vraw.get("mode")
    if variant and variant in (meta.get("variants") or {}):
        base = deep_merge(base, meta["variants"][variant])
    v = deep_merge(base, vraw)
    v["theme"] = meta.get("name", v.get("theme"))
    v["_fill_types"] = meta.get("fill_types") or []
    v["_theme_css"] = css
    v["_brand_mode"] = meta.get("brand", "locked")   # "free": off-brand by design (own palette and fonts)
    v["_theme_fonts"] = meta.get("fonts") or []
    v["_theme_palette"] = meta.get("palette") or {}
    return v


def build_slides_html(v, script, brand, carousel_dir, root):
    brand = with_theme_fonts(brand, v)
    slides = script.get("slides") or []
    if not slides:
        raise SystemExit("script.json has no slides")
    fams = list(dict.fromkeys([v["type"]["display"], v["type"]["body"], v["type"]["mono"]]))
    body = "\n".join(slide_html(s, i, len(slides), v, brand, carousel_dir) for i, s in enumerate(slides, 1))
    title = html.escape(script.get("title") or os.path.basename(carousel_dir))
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{title}</title>
{font_head(brand, fams, os.path.join(root, "brand"))}<style>{root_vars(v, brand)}{CSS}{v.get("_theme_css") or ""}{v.get("custom_css") or ""}</style>
</head><body data-min-text="{int(v['layout'].get('min_text_px') or 0)}">
{body}
<script type="application/json" id="fams">{json.dumps(fams)}</script>
<script>{JS}</script>
</body></html>
"""


# ---------------------------------------------------------------- board

BOARD_CSS = r"""
*{box-sizing:border-box;margin:0;padding:0}
body{width:1500px;background:#17191E;color:#E9EBF0;font-family:var(--f-body);padding:64px}
.lbl{font-family:var(--f-mono);font-size:15px;letter-spacing:.14em;text-transform:uppercase;color:#9AA1B2}
.hd{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:2px solid #2B2F38;padding-bottom:24px;margin-bottom:36px}
.ttl{font-family:var(--f-display);font-size:52px;line-height:1.05;margin-top:10px;max-width:1000px}
.tag{font-family:var(--f-mono);font-size:15px;letter-spacing:.12em;text-transform:uppercase;padding:10px 16px;border:1.5px solid}
.panels{display:grid;grid-template-columns:1fr 1.35fr 1.2fr;gap:28px;margin-bottom:28px}
.card{background:#1F2228;border:1px solid #2B2F38;padding:26px;display:flex;flex-direction:column;gap:16px}
.chips{display:flex;flex-wrap:wrap;gap:10px}
.chip{font-size:20px;padding:8px 14px;border:1px solid #3A3F4A}
.sw{display:flex;gap:14px;align-items:center;font-size:17px}
.sw b{display:block;width:54px;height:54px;border:1px solid #3A3F4A;flex:none}
.sw .m{font-family:var(--f-mono);font-size:14px;color:#9AA1B2}
.ok{color:#7FD4A0}.bad{color:#FF8A7A}
.spec{display:flex;align-items:baseline;gap:16px;font-size:18px;color:#9AA1B2}
.spec .s{color:#E9EBF0}
.dec{font-size:18px;line-height:1.45}
.dec b{font-weight:600}
.grid{display:grid;grid-template-columns:repeat(4,324px);gap:44px 24px;margin-top:12px}
.refs{display:flex;gap:24px;flex-wrap:wrap;margin:12px 0 36px}
.ref{width:240px}
.ref img{width:240px;height:300px;object-fit:cover;display:block;border:1px solid #2B2F38}
.ref .cap{font-size:16px;line-height:1.4;color:#C9CDD6;margin-top:10px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:28px;margin-bottom:36px}
.th img{width:324px;height:405px;display:block;border:1px solid #2B2F38}
.th .cap{display:flex;justify-content:space-between;margin-top:12px}
"""


def build_board_html(v, script, brand, carousel_dir, root):
    brand = with_theme_fonts(brand, v)
    c, t, L = v["colors"], v["type"], v["layout"]
    fams = list(dict.fromkeys([t["display"], t["body"], t["mono"]]))
    status = (v.get("status") or "draft").upper()
    tag_color = "#7FD4A0" if status == "LOCKED" else "#F2B544"
    mood = "".join(f'<span class="chip">{fmt(m)}</span>' for m in v.get("mood") or []) or '<span class="m">(none yet)</span>'

    def sw(name, hexv, against=None, need=None):
        extra = ""
        if against:
            r = contrast(hexv, against)
            cls = "ok" if r >= need else "bad"
            extra = f' &middot; <span class="{cls}">{r:.1f}:1 on {"fill" if against == c["fill"] else "bg"}</span>'
        return f'<div class="sw"><b style="background:{hexv}"></b><div>{name}<div class="m">{hexv}{extra}</div></div></div>'

    swatches = "".join([
        sw("Background", c["bg"]),
        sw("Text", c["text"], c["bg"], 4.5),
        sw("Muted", c["muted"], c["bg"], 4.5),
        sw("Accent", c["accent"], c["bg"], 4.5),
        sw("Fill", c["fill"]),
        sw("On fill", c["on_fill"], c["fill"], 4.5),
    ])
    specs = (
        f'<div class="spec"><span class="s" style="font-family:var(--f-display);font-size:58px;line-height:1">Aa</span>{html.escape(t["display"])} &middot; display{" &middot; UPPERCASE" if t.get("display_case") == "upper" else ""}</div>'
        f'<div class="spec"><span class="s" style="font-size:30px">Aa</span>{html.escape(t["body"])} &middot; body {t["scale"]["body"]}px</div>'
        f'<div class="spec"><span class="s" style="font-family:var(--f-mono);font-size:24px">Aa</span>{html.escape(t["mono"])} &middot; labels {t["scale"]["label"]}px</div>'
    )
    layout_bits = [f'align {L["align"]}', f'margin {L["margin"]}px', f'texture {L.get("texture", "none")}']
    if L.get("cta_fill"):
        layout_bits.append("CTA on fill")
    if L.get("progress"):
        layout_bits.append("progress bar")
    layout = "".join(f'<span class="chip">{html.escape(b)}</span>' for b in layout_bits)
    decisions = "".join(
        f'<div class="dec"><b>{fmt(d.get("q"))}</b> &rarr; {fmt(d.get("answer"))}</div>' for d in v.get("decisions") or []
    ) or '<div class="dec" style="color:#9AA1B2">No designer decisions recorded yet.</div>'
    calls = "".join(
        f'<div class="dec"><b>{fmt(d.get("call"))}</b>{" &middot; " + fmt(d.get("why")) if d.get("why") else ""}</div>'
        for d in v.get("draft_calls") or []
    ) or '<div class="dec" style="color:#9AA1B2">None.</div>'
    refs_dir = os.path.join(carousel_dir, "refs")
    ref_files = sorted(f for f in os.listdir(refs_dir) if re.search(r"\.(png|jpe?g|webp|gif)$", f, re.I)) if os.path.isdir(refs_dir) else []
    ref_notes = v.get("references") or []
    ref_html = []
    for k, f in enumerate(ref_files):
        letter = chr(65 + k)
        note = next((r for r in ref_notes if r.get("file") == f or str(r.get("ref", "")).upper() == letter), {})
        ref_html.append(f'<div class="ref"><img src="refs/{html.escape(f)}"><div class="lbl" style="margin-top:10px">Ref {letter}</div>'
                        f'<div class="cap">{fmt(note.get("took", ""))}</div></div>')
    refs_block = (f'<div class="lbl">Designer references</div><div class="refs">{"".join(ref_html)}</div>' if ref_html else "")
    thumbs = []
    for i, s in enumerate(script.get("slides") or [], 1):
        thumbs.append(f'<div class="th"><img src="slides/{i:02d}.png?v={int(dt.datetime.now().timestamp())}">'
                      f'<div class="cap"><span class="lbl">{i:02d}</span><span class="lbl">{html.escape(s.get("type", ""))}</span></div></div>')
    title = fmt(script.get("title") or os.path.basename(carousel_dir))
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Board</title>
{font_head(brand, fams, os.path.join(root, "brand"))}<style>{root_vars(v, brand)}{BOARD_CSS}</style></head><body>
<div class="hd"><div><div class="lbl">Vision board &middot; theme {html.escape(v.get("theme", ""))}{(" / " + html.escape(str(v.get("variant")))) if v.get("variant") else ""} &middot; vision {html.escape(v.get("name") or "untitled")} &middot; {html.escape(str(v.get("mode", "")))}</div>
<div class="ttl">{title}</div></div><span class="tag" style="color:{tag_color};border-color:{tag_color}">{status}</span></div>
<div class="panels">
<div class="card"><div class="lbl">Mood</div><div class="chips">{mood}</div><div class="lbl" style="margin-top:8px">Layout</div><div class="chips">{layout}</div></div>
<div class="card"><div class="lbl">Palette</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">{swatches}</div></div>
<div class="card"><div class="lbl">Type</div>{specs}</div>
</div>
<div class="two"><div class="card"><div class="lbl">Designer decisions</div>{decisions}</div>
<div class="card"><div class="lbl">Claude's draft calls (not yet confirmed)</div>{calls}</div></div>
{refs_block}
<div class="lbl">Slides at roughly phone size</div>
<div class="grid">{"".join(thumbs)}</div>
<script>(async()=>{{await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode().catch(()=>{{}})));document.body.dataset.ready='1';}})();</script>
</body></html>
"""


# ---------------------------------------------------------------- chrome

def find_chrome():
    cands = [
        os.environ.get("CHROME_PATH"),
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        shutil.which("google-chrome"), shutil.which("google-chrome-stable"),
        shutil.which("chromium"), shutil.which("chromium-browser"), shutil.which("chrome"),
    ]
    home = os.path.expanduser("~")
    cands += sorted(glob.glob(f"{home}/Library/Caches/ms-playwright/chromium-*/chrome-mac*/*.app/Contents/MacOS/*"), reverse=True)
    cands += sorted(glob.glob(f"{home}/.cache/ms-playwright/chromium-*/chrome-linux*/chrome"), reverse=True)
    for c in cands:
        if c and os.path.isfile(c) and os.access(c, os.X_OK):
            return c
    return None


class Browser:
    """Minimal Chrome DevTools Protocol client over --remote-debugging-pipe (stdlib only)."""

    def __init__(self, binary):
        self.prof = tempfile.mkdtemp(prefix="carousel-chrome-")
        r1, w1 = os.pipe()  # we write -> chrome reads on fd 3
        r2, w2 = os.pipe()  # chrome writes on fd 4 -> we read
        a = fcntl.fcntl(r1, fcntl.F_DUPFD, 10)
        b = fcntl.fcntl(w2, fcntl.F_DUPFD, 10)

        def child_fds():
            os.dup2(a, 3)
            os.dup2(b, 4)

        self.proc = subprocess.Popen(
            [binary, "--headless=new", "--remote-debugging-pipe", "--disable-gpu", "--hide-scrollbars",
             "--no-first-run", "--no-default-browser-check", "--disable-extensions",
             "--allow-file-access-from-files", "--force-device-scale-factor=1",
             f"--user-data-dir={self.prof}", "about:blank"],
            preexec_fn=child_fds, close_fds=False,
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for fd in (r1, w2, a, b):
            os.close(fd)
        self.w, self.r = w1, r2
        self.buf, self.seq, self.queue = b"", 0, []

    def _read(self, timeout):
        while b"\0" not in self.buf:
            ready, _, _ = select.select([self.r], [], [], timeout)
            if not ready:
                raise TimeoutError("Chrome did not answer in time")
            chunk = os.read(self.r, 1 << 20)
            if not chunk:
                raise RuntimeError("Chrome exited unexpectedly")
            self.buf += chunk
        raw, self.buf = self.buf.split(b"\0", 1)
        return json.loads(raw)

    def _wait(self, pred, timeout=60):
        for i, m in enumerate(self.queue):
            if pred(m):
                return self.queue.pop(i)
        deadline = time.time() + timeout
        while True:
            m = self._read(max(0.05, deadline - time.time()))
            if pred(m):
                return m
            self.queue.append(m)
            if time.time() > deadline:
                raise TimeoutError("timed out waiting for Chrome")

    def send(self, method, params=None, session=None, timeout=60):
        self.seq += 1
        n = self.seq
        msg = {"id": n, "method": method, "params": params or {}}
        if session:
            msg["sessionId"] = session
        data = json.dumps(msg).encode() + b"\0"
        while data:
            data = data[os.write(self.w, data):]
        m = self._wait(lambda x: x.get("id") == n, timeout)
        if "error" in m:
            raise RuntimeError(f"{method}: {m['error'].get('message')}")
        return m.get("result", {})

    def page(self, w, h):
        tid = self.send("Target.createTarget", {"url": "about:blank"})["targetId"]
        sid = self.send("Target.attachToTarget", {"targetId": tid, "flatten": True})["sessionId"]
        self.send("Page.enable", session=sid)
        self.resize(sid, w, h)
        return sid

    def resize(self, sid, w, h):
        self.send("Emulation.setDeviceMetricsOverride",
                  {"width": w, "height": h, "deviceScaleFactor": 1, "mobile": False}, sid)

    def goto(self, sid, url, ready_timeout=60):
        self.queue = [m for m in self.queue if m.get("method") != "Page.loadEventFired"]
        self.send("Page.navigate", {"url": url}, sid)
        self._wait(lambda m: m.get("method") == "Page.loadEventFired" and m.get("sessionId") == sid, ready_timeout)
        self.js(sid, "new Promise(r => { const t = () => document.body.dataset.ready ? r(1) : setTimeout(t, 50); t(); })",
                ready_timeout)

    def js(self, sid, expr, timeout=60):
        res = self.send("Runtime.evaluate", {"expression": expr, "awaitPromise": True, "returnByValue": True},
                        sid, timeout)
        if "exceptionDetails" in res:
            raise RuntimeError("page script failed: " + json.dumps(res["exceptionDetails"])[:500])
        return res.get("result", {}).get("value")

    def shot(self, sid, path, w, h):
        res = self.send("Page.captureScreenshot",
                        {"format": "png", "clip": {"x": 0, "y": 0, "width": w, "height": h, "scale": 1}}, sid)
        with open(path, "wb") as f:
            f.write(base64.b64decode(res["data"]))

    def close(self):
        try:
            self.send("Browser.close", timeout=5)
        except Exception:
            pass
        try:
            self.proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.proc.kill()
        for fd in (self.w, self.r):
            try:
                os.close(fd)
            except OSError:
                pass
        shutil.rmtree(self.prof, ignore_errors=True)


def file_url(path):
    return "file://" + urllib.parse.quote(os.path.abspath(path))


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big")


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="Render a carousel folder to 1080x1350 PNGs.")
    ap.add_argument("carousel", help="path to carousels/<slug>")
    ap.add_argument("--only", help="comma-separated slide numbers to re-shoot")
    ap.add_argument("--html-only", action="store_true")
    ap.add_argument("--no-board", action="store_true")
    args = ap.parse_args()

    cdir = os.path.abspath(args.carousel)
    global THEME_START
    THEME_START = cdir
    root = find_root(cdir)
    if not root:
        sys.exit("No brand kit found: neither a brand/brand.json above this folder nor the skill's assets/brand/brand.json.")
    brand = load_json(os.path.join(root, "brand", "brand.json"), {})
    vraw = load_json(os.path.join(cdir, "vision.json"))
    script = load_json(os.path.join(cdir, "script.json"))
    if vraw is None or script is None:
        sys.exit("Need vision.json and script.json in the carousel folder.")
    v = resolve_vision(root, vraw)
    total = len(script.get("slides") or [])

    sh = os.path.join(cdir, "slides.html")
    with open(sh, "w", encoding="utf-8") as f:
        f.write(build_slides_html(v, script, brand, cdir, root))
    print(f"wrote {os.path.relpath(sh)}")
    if args.html_only:
        return

    binary = find_chrome()
    if not binary:
        print("No Chrome/Chromium found. slides.html is written; open it in a browser and export each slide, "
              "or set CHROME_PATH.", file=sys.stderr)
        sys.exit(2)

    os.makedirs(os.path.join(cdir, "slides"), exist_ok=True)
    wanted = list(range(1, total + 1))
    if args.only:
        wanted = [int(x) for x in args.only.split(",") if x.strip()]
    for stale in glob.glob(os.path.join(cdir, "slides", "*.png")):
        n = int(re.sub(r"\D", "", os.path.basename(stale)) or 0)
        if n > total:
            os.remove(stale)

    browser = Browser(binary)
    problems = []
    try:
        # 1. lay out every slide: shrink-to-fit, then measure overflow, type sizes, fonts
        sid = browser.page(W, H)
        browser.goto(sid, file_url(sh))
        report = browser.js(sid, "window.REPORT")
        # 2. shoot each slide
        for n in wanted:
            out = os.path.join(cdir, "slides", f"{n:02d}.png")
            browser.js(sid, f"show({n})")
            browser.shot(sid, out, W, H)
            if png_size(out) != (W, H):
                problems.append(f"slide {n}: expected {W}x{H}, got {png_size(out)}")
        report.update({"rendered_at": now(), "chrome": binary, "size": [W, H], "problems": problems,
                       "vision_resolved": dict({k: v[k] for k in ("theme", "colors", "type", "layout")},
                                               brand_mode=v["_brand_mode"], theme_palette=v["_theme_palette"],
                                               theme_fonts=[f.get("family") for f in v["_theme_fonts"]])})
        write_json(os.path.join(cdir, "render_report.json"), report)
        # 3. board
        if not args.no_board:
            bh = os.path.join(cdir, "board.html")
            with open(bh, "w", encoding="utf-8") as f:
                f.write(build_board_html(v, script, brand, cdir, root))
            bid = browser.page(1500, 1200)
            browser.goto(bid, file_url(bh))
            height = int(browser.js(bid, "document.documentElement.scrollHeight"))
            browser.resize(bid, 1500, height)
            browser.shot(bid, os.path.join(cdir, "board.png"), 1500, height)
    finally:
        browser.close()

    # 4. status
    sp = os.path.join(cdir, "status.json")
    st = load_json(sp, {}) or {}
    st["slug"] = os.path.basename(cdir)
    st.setdefault("history", [])
    st["stage"] = "rendered" if v.get("status") == "locked" else "vision_draft"
    st["updated"] = now()
    st["history"].append({"at": st["updated"], "event": "rendered",
                          "slides": wanted if args.only else "all", "vision": v.get("status")})
    write_json(sp, st)

    # 5. summary
    fl = report.get("fonts_loaded", {})
    print(f"rendered {len(wanted)} slide(s) -> {os.path.relpath(os.path.join(cdir, 'slides'))}/")
    for fam, ok in fl.items():
        if not ok:
            print(f"  ! font not loaded, fell back: {fam}")
    for s in report["slides"]:
        flags = []
        if s["overflow"]:
            flags.append("OVERFLOW (text clipped)")
        if s["fit"] < 1:
            flags.append(f"shrunk to {int(s['fit'] * 100)}%")
        if flags:
            print(f"  slide {s['n']:02d} {s['type']}: " + ", ".join(flags))
    for p in problems:
        print("  ! " + p)
    if not args.no_board:
        print(f"board -> {os.path.relpath(os.path.join(cdir, 'board.png'))}")


if __name__ == "__main__":
    main()
