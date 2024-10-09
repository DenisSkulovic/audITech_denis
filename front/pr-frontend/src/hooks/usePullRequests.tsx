import { useState, useEffect } from "react"
import PullRequestService from "../service/PullRequestService"
import PullRequestDTO from "../dto/PullRequestDTO"

export const usePullRequests = (
    limit: number,
    offset: number
): {
    pullRequests: PullRequestDTO[];
    isLoading: boolean;
    error: string | null;
    total: number;
} => {
    const [pullRequests, setPullRequests] = useState<PullRequestDTO[]>([])
    const [total, setTotal] = useState(0)
    const [isLoading, setIsLoading] = useState<boolean>(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        const fetch = async () => {
            try {
                setIsLoading(true)
                const resp = await PullRequestService.searchPullRequests(limit, offset)
                if (!resp) throw new Error("failed to get response to list PR items")
                const items: PullRequestDTO[] = resp.items
                const newTotal: number = resp.total
                setTotal(newTotal)
                setPullRequests(items || [])
                setError(null)
            } catch (err: any) {
                setError(err)
            } finally {
                setIsLoading(false)
            }
        }
        fetch()

    }, [limit, offset])

    return {pullRequests, isLoading, error, total}
}