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

// Call the function with your API key
makeRequests("test_api_key");
