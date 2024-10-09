import axios from 'axios'
import PullRequestDTO from "../dto/PullRequestDTO"


class PullRequestService {

    public static async searchPullRequests(
        limit: number,
        offset: number,
    ): Promise<{total: number, items: PullRequestDTO[]} | undefined> {
        try {
            const PR_API_URL: string | undefined = process.env.PR_API_URL
            if (!PR_API_URL) throw new Error("PR_API_URL is a mandatory env param")
            const response = await axios.get(`${PR_API_URL}/detail/search`, {params: {limit, offset}})
            const rawData: any = JSON.parse(response.data)
            const total: number | undefined = rawData.total
            const rawItems: any = rawData.items
            if (!Array.isArray(rawItems)) throw new Error("api response must be an array of objects")
            if (typeof total !== "number") throw new Error("'total' is missing in the response of is not a number")
            const items: PullRequestDTO[] = rawItems.map((rawItem: any) => PullRequestDTO.build(rawItem))
            return {items, total}
        } catch (err: any) {
            console.error("FAILED TO FETCH PR ITEMS", err)
        }
    }
}

export default PullRequestService