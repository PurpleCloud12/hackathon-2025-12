
import type { ReactNode } from 'react';

export type MessageRole = 'user' | 'bot';

export interface Message {
  id: string;
  role: MessageRole;
  content: ReactNode;
}

export type QueryResult = Record<string, any>[];
