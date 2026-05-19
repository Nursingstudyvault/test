module.exports = function(eleventyConfig) {
  
  eleventyConfig.addPassthroughCopy("assets");
  eleventyConfig.addPassthroughCopy("admin");
  eleventyConfig.addPassthroughCopy("pages/*.html");
  eleventyConfig.addPassthroughCopy("*.html");
  
  eleventyConfig.addCollection("nursingCarePlan", function(collection) {
    return collection.getFilteredByGlob("content/nursing-care-plan/*.md");
  });
  
  eleventyConfig.addCollection("surgicalCarePlan", function(collection) {
    return collection.getFilteredByGlob("content/surgical-care-plan/*.md");
  });
  
  eleventyConfig.addCollection("caseStudy", function(collection) {
    return collection.getFilteredByGlob("content/case-study/*.md");
  });
  
  eleventyConfig.addCollection("healthTalk", function(collection) {
    return collection.getFilteredByGlob("content/health-talk/*.md");
  });
  
  eleventyConfig.addCollection("healthEducation", function(collection) {
    return collection.getFilteredByGlob("content/health-education/*.md");
  });
  
  eleventyConfig.addCollection("procedure", function(collection) {
    return collection.getFilteredByGlob("content/procedure/*.md");
  });
  
  eleventyConfig.addCollection("assignment", function(collection) {
    return collection.getFilteredByGlob("content/assignment/*.md");
  });
  
  eleventyConfig.addCollection("nursingNotes", function(collection) {
    return collection.getFilteredByGlob("content/nursing-notes/*.md");
  });
  
  eleventyConfig.addCollection("familyFolder", function(collection) {
    return collection.getFilteredByGlob("content/family-folder/*.md");
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
