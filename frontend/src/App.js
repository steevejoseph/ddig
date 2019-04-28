import React, { Component } from 'react';
import { DropzoneArea } from 'material-ui-dropzone';
import Button from '@material-ui/core/Button';
import axios from 'axios';
import './App.css';
import {} from 'dotenv/config';


class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      files: []
    };

    this.onButtonClick = this.onButtonClick.bind(this);
  }

  handleChange(files) {
    this.setState({
      files
    });
  }

  onButtonClick() {
    // console.log('teh file', this.state.files);
    const reader = new FileReader();
    reader.readAsDataURL(this.state.files[0])
    reader.onabort = () => console.log('file reading was aborted');
    reader.onerror = () => console.log('file reading has failed');
    reader.onload = () => {
      // console.log(reader.result);
      axios
        .post(`${process.env.REACT_APP_API_URL}/upload`, { data: reader.result })
        .then(res => {
          console.log(res);
          this.props.history.push('/image',  {imageUrl:res.data.link})
        })
        .catch(err => console.log(err))
    };
  }

  render() {
    return (
      <div style={{ textAlign: "center" }}>
        <header className="App-header">
          <DropzoneArea
            acceptedFiles={['image/*']}
            filesLimit={1}
            onChange={this.handleChange.bind(this)}
            showPreviews
            showAlerts
            showFileNamesInPreview
          />
        </header>
        <Button onClick={this.onButtonClick}>Submit</Button>
      </div>
    );
  }
}

export default App;
