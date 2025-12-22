module.exports = function(eleventyConfig) {
  eleventyConfig.addPassthroughCopy({ "site/assets": "assets" });
  eleventyConfig.addPassthroughCopy({ "site/public": "." });
  eleventyConfig.addPassthroughCopy({
    "node_modules/openseadragon/build/openseadragon/openseadragon.min.js": "assets/vendor/openseadragon.min.js",
    "node_modules/openseadragon/build/openseadragon/images": "assets/vendor/openseadragon-images"
  });

  return {
    dir: {
      input: "site",
      includes: "_includes",
      data: "_data",
      output: "dist"
    }
  };
};
