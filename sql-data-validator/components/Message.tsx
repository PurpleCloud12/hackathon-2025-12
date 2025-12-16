
import React from 'react';
import type { Message as MessageType } from '../types';
import { UserIcon, BotIcon } from './icons';

interface MessageProps {
  message: MessageType;
}

const Message: React.FC<MessageProps> = ({ message }) => {
  const isUser = message.role === 'user';

  const wrapperClasses = `flex items-start gap-3 ${isUser ? 'justify-end' : 'justify-start'}`;
  const bubbleClasses = `max-w-xl lg:max-w-2xl rounded-lg px-4 py-3 ${
    isUser
      ? 'bg-blue-600 text-white rounded-br-none'
      : 'bg-gray-700 text-gray-200 rounded-bl-none'
  }`;

  const Icon = isUser ? UserIcon : BotIcon;

  return (
    <div className={wrapperClasses}>
      {!isUser && <Icon className="h-8 w-8 text-gray-400 flex-shrink-0 mt-1" />}
      <div className={bubbleClasses}>
        <div className="prose prose-invert prose-sm max-w-none">{message.content}</div>
      </div>
      {isUser && <Icon className="h-8 w-8 text-gray-400 flex-shrink-0 mt-1" />}
    </div>
  );
};

export default Message;
