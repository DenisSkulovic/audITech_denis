import React from "react"

interface Props {
    limit: number
    offset: number
    total: number
    onPageChange: (newOffset: number) => void
}

const Pagination: React.FC<Props> = ({limit, offset, total, onPageChange}) => {
    const currentPage: number = Math.floor(offset / limit) + 1;
    const totalPages: number = Math.ceil(total / limit);
  
    const handlePrevious = () => {
      if (offset > 0) onPageChange(offset - limit);
    };
    const handleNext = () => {
      if (offset + limit < total) onPageChange(offset + limit);
    };
  
    return (
      <div>
        <button className="btn btn-primary" onClick={handlePrevious} disabled={offset === 0}>
          Previous
        </button>
        <span>{` Page ${currentPage} of ${totalPages} `}</span>
        <button className="btn btn-primary" onClick={handleNext} disabled={offset + limit >= total}>
          Next
        </button>
      </div>
    );
}

export default Pagination;