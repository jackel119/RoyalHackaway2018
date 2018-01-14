import React, { Component } from 'react';
import MessageList from './MessageList'
import './App.css';

class App extends Component {

  constructor(props) {
    super(props)
    this.state = {
      messages: [
        { body: "Connecting..." },
        { author: "You", body: "Hello!", me: true },
        { author: "Them",body: "Hey there!"  },
        { author: "You", body: "Jet fuel can't melt steel beams"  },
      ],
    }
  } 

  render() {
    return (
      <div className="App">
      <MessageList messages = {this.state.messages}/>
      </div>
    )
  }
}

export default App;
