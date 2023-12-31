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

// let x = insertLineBreakAfterThreeSentences(
//   "<p class='' style=''>Learning programming languages is a good option to find a good job. Above all, if you dedicate yourself to this. Because for no one is a secret that we live in times where many applications are used. That’s why this post will teach you how to install <a href='https://www.osradar.com/install-rust-programming-language-ubuntu-debian/'>Rust</a> on Ubuntu 20.04 / Debian 10. If you're looking to dive deep into Rust programming, you might be interested in <a href='https://www.amazon.com/dp/1718503105?&amp;_encoding=UTF8&amp;tag=synth0f-20'>The Rust Programming Language, 2nd Edition</a> or <a href='https://www.amazon.com/dp/1492052590?&amp;_encoding=UTF8&amp;tag=synth0f-20'>Programming Rust: Fast, Safe Systems Development</a>. Additionally, if you want to explore practical examples, consider <a href='https://www.amazon.com/dp/1788390636?&amp;_encoding=UTF8&amp;tag=synth0f-20'>Rust Programming By Example: Enter the world of Rust by building engaging, concurrent, reactive, and robust applications</a> or <a href='https://www.amazon.com/dp/B0742HGLWB?&amp;_encoding=UTF8&amp;tag=synth0f-20'>Rust Essentials: A quick guide to writing fast, safe, and concurrent systems and applications, 2nd Edition</a>. For dealing with rust in a different context, you might find <a href='https://www.amazon.com/dp/B0000AY8PB?&amp;_encoding=UTF8&amp;tag=synth0f-20'>Star brite Rust Eater &amp; Converter - Chemically Converts Rust Into Steel</a> useful.</p>"
// );
// console.log(x);
