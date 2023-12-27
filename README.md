# affiliate-product-recommendation-tool

<h3>This tool generates amazon affiliate links for your websites.</h3>
<p>Upload a .csv to the /upload endpoint of the website. The .csv should be be one column with the links of all the article URL's you want to generate amazon affiliate links for.</p>
<p>Once this list is uploaded, a scrapy crawler gets initiated and crawls all of the url's provided. It creates a list of JSON objects that contain the url, title, and first paragraph of the article.</p>
<p>When the crawler completes, all of this JSON data is sent to OpenAI's API for analysis. Based off the provided data, OpenAI will send us a list of possible products that would be relevant to the article.</p>
<p>After we get this list of products, we go through the Amazon Advertisement API to search for real listed amazon products under those keywords given to us by OpenAI per article.</p>
<p>Once we obtain a list of real amazon products from the Amazon Advertisement API per article, we then send those product names along with their links to OpenAI and retrieve a new HTML paragraph that is relevant to the article and contains the generated amazon affiliate links and store them in a database.</p>
<p>Place the 'injection.js' script in the header of your website either through jsDelivr or pasting it in a <script></script> tag, and the injection will occur.</p>
