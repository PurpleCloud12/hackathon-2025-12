
import React from 'react';

interface QueryConfirmationProps {
  sqlQuery: string;
  onConfirm: () => void;
  onCancel: () => void;
}

const QueryConfirmation: React.FC<QueryConfirmationProps> = ({ sqlQuery, onConfirm, onCancel }) => {
  return (
    <div className="space-y-4">
      <div>
        <p className="font-semibold">Generated SQL:</p>
        <pre className="mt-2 bg-gray-800 p-3 rounded-md text-sm text-cyan-300 overflow-x-auto">
          <code>{sqlQuery}</code>
        </pre>
      </div>
      <p className="font-semibold text-yellow-300">Do you want to execute this query?</p>
      <div className="flex items-center gap-4">
        <button
          onClick={onConfirm}
          className="bg-green-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-green-700 transition-colors duration-200"
          aria-label="Confirm and run query"
        >
          Yes, Run Query
        </button>
        <button
          onClick={onCancel}
          className="bg-red-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-red-700 transition-colors duration-200"
          aria-label="Cancel query execution"
        >
          No, Cancel
        </button>
      </div>
    </div>
  );
};

export default QueryConfirmation;
