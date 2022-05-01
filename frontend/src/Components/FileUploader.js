import React , { Fragment, useState } from 'react';
import axios from 'axios';

const FileUploader = () => {
  const [file, setFile] = useState('');
  const [filename, setFilename] = useState('Choose File');
  const [uploadedFile, setUploadedFile] = useState({});

  const onChange = e => {
    setFile(e.target.files[0]);
    setFilename(e.target.files[0].name);
  }

  const onSubmit = async e => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', File);
    const fileName = new FormData();
    fileName.append('name', filename)

    try {
      const res = await axios.post('/uploadURL', formData, fileName);
      //this line is to set the res data
      const { fileName, filePath} = res.data;
      setUploadedFile = ({fileName, filePath})
    } catch (err) {
      if(err.response.status === 500) {
        console.log('There was a problem with the server');
      }
      else {
        console.log(err.response.data.msg);
      }
    }
  };

  return (
    <Fragment>
      <form onSubmit={onSubmit}>
        <div className ="custom-file mb-4">
          <input type="file" className ="custom-file-input" id="customFile" onChange={onChange}/>
          <label className ="custom-file-label" htmlFor="customFile">
            {filename}
          </label>
        </div>
        <input type="submit" value="Upload" className="btn btn-primary btn-block mt-4" />
      </form>
    </Fragment>
  );
};

export default FileUploader;
