import React, { Component } from 'react';
import MessageList from './MessageList'
import MessageForm from './MessageForm'
import './App.css';

class App extends Component {

  constructor(props) {
    super(props)
    var that = this
    var Httpreq = new XMLHttpRequest()
    Httpreq.onreadystatechange = function() {
      that.state = {
        messages : [] // JSON.parse(this.responseText)
      }
      console.log(this.responseText)
      console.log("API call successful")
    }
    Httpreq.open("GET", "http://127.0.0.1:5002/messages", true, { contentType: 'string' })
    Httpreq.send(null);
  } 

  handleNewMessage = (text) => {
    this.setState({
      messages: [...this.state.messages, { me: true, author: "Me", body: text }],
    })
  }

  render() {
    return (
       <div className="App">
        <MessageList messages={this.state.messages} />
        <MessageForm onMessageSend={this.handleNewMessage} />
       </div>
    )
  }
}

export default App;
