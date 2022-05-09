import React , { Fragment, useState } from 'react';
import axios from 'axios';
import '../App.css';

const FileUploader = () => {
  const [file, setFile] = useState('');
  const [filename, setFilename] = useState('Choose File');
  let [uploadedFile, setUploadedFile] = useState({});

  const onChange = e => {
    setFile(e.target.files[0]);
    setFilename(e.target.files[0].name);
  }

  const onSubmit = async e => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await axios.post('http://127.0.0.1:5000/uploader', formData);
      //this line is to set the res data
      const { filename, filePath} = res.data;
      setUploadedFile = ({filename, filePath})
    } catch (err) {
      console.log(err)
      // if(err.response.status === 500) {
      //   console.log('There was a problem with the server');
      // }
      // else {
      //   console.log(err.response.data.msg);
      // }
    }
  };

  return (
    <Fragment>
      <form onSubmit={onSubmit}>
        <div className='div center'>
          <input type="file" className ="custom-file-input" id="customFile" onChange={onChange}/>
          {/* <label className ="custom-file-label" htmlFor="customFile">
            {filename}
          </label> */}
        </div>
        <div className = 'div left'>
        <input type="submit" value="Upload" className="button" />
        </div>
      </form>
    </Fragment>
  );
};

export default FileUploader;
