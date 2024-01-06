import { Dispatch, SetStateAction, useState } from "react";
import { URL } from "../types/URL";

interface EditUrlProps {
  url: URL;
  setText: Dispatch<SetStateAction<string>>;
}

const EditUrl: React.FC<EditUrlProps> = ({ url, setText }) => {
  const [paragraphText, setParagraphText] = useState<string>(
    url.injected_article_paragraph
  );
  return (
    <div className="my-4">
      <h1 className="font-semibold text-xl">
        {" "}
        Currently Showing Data for URL:
      </h1>
      <kbd className="kbd my-4">{url.url}</kbd>
      <div className="flex justify-center">
        <div className="collapse bg-base-200 max-w-[75%]">
          <input type="checkbox" className="peer" />
          <div className="collapse-title bg-neutral text-primary-content peer-checked:bg-neutral peer-checked:text-secondary-content">
            Edit Injected Paragraph
          </div>
          <div className="collapse-content bg-neutral text-primary-content peer-checked:bg-neutral peer-checked:text-secondary-content">
            <textarea
              className="textarea textarea-info w-full my-8 text-black h-48"
              value={paragraphText}
              onChange={(e) => {
                setParagraphText(e.target.value);
                setText(e.target.value);
              }}
            ></textarea>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EditUrl;
