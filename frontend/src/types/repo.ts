export interface Repo {
  id: number;
  name: string;
  github_url: string;
  branch?: string;
  user_id: number;
  created_at: string;
  updated_at: string;
  download_tasks?: RepoDownloadTask[];
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
  total_count: number;
  page: number;
  per_page: number;
  total_pages: number;
}

export interface RepoDownloadTask {
  id: number;
  task_id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  output_path?: string;
  error_message?: string;
  created_at: string;
  updated_at: string;
  repo_id: number;
} 