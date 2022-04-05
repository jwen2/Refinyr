import React, { useState } from "react";
import './App.css';

export default function App() {
   const [file, setFile] = useState();
   const [array, setArray] = useState([]);
 
   const fileReader = new FileReader();
 
   const handleOnChange = (e) => {
     setFile(e.target.files[0]);
   };
 
   const csvFileToArray = string => {
     const csvHeader = string.slice(0, string.indexOf("\n")).split(",");
     const csvRows = string.slice(string.indexOf("\n") + 1).split("\n");
 
     const array = csvRows.map(i => {
       const values = i.split(",");
       const obj = csvHeader.reduce((object, header, index) => {
         object[header] = values[index];
         return object;
       }, {});
       return obj;
     });
 
     setArray(array);
   };
 
   const handleOnSubmit = (e) => {
     e.preventDefault();
 
     if (file) {
       fileReader.onload = function (event) {
         const text = event.target.result;
         csvFileToArray(text);
       };
 
       fileReader.readAsText(file);
     }
   };
 
   const headerKeys = Object.keys(Object.assign({}, ...array));

   
 
   return (
     <div className="App">
       <h1 className="styling">Low Fidelity CSV Utility</h1>
       <h1 className="stylingh2">Transform your data with us.</h1>
       <form>
         <input
           type={"file"}
           id={"csvFileInput"}
           class="hidden"
           accept={".csv"}
           onChange={handleOnChange}
         />
          <label for="csvFileInput" class="button">Select File</label>
         <button className="button" 
           onClick={(e) => {
             handleOnSubmit(e);
           }}
         >
           IMPORT CSV
         </button>
       </form>
 
       <br />
 
       <table className="table">
         <thead>
           <tr key={"header"}>
             {headerKeys.map((key) => (
               <th className="th">{key}</th>
             ))}
           </tr>
         </thead>
 
         <tbody>
           {array.map((item) => (
             <tr key={item.id}>
               {Object.values(item).map((val) => (
                 <td className="td">{val}</td>
               ))}
             </tr>
           ))}
         </tbody>
       </table>
     </div>
   );
 }

