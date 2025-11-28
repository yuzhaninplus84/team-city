document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('addStudentForm');
    const saveBtn = document.getElementById('saveButton');
    const modalEl = document.getElementById('add_student');

    saveBtn.addEventListener('click', (e) => {
        e.preventDefault(); // ngăn form submit truyền thống

        // Lấy dữ liệu từ form
        const formData = new FormData(form);

        // Chuyển sang JSON
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        let valid = true;  // biến kiểm tra
        formData.forEach((value, key) => {
            data[key] = value;
            // Kiểm tra required fields
            if (form.querySelector(`[name="${key}"]`)?.hasAttribute('required') && !value) {
                valid = false;
            }
        });

        if (!valid) {
            alert('Please fill in all required information!');
            return; // dừng gửi
        }



        // Gửi dữ liệu tới server bằng Fetch API
        fetch('/add_student', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(res => res.json())
            .then(response => {
                if (response.success) {
                    alert('Student added successfully!');
                    // reset form
                    form.reset();
                    // đóng modal
                    const modal = bootstrap.Modal.getInstance(modalEl);
                    modal.hide();
                    // tùy chọn: reload bảng students hoặc append row mới
                    // Thêm row mới vào table
                    const tbody = document.getElementById('studentsTableBody');
                    const s = response.student;
                    const newRow = document.createElement('tr');
                    newRow.innerHTML = `
        <td>${s.id_student}</td>
        <td>${s.last_name}</td>
        <td>${s.full_name}</td>
        <td>${s.year_of_admission}</td>
        <td>${s.form_of_study ?? ''}</td>
        <td>${s.education_level ?? ''}</td>
        <td>${s.course_code ?? ''}</td>
        <td>${s.group_number ?? ''}</td>
        <td>${s.number_phone ?? ''}</td>
        <td>${s.email ?? ''}</td>
        <td>
            <div class="btn-group">
                <button type="button" class="btn btn-success btn-sm"
                        data-bs-toggle="modal" data-bs-target="#view_student"
                        data-idstudent="${s.id_student}">View</button>
                <button type="button" class="btn btn-warning btn-sm"
                        data-bs-toggle="modal" data-bs-target="#update_student"
                        data-idstudent="${s.id_student}">Update</button>
                <button type="button" class="btn btn-danger btn-sm"
                        data-bs-toggle="modal" data-bs-target="#delete_student"
                        data-idstudent="${s.id_student}">Delete</button>
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
