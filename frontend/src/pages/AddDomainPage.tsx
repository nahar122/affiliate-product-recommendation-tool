import { FormEvent, useRef, useState } from "react";
import axios from "../axios";

const AddDomainPage = () => {
  const [domainName, setDomainName] = useState<string>("");
  const [paragraphText, setParagraphText] = useState<string>("");
  const fileInputRef1 = useRef<HTMLInputElement>(null);
  const fileInputRef2 = useRef<HTMLInputElement>(null);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData();

    // Append domain name and paragraph text
    formData.append("domainName", domainName);
    formData.append("paragraphText", paragraphText);

    // Assuming fileInputRef2 is the file to upload
    if (fileInputRef2.current?.files && fileInputRef2.current.files[0]) {
      formData.append("file", fileInputRef2.current.files[0]); // Use 'file' as the key
    }

    if (fileInputRef1.current?.files && fileInputRef1.current.files[0]) {
      formData.append("urls", fileInputRef1.current.files[0]); // Use 'file' as the key
    }
    // Create the domain
    let create_domain_response = await axios.post("/add-domain", {
      domain: domainName,
      universal_passback_paragraph: paragraphText,
    });
    if (!create_domain_response.data.success) {
      console.error(create_domain_response.data.error);
      return;
    }
    let domain_id = create_domain_response.data.domain_id;
    console.log(domain_id);

    // Append domain_id to formData for the file upload
    formData.append("domain_id", domain_id);

    // Upload the file
    try {
      let upload_excluded_urls = await axios.post(
        "/upload-excluded-urls",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data", // This might be optional as axios sets it automatically
          },
        }
      );

      if (!upload_excluded_urls.data.success) {
        console.error(upload_excluded_urls.data.error);
        return;
      }

      console.log("File uploaded successfully");
    } catch (error) {
      console.error("Error uploading file:", error);
    }

    try {
      let upload_urls = await axios.post("/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data", // This might be optional as axios sets it automatically
        },
      });

      if (!upload_urls.data.success) {
        console.error(upload_urls.data.error);
        return;
      }

      console.log("File uploaded successfully");
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <form
      className="flex flex-col justify-center align-middle mx-auto text-center border border-black rounded-md p-8 my-8"
      onSubmit={handleSubmit}
    >
      <h1 className="text-2xl font-bold">Add a Domain</h1>
      <h3 className="text-xl font-semibold my-4">
        Enter Domain Name (e.g. osradar.com)
      </h3>
      <input
        type="text"
        placeholder="Enter Domain Here"
        className="input input-bordered w-3/6 mx-auto"
        onChange={(e) => setDomainName(e.target.value)}
      />
      <h3 className="text-xl font-semibold my-4">Upload URL CSV</h3>
      <input
        type="file"
        accept=".csv"
        ref={fileInputRef1}
        className="file-input file-input-bordered w-3/6 mx-auto"
      />
      <label className="flex flex-col text-xl font-semibold my-4">
        Universal Passback Paragraph (must be HTML)
        <textarea
          className="textarea textarea-info w-3/6 my-2 text-black h-48 mx-auto"
          value={paragraphText}
          placeholder="Enter HTML Here"
          onChange={(e) => {
            setParagraphText(e.target.value);
          }}
        ></textarea>
      </label>
      <h3 className="text-xl font-semibold my-2">
        Upload CSV of URLs to Exclude
      </h3>
      <input
        type="file"
        accept=".csv"
        ref={fileInputRef2}
        className="file-input file-input-bordered my-2 w-3/6 mx-auto"
      />
      <button
        type="submit"
        className="btn btn-active btn-neutral my-4 w-3/6 mx-auto"
      >
        Add Domain
      </button>
    </form>
  );
};

export default AddDomainPage;
