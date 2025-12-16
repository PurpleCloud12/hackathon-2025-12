
import React from 'react';
import type { QueryResult } from '../types';

interface ResultTableProps {
  data: QueryResult;
}

const ResultTable: React.FC<ResultTableProps> = ({ data }) => {
  if (!data || data.length === 0) {
    return <p className="text-gray-400">The query executed successfully, but returned no results.</p>;
  }

  const headers = Object.keys(data[0]);

  return (
    <div className="space-y-3">
        <p>Query executed successfully. Here are the results:</p>
        <div className="overflow-x-auto bg-gray-800 rounded-lg border border-gray-700">
        <table className="min-w-full text-sm text-left text-gray-300">
            <thead className="bg-gray-700/50 text-xs text-gray-300 uppercase">
            <tr>
                {headers.map((header) => (
                <th key={header} scope="col" className="px-6 py-3">
                    {header}
                </th>
                ))}
            </tr>
            </thead>
            <tbody>
            {data.map((row, rowIndex) => (
                <tr key={rowIndex} className="border-b border-gray-700 hover:bg-gray-700/40">
                {headers.map((header, cellIndex) => (
                    <td key={`${rowIndex}-${cellIndex}`} className="px-6 py-4">
                    {String(row[header])}
                    </td>
                ))}
                </tr>
            ))}
            </tbody>
        </table>
        </div>
    </div>
  );
};

export default ResultTable;
