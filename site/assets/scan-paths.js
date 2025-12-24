(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.ScanPaths = factory();
  }
})(typeof self !== 'undefined' ? self : this, function () {
  function getPathPrefix() {
    if (typeof globalThis !== 'undefined' && typeof globalThis.__ELEVENTY_PATH_PREFIX__ === 'string') {
      return globalThis.__ELEVENTY_PATH_PREFIX__;
    }
    if (typeof process !== 'undefined' && process.env) {
      if (process.env.ELEVENTY_PATH_PREFIX) {
        return process.env.ELEVENTY_PATH_PREFIX;
      }
      if (process.env.GITHUB_REPOSITORY) {
        const repo = process.env.GITHUB_REPOSITORY.split('/')[1];
        if (repo) {
          return `/${repo}`;
        }
      }
    }
    return '';
  }

  function buildBasePath() {
    const prefix = getPathPrefix();
    const normalized = prefix && prefix !== '/' ? prefix.replace(/\/$/, '') : '';
    return `${normalized}/friedhofsregister_der_juedischen_gemeinde_strelitz`;
  }

  function resolveScanAssets(pageNumber) {
    const basePath = buildBasePath();
    const pageNo = Number(pageNumber);
    const validPage = Number.isFinite(pageNo) ? pageNo : null;
    const imageNumber = validPage !== null ? validPage + 1 : null;
    const imageUrl = imageNumber !== null ? `${basePath}/jpg/altstrelitz_friedregister${imageNumber}.jpg` : null;
    const thumbUrl = imageNumber !== null ? `${basePath}/jpg/thumbs/altstrelitz_friedregister_thumbs_${imageNumber}.jpg` : null;

    return { pageNumber: validPage, imageNumber, imageUrl, thumbUrl, basePath };
  }

  return { resolveScanAssets };
});
