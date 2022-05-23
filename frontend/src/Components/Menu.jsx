import axios from "axios";
import React, { useState } from "react";
import Select from "react-select";


const Menu = ({
  fileSelected,
  filename,
  columnSelected,
  setColumnDefs,
  setRowData,
}) => {

  const [selection, setSelection] = useState({});

  //can be replaced dynamic data with an async call
  const options = [
    { value: "rm_dups", label: "Remove Duplicates" },
    { value: "rm_nulls", label: "Remove Nulls" },
    { value: "replace_na_mean", label: "Replace NA with Mean" },
    { value: "replace_na_median", label: "Replace NA with Median" },
    { value: "replace_na_mode_numeric", label: "Replace NA with Mode Numeric" },
    { value: "replace_na_unknown", label: "Replace NA with Unknown" },
    { value: "replace_na_ffill", label: "Replace NA with ffill" },
    { value: "replace_na_bfill", label: "Replace NA with bfill" },
    { value: "replace_na_mode_categorical", label: "Replace NA with Mode Categorical" },
    //need to have pop up or something to input second value for rename column
    //{ value: "rename_column", label: "Rename Column"},
    { value: "normalize", label: "Normalize Column" },
  ];

  const handleClick = async () => {
    console.log(selection.value);
    console.log(filename);
    console.log(columnSelected);

    try {
      const res = await axios.get(
        `http://127.0.0.1:5000/pandas/${selection.value}/${filename}/${columnSelected}`,
        filename,
        columnSelected
      );
      console.log(res.data);
      setRowData(res.data);

      const keys = Object.keys(res.data[0]).map((key) => ({
        field: key,
        headerName: key[0].toUpperCase() + key.slice(1),
      }));
      setColumnDefs(keys);
    } catch (error) {
      console.log(error);
    }
  };

  const onConfirm = () => {};

  const customTheme = (theme) => {
    return {
      ...theme,
      colors: {
        ...theme.colors,
        primary25: "orange",
        primary: "green",
      },
    };
  };

  return (
    <div className="menuContainer">
      <h3 className="optionTitle">Transform:</h3>
      {!fileSelected ? (
        ""
      ) : (
        <div className="menuInnerContainer">
          <Select
            options={options}
            theme={customTheme}
            className="selectMenu"
            placeholder="Select option..."
            onChange={setSelection}
            isSearchable
            autoFocus
          />

          <button className="button" onClick={handleClick}>
            Transform
          </button>
        </div>
      )}
    </div>
  );
};

export default Menu;
