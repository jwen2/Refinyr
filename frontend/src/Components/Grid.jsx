import React, { Fragment, useState, useCallback, useRef } from "react";
import { AgGridColumn, AgGridReact } from "ag-grid-react";
import "ag-grid-community/dist/styles/ag-grid.css";
import "ag-grid-community/dist/styles/ag-theme-alpine.css";
import axios from "axios";
import Menu from "./Menu";
import "../App.css";

const Grid = () => {
  const gridRef = useRef();
  const onBtnExport = useCallback(() => {
    gridRef.current.api.exportDataAsCsv();
  }, []);
  const [columnDefs, setColumnDefs] = useState([]);
  const [rowData, setRowData] = useState([]);
  const [attribute, setAttribute] = useState([]);
  const [filename, setFilename] = useState("Choose File");
  const [fileSelected, setfileSelected] = useState(false);
  const [dataTypes, setDataTypes] = useState([]);
  const [currentType, setCurrentType] = useState("");
  const [file, setFile] = useState("");
  const [uploadedFile, setUploadedFile] = useState({});

  const onChange = (e) => {
    setFile(e.target.files[0]);
    setFilename(e.target.files[0].name);
  };

  //uploading file and displaying rows and cols to ag-grid
  const onSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("file", file);
    try {
      const { data } = await axios.post(
        "http://127.0.0.1:5000/uploader",
        formData
      );
      console.log(data);
      setRowData(data[0]);

      let keys = Object.keys(data[0][0]).map((key) => ({
        field: key,
        headerName: key[0].toUpperCase() + key.slice(1),
        editable: true,
        sortable: true,
        resizable: true,
        cellStyle: (params) => {
          if (params.colDef.field === attribute) {
            return { color: "#001D6D", backgroundColor: "#F3F7FF" };
          }
          return null;
        },
      }));
      keys.forEach((key, i) => {
        key["columnType"] = data[1][i];
      });
      setDataTypes(data[1]);
      console.log(data[1]);
      console.log(keys);
      setColumnDefs(keys);
    } catch (err) {
      console.log(err);
    }
  };

  //clicking on columns
  const headerClickListener = async () => {
    console.log("clicked once");
    const colElements = Array.from(
      document.getElementsByClassName("ag-header-cell")
    );

    colElements.forEach((elem, i) => {
      elem.addEventListener("click", () => {
        console.log("clicked once");
        let attribute = elem.getAttribute("col-id");
        console.log(attribute);
        setAttribute(attribute);
        setCurrentType(dataTypes[i]);
        console.log(dataTypes);
        console.log(dataTypes[i]);
        //need to look into putting this on when a column is selected (bug where if you click two columns it doesn't work)
        console.log(filename);
        if (filename !== null || filename !== "Choose File")
          setfileSelected(true);
      });
    });
  };

  return (
    <>
      <form onSubmit={onSubmit}>
        <div className="fileUploader">
          <input
            type="file"
            className="custom-file-input"
            id="customFile"
            onChange={onChange}
          />
        </div>

        <div className="fileUploaderBtns">
          <input
            type="submit"
            value="Upload"
            className="headerButton"
            style={{ fontSize: "0.65em" }}
          />
          <button
            className="headerButton"
            style={{ fontSize: "0.65em" }}
            onClick={onBtnExport}
          >
            Download CSV
          </button>
        </div>
      </form>

      <div className="mainContainer">
        <Menu
          setRowData={setRowData}
          setColumnDefs={setColumnDefs}
          fileSelected={fileSelected}
          columnSelected={attribute}
          filename={filename}
          setDataTypes={setDataTypes}
          attribute={attribute}
          currentType={currentType}
        />

        <div
          className="ag-theme-alpine"
          onClick={headerClickListener}
          style={{
            height: "60vh",
            width: "80vw",
          }}
        >
          <AgGridReact
            ref={gridRef}
            pagination={true}
            columnDefs={columnDefs}
            rowData={rowData}
          />
        </div>
      </div>
    </>
  );
};

export default Grid;
