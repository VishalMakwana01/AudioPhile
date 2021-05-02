import React, { Fragment, useState } from 'react';

import styled from 'styled-components';

import Slider from '@material-ui/lab/Slider';
import FormHelperText from '@material-ui/core/FormHelperText';

import { pdfjs } from "react-pdf"
import Button from '@material-ui/core/Button';
import axios from "axios"

const FileInput = ({ setSp }) => {
  const hiddenFileInput = React.useRef(null);
  const [state, setState] = useState(false);
  const handleClick = event => {
    hiddenFileInput.current.click();
  };
  const handleChange = async (event, value) => {
    const formData = new FormData();
    if (event.target && event.target.files) {
      formData.append(
        "ebook",
        event.target.files[0],
        event.target.files[0].name
      )
      axios
        .post("http://127.0.0.1:8000/audio/", formData)
        .then(res => setSp(res.data.url))
        .catch((err) => console.log(err));

      console.log(formData)

      setState(true)
    }

  };
  const renderUpload = () => {
    if (state) {
      return <FormHelperText>File Uploaded</FormHelperText>
    }
  }
  return (
    <Fragment>
      <div style={{ display: "flex", flexDirection: 'row' }}>
        <div style={{ width: "0%" }}> <input type='file' ref={hiddenFileInput} accept="application/pdf" onChange={handleChange}
          style={{ display: "none" }}
        ></input></div>
        <div style={{ width: "100%" }}><Button
          variant="contained"
          color="primary"
          onClick={handleClick}
        >
          Upload File
          </Button></div>
      </div>
      {renderUpload()}
    </Fragment>
  );
}

export default FileInput;