
import React, { useEffect, useRef } from 'react';
import type { Message as MessageType } from '../types';
import Message from './Message';

interface ChatWindowProps {
  messages: MessageType[];
}

const ChatWindow: React.FC<ChatWindowProps> = ({ messages }) => {
  const endOfMessagesRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {messages.map((msg) => (
        <Message key={msg.id} message={msg} />
      ))}
      <div ref={endOfMessagesRef} />
    </div>
  );
};

export default ChatWindow;
