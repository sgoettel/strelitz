#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const TEI_DIR = path.join(ROOT, 'friedhofsregister_der_juedischen_gemeinde_strelitz', 'TEI');
const JPG_DIR = path.join(ROOT, 'friedhofsregister_der_juedischen_gemeinde_strelitz', 'jpg');
const THUMBS_DIR = path.join(JPG_DIR, 'thumbs');
const OUTPUT = path.join(ROOT, 'site', '_data', 'scan-manifest.json');

const PB_REGEX = /<pb\b[^>]*\bn=["']([^"']+)["'][^>]*>/g;
const IMAGE_PATTERNS = [
  /altstrelitz_friedregister(?:_thumbs_)?(\d+)\.(?:jpe?g|png)$/i,
  /(\d+)\.(?:jpe?g|png)$/i
];

const toPosix = (value) => value.split(path.sep).join('/');

const walkDir = (dir) => {
  if (!fs.existsSync(dir)) {
    return [];
  }
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const results = [];
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      results.push(...walkDir(fullPath));
    } else {
      results.push(fullPath);
    }
  }
  return results;
};

const extractPbValues = (content) => {
  const values = [];
  let match;
  while ((match = PB_REGEX.exec(content)) !== null) {
    const value = match[1].trim();
    if (value) {
      values.push(value);
    }
  }
  return values;
};

const extractNumber = (filename) => {
  for (const pattern of IMAGE_PATTERNS) {
    const match = filename.match(pattern);
    if (match) {
      return Number.parseInt(match[1], 10);
    }
  }
  return null;
};

const listImages = (dir, { excludeThumbs } = { excludeThumbs: false }) => {
  const files = walkDir(dir);
  return files
    .filter((file) => /\.(jpe?g|png)$/i.test(file))
    .filter((file) => {
      const rel = path.relative(dir, file);
      if (!excludeThumbs) {
        return true;
      }
      return !rel.split(path.sep).includes('thumbs') && !/thumbs/i.test(path.basename(file));
    })
    .map((file) => {
      const rel = path.relative(dir, file);
      return {
        file,
        relative: toPosix(rel),
        filename: path.basename(file),
        number: extractNumber(path.basename(file))
      };
    })
    .filter((entry) => Number.isFinite(entry.number));
};

const fail = (message) => {
  console.error(`\n[scan-manifest] ${message}\n`);
  process.exit(1);
};

const main = () => {
  if (!fs.existsSync(TEI_DIR)) {
    fail(`TEI directory not found: ${TEI_DIR}`);
  }

  const teiFiles = fs.readdirSync(TEI_DIR).filter((file) => file.endsWith('.xml')).sort();
  if (!teiFiles.length) {
    fail(`No TEI XML files found in ${TEI_DIR}`);
  }

  const pbValuesOrdered = [];
  const seenPb = new Set();
  const duplicatePb = new Set();

  for (const file of teiFiles) {
    const content = fs.readFileSync(path.join(TEI_DIR, file), 'utf-8');
    const values = extractPbValues(content);
    values.forEach((value) => {
      if (seenPb.has(value)) {
        duplicatePb.add(value);
        return;
      }
      seenPb.add(value);
      pbValuesOrdered.push(value);
    });
  }

  if (!pbValuesOrdered.length) {
    fail('No <pb n="..."> markers were found in TEI files.');
  }

  const images = listImages(JPG_DIR, { excludeThumbs: true }).sort((a, b) => {
    if (a.number !== b.number) {
      return a.number - b.number;
    }
    return a.filename.localeCompare(b.filename);
  });

  const thumbs = listImages(THUMBS_DIR).sort((a, b) => {
    if (a.number !== b.number) {
      return a.number - b.number;
    }
    return a.filename.localeCompare(b.filename);
  });

  if (!images.length) {
    fail(`No scan images found in ${JPG_DIR}`);
  }

  if (pbValuesOrdered.length > images.length) {
    fail([
      `Only ${images.length} scan images found for ${pbValuesOrdered.length} TEI <pb> markers.`,
      `Active filename patterns: ${IMAGE_PATTERNS.map((re) => re.toString()).join(', ')}`,
      `Files found: ${images.map((image) => image.filename).join(', ')}`
    ].join('\n'));
  }

  const thumbByNumber = new Map();
  thumbs.forEach((thumb) => {
    thumbByNumber.set(thumb.number, thumb);
  });

  const byPb = {};
  pbValuesOrdered.forEach((pbValue, index) => {
    const image = images[index];
    if (!image) {
      fail([
        `Missing scan image for pb="${pbValue}" at position ${index + 1}.`,
        `Active filename patterns: ${IMAGE_PATTERNS.map((re) => re.toString()).join(', ')}`,
        `Files found: ${images.map((entry) => entry.filename).join(', ')}`
      ].join('\n'));
    }

    const imageUrl = `/friedhofsregister_der_juedischen_gemeinde_strelitz/jpg/${image.relative}`;
    const thumbMatch = thumbByNumber.get(image.number);
    const thumbUrl = thumbMatch
      ? `/friedhofsregister_der_juedischen_gemeinde_strelitz/jpg/thumbs/${thumbMatch.relative}`
      : null;

    byPb[pbValue] = {
      image: imageUrl,
      thumb: thumbUrl,
      imageNumber: image.number
    };
  });

  const manifest = {
    byPb,
    meta: {
      generatedAt: new Date().toISOString(),
      pbCount: pbValuesOrdered.length,
      imageCount: images.length,
      thumbCount: thumbs.length,
      duplicatePb: Array.from(duplicatePb),
      rules: IMAGE_PATTERNS.map((re) => re.toString())
    }
  };

  fs.mkdirSync(path.dirname(OUTPUT), { recursive: true });
  fs.writeFileSync(OUTPUT, JSON.stringify(manifest, null, 2), 'utf-8');
  console.log(`[scan-manifest] Wrote ${pbValuesOrdered.length} mappings to ${OUTPUT}`);
};

main();
