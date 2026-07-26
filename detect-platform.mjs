#!/usr/bin/env node
/**
 * 自动识别视频来源平台：B 站 / 小红书
 *
 * Usage:
 *   node detect-platform.mjs "<url>"
 *   echo '{"url":"..."}' | node detect-platform.mjs
 */
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { URL } from 'node:url';

const BILIBILI_HOSTS = new Set([
  'bilibili.com',
  'www.bilibili.com',
  'm.bilibili.com',
  'b23.tv',
  'www.b23.tv',
]);

const XIAOHONGSHU_HOSTS = new Set([
  'xiaohongshu.com',
  'www.xiaohongshu.com',
  'xhslink.com',
  'www.xhslink.com',
  'xhslink.cn',
  'www.xhslink.cn',
]);

function normalizeHost(hostname) {
  return String(hostname || '')
    .trim()
    .toLowerCase()
    .replace(/:\d+$/, '');
}

function hostMatches(hostname, allowed) {
  const host = normalizeHost(hostname);
  if (!host) return false;
  if (allowed.has(host)) return true;
  return [...allowed].some(
    domain => host === domain || host.endsWith(`.${domain}`)
  );
}

export function detectPlatform(rawUrl) {
  const input = String(rawUrl || '').trim();
  if (!input) {
    return {
      ok: false,
      error: 'missing_url',
      message: 'url 字段缺失或为空',
    };
  }

  let parsed;
  try {
    parsed = new URL(input.includes('://') ? input : `https://${input}`);
  } catch {
    return {
      ok: false,
      error: 'invalid_url',
      message: 'url 无法解析',
      url: input,
    };
  }

  const host = normalizeHost(parsed.hostname);
  if (hostMatches(host, BILIBILI_HOSTS)) {
    return {
      ok: true,
      platform: 'bilibili',
      label: 'B站',
      url: parsed.toString(),
      host,
      downloadStrategy: 'bilibili',
    };
  }

  if (hostMatches(host, XIAOHONGSHU_HOSTS)) {
    return {
      ok: true,
      platform: 'xiaohongshu',
      label: '小红书',
      url: parsed.toString(),
      host,
      downloadStrategy: 'xiaohongshu',
    };
  }

  return {
    ok: false,
    error: 'unsupported_host',
    message: '仅支持 bilibili.com / b23.tv / xiaohongshu.com / xhslink.cn',
    url: parsed.toString(),
    host,
  };
}

function readStdin() {
  return new Promise(resolve => {
    if (process.stdin.isTTY) {
      resolve('');
      return;
    }
    let data = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', chunk => {
      data += chunk;
    });
    process.stdin.on('end', () => resolve(data));
  });
}

async function main() {
  const arg = process.argv[2];
  let url = arg;
  if (!url) {
    const stdin = (await readStdin()).trim();
    if (stdin.startsWith('{')) {
      try {
        url = JSON.parse(stdin).url;
      } catch {
        url = stdin;
      }
    } else {
      url = stdin;
    }
  }

  const result = detectPlatform(url);
  console.log(JSON.stringify(result, null, 2));
  process.exit(result.ok ? 0 : 1);
}

const isCli =
  process.argv[1] &&
  path.resolve(process.argv[1]) === path.resolve(fileURLToPath(import.meta.url));
if (isCli) {
  main();
}
