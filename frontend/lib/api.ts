const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

export type LoginResponse = {
    access_token: string;
    token_type: string;
};

export type User = {
    id: number;
    name: string;
    email: string;
    role: string;
};


export type Project = {
    id: number;
    name: string;
    description?: string | null;
    created_by?: number;
};

export type Task = {
    id: number;
    title: string;
    description?: string | null;
    status: string;
    project_id: number;
    assigned_to?: number | null;
    due_date?: string | null;
};

export type TaskListResponse = {
    items: Task[];
    total: number;
    page: number;
    size: number;
};

export async function loginUser(
  username: string,
  password: string
): Promise<LoginResponse> {
  const formData = new URLSearchParams();
  formData.append("username", username);
  formData.append("password", password);

  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: formData.toString(),
  });

  if (!response.ok) {
    throw new Error("Login failed");
  }

  return response.json();
}

export async function getProjects(token: string): Promise<Project[]> {
    const response = await fetch(`${API_BASE_URL}/projects/`, {
        method: "GET",
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

    if (!response.ok) {
        throw new Error("Failed to fetch projects");
    }

    return response.json();
}

export async function createProject(
    token: string,
    payload: {
        name: string;
        description?: string;
    }
): Promise<Project> {
    const response = await fetch(`${API_BASE_URL}/projects/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
    });

    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText || "Failed to create project");
    }

    return response.json();
}

export async function getTasks(
    token: string,
    page = 1,
    size = 10
): Promise<TaskListResponse> {
    const response = await fetch(`${API_BASE_URL}/tasks/?page=${page}&size=${size}`, {
        method: "GET",
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

    if (!response.ok) {
        throw new Error("Failed to fetch tasks");
    }

    return response.json();
}


export async function getCurrentUser(token: string): Promise<User> {
  const response = await fetch(`${API_BASE_URL}/users/me`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch current user");
  }

  return response.json();
}

export async function getUsers(token: string): Promise<User[]> {
    const response = await fetch(`${API_BASE_URL}/users/`, {
        method: "GET",
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

    if (!response.ok) {
        throw new Error("Failed to fetch users");
    }

    return response.json();
}


export async function createUser(
  token: string,
  payload: {
    name: string;
    email: string;
    password: string;
    role: string;
  }
): Promise<User> {
  const response = await fetch(`${API_BASE_URL}/users/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || "Failed to create user");
  }

  return response.json();
}


export async function updateTaskStatus(
  token: string,
  taskId: number,
  status: string
) {
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_BASE_URL}/tasks/${taskId}/status`,
    {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ status }),
    }
  );

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || "Failed to update task status");
  }

  return response.json();
}


export async function createTask(
    token: string,
    payload: {
        title: string;
        description?: string;
        project_id: number;
        assigned_to?: number;
        due_date?: string;
    }
): Promise<Task> {
    const response = await fetch(`${API_BASE_URL}/tasks/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
    });

    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText || "Failed to create task");
    }

    return response.json();
}