import React, { Component } from 'react'
import './MessageList.css'

class MessageList extends Component {
  render() {
    return (
      <div className="MessageList">
        <div>Connecting...</div>
        <div><span className="author">You:</span> Hello!</div>
        <div><span className="author">Them:</span> Hey there!</div>
      </div>
    )
  }
}

export default MessageList
