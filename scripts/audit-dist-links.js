#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const DIST_DIR = path.join(ROOT, 'dist');

const resolvePathPrefix = () => {
  if (process.env.ELEVENTY_PATH_PREFIX) {
    return process.env.ELEVENTY_PATH_PREFIX;
  }
  if (process.env.GITHUB_REPOSITORY) {
    const repo = process.env.GITHUB_REPOSITORY.split('/')[1];
    if (repo) {
      return `/${repo}`;
    }
  }
  return '';
};

const PATH_PREFIX = resolvePathPrefix();

const isExternal = (value) => /^(?:[a-z]+:)?\/\//i.test(value) || /^(mailto|tel|data|javascript):/i.test(value);

const walkDir = (dir) => {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...walkDir(fullPath));
    } else {
      files.push(fullPath);
    }
  }
  return files;
};

const normalizeTarget = (target, currentDir) => {
  if (!target) {
    return null;
  }
  const trimmed = target.trim();
  if (!trimmed || trimmed.startsWith('#')) {
    return null;
  }
  if (isExternal(trimmed)) {
    return null;
  }

  const cleanTarget = trimmed.split('#')[0].split('?')[0];
  if (!cleanTarget) {
    return null;
  }

  if (cleanTarget.startsWith('/')) {
    const withPrefix = PATH_PREFIX && cleanTarget.startsWith(PATH_PREFIX)
      ? cleanTarget.slice(PATH_PREFIX.length)
      : cleanTarget;
    return path.join(DIST_DIR, withPrefix);
  }

  return path.join(currentDir, cleanTarget);
};

const resolveFile = (targetPath) => {
  if (!targetPath) {
    return null;
  }
  if (fs.existsSync(targetPath) && fs.statSync(targetPath).isFile()) {
    return targetPath;
  }
  if (fs.existsSync(targetPath) && fs.statSync(targetPath).isDirectory()) {
    const indexPath = path.join(targetPath, 'index.html');
    if (fs.existsSync(indexPath)) {
      return indexPath;
    }
  }
  if (!path.extname(targetPath)) {
    const indexPath = path.join(targetPath, 'index.html');
    if (fs.existsSync(indexPath)) {
      return indexPath;
    }
  }
  return null;
};

const extractLinks = (html) => {
  const links = [];
  const hrefRegex = /href\s*=\s*"([^"]+)"/gi;
  const srcRegex = /src\s*=\s*"([^"]+)"/gi;
  const srcsetRegex = /srcset\s*=\s*"([^"]+)"/gi;
  let match;

  while ((match = hrefRegex.exec(html)) !== null) {
    links.push(match[1]);
  }
  while ((match = srcRegex.exec(html)) !== null) {
    links.push(match[1]);
  }
  while ((match = srcsetRegex.exec(html)) !== null) {
    const entries = match[1].split(',').map((item) => item.trim().split(' ')[0]);
    links.push(...entries);
  }
  return links;
};

const main = () => {
  if (!fs.existsSync(DIST_DIR)) {
    console.error(`[audit] dist directory not found at ${DIST_DIR}`);
    process.exit(1);
  }

  const htmlFiles = walkDir(DIST_DIR).filter((file) => file.endsWith('.html'));
  const missing = [];

  htmlFiles.forEach((file) => {
    const html = fs.readFileSync(file, 'utf-8');
    const links = extractLinks(html);
    const currentDir = path.dirname(file);

    links.forEach((link) => {
      const targetPath = normalizeTarget(link, currentDir);
      if (!targetPath) {
        return;
      }
      const resolved = resolveFile(targetPath);
      if (!resolved) {
        missing.push({ file: path.relative(DIST_DIR, file), link });
      }
    });
  });

  if (missing.length) {
    console.error('[audit] Missing referenced assets or pages:');
    missing.slice(0, 200).forEach((entry) => {
      console.error(`- ${entry.file}: ${entry.link}`);
    });
    if (missing.length > 200) {
      console.error(`...and ${missing.length - 200} more`);
    }
    process.exit(1);
  }

  console.log('[audit] All href/src references resolved in dist.');
};

main();
