import React, { Fragment } from 'react';

import styled from 'styled-components';

import Slider from '@material-ui/lab/Slider';
import FormHelperText from '@material-ui/core/FormHelperText';

import { pdfjs } from "react-pdf"


const FileInput = ({ value, setValue }) => {

  const handleChange = (event, value) => {
    const file = event.target.files[0]
    console.log(file)
    pdfjs.workerSrc = '//mozilla.github.io/pdf.js/build/pdf.worker.js';
    var pdfDocument = file;
    var pagesPromises = [];

    for (var i = 0; i < file.pdfInfo.numPages; i++) {
      // Required to prevent that i is always the total of pages
      (function (pageNumber) {
        pagesPromises.push(getPageText(pageNumber, pdfDocument));
      })(i + 1);
    }

    Promise.all(pagesPromises).then(function (pagesText) {
      // Remove loading
      // Render text
      for (var i = 0; i < pagesText.length; i++) {
        console.log(pagesText[i]);;
      }
    });
    function getPageText(pageNum, PDFDocumentInstance) {
      // Return a Promise that is solved once the text of the page is retrieven
      return new Promise(function (resolve, reject) {
        PDFDocumentInstance.getPage(pageNum).then(function (pdfPage) {
          // The main trick to obtain the text of the PDF page, use the getTextContent method
          pdfPage.getTextContent().then(function (textContent) {
            var textItems = textContent.items;
            var finalString = "";

            // Concatenate the string of the item to the final string
            for (var i = 0; i < textItems.length; i++) {
              var item = textItems[i];

              finalString += item.str + " ";
            }

            // Solve promise with the text retrieven from the page
            resolve(finalString);
          });
        });
      });
    }
  };

  return (
    <Fragment>
      <input type='file' value={value} onChange={handleChange}></input>
      <FormHelperText>Upload File</FormHelperText>
    </Fragment>
  );
}

export default FileInput;