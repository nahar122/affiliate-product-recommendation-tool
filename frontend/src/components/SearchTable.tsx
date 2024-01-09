import { useState } from "react";

interface SearchInputProps<T> {
  dataList: T[];
  searchKey: keyof T;
  onFilter: (filteredData: T[]) => void;
  placeholderText: string;
}
const SearchInput = <T extends Record<string, any>>({
  dataList,
  searchKey,
  onFilter,
  placeholderText,
}: SearchInputProps<T>) => {
  const [inputValue, setInputValue] = useState("");
  const [filteredData, setFilteredData] = useState<T[]>(dataList);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = event.target.value;
    setInputValue(newValue);

    let newFilteredData = dataList;

    if (newValue) {
      newFilteredData = dataList.filter((item) => {
        if (
          item !== null &&
          item[searchKey] !== null &&
          item[searchKey] !== undefined
        ) {
          return item[searchKey]
            .toString()
            .toLowerCase()
            .includes(newValue.toLowerCase());
        }
        return "";
      });

      setFilteredData(newFilteredData);
      onFilter(newFilteredData); // Pass filtered data to parent
    }
  };

  return (
    <div tabIndex={0} className="dropdown">
      <input
        type="text"
        value={inputValue}
        onChange={handleInputChange}
        className="input input-bordered input-primary w-full max-w-xs"
        placeholder={placeholderText}
      />
      {filteredData.length > 0 && (
        <ul
          tabIndex={0}
          className="dropdown-content z-[3] menu p-3 shadow-md bg-base-100 rounded-box"
        >
          {filteredData.slice(0, 5).map((item, index) => {
            if (item[searchKey] === undefined || item[searchKey] === null) {
              return;
            }
            return (
              <li key={index}>
                <a>{item[searchKey]?.toString()}</a>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
};

export default SearchInput;
