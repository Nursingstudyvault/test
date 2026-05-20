module.exports = function(eleventyConfig) {
  
  eleventyConfig.addPassthroughCopy("assets");
  eleventyConfig.addPassthroughCopy("admin");
  eleventyConfig.addPassthroughCopy("pages/*.html");
  eleventyConfig.addPassthroughCopy("*.html");
  
  eleventyConfig.addCollection("nursingCarePlan", function(collection) {
    return collection.getFilteredByGlob("nursing-care-plan/*.md");
  });
  
  eleventyConfig.addCollection("surgicalCarePlan", function(collection) {
    return collection.getFilteredByGlob("surgical-care-plan/*.md");
  });
  
  eleventyConfig.addCollection("caseStudy", function(collection) {
    return collection.getFilteredByGlob("case-study/*.md");
  });
  
  eleventyConfig.addCollection("healthTalk", function(collection) {
    return collection.getFilteredByGlob("health-talk/*.md");
  });
  
  eleventyConfig.addCollection("healthEducation", function(collection) {
    return collection.getFilteredByGlob("health-education/*.md");
  });
  
  eleventyConfig.addCollection("procedure", function(collection) {
    return collection.getFilteredByGlob("procedure/*.md");
  });
  
  eleventyConfig.addCollection("assignment", function(collection) {
    return collection.getFilteredByGlob("assignment/*.md");
  });
  
  eleventyConfig.addCollection("nursingNotes", function(collection) {
    return collection.getFilteredByGlob("nursing-notes/*.md");
  });
  
  eleventyConfig.addCollection("familyFolder", function(collection) {
    return collection.getFilteredByGlob("family-folder/*.md");
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
