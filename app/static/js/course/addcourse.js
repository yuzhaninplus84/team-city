document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('addCourseForm');
    const saveBtn = document.getElementById('saveButton');
    const modalEl = document.getElementById('add_course');

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

        console.log(data);

        // Gửi dữ liệu tới server bằng Fetch API
        fetch('/add_course', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(res => res.json())
            .then(response => {
                if (response.success) {
                    alert('Course added successfully!');
                    // reset form
                    form.reset();
                    // đóng modal
                    const modal = bootstrap.Modal.getInstance(modalEl);
                    modal.hide();
                    // tùy chọn: reload bảng students hoặc append row mới
                    // Thêm row mới vào table

                    const tbody = document.getElementById('coursesTableBody'); // nên đổi id luôn
                    const c = response.course;
                    const newRow = document.createElement('tr');
                    newRow.innerHTML = `
    <td>${c.id_course}</td>
    <td>${c.name_course}</td>
    <td>${c.total_hours}</td>
    <td>${c.number_year}</td>
    <td>${c.description}</td>
    <td>
        <div class="btn-group">
            <button type="button" class="btn btn-success btn-sm"
                    data-bs-toggle="modal" data-bs-target="#view_course"
                    data-idcourse="${c.id_course}">View</button>
            <button type="button" class="btn btn-warning btn-sm"
                    data-bs-toggle="modal" data-bs-target="#update_course"
                    data-idcourse="${c.id_course}">Update</button>
            <button type="button" class="btn btn-danger btn-sm"
                    data-bs-toggle="modal" data-bs-target="#delete_course"
                    data-idcourse="${c.id_course}">Delete</button>
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
