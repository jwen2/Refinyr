import React, { Fragment, useState } from "react";
import axios from "axios";
import "../App.css";

const FileUploader = ({ setRowData, setColumnDefs, filename, setFilename }) => {
  const [file, setFile] = useState("");
  const [uploadedFile, setUploadedFile] = useState({});

  const onChange = (e) => {
    setFile(e.target.files[0]);
    setFilename(e.target.files[0].name);
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("file", file);
    try {
      const { data } = await axios.post(
        "http://127.0.0.1:5000/uploader",
        formData
      );
      setRowData(data);
      console.log(data[0]);
      //getting keys for columndefs based on the first element in the row data
      const keys = Object.keys(data[0]).map((key) => ({
        field: key,
        headerName: key[0].toUpperCase() + key.slice(1),
      }));
      console.log(keys);
      setColumnDefs(keys);

      //this line is to set the res data
      // const { filename, filePath } = res.data;
      // setUploadedFile = { filename, filePath };
    } catch (err) {
      console.log(err);
      // if(err.response.status === 500) {
      //   console.log('There was a problem with the server');
      // }
      // else {
      //   console.log(err.response.data.msg);
      // }
    }
  };
  //   const config = {
  //     headers: { "content-type": "multipart/form-data" },
  //   };
  //   const url = "http://127.0.0.1:5000/test";

  // //   try {
  // //     const res = await axios.post(url, { formData }, config);
  // //     //this line is to set the res data
  // //     console.log(res);
  // //   } catch (err) {
  // //     // if (err.response.status === 500) {
  // //     //   console.log("There was a problem with the server");
  // //     // } else {
  // //     //   console.log(err.response.data.msg);
  // //     // }
  // //   }
  // // };

  return (
    <>
      <form onSubmit={onSubmit}>
        <div className="div center">
          <input
            type="file"
            className="custom-file-input"
            id="customFile"
            onChange={onChange}
          />
          {/* <label className ="custom-file-label" htmlFor="customFile">
            {filename}
          </label> */}
        </div>
        <div className="div left">
          <input type="submit" value="Upload" className="button" />
        </div>
      </form>
    </>
  );
};

export default FileUploader;
