const nunjucks = require('nunjucks');
const scanPaths = require('./site/assets/scan-paths');
const repoData = require('./site/_data/repo.json');

function resolvePathPrefix() {
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
}

module.exports = function(eleventyConfig) {
  const pathPrefix = resolvePathPrefix();
  eleventyConfig.addGlobalData("pathPrefix", pathPrefix);
  eleventyConfig.addGlobalData("repo", repoData);

  eleventyConfig.addPassthroughCopy({ "site/assets": "assets" });
  eleventyConfig.addPassthroughCopy({ "site/public": "." });
  eleventyConfig.addPassthroughCopy({
    "friedhofsregister_der_juedischen_gemeinde_strelitz": "friedhofsregister_der_juedischen_gemeinde_strelitz"
  });
  eleventyConfig.addPassthroughCopy({
    "node_modules/openseadragon/build/openseadragon/openseadragon.min.js": "assets/vendor/openseadragon.min.js",
    "node_modules/openseadragon/build/openseadragon/images": "assets/vendor/openseadragon-images"
  });

  eleventyConfig.addFilter('sortEntries', (entries) => {
    if (!Array.isArray(entries)) return entries;
    return [...entries].sort((a, b) => {
      const aNo = Number(a.no);
      const bNo = Number(b.no);
      const aHasNo = Number.isFinite(aNo);
      const bHasNo = Number.isFinite(bNo);
      if (aHasNo && bHasNo) {
        return aNo - bNo;
      }
      if (aHasNo !== bHasNo) {
        return aHasNo ? -1 : 1;
      }
      return String(a.id).localeCompare(String(b.id));
    });
  });

  eleventyConfig.addFilter('scanAssets', (pageNo) => scanPaths.resolveScanAssets(pageNo));

  // Liquid-only: allow using | safe in .html (Liquid) templates
  eleventyConfig.addLiquidFilter("safe", (value) => value);

  // Nunjucks: allow rendering trusted HTML strings in entry.njk via | safeHtml
  // Only mark HTML as safe when it comes from the whitelist serializer (entry.text_html).
  eleventyConfig.addNunjucksFilter("safeHtml", (value) => {
    if (typeof value !== "string") {
      return value;
    }
    return new nunjucks.runtime.SafeString(value);
  });

  eleventyConfig.addGlobalData("pathPrefix", pathPrefix);

  return {
    pathPrefix,
    dir: {
      input: "site",
      includes: "_includes",
      data: "_data",
      output: "dist"
    }
  };
};
