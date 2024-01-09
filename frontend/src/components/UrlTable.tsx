import { Dispatch, SetStateAction, useState } from "react";
import { URL } from "../types/URL";

interface UrlTableProps {
  data: URL[];
  setUrl: Dispatch<SetStateAction<URL | null>>;
  currentPage: number;
  setCurrentPageNumber: (pageNumber: number) => void;
}

const UrlTable: React.FC<UrlTableProps> = ({
  data,
  setUrl,
  currentPage,
  setCurrentPageNumber,
}) => {
  const [selectedRowIndex, setSelectedRowIndex] = useState<number | null>(null);
  const rowLimit = 5;

  const handlePageChange = (pageNumber: number) => {
    setCurrentPageNumber(pageNumber);
  };
  return (
    <div className="overflow-auto">
      <table className="table table-xs table-pin-rows table-pin-cols">
        {/* head */}
        <thead>
          <tr>
            <th>ID</th>
            <th>URL</th>
            <th>Article Title</th>
            <th>Initial Article Paragraph</th>
            <th>Injected Article Paragraph</th>
          </tr>
        </thead>
        <tbody>
          {data
            .slice(currentPage * rowLimit, currentPage * rowLimit + rowLimit)
            .map((url, index) => (
              <tr
                key={index}
                onClick={() => {
                  setSelectedRowIndex(index);
                  setUrl(url);
                }}
                className={`cursor-pointer ${
                  selectedRowIndex === index ? "bg-base-200" : ""
                }`}
              >
                <td className="overflow-auto">{`${url.id}`}</td>
                <td className="overflow-auto">{url.url}</td>
                <td className="overflow-auto">{url.article_title}</td>
                <td className="overflow-auto">
                  {url.initial_article_paragraph}
                </td>
                <td className="overflow-auto">
                  {url.injected_article_paragraph}
                </td>
              </tr>
            ))}
        </tbody>
      </table>
      <div className="join my-4">
        <button
          onClick={() => handlePageChange(0)}
          className={`join-item btn ${currentPage === 0 ? "btn-disabled" : ""}`}
        >
          ««
        </button>
        <button
          onClick={() => handlePageChange(currentPage - 1)}
          className={`join-item btn ${currentPage === 0 ? "btn-disabled" : ""}`}
        >
          «
        </button>
        <button className="join-item btn">{`${currentPage + 1} / ${
          Math.floor(data.length / rowLimit) + 1
        }`}</button>
        <button
          onClick={() => handlePageChange(currentPage + 1)}
          className={`join-item btn ${
            currentPage === Math.floor(data.length / rowLimit)
              ? "btn-disabled"
              : ""
          }`}
        >
          »
        </button>
        <button
          onClick={() =>
            handlePageChange(Math.floor(data.length / rowLimit) - 1)
          }
          className={`join-item btn ${
            currentPage === Math.floor(data.length / rowLimit)
              ? "btn-disabled"
              : ""
          }`}
        >
          »»
        </button>
      </div>
    </div>
  );
};

export default UrlTable;
