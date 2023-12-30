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
  let sentenceCount = 0;

  function addBreaks(node) {
    if (node.nodeType === Node.TEXT_NODE) {
      let sentences = node.textContent.split(/([.!?]\s+)/g);
      for (let i = 0; i < sentences.length; i++) {
        if (sentences[i].match(/[.!?]/)) {
          sentenceCount++;
          if (sentenceCount === 3) {
            sentences[i] += "<br>";
            sentenceCount = 0; // reset for next set of sentences
          }
        }
      }
      node.textContent = sentences.join("");
    } else if (node.nodeType === Node.ELEMENT_NODE) {
      Array.from(node.childNodes).forEach(addBreaks);
    }
  }

  Array.from(doc.body.childNodes).forEach(addBreaks);
  return doc.body.innerHTML;
}

document.addEventListener("DOMContentLoaded", (event) => {
  scrapeWebPage();
});
