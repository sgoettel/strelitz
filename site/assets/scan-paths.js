const fs = require('fs');
const path = require('path');

const MANIFEST_PATH = path.join(__dirname, '..', '_data', 'scan-manifest.json');
let cachedManifest;

const loadManifest = () => {
  if (cachedManifest) {
    return cachedManifest;
  }
  if (!fs.existsSync(MANIFEST_PATH)) {
    throw new Error(`Scan manifest missing at ${MANIFEST_PATH}. Run scripts/build_scan_manifest.js first.`);
  }
  const raw = fs.readFileSync(MANIFEST_PATH, 'utf-8');
  cachedManifest = JSON.parse(raw);
  return cachedManifest;
};

const resolveScanAssets = (pageNumber) => {
  const manifest = loadManifest();
  const key = String(pageNumber);
  const entry = manifest.byPb?.[key];
  if (!entry) {
    const known = Object.keys(manifest.byPb || {});
    throw new Error(
      `No scan mapping found for pb="${key}". Known pb values: ${known.slice(0, 10).join(', ')}${known.length > 10 ? '…' : ''}`
    );
  }

  return {
    pageNumber: Number.isFinite(Number(pageNumber)) ? Number(pageNumber) : pageNumber,
    imageNumber: entry.imageNumber,
    imageUrl: entry.image,
    thumbUrl: entry.thumb
  };
};

module.exports = {
  resolveScanAssets
};
