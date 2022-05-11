import React, { useCallback, useRef, useState, useEffect } from "react";
import { AgGridColumn, AgGridReact } from "ag-grid-react";
import axios from "axios";
import "./App.css";

import "ag-grid-community/dist/styles/ag-grid.css";
import "ag-grid-community/dist/styles/ag-theme-alpine.css";

import FileUploader from "./Components/FileUploader";

const App = () => {
  const gridRef = useRef();
  const [columnDefs, setColumnDefs] = useState([]);
  const [rowData, setRowData] = useState([]);
  const [attribute, setAttribute] = useState([]);
  const [selectedColumnValues, setSelectedColumnValues] = useState([]);

  const onBtnExport = useCallback(() => {
    gridRef.current.api.exportDataAsCsv();
  }, []);

  const headerClickListener = async() => {
    let colElements =  Array.from(document.getElementsByClassName('ag-header-cell'));
    colElements.forEach((elem, index) => {
      elem.addEventListener('click', () => {
        let attribute = elem.getAttribute('col-id');
        console.log(attribute);
        setAttribute(attribute);
      })
    })
    getFileData();
  }

  // For Fetch - add a variable for the file name at the end of the fetch URL
  useEffect(() => {
    getFileData();
  }, []);

  const getFileData = async () => {
    let tempSelectedColumnValues = [];
    const { data } = await axios.get(
      // "http://127.0.0.1:5000/pandas/head/cWithDups.csv/10"
      "https://www.ag-grid.com/example-assets/row-data.json"
    );
    setRowData(data);
    // console.log(data[0]);
    //getting keys for columndefs based on the first element in the row data
    const keys = Object.keys(data[0]).map((key) => ({
      field: key,
      headerName: key,
      editable: true,
      // sortable: true,
      resizable: true,
      cellStyle: (params) => {
        if (params.colDef.field === attribute) {
          tempSelectedColumnValues.push(params.value);
          return { color: '#001D6D', backgroundColor: '#F3F7FF' };
        }
        return null;
      },
    }));
    setSelectedColumnValues(tempSelectedColumnValues);
    if (selectedColumnValues.length !== 0) {
      console.log(selectedColumnValues);
    }
    setColumnDefs(keys);
  };

  return (
    <div className="container mt-4">
      <hr className="divider"></hr>

      <div>
        <FileUploader setRowData={setRowData} setColumnDefs={setColumnDefs} />
      </div>

      <div className="div right">
        <button className="button" onClick={onBtnExport}>
          Download CSV
        </button>
      </div>

      <div
        className="ag-theme-alpine"
        onClick={headerClickListener}
        style={{
          height: 900,
          width: 900,
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
  );
};
export default App;

//https://www.youtube.com/watch?v=6PA45adHun8&t=222s
