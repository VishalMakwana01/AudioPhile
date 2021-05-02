import React, { useState } from 'react';

import styled from 'styled-components';

import SpeechSpeedSetter from './SpeechSpeedSetter';
import LanguageSelect from './LanguageSelect';
import TextToSpeech from './TextToSpeech';

import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';

import { DEFAULTS } from './appEnums';
import Navbar from './Navbar';
import FileInput from './FileInput';
import axios from 'axios';

const apiKey = '332c16d1a8db4a10b44047fd0888b485';

const App = ({ className }) => {
  const [language, setLanguage] = useState(DEFAULTS.LANGUAGES);
  const [speed, setSpeed] = useState(DEFAULTS.SPEED);
  const [text, setText] = useState(DEFAULTS.TEXT);
  const [speech, setSpeech] = useState(DEFAULTS.SPEECH);
  const [filetext, setFileText] = useState(false);
  const [play, setPlay] = useState(false);

  const handleClick = () => {
    setPlay(true)

  };
  const handleTextClick = () => {
    if (text.trim() == "") {
      alert("Enter text")
    }
    else {
      const body = { text: text }
      console.log(body)
      axios
        .post("http://127.0.0.1:8000/audio/", body)
        .then(res => setSpeech(res.data.url))
        .catch((err) => console.log(err));
      setSpeech("http://127.0.0.1:8000/audio/")

    }
  }
  const playFile = () => {
    console.log("Playig")
    setPlay(true);
  }
  return (
    <>{console.log(speech)}
      <Navbar />
      <div className={className}>
        <Grid container spacing={16}>
          <Grid item xs={6}>
            <LanguageSelect value={language} setValue={setLanguage} />
          </Grid>
          <Grid item xs={6}>
            <SpeechSpeedSetter value={speed} setValue={setSpeed} />
          </Grid>
          <Grid item xs={12}>
            <TextToSpeech value={text} setValue={setText} />
          </Grid>
          <Grid item xs={12} >
            <div style={{ textAlign: "center" }}>
              <Button
                variant="contained"
                color="primary"
                onClick={() => handleTextClick()}
              >
                Convert
          </Button>
            </div>
          </Grid>
          <Grid item xs={12}>
            <div style={{ textAlign: "center" }}>OR</div>
          </Grid>
          <Grid item xs={12}>
            <div style={{ textAlign: "center" }}>
              <FileInput setSp={setSpeech}></FileInput>
            </div>
          </Grid>
          <Grid item xs={6} >
            {speech
              &&
              <div style={{ textAlign: "center" }}>
                <a href={speech} target="_blank" download="audio.mp3"><Button
                  variant="contained"
                  color="primary"
                >
                  Download
          </Button></a>
              </div>
            }

          </Grid>
          <Grid item xs={6} >
            {speech
              &&
              <div style={{ textAlign: "center" }}>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleClick}
                >
                  Play
          </Button>
              </div>
            }{play && <audio src={speech} autoPlay></audio>}

          </Grid>
        </Grid>
      </div>
    </>
  );
}

const StyledApp = styled(App)`
  max-width: 640px;
  margin: 0 auto;
  padding-top: 40px;
`

export default StyledApp;
