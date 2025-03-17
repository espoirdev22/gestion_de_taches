export interface Project {
    id: number;
    title: string;
    description: string;
    created_by: {
      id: number;
      username: string;
      first_name: string;
      last_name: string;
      tasks_count?: number;  

    };
    created_at: string;
    updated_at: string;
    members: {
      id: number;
      username: string;
      first_name: string;
      last_name: string;
    }[];
  }
  