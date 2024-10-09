class PullRequestDTO {
    constructor(
        public id: number, 
        public pr_title: string,
        public author: string,
        public state: string, 
        public source_branch: string, 
        public target_branch: string, 
        public pr_url: string, 
        public created_at: number
    ) { }

    public static validate(obj: any): void {
        if (typeof obj.id === "undefined") throw new Error("'id' cannot be undefined on PR item")
        if (typeof obj.pr_title === "undefined") throw new Error("'pr_title' cannot be undefined on PR item")
        if (typeof obj.author === "undefined") throw new Error("'author' cannot be undefined on PR item")
        if (typeof obj.state === "undefined") throw new Error("'state' cannot be undefined on PR item")
        if (typeof obj.source_branch === "undefined") throw new Error("'source_branch' cannot be undefined on PR item")
        if (typeof obj.target_branch === "undefined") throw new Error("'target_branch' cannot be undefined on PR item")
        if (typeof obj.pr_url === "undefined") throw new Error("'pr_url' cannot be undefined on PR item")
        if (typeof obj.created_at === "undefined") throw new Error("'created_at' cannot be undefined on PR item")
    }

    public static build(obj: any) {
        PullRequestDTO.validate(obj)
        return new PullRequestDTO(
            obj.id, 
            obj.pr_title,
            obj.author,
            obj.state, 
            obj.source_branch, 
            obj.target_branch, 
            obj.pr_url, 
            obj.created_at
        )
    }
}

export default PullRequestDTO