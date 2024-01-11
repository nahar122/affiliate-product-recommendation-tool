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

    let response = await fetch("https://rankmargin.com/api/retrieve-url-data", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: window.location.href }),
    });

    let data = await response.json();

    if (data.excluded) {
      console.log("Article is excluded.");
      return;
    }

    if (firstParagraphElement && html_string) {
      // Create a container to hold the HTML string
      const container = document.createElement("div");
      container.innerHTML = html_string;

      // Extract the first element (assumed to be the new paragraph) from the container
      const newParagraphElement = container.firstElementChild;

      if (newParagraphElement) {
        // Merge classes from both elements
        let mergedClasses =
          `${firstParagraphElement.className} ${newParagraphElement.className}`.trim();

        // Replace the original paragraph with the new content
        firstParagraphElement.replaceWith(container);

        // Apply the merged classes to the new paragraph element
        newParagraphElement.className = mergedClasses;
      }
    } else {
      console.error("Failed to inject content.");
    }

    console.log("Content injection successful.");
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
  const body = doc.body;

  function insertBreaks(text) {
    let sentenceCount = 0;
    let newText = "";
    const parts = text.split(/([.!?]\s+)/g);

    for (let i = 0; i < parts.length; i++) {
      newText += parts[i];
      if (/[.!?]/.test(parts[i]) && i < parts.length - 1) {
        sentenceCount++;
        if (sentenceCount >= 3) {
          newText += "<br><br>"; // Insert break after the punctuation
          sentenceCount = 0;
        }
      }
    }
    return newText;
  }

  const walker = document.createTreeWalker(
    body,
    NodeFilter.SHOW_TEXT,
    null,
    false
  );
  const nodesToReplace = [];

  while (walker.nextNode()) {
    const node = walker.currentNode;
    nodesToReplace.push(node);
  }

  nodesToReplace.forEach((node) => {
    const span = document.createElement("span");
    span.innerHTML = insertBreaks(node.textContent);
    node.parentNode.replaceChild(span, node);
  });

  return body.innerHTML;
}

document.addEventListener("DOMContentLoaded", (event) => {
  scrapeWebPage();
});
