document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('addLogForm');
    const saveBtn = document.getElementById('saveButton');
    const modalEl = document.getElementById('add_log');

    saveBtn.addEventListener('click', (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        const data = {};
        let valid = true;

        formData.forEach((value, key) => {
            data[key] = value;
            if (form.querySelector(`[name="${key}"]`)?.hasAttribute('required') && !value) {
                valid = false;
            }
        });

        if (!valid) {
            alert('Please fill in all required information!');
            return;
        }

        fetch('/add_grades', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(response => {
            if (response.success) {
                alert('Progress log added successfully!');
                form.reset();

                // đóng modal
                const modal = bootstrap.Modal.getInstance(modalEl);
                modal.hide();

                // append row mới vào table
                const tbody = document.getElementById('ProgressLogTableBody');
                const c = response.progress_log;
                const newRow = document.createElement('tr');
                newRow.innerHTML = `
                    <td>${c.id_log}</td>
                    <td>${c.semester}</td>
                    <td>${c.student_id}</td>
                    <td>${c.course_id}</td>
                    <td>${c.grade}</td>
                    <td>
                        <div class="btn-group">
                            <button type="button" class="btn btn-success btn-sm" data-bs-toggle="modal" data-bs-target="#view_log" data-idlog="${c.id_log}">View</button>
                            <button type="button" class="btn btn-warning btn-sm" data-bs-toggle="modal" data-bs-target="#update_log" data-idlog="${c.id_log}">Update</button>
                            <button type="button" class="btn btn-danger btn-sm" data-bs-toggle="modal" data-bs-target="#delete_log" data-idlog="${c.id_log}">Delete</button>
                        </div>
                    </td>`;
                tbody.appendChild(newRow);
            } else {
                alert('Error: ' + response.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Something went wrong!');
        });
    });
});
