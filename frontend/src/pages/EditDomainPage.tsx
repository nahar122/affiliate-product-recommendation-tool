import DomainTable from "../components/DomainTable";
import axios from "../axios";
import { useActionData } from "react-router-dom";
import { useEffect, useState } from "react";
import { Domain } from "../types/Domain";
import UrlTable from "../components/UrlTable";
import { URL } from "../types/URL";
import EditUrl from "../components/EditUrl";
import { useNavigate } from "react-router-dom";

const EditDomainPage = () => {
  const navigate = useNavigate();
  const [domains, setDomains] = useState<Domain[]>([]);
  const [urls, setUrls] = useState<URL[]>([]);
  const [currentDomain, setCurrentDomain] = useState<Domain | null>(null);
  const [currentURL, setCurrentURL] = useState<URL | null>(null);
  const [currentStep, setCurrentStep] = useState<number>(0);
  const [updatedText, setUpdatedText] = useState<string>("");
  console.log(process.env.REACT_APP_API_URL);
  const updateInjectedParagraph = async () => {
    if (!currentURL) {
      console.error("An error has occured. URL not found.");
      return false;
    }
    try {
      console.log(process.env.REACT_APP_API_URL);
      const response = await axios.patch(`/edit-url/${currentURL.id}`, {
        injected_article_paragraph: updatedText,
      });
      navigate("/");
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("/get-domains"); // Use relative URL path
        // console.log(response.data);
        setDomains(response.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    console.log(currentDomain);
    if (currentDomain === null) {
      return;
    }

    const fetchData = async () => {
      try {
        const response = await axios.get(`/get-urls/${currentDomain.id}`); // Use relative URL path
        // console.log(response.data);
        setUrls(response.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, [currentDomain]);
  return (
    <div className="flex flex-col justify-between my-4">
      <h1 className="text-2xl my-6 font-bold">Edit Domain URLs Page</h1>
      <ul className="steps p-4 steps-vertical lg:steps-horizontal">
        <li
          className={`font-semibold step ${
            currentStep >= 0 ? "step-primary" : ""
          }`}
        >
          Pick a Domain to Edit
        </li>
        <li
          className={`font-semibold step ${
            currentStep >= 1 ? "step-primary" : ""
          }`}
        >
          Pick a URL to edit
        </li>
        <li
          className={`font-semibold step ${
            currentStep >= 2 ? "step-primary" : ""
          }`}
        >
          Edit Injected Paragraph
        </li>
      </ul>
      <div className="flex justify-center border border-black rounded-lg">
        {currentStep === 0 && domains ? (
          <DomainTable data={domains} setDomain={setCurrentDomain} />
        ) : currentStep === 1 && urls ? (
          <UrlTable data={urls} setUrl={setCurrentURL} />
        ) : currentStep === 2 && currentURL ? (
          <EditUrl url={currentURL} setText={setUpdatedText} />
        ) : (
          <h1>Successfully updated row!</h1>
        )}
      </div>
      <div className="join grid grid-cols-2 my-6">
        <button
          className={`join-item btn ${currentStep === 0 ? "btn-disabled" : ""}`}
          onClick={() => setCurrentStep(currentStep - 1)}
        >
          Previous Step
        </button>
        <button
          className={`join-item btn ${
            currentStep === 0 && !currentDomain && urls.length === 0
              ? "btn-disabled"
              : currentStep === 1 && !currentURL
              ? "btn-disabled"
              : currentStep === 3
              ? "btn-disabled"
              : ""
          }`}
          onClick={async () => {
            setCurrentStep(currentStep + 1);
            if (currentStep === 2) {
              await updateInjectedParagraph();
            }
          }}
        >
          {currentStep === 2 ? "Save" : "Next Step"}
        </button>
      </div>
    </div>
  );
};

export default EditDomainPage;
