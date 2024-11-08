async function createTaskRequest() {
    const response = await fetch('/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: null
    });
    const result = await response.json();
}

async function DeleteTaskRequest() {
    const data = document.getElementById('deleteInput').value;
    const response = await fetch(`/tasks/${data}`, {
        method: 'DELETE',
    });
    const result = await response.json();
}

async function fetchTaskData() {
    const response = await fetch('/tasks');
    const result = await response.json();
    const tableBody = document.getElementById('taskTableBody');
    tableBody.innerHTML = '';
    
    result.forEach(task => {
        const row = document.createElement('tr');
        row.innerHTML = `
        <td>${task.id}</td>
        <td>${task.status}</td>
        <td>${task.created_at}</td>
        <td>${task.updated_at}</td>
        `;
        tableBody.appendChild(row);
    });
}

// Polling every 1 second
setInterval(fetchTaskData, 1000);
fetchTaskData(); // Initial fetch
