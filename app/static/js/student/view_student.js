document.addEventListener("DOMContentLoaded", function () {
    const viewModal = document.getElementById("view_student");

    viewModal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget;
        const studentId = button.getAttribute("data-idstudent");

        const modalBody = viewModal.querySelector(".modal-body");
        modalBody.innerHTML = "<p>Loading...</p>";

        // Gọi API Flask để lấy dữ liệu sinh viên
        fetch(`/student/${studentId}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    modalBody.innerHTML = `<p class="text-danger">${data.error}</p>`;
                } else {
                    modalBody.innerHTML = `
                        <ul class="list-group">
                            <li class="list-group-item"><b>ID:</b> ${data.id_student}</li>
                            <li class="list-group-item"><b>Last Name:</b> ${data.last_name}</li>
                            <li class="list-group-item"><b>Full Name:</b> ${data.full_name}</li>
                            <li class="list-group-item"><b>Year of Admission:</b> ${data.year_of_admission}</li>
                            <li class="list-group-item"><b>Form of Study:</b> ${data.form_of_study}</li>
                            <li class="list-group-item"><b>Education Level:</b> ${data.education_level}</li>
                            <li class="list-group-item"><b>Course Code:</b> ${data.course_code}</li>
                            <li class="list-group-item"><b>Group Number:</b> ${data.group_number}</li>
                            <li class="list-group-item"><b>Phone:</b> ${data.number_phone}</li>
                            <li class="list-group-item"><b>Email:</b> ${data.email}</li>
                        </ul>
                    `;
                }
            })
            .catch(error => {
                modalBody.innerHTML = `<p class="text-danger">Error: ${error}</p>`;
            });
    });
});
