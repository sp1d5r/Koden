export interface Repo {
  id: number;
  name: string;
  github_url: string;
  branch: string;
  user_id: number;
  created_at: string;
  updated_at: string;
}

export interface RepoCreate {
  name: string;
  github_url: string;
  branch?: string;
}

export interface RepoUpdate {
  name?: string;
  github_url?: string;
  branch?: string;
}

export interface RepoListResponse {
  repos: Repo[];
  total: number;
  skip: number;
  limit: number;
} 