document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('addStudyPlanForm');
    const saveBtn = document.getElementById('saveButton');
    const modalEl = document.getElementById('add_studyplan');

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
        fetch('/add_studyplan', {
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

                    const tbody = document.getElementById('studyplanTableBody'); // nên đổi id luôn
                    const c = response.studyplan;
                    const newRow = document.createElement('tr');
                    newRow.innerHTML = `
    <td>${c.id_plan}</td>
    <td>${c.id_course}</td>
    <td>${c.discipline}</td>
    <td>${c.semester}</td>
    <td>${c.credit_of_discipline}</td>
    <td>${c.exam_format}</td>

    <td>
        <div class="btn-group">
            <button type="button" class="btn btn-success btn-sm"
                    data-bs-toggle="modal" data-bs-target="#view_studyplan"
                    data-idcourse="${c.id_plan}">View</button>
            <button type="button" class="btn btn-warning btn-sm"
                    data-bs-toggle="modal" data-bs-target="#update_studyplan"
                    data-idcourse="${c.id_plan}">Update</button>
            <button type="button" class="btn btn-danger btn-sm"
                    data-bs-toggle="modal" data-bs-target="#delete_studyplan"
                    data-idcourse="${c.id_plan}">Delete</button>
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
