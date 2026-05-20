module.exports = function(eleventyConfig) {

  eleventyConfig.addPassthroughCopy("assets");
  eleventyConfig.addPassthroughCopy("admin");
  eleventyConfig.addPassthroughCopy("pages/*.html");
  eleventyConfig.addPassthroughCopy("*.html");
  eleventyConfig.addPassthroughCopy("robots.txt");

  const folders = {
    nursingCarePlan: "nursing-care-plan",
    surgicalCarePlan: "surgical-care-plan",
    caseStudy: "case-study",
    healthTalk: "health-talk",
    healthEducation: "health-education",
    procedure: "procedure",
    assignment: "assignment",
    nursingNotes: "nursing-notes",
    familyFolder: "family-folder"
  };

  Object.keys(folders).forEach(name => {
    eleventyConfig.addCollection(name, function(collection) {
      return collection.getFilteredByGlob(`${folders[name]}/*.md`);
    });
  });

  eleventyConfig.addCollection("sitemapPages", function(collection) {
    return collection.getAll().filter(item => {
      return item.url && !item.url.includes("/admin/");
    });
  });

  return {
    dir: {
      input: ".",
      output: "_site",
      includes: "_includes"
    },
    templateFormats: ["md", "njk", "html"],
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk"
  };
};
