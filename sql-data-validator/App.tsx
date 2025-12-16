
import React, { useState, useCallback } from 'react';
import { GoogleGenAI } from '@google/genai';
import type { Message, QueryResult } from './types';
import ChatWindow from './components/ChatWindow';
import ChatInput from './components/ChatInput';
import TableSetup from './components/TableSetup';
import ResultTable from './components/ResultTable';
import { BotIcon } from './components/icons';
import QueryConfirmation from './components/QueryConfirmation';

const App: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'init',
      role: 'bot',
      content: (
        <div className="space-y-2">
          <p>Welcome to the SQL Data Validator!</p>
          <p>
            Please enter your source and target table names above. Then, tell me what you'd like to compare or validate.
          </p>
          <p className="text-sm text-gray-400">
            For example: "Find records in the source table that are not in the target table based on the 'id' column."
          </p>
        </div>
      ),
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [sourceTable, setSourceTable] = useState('');
  const [targetTable, setTargetTable] = useState('');
  const [pendingQuery, setPendingQuery] = useState<string | null>(null);

  const addMessage = useCallback((message: Omit<Message, 'id'>) => {
    setMessages((prev) => [...prev, { ...message, id: Date.now().toString() + Math.random() }]);
  }, []);

  const updateLastMessage = useCallback((content: React.ReactNode) => {
    setMessages(prev => {
      if (prev.length === 0) return prev;
      const newMessages = [...prev];
      const lastMessage = { ...newMessages[newMessages.length - 1] };
      lastMessage.content = content;
      newMessages[newMessages.length - 1] = lastMessage;
      return newMessages;
    });
  }, []);

  const handleSendMessage = useCallback(async (userInput: string) => {
    if (isLoading || pendingQuery || !userInput.trim()) return;
    if (!sourceTable.trim() || !targetTable.trim()) {
      addMessage({
        role: 'bot',
        content: 'Please set both the source and target table names before sending a command.',
      });
      return;
    }

    setIsLoading(true);
    addMessage({ role: 'user', content: userInput });

    try {
      addMessage({
        role: 'bot',
        content: (
          <div className="flex items-center gap-2">
            <BotIcon className="h-5 w-5 animate-pulse" />
            <span>Generating SQL query...</span>
          </div>
        ),
      });

      // Fix: Use process.env for compatibility with non-Vite environments
      const ai = new GoogleGenAI({ apiKey: process.env.VITE_API_KEY!, vertexai: true });
      const prompt = `
        You are an expert SQL generator. Your task is to create a single, executable SQL query to compare a source table named '${sourceTable}' and a target table named '${targetTable}'.
        The user wants to perform the following action: "${userInput}".
        Based on the user's request, generate the appropriate SQL query.
        IMPORTANT: Respond with ONLY the raw SQL query and nothing else. Do not wrap it in markdown, add explanations, or any other text.
      `;
      
      const response = await ai.models.generateContent({
        model: 'gemini-2.5-flash',
        contents: { role: 'user', parts: [{ text: prompt }] },
      });
      
      const sqlQuery = response.text.trim();

      if (!sqlQuery) {
        throw new Error('The AI failed to generate an SQL query.');
      }

      // Define handlers inside this callback to close over the fresh sqlQuery
      const onConfirm = async () => {
        setPendingQuery(null);
        setIsLoading(true);

        updateLastMessage(
            <div className="space-y-4">
              <div>
                <p className="font-semibold">Generated SQL:</p>
                <pre className="mt-2 bg-gray-800 p-3 rounded-md text-sm text-cyan-300 overflow-x-auto">
                  <code>{sqlQuery}</code>
                </pre>
              </div>
              <p className="font-semibold text-green-400">Query execution confirmed.</p>
            </div>
        );

        addMessage({ role: 'bot', content: ( <div className="flex items-center gap-2"> <BotIcon className="h-5 w-5 animate-spin" /> <span>Executing query against the database...</span> </div> ), });

        try {
          // Fix: Use process.env for compatibility with non-Vite environments
          const backendUrl = process.env.VITE_BACKEND_URL;
          if (!backendUrl) {
            throw new Error("Backend URL is not configured. Please set VITE_BACKEND_URL in your .env file.");
          }

          const backendResponse = await fetch(backendUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              source_table: sourceTable,
              target_table: targetTable,
            }),
          });
          if (!backendResponse.ok) {
            const errorData = await backendResponse.json().catch(() => ({ error: 'Failed to execute query. The backend returned an invalid response.' }));
            throw new Error(errorData.error || `HTTP error! Status: ${backendResponse.status}`);
          }
          const resultData: QueryResult = await backendResponse.json();
          updateLastMessage(<ResultTable data={resultData} />);
        } catch (error) {
          console.error("Fetch Error:", error);
          let detailedMessage = "An unknown error occurred.";
          if (error instanceof TypeError && error.message === 'Failed to fetch') {
              // Fix: Use process.env for compatibility with non-Vite environments
              detailedMessage = `The request to the backend failed. This is often due to one of the following reasons:\n\n1. The backend server at ${process.env.VITE_BACKEND_URL} is not running or is unreachable.\n2. A network issue (like a firewall) is blocking the connection.\n3. The backend server is not configured for Cross-Origin Resource Sharing (CORS).\n\nPlease check the browser's developer console (F12 -> Network tab) for more specific error details.`;
          } else if (error instanceof Error) {
              detailedMessage = error.message;
          }
          
          updateLastMessage(
            <div className="text-red-400 space-y-2">
              <p><strong>Error Communicating with Backend</strong></p>
              <p className="whitespace-pre-wrap text-sm font-mono">{detailedMessage}</p>
            </div>
          );
        } finally {
          setIsLoading(false);
        }
      };

      const onCancel = () => {
        setPendingQuery(null);
        updateLastMessage(
            <div className="space-y-4">
              <div>
                <p className="font-semibold">Generated SQL:</p>
                <pre className="mt-2 bg-gray-800 p-3 rounded-md text-sm text-cyan-300 overflow-x-auto">
                  <code>{sqlQuery}</code>
                </pre>
              </div>
              <p className="font-semibold text-red-400">Query execution cancelled.</p>
            </div>
        );
      };

      setPendingQuery(sqlQuery);
      updateLastMessage(
          <QueryConfirmation
            sqlQuery={sqlQuery}
            onConfirm={onConfirm}
            onCancel={onCancel}
          />
      );
      setIsLoading(false); // Stop loading for generation, wait for user confirmation

    } catch (error) {
      console.error(error);
      const errorMessage = error instanceof Error ? error.message : 'An unknown error occurred.';
      updateLastMessage(
        <div className="text-red-400">
          <p><strong>Error:</strong></p>
          <p>{errorMessage}</p>
        </div>
      );
      setIsLoading(false);
    }
  }, [isLoading, pendingQuery, sourceTable, targetTable, addMessage, updateLastMessage]);

  return (
    <div className="flex flex-col h-screen bg-gray-900 font-sans">
      <header className="bg-gray-800/50 backdrop-blur-sm border-b border-gray-700 p-4 shadow-lg z-10">
        <h1 className="text-xl font-bold text-center text-white">
          AI SQL Data Validator
        </h1>
      </header>
      
      <TableSetup
        sourceTable={sourceTable}
        setSourceTable={setSourceTable}
        targetTable={targetTable}
        setTargetTable={setTargetTable}
      />

      <main className="flex-1 overflow-y-auto p-4">
        <ChatWindow messages={messages} />
      </main>

      <footer className="p-4 bg-gray-900 border-t border-gray-700">
        <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading || !!pendingQuery} />
      </footer>
    </div>
  );
};

export default App;
