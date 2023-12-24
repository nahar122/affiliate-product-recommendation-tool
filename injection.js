async function scrapeWebPage() {
  try {
    // Use document.querySelector to access the first <h1> tag for the title
    const title = document.querySelector("h1")
      ? document.querySelector("h1").innerText
      : "";
    let firstParagraphElement = null;
    let firstParagraphText = "";

    // Get all <p> tags
    const paragraphs = document.querySelectorAll("p");

    // Iterate over all <p> tags to find the first long paragraph
    for (const p of paragraphs) {
      if (!firstParagraphElement) {
        const paragraphText = p.innerText;
        const wordCount = paragraphText.split(" ").length;
        if (wordCount > 30) {
          firstParagraphElement = p;
          firstParagraphText = paragraphText;
          break;
        }
      }
    }

    // Make POST request with current URL
    let response = await fetch("https://rankmargin.com/retrieve-url-data", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url: window.location.href }),
    });

    const data = await response.json();

    // Check similarity between scraped paragraph and initial_first_paragraph
    if (!isSimilar(firstParagraphText, data.initial_article_paragraph)) {
      // Send data to process-article endpoint
      response = await fetch("https://rankmargin.com/process-article", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          url: window.location.href,
          title: title,
          paragraph: firstParagraphText,
        }),
      });

      const processData = await response.json();

      if (processData.success) {
        console.log("Article data processed successfully.");
        let new_response = await fetch(
          "https://rankmargin.com/retrieve-url-data",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ url: window.location.href }),
          }
        );

        let new_data = await new_response.json();
        if (firstParagraphElement && new_data.initial_article_paragraph) {
          firstParagraphElement.innerHTML = new_data.injected_article_paragraph;
        }
      }
    } else if (firstParagraphElement && data.injected_article_paragraph) {
      // Replace the first paragraph's HTML
      firstParagraphElement.innerHTML = data.injected_article_paragraph;
    } else {
      console.error(
        "Failed to retrieve amazon affiliate data for this article."
      );
    }

    console.log("Successfully added amazon affiliate products.");
  } catch (error) {
    console.error("Error scraping the web page:", error);
  }
}

// Placeholder function for similarity check - implement actual logic
function isSimilar(text1, text2) {
  // Implement a more robust comparison algorithm
  return text1.trim().substring(0, 50) === text2.trim().substring(0, 50);
}

document.addEventListener("DOMContentLoaded", (event) => {
  scrapeWebPage();
});

// makeRequests("test_api_key");
