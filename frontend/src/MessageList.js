import React, { Component } from 'react'
import PropTypes from 'prop-types'
import './MessageList.css'
import Message from './Message'

class MessageList extends Component {
  static propTypes = {
    messages: PropTypes.arrayOf(PropTypes.object)
  }

  static defaultProps = {
    messages: [],
  }

  render() {
    return (
      <div className="MessageList">
        {this.props.messages.map((message, i) => (
            <Message key={i} {...message} />
          ))}
      </div>
    )
  }

}

export default MessageList
