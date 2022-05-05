import React, { Fragment, useState } from "react";
import * as Papa from "papaparse";
import axios from "axios";

const FileUploader = () => {
  const [file, setFile] = useState("");
  const [filename, setFilename] = useState("Choose File");
  let [uploadedFile, setUploadedFile] = useState({});

  const formData = new FormData();
  const fileReader = new FileReader();

  const onChange = (e) => {
    const file = e.target.files[0];
    Papa.parse(file, {
      header: true,
      skipEmptyLines: true,
      complete: function (results) {
        console.log(results.data);
      },
    });
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await axios.post("http://127.0.0.1:5000/uploader", formData);
      //this line is to set the res data
      const { fileName, filePath } = res.data;
      setUploadedFile = { fileName, filePath };
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
        <div className="custom-file mb-4">
          <label>Select File: </label>
          <input
            type="file"
            className="custom-file-input"
            id="customFile"
            onChange={onChange}
          />
        </div>
        <button>Upload</button>
      </form>
    </>
  );
};

export default FileUploader;
