#!/usr/bin/env node
/**
 * Wrap "详细文字转录" in <details> (collapsed by default) across article HTML files.
 */
import fs from 'node:fs';
import path from 'node:path';

const DOCS = path.join(import.meta.dirname, '..', 'docs');

const COLLAPSE_CSS = `.transcript-collapsible{border:none;margin:0;padding:0}.transcript-collapsible summary{display:flex;align-items:center;gap:10px;cursor:pointer;list-style:none;user-select:none;font-size:24px;font-weight:700;color:#1c1917;margin:0;padding-bottom:8px;border-bottom:2px solid #e7e5e4}.transcript-collapsible summary::-webkit-details-marker,.transcript-collapsible summary::marker{display:none}.transcript-collapsible summary::before{content:"▶";font-size:12px;color:#b45309;transition:transform .2s;flex-shrink:0}.transcript-collapsible[open] summary::before{transform:rotate(90deg)}.transcript-collapsible[open] summary{margin-bottom:16px}.transcript-collapsible .transcript-body{margin-top:0}`;

const TRANSCRIPT_SCRIPT = `<script>(function(){var d=document.querySelector(".transcript-collapsible");if(!d)return;function open(){d.setAttribute("open","")}document.querySelectorAll('a[href="#transcript"]').forEach(function(a){a.addEventListener("click",open)});if(location.hash==="#transcript")open()})();</script>`;

function ensureCss(html) {
  if (html.includes('.transcript-collapsible{')) return html;
  if (html.includes('</style>')) {
    return html.replace('</style>', `${COLLAPSE_CSS}</style>`);
  }
  return html;
}

function ensureScript(html) {
  if (html.includes('a[href="#transcript"]')) return html;
  if (html.includes('</body>')) {
    return html.replace('</body>', `${TRANSCRIPT_SCRIPT}</body>`);
  }
  return html;
}

function collapseTranscript(html) {
  if (html.includes('class="transcript-collapsible"')) return html;

  const sectionRe = /(<section class="transcript-section"[^>]*>)\s*<h2>详细文字转录<\/h2>/;
  if (!sectionRe.test(html)) return html;

  let updated = html.replace(
    sectionRe,
    '$1<details class="transcript-collapsible"><summary>详细文字转录</summary><div class="transcript-body">'
  );

  // Close details before the transcript section ends.
  updated = updated.replace(
    /(<section class="transcript-section"[^>]*>[\s\S]*?)<\/section>/,
    '$1</div></details></section>'
  );

  return updated;
}

function processFile(filePath) {
  const original = fs.readFileSync(filePath, 'utf8');
  let html = original;
  html = ensureCss(html);
  html = collapseTranscript(html);
  html = ensureScript(html);

  if (html !== original) {
    fs.writeFileSync(filePath, html, 'utf8');
    return true;
  }
  return false;
}

const files = fs.readdirSync(DOCS)
  .filter(name => name.endsWith('-图文实录.html'))
  .map(name => path.join(DOCS, name));

let changed = 0;
for (const file of files) {
  if (processFile(file)) changed++;
}

console.log(`Updated ${changed} / ${files.length} article files`);
