(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.ScanPaths = factory();
  }
})(typeof self !== 'undefined' ? self : this, function () {
  const basePath = '/friedhofsregister_der_juedischen_gemeinde_strelitz';

  function resolveScanAssets(pageNumber) {
    const pageNo = Number(pageNumber);
    const validPage = Number.isFinite(pageNo) ? pageNo : null;
    const imageNumber = validPage !== null ? validPage + 1 : null;
    const imageUrl = imageNumber !== null ? `${basePath}/jpg/altstrelitz_friedregister${imageNumber}.jpg` : null;
    const thumbUrl = imageNumber !== null ? `${basePath}/jpg/thumbs/altstrelitz_friedregister_thumbs_${imageNumber}.jpg` : null;

    return { pageNumber: validPage, imageNumber, imageUrl, thumbUrl, basePath };
  }

  return { resolveScanAssets };
});
