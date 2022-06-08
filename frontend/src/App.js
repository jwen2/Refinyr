import React, { useCallback, useRef, useState, useEffect } from "react";
import { AgGridColumn, AgGridReact } from "ag-grid-react";
import axios from "axios";
import "./App.css";
import { Row, Col } from "react-bootstrap";

import "ag-grid-community/dist/styles/ag-grid.css";
import "ag-grid-community/dist/styles/ag-theme-alpine.css";

import FileUploader from "./Components/FileUploader";
import Menu from "./Components/Menu";
import Footer from "./Components/Footer";

const App = () => {
  const gridRef = useRef();
  const [columnDefs, setColumnDefs] = useState([]);
  const [rowData, setRowData] = useState([]);
  const [attribute, setAttribute] = useState([]);
  const [filename, setFilename] = useState("Choose File");
  const [fileSelected, setfileSelected] = useState(false);

  const onBtnExport = useCallback(() => {
    gridRef.current.api.exportDataAsCsv();
  }, []);

  const headerClickListener = async () => {
    const colElements = Array.from(
      document.getElementsByClassName("ag-header-cell")
    );

    colElements.forEach((elem, index) => {
      elem.addEventListener("click", () => {
        let attribute = elem.getAttribute("col-id");
        setAttribute(attribute);
        //need to look into putting this on when a column is selected (bug where if you click two columns it doesn't work)
        console.log(filename);
        if (filename !== null || filename !== "Choose File")
          setfileSelected(true);
      });
    });
  };

  // For Fetch - add a variable for the file name at the end of the fetch URL
  useEffect(() => {
    getFileData();
  }, []);

  const getFileData = async () => {
    let tempSelectedColumnValues = [];
    const { data } = await axios.get(
      `http://127.0.0.1:5000/pandas/get_head/${filename}/1000`
      // "https://www.ag-grid.com/example-assets/row-data.json"
    );
    setRowData(data);
    console.log(data[0]);
    //getting keys for columndefs based on the first element in the row data
    const keys = Object.keys(data[0]).map((key) => ({
      field: key,
      headerName: key[0].toUpperCase() + key.slice(1),
      editable: true,
      // sortable: true,
      resizable: true,

      cellStyle: (params) => {
        if (params.colDef.field === attribute) {
          return { color: "#001D6D", backgroundColor: "#F3F7FF" };
        }
        return null;
      },
    }));
    setColumnDefs(keys);
  };

  return (
    <div className="pageContainer">
      <FileUploader
        setRowData={setRowData}
        setColumnDefs={setColumnDefs}
        filename={filename}
        setFilename={setFilename}
        onBtnExport={onBtnExport}
      />
      <div className="mainContainer">
        <Menu
          setRowData={setRowData}
          setColumnDefs={setColumnDefs}
          fileSelected={fileSelected}
          columnSelected={attribute}
          filename={filename}
        />

        <div
          className="ag-theme-alpine"
          onClick={headerClickListener}
          style={{
            height: 450,
            width: "70%",
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
      <Footer />
    </div>
  );
};
export default App;

//https://www.youtube.com/watch?v=6PA45adHun8&t=222s
