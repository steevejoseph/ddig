import React, { Component } from 'react';
import { DropzoneArea } from 'material-ui-dropzone';
import Button from '@material-ui/core/Button';
import axios from 'axios';
import Spinner from 'react-spinkit';

import './App.css';
import {} from 'dotenv/config';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      files: [],
      loading: false,
    };

    this.handleChange = this.handleChange.bind(this);
    this.onButtonClick = this.onButtonClick.bind(this);
  }

  onButtonClick() {
    const { files } = this.state;
    const { history } = this.props;
    this.setState({ loading: true });
    // console.log('teh file', this.state.files);
    const reader = new FileReader();
    reader.readAsDataURL(files[0]);
    reader.onabort = () => console.log('file reading was aborted');
    reader.onerror = () => console.log('file reading has failed');
    reader.onload = () => {
      // console.log(reader.result);
      axios
        .post(`${'http://localhost:5000'}/upload`, { data: reader.result })
        .then((res) => {
          console.log(res);
          history.push('/image', { imageUrl: res.data.link });
        })
        .catch(err => console.log(err));
    };
  }

  handleChange(files) {
    this.setState({
      files,
    });
  }

  renderDropZone() {
    const { loading } = this.state;
    if (loading) {
      return (
        <>
          <Spinner name="ball-grid-beat" color="white" />
          <p>Please wait while dream is generated...</p>
        </>
      );
    }

    return (
      <>
        <DropzoneArea
          dropZoneClass="dz"
          acceptedFiles={['image/*']}
          filesLimit={1}
          onChange={this.handleChange}
          showPreviews
          showAlerts
          showFileNamesInPreview
        />
        <Button style={{ backgroundColor: 'white' }} onClick={this.onButtonClick}>Submit</Button>
      </>
    );
  }

  render() {
    return (
      <div style={{ textAlign: 'center' }}>
        <header className="App-header">
          {this.renderDropZone()}
        </header>
      </div>
    );
  }
}

export default App;
