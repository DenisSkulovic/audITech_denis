import axios from 'axios'
import PullRequestDTO from "../dto/PullRequestDTO"
import {PR_API_URL} from "../config"

class PullRequestService {

    public static async searchPullRequests(
        limit: number,
        offset: number,
    ): Promise<{ total: number, items: PullRequestDTO[] } | undefined> {
        try {
            const response = await axios.get(`${PR_API_URL}/detail/search`, { params: { limit, offset } })
            console.log(`response`, response)
            const rawData: any = JSON.parse(response.data)
            const total: number | undefined = rawData.total
            const rawItems: any = rawData.items
            if (!Array.isArray(rawItems)) throw new Error("api response must be an array of objects")
            if (typeof total !== "number") throw new Error("'total' is missing in the response of is not a number")
            const items: PullRequestDTO[] = rawItems.map((rawItem: any) => PullRequestDTO.build(rawItem))
            return { items, total }
        } catch (err: any) {
            console.error("FAILED TO FETCH PR ITEMS", err)
        }
    }
}

export default PullRequestService