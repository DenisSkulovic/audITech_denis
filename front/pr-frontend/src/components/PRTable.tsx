import React from "react"
import PullRequestDTO from "../dto/PullRequestDTO"

interface Props {
    pullRequests: PullRequestDTO[]
}

const PRTable: React.FC<Props> = ({pullRequests}) => {
    return (
        <table className="table table-striped">
        <thead className="thead-dark">
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Author</th>
            <th>State</th>
            <th>Source Branch</th>
            <th>Target Branch</th>
            <th>Created At</th>
            <th>Link</th>
          </tr>
        </thead>
        <tbody>
          {pullRequests.map((pr: PullRequestDTO) => (
            <tr key={pr.id}>
              <td>{pr.id}</td>
              <td>{pr.pr_title}</td>
              <td>{pr.author}</td>
              <td>{pr.state}</td>
              <td>{pr.source_branch}</td>
              <td>{pr.target_branch}</td>
              <td>{new Date(pr.created_at).toLocaleString()}</td>
              <td>
                <a href={pr.pr_url} target="_blank" rel="noopener noreferrer">
                  View PR
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    )
}

export default PRTable;