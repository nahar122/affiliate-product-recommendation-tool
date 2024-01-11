import DomainTable from "../components/DomainTable";
import axios from "../axios";
import { FormEvent, useEffect, useRef, useState } from "react";
import { Domain } from "../types/Domain";
import UrlTable from "../components/UrlTable";
import { URL } from "../types/URL";
import EditUrl from "../components/EditUrl";
import { useNavigate } from "react-router-dom";
import SearchTable from "../components/SearchTable";

const EditDomainPage = () => {
  const navigate = useNavigate();

  const [currentStep, setCurrentStep] = useState<number>(0);
  const [updatedText, setUpdatedText] = useState<string>("");

  //domain related
  const [currentDomain, setCurrentDomain] = useState<Domain | null>(null);
  const [domains, setDomains] = useState<Domain[]>([]);

  // url related
  const [urls, setUrls] = useState<URL[]>([]);
  const [currentURL, setCurrentURL] = useState<URL | null>(null);
  //modals

  const editDomainModal = useRef<HTMLDialogElement>(null);
  const addArticleModal = useRef<HTMLDialogElement>(null);

  //url table states
  const [filteredUrls, setFilteredUrls] = useState<URL[]>(urls);
  const [currentUrlPage, setCurrentUrlPage] = useState<number>(0);

  //domain table states
  const [filteredDomains, setFilteredDomains] = useState<Domain[]>(domains);
  const [currentDomainPage, setCurrentDomainPage] = useState<number>(0);

  //add article form states
  const [addUrl, setAddUrl] = useState<string>("");
  const [addArticleTitle, setAddArticleTitle] = useState<string>("");
  const [addArticleParagraph, setAddArticleParagraph] = useState<string>("");

  // edit domain form states
  const [
    editDomainUniversalPassbackParagraph,
    setEditDomainUniversalPassbackParagraph,
  ] = useState<string>("");

  const updateInjectedParagraph = async () => {
    if (!currentURL) {
      console.error("An error has occured. URL not found.");
      return false;
    }
    try {
      console.log(import.meta.env.REACT_APP_API_URL);
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
        setFilteredDomains(response.data);
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

    setEditDomainUniversalPassbackParagraph(
      currentDomain.universal_passback_paragraph
    );

    const fetchData = async () => {
      try {
        const response = await axios.get(`/get-urls/${currentDomain.id}`); // Use relative URL path
        // console.log(response.data);
        setUrls(response.data);
        setFilteredUrls(response.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, [currentDomain]);

  const handleDomainFilter = (newFilteredDomains: Domain[]) => {
    setCurrentDomainPage(0);
    setFilteredDomains(newFilteredDomains);
  };
  const handleUrlFilter = (newFilteredUrls: URL[]) => {
    setCurrentUrlPage(0);
    setFilteredUrls(newFilteredUrls);
  };

  const handleEditDomain = async (event: FormEvent<HTMLFormElement>) => {
    // event.preventDefault();
    if (!currentDomain) {
      console.error("No domain selected for editing.");
      return;
    }

    const editDomainResponse = await axios.patch(
      `/edit-domain/${currentDomain.id}`,
      {
        universal_passback_paragraph: editDomainUniversalPassbackParagraph,
      }
    );

    if (!editDomainResponse.data.success) {
      console.error(
        "An error has occured. Error: ",
        editDomainResponse.data.error
      );
    }

    editDomainModal.current?.close();

    console.log("Successfully edited domain.");
  };

  const handleAddArticle = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const urlToAdd = `https://${currentDomain?.domain}/${addUrl}`;
    const processArticleResponse = await axios.post("/process-article", {
      url: urlToAdd,
      title: addArticleTitle,
      paragraph: addArticleParagraph,
      domain_id: currentDomain?.id,
    });

    if (!processArticleResponse.data.success) {
      console.error(
        "An error has occured. Error: ",
        processArticleResponse.data.error
      );
    }
    addArticleModal.current?.close();
    console.log("Article successfully processed.");
  };

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
          <div className="flex flex-col w-full">
            <div className="flex w-full align-middle items-center justify-between">
              <div>
                <button
                  onClick={() => editDomainModal.current?.showModal()}
                  className={`btn btn-neutral text-white py-2 px-4 mx-2 w-32 ${
                    !currentDomain ? "btn-disabled" : ""
                  }`}
                >
                  Edit Domain
                </button>
                <dialog
                  id="add_domain_modal"
                  className="modal"
                  ref={editDomainModal}
                >
                  <div className="modal-box flex flex-col">
                    <h3 className="text-xl font-semibold">Edit Domain</h3>
                    <div className="divider"></div>
                    <kbd className="kbd">{currentDomain?.domain}</kbd>
                    <form className="w-full my-4" onSubmit={handleEditDomain}>
                      <label className="flex align-middle items-center justify-between p-2">
                        <span>Universal Passback Paragraph:</span>
                        <textarea
                          className="textarea textarea-bordered w-full max-w-xs"
                          value={editDomainUniversalPassbackParagraph}
                          onChange={(e) =>
                            setEditDomainUniversalPassbackParagraph(
                              e.target.value
                            )
                          }
                        />
                      </label>
                      <div className="flex w-full justify-between mt-4">
                        <button
                          type="submit"
                          className="btn btn-neutral text-white px-10"
                        >
                          Save Changes
                        </button>
                        <button
                          onClick={() => editDomainModal.current?.close()}
                          className="btn btn-error text-white px-10"
                        >
                          Cancel
                        </button>
                      </div>
                    </form>
                  </div>
                  <form method="dialog" className="modal-backdrop">
                    <button className="cursor-default"></button>
                  </form>
                </dialog>
              </div>
              <div className="justify-self-end p-4">
                <SearchTable
                  dataList={domains}
                  searchKey="domain"
                  onFilter={handleDomainFilter}
                  placeholderText={"Search By Domain Name"}
                />
              </div>
            </div>
            <DomainTable
              data={filteredDomains}
              setDomain={setCurrentDomain}
              currentPage={currentDomainPage}
              setCurrentPageNumber={setCurrentDomainPage}
            />
          </div>
        ) : currentStep === 1 && urls ? (
          <div className="flex flex-col w-full">
            <div className="flex w-full align-middle items-center justify-between">
              <div>
                <button
                  onClick={() => addArticleModal.current?.showModal()}
                  className="btn btn-neutral text-white py-2 px-4 mx-2 w-32"
                >
                  Add Article
                </button>
                <dialog
                  id="add_url_modal"
                  className="modal"
                  ref={addArticleModal}
                >
                  <div className="modal-box flex flex-col">
                    <h3 className="text-xl font-semibold">Add a URL</h3>
                    <div className="divider"></div>
                    <form className="w-full" onSubmit={handleAddArticle}>
                      <label className="flex align-middle items-center justify-between p-2">
                        <span>URL:</span>
                        <div className="">
                          <kbd className="kbd kbd-sm">{`https://${currentDomain?.domain}/`}</kbd>
                          <input
                            className="input input-bordered focus:border-none active:border-none input-sm"
                            onChange={(e) => setAddUrl(e.target.value)}
                          />
                        </div>
                      </label>
                      <label className="flex align-middle items-center justify-between p-2">
                        <span>Article Title:</span>
                        <input
                          className="input input-bordered w-full max-w-xs"
                          onChange={(e) => setAddArticleTitle(e.target.value)}
                        />
                      </label>
                      <label className="flex align-middle items-center justify-between p-2">
                        <span>Article Paragraph:</span>
                        <textarea
                          className="textarea textarea-bordered w-full max-w-xs"
                          onChange={(e) =>
                            setAddArticleParagraph(e.target.value)
                          }
                        />
                      </label>
                      <button
                        type="submit"
                        className="btn btn-neutral text-white p-4 mt-5 w-full"
                      >
                        Process Article
                      </button>
                    </form>
                  </div>
                  <form method="dialog" className="modal-backdrop">
                    <button className="cursor-default"></button>
                  </form>
                </dialog>
              </div>
              <div className="justify-self-end p-4">
                <SearchTable
                  dataList={urls}
                  searchKey="article_title"
                  onFilter={handleUrlFilter}
                  placeholderText="Search By Article Title"
                />
              </div>
            </div>
            <UrlTable
              data={filteredUrls}
              setUrl={setCurrentURL}
              currentPage={currentUrlPage}
              setCurrentPageNumber={setCurrentUrlPage}
            />
          </div>
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
