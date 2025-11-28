document.addEventListener("DOMContentLoaded", function () {
    let studentIdToUpdate = null;

    // Khi mở modal Update
    const updateModal = document.getElementById("update_student");
    updateModal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget;
        studentIdToUpdate = button.getAttribute("data-idstudent");

        // Lấy thông tin sinh viên từ server
        fetch(`/student/${studentIdToUpdate}`)
            .then(response => response.json())
            .then(data => {
                // Đổ dữ liệu vào form
                document.getElementById("update_id_student").value = data.id_student;
                document.getElementById("update_last_name").value = data.last_name;
                document.getElementById("update_full_name").value = data.full_name;
                document.getElementById("update_year_of_admission").value = data.year_of_admission;
                document.getElementById("update_form_of_study").value = data.form_of_study;
                document.getElementById("update_education_level").value = data.education_level;
                document.getElementById("update_course_code").value = data.course_code;
                document.getElementById("update_group_number").value = data.group_number;
                document.getElementById("update_number_phone").value = data.number_phone;
                document.getElementById("update_email").value = data.email;
            });
    });

    // Khi nhấn nút "Update"
    document.getElementById("confirmUpdateButton").addEventListener("click", function () {
        const formData = new FormData(document.getElementById("updateStudentForm"));
        fetch(`/student/${studentIdToUpdate}`, {
            method: "PUT",
            body: formData
        })
        .then(response => {
            if (response.ok) {
                window.location.reload();
            } else {
                alert("Error updating student!");
            }
        })
        .catch(error => console.error("Error:", error));
    });
});
