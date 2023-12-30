async function scrapeWebPage() {
  try {
    const title = document.querySelector("h1")
      ? document.querySelector("h1").innerText
      : "";
    let firstParagraphElement = null;
    let firstParagraphText = "";

    const paragraphs = document.querySelectorAll("p");
    for (const p of paragraphs) {
      if (!firstParagraphElement) {
        const paragraphText = p.innerText;
        if (paragraphText.split(" ").length > 30) {
          firstParagraphElement = p;
          firstParagraphText = paragraphText;
          break;
        }
      }
    }

    let response = await fetch("https://rankmargin.com/retrieve-url-data", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: window.location.href }),
    });

    let data = await response.json();
    if (firstParagraphElement && data.injected_article_paragraph) {
      const newParagraph = document.createElement("div");
      newParagraph.innerHTML = insertLineBreakAfterThreeSentences(
        data.injected_article_paragraph
      );
      const newParagraphElement = newParagraph.firstChild;

      if (newParagraphElement) {
        newParagraphElement.className = firstParagraphElement.className;
        newParagraphElement.style.cssText = firstParagraphElement.style.cssText;
      }

      firstParagraphElement.replaceWith(newParagraphElement);
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

function isSimilar(text1, text2) {
  return text1.trim().substring(0, 50) === text2.trim().substring(0, 50);
}

function insertLineBreakAfterThreeSentences(htmlString) {
  const parser = new DOMParser();
  const doc = parser.parseFromString(htmlString, "text/html");
  const walker = document.createTreeWalker(
    doc.body,
    NodeFilter.SHOW_TEXT,
    null,
    false
  );

  let sentenceCount = 0;
  let sentences = "";
  let currentText = "";

  while (walker.nextNode()) {
    currentText = walker.currentNode.textContent;
    let parts = currentText.split(/([.!?]\s+)/g);

    for (let part of parts) {
      if (part.match(/[.!?]/)) {
        sentenceCount++;
        sentences += part;
        if (sentenceCount >= 3) {
          let tempDiv = document.createElement("div");
          tempDiv.innerHTML = sentences;
          walker.currentNode.parentNode.insertBefore(
            tempDiv.firstChild,
            walker.currentNode
          );
          sentences = "";
          sentenceCount = 0;
        }
      } else {
        sentences += part;
      }
    }
    walker.currentNode.textContent = sentences;
    sentences = "";
  }

  return doc.body.innerHTML;
}

document.addEventListener("DOMContentLoaded", (event) => {
  scrapeWebPage();
});
