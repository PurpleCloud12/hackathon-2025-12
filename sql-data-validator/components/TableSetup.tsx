
import React from 'react';

interface TableSetupProps {
  sourceTable: string;
  setSourceTable: (value: string) => void;
  targetTable: string;
  setTargetTable: (value: string) => void;
}

const TableSetup: React.FC<TableSetupProps> = ({
  sourceTable,
  setSourceTable,
  targetTable,
  setTargetTable,
}) => {
  return (
    <div className="bg-gray-800 p-4 border-b border-gray-700">
      <div className="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label htmlFor="sourceTable" className="block text-sm font-medium text-gray-300 mb-1">
            Source Table
          </label>
          <input
            id="sourceTable"
            type="text"
            value={sourceTable}
            onChange={(e) => setSourceTable(e.target.value)}
            placeholder="e.g., staging_users"
            className="w-full bg-gray-700 border border-gray-600 rounded-lg py-2 px-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200"
            aria-label="Source Table Name"
          />
        </div>
        <div>
          <label htmlFor="targetTable" className="block text-sm font-medium text-gray-300 mb-1">
            Target Table
          </label>
          <input
            id="targetTable"
            type="text"
            value={targetTable}
            onChange={(e) => setTargetTable(e.target.value)}
            placeholder="e.g., production_users"
            className="w-full bg-gray-700 border border-gray-600 rounded-lg py-2 px-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200"
            aria-label="Target Table Name"
          />
        </div>
      </div>
    </div>
  );
};

export default TableSetup;
