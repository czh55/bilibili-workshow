#!/usr/bin/env node
/**
 * Serializes Xiaohongshu network requests across local automation runs.
 * Invoke immediately before every yt-dlp request to a Xiaohongshu URL.
 */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const intervalMs = 60_000;
const stateFile = process.env.XHS_RATE_LIMIT_FILE ||
  path.join(os.tmpdir(), 'bilibili-workshop-xhs-last-request');
const lockFile = `${stateFile}.lock`;

const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

async function acquireLock() {
  while (true) {
    try {
      return fs.openSync(lockFile, 'wx');
    } catch (error) {
      if (error.code !== 'EEXIST') throw error;
      await sleep(100);
    }
  }
}

const lock = await acquireLock();
try {
  const lastRequest = Number(
    fs.existsSync(stateFile) ? fs.readFileSync(stateFile, 'utf8') : 0
  );
  const waitMs = Math.max(0, intervalMs - (Date.now() - lastRequest));
  if (waitMs > 0) {
    console.log(`小红书请求限流：等待 ${Math.ceil(waitMs / 1000)} 秒`);
    await sleep(waitMs);
  }

  // Reserve the slot while holding the lock. The following request must start now.
  fs.writeFileSync(stateFile, String(Date.now()));
} finally {
  lock.close();
  fs.unlinkSync(lockFile);
}
