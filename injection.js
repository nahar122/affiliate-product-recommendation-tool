async function makeRequests(api_key) {
  try {
    // Make a POST request to 'http://localhost/login'
    let response = await fetch("http://localhost/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ api_key: api_key }),
    });

    // Check if the request was successful
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    // Extract the JSON body content from the response
    let data = await response.json();
    console.log(data);
    let accessToken = data.access_token;

    // Make a GET request to 'http://localhost'
    response = await fetch("http://localhost", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    // Get HTML response as text
    const html = await response.text();

    // Find the element with id 'test'
    const element = document.getElementById("test");
    if (element) {
      // Update the innerHTML of the element
      element.innerHTML = html;
    } else {
      console.log('Element with id "test" not found');
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

const cheerio = require("cheerio");
const axios = require("axios");

async function scrapeWebPage(url) {
  try {
    // Fetch the HTML of the page
    const { data } = await axios.get(url);
    const $ = cheerio.load(data);

    // Extract the first <h1> tag for the title
    const title = $("h1").first().text();

    // Initialize the first paragraph variable
    let firstParagraph = null;

    // Check all <p> tags
    $("p").each((i, elem) => {
      if (firstParagraph === null) {
        const paragraphText = $(elem).text();
        const wordCount = paragraphText.split(" ").length;
        // If word count is more than 30, set as first paragraph and break
        if (wordCount > 30) {
          firstParagraph = paragraphText;
          return false; // Break the loop
        }
      }
    });

    // If no suitable <p> tag found, get all text after <h1> until the first <br>
    if (!firstParagraph) {
      firstParagraph = $("h1").first().nextUntil("br").text();
    }

    console.log("Title:", title);
    console.log("First Paragraph:", firstParagraph);
  } catch (error) {
    console.error("Error scraping the web page:", error);
  }
}

// Usage
scrapeWebPage(
  "https://www.osradar.com/how-to-enable-wifi-in-windows-server-2022/"
);

// makeRequests("test_api_key");
