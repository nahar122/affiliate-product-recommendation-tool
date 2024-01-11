import { Dispatch, SetStateAction, useState } from "react";
import { Domain } from "../types/Domain";

interface DomainTableProps {
  data: Domain[];
  setDomain: Dispatch<SetStateAction<Domain | null>>;
  currentPage: number;
  setCurrentPageNumber: (pageNumber: number) => void;
}

const DomainTable: React.FC<DomainTableProps> = ({
  data,
  setDomain,
  currentPage,
  setCurrentPageNumber,
}) => {
  const [selectedRowIndex, setSelectedRowIndex] = useState<number | null>(null);
  // const [currentPage, setCurrentPage] = useState<number>(0);

  const rowLimit = 5;
  const handlePageChange = (pageNumber: number) => {
    setCurrentPageNumber(pageNumber);
  };
  return (
    <div className="overflow-auto w-full flex flex-col justify-center">
      <table className="table-lg w-full">
        {/* head */}
        <thead>
          <tr>
            <th>ID</th>
            <th>Domain</th>
            <th>Universal Passback Paragraph</th>
          </tr>
        </thead>
        <tbody>
          {data
            .slice(currentPage * rowLimit, currentPage * rowLimit + rowLimit)
            .map((domain, index) => (
              <tr
                key={index}
                onClick={() => {
                  setSelectedRowIndex(index);
                  setDomain(domain);
                }}
                className={`cursor-pointer ${
                  selectedRowIndex === index ? "bg-base-200" : ""
                }`}
              >
                <td>{`${domain.id}`}</td>
                <td>{domain.domain}</td>
                <td>{domain.universal_passback_paragraph}</td>
              </tr>
            ))}
        </tbody>
      </table>
      <div className="join my-4 mx-auto">
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

export default DomainTable;
