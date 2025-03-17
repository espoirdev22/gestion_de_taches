export interface Task {
    id: number;
    title: string;
    description: string;
    status: 'todo' | 'in_progress' | 'completed';
    assigned_to: {
      id: number;
      username: string;
      due_date:string;
    };
    project: {
      id: number;
      title: string;
    };
    due_date: string;
    created_at: string;
    updated_at: string;
  }
  