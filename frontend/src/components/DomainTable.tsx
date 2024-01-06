import { Dispatch, SetStateAction, useState } from "react";
import { Domain } from "../types/Domain";

interface DomainTableProps {
  data: Domain[];
  setDomain: Dispatch<SetStateAction<Domain | null>>;
}

const DomainTable: React.FC<DomainTableProps> = ({ data, setDomain }) => {
  const [selectedRowIndex, setSelectedRowIndex] = useState<number | null>(null);
  const [currentPage, setCurrentPage] = useState<number>(0);
  const rowLimit = 5;
  return (
    <div className="overflow-auto w-full">
      <table className="table-lg w-full">
        {/* head */}
        <thead>
          <tr>
            <th>ID</th>
            <th>Domain</th>
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
              </tr>
            ))}
        </tbody>
      </table>
      <div className="join my-4">
        <button
          onClick={() => setCurrentPage(currentPage - 1)}
          className={`join-item btn ${currentPage === 0 ? "btn-disabled" : ""}`}
        >
          «
        </button>
        <button className="join-item btn">{currentPage + 1}</button>
        <button
          onClick={() => setCurrentPage(currentPage + 1)}
          className={`join-item btn ${
            currentPage === Math.floor(data.length / rowLimit)
              ? "btn-disabled"
              : ""
          }`}
        >
          »
        </button>
      </div>
    </div>
  );
};

export default DomainTable;
