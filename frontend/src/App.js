import React, { useState, useEffect } from "react";
import { AgGridReact } from "ag-grid-react";

import "ag-grid-community/dist/styles/ag-grid.css";
import "ag-grid-community/dist/styles/ag-theme-alpine.css";

import SubmitComponent from "./Components/SubmitButton";

const App = () => {
  const [columnDefs] = useState([
    { field: "make" , sortable: true, filter: true },
    { field: "model", sortable: true, filter: true },
    { field: "price", sortable: true, filter: true },
  ]);

  // const [rowData] = useState ([
  //   { make: "Toyota",  model: "make",  price: "make" },
  //   { make: "Ford",  model: "make",  price: "make" },
  //   { make: "Porsche",  model: "make",  price: "make" },
  // ]);

const [rowData, setRowData] = useState([])

useEffect(() => {
  fetch("https://www.ag-grid.com/example-assets/row-data.json")
  .then((response) => response.json())
  .then((data) => setRowData(data));
}, []);

return (
<div>
  <div>
    <SubmitComponent/>
  </div>
  <div className="ag-theme-alpine" style={{
    height:900, width:900
  }}>
    <AgGridReact
    pagination={true}
    rowData={rowData}
    columnDefs={columnDefs}
    />
  </div>
</div>
)


};
export default App;


//https://www.youtube.com/watch?v=6PA45adHun8&t=222s
