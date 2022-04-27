import React, { Component } from 'react'
import axios, { post } from 'axios'; //library to call API, can use fetchAPI instead


class SubmitComponent extends Component {

    constructor(props) {
      super(props);
      this.state = {
          image: ''
      }
    }

    onChange(e)
    {
let files=e.target.files;

let reader = new FileReader();
reader.readAsDataURL(files[0]);

reader.onload=(e)=>{
//This function puts the file into the API. Sends to backend
  const url="http://127.0.0.1:5000/test";
    const formData = { file:e.target.result }
    return post(url, formData)
      .then(response => console.warn("result", response))
}

    }
    render () {
      return (

        <div onSubmit={this.onFormSubmit}>
          <input type="file" name="file" onChange={(e)=> this.onChange(e)} />
        </div>
      )
    }
}


export default SubmitComponent ;
