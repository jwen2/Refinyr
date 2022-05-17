import axios from "axios";
import React, { useState } from "react";
import Select from "react-select";

const Menu = ({ fileSelected, filename, attribute }) => {
  const [selection, setSelection] = useState({});

  //can be replaced dynamic data with an async call
  const options = [
    { value: "rm_dups", label: "Remove Duplicates" },
    { value: "option2", label: "option2" },
    { value: "option3", label: "option3" },
  ];

  const handleClick = async () => {
    console.log(selection.value);
    console.log(filename);
    console.log(attribute);

    try {
      const res = await axios.get(
        `http://127.0.0.1:5000/pandas/${selection.value}/${filename}/${attribute}`,
        filename,
        attribute
      );

      console.log(res);
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
