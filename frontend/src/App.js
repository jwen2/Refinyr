import React, { useCallback, useRef, useState, useEffect } from "react";
import { AgGridColumn, AgGridReact } from "ag-grid-react";
import axios from "axios";

import "ag-grid-community/dist/styles/ag-grid.css";
import "ag-grid-community/dist/styles/ag-theme-alpine.css";

import FileUploader from "./Components/FileUploader";

const App = () => {
  const gridRef = useRef();
  const [columnDefs, setColumnDefs] = useState([]);
  const [rowData, setRowData] = useState([]);

  const onBtnExport = useCallback(() => {
    gridRef.current.api.exportDataAsCsv();
  }, []);

  // For Fetch - add a variable for the file name at the end of the fetch URL
  useEffect(() => {
    getFileData();
  }, []);

  const getFileData = async () => {
    const { data } = await axios.get(
      // "http://127.0.0.1:5000/pandas/head/cWithDups.csv/10"
      "https://www.ag-grid.com/example-assets/row-data.json"
    );
    setRowData(data);
    console.log(data[0]);
    //getting keys for columndefs based on the first element in the row data
    const keys = Object.keys(data[0]).map((key) => ({
      field: key,
      headerName: key,
      editable: true,
      sortable: true,
      resizable: true,
    }));
    console.log(keys);
    setColumnDefs(keys);
  };

  return (
    <div className="container mt-4">
      <div>
        <FileUploader />
      </div>

      <div className="Export">
        <button onClick={onBtnExport}>Download CSV export file</button>
      </div>

      <div
        className="ag-theme-alpine"
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
