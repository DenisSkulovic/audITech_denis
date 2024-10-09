import React, { useState } from 'react';
import './App.css';
import { usePullRequests } from './hooks/usePullRequests';
import Pagination from './components/Pagination';
import PRTable from './components/PRTable';

const LIMIT = 10


const App: React.FC = () => {
  const [offset, setOffset] = useState(0)
  const { pullRequests, isLoading, error, total } = usePullRequests(LIMIT, offset)

  return (
    <div>
      <h1>GitHub Pull Requests</h1>

      {isLoading && <p>Loading...</p>}
      {error && <p>{error}</p>}

      {!isLoading && !error && (
        <>
          <PRTable pullRequests={pullRequests} />
          <Pagination
            limit={LIMIT}
            offset={offset}
            total={total}
            onPageChange={setOffset}
          />
        </>
      )}
    </div>
  );
}

export default App;
