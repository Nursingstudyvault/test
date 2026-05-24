module.exports = function(eleventyConfig) {
    eleventyConfig.addPassthroughCopy("theme.css");
    eleventyConfig.addPassthroughCopy("robots.txt");
    eleventyConfig.addPassthroughCopy("admin");
    eleventyConfig.addPassthroughCopy("*.html");

    eleventyConfig.addFilter("readableDate", function(dateObj) {
        if (!dateObj) return "";
        const date = new Date(dateObj);
        return date.toLocaleDateString("en-IN", {
            day: "2-digit", month: "short", year: "numeric"
        });
    });

    eleventyConfig.addFilter("wordCount", function(content) {
        if (!content) return 0;
        return Math.ceil(content.split(/\s+/).length / 200);
    });

    const categories = [
        "nursingCarePlan", "surgicalCarePlan", "caseStudy", "healthTalk",
        "healthEducation", "procedure", "assignment", "familyFolder"
    ];

    categories.forEach(cat => {
        let folder = cat.replace(/([A-Z])/g, '-$1').toLowerCase();
        eleventyConfig.addCollection(cat, function(collection) {
            return collection.getFilteredByGlob(`${folder}/*.md`).sort((a, b) => b.date - a.date);
        });
    });

    return { dir: { input: ".", output: "_site", includes: "_includes" } };
};

// Request Topic and Thank You pages are already in root as .njk files
