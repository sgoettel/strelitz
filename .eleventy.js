const scanPaths = require('./site/assets/scan-paths');

module.exports = function(eleventyConfig) {
  eleventyConfig.addPassthroughCopy({ "site/assets": "assets" });
  eleventyConfig.addPassthroughCopy({ "site/public": "." });
  eleventyConfig.addPassthroughCopy({
    "node_modules/openseadragon/build/openseadragon/openseadragon.min.js": "assets/vendor/openseadragon.min.js",
    "node_modules/openseadragon/build/openseadragon/images": "assets/vendor/openseadragon-images"
  });

  eleventyConfig.addFilter('sortEntries', (entries) => {
    if (!Array.isArray(entries)) return entries;
    return [...entries].sort((a, b) => {
      const ai = Number(a.id);
      const bi = Number(b.id);
      if (Number.isFinite(ai) && Number.isFinite(bi)) {
        return ai - bi;
      }
      return String(a.id).localeCompare(String(b.id));
    });
  });

  eleventyConfig.addFilter('scanAssets', (pageNo) => scanPaths.resolveScanAssets(pageNo));

  return {
    dir: {
      input: "site",
      includes: "_includes",
      data: "_data",
      output: "dist"
    }
  };
};
