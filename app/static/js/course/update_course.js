document.addEventListener("DOMContentLoaded", function () {
    let studentIdToUpdate = null;

    // Khi mở modal Update
    const updateModal = document.getElementById("update_course");
    updateModal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget;
        courseIdToUpdate = button.getAttribute("data-idcourse");

        // Lấy thông tin khóa học từ server
        fetch(`/course/${courseIdToUpdate}`)
            .then(response => response.json())
            .then(data => {
                // Đổ dữ liệu vào form
                document.getElementById("update_id_course").value = data.id_course;
                document.getElementById("update_name_course").value = data.name_course;
                document.getElementById("update_total_hours").value = data.total_hours;
                document.getElementById("update_number_year").value = data.number_year;
                document.getElementById("update_description").value = data.description;
            });
    });

    // Khi nhấn nút "Update"
    document.getElementById("confirmUpdateButton").addEventListener("click", function () {
        const formData = new FormData(document.getElementById("updateCourseForm"));
        fetch(`/course/${courseIdToUpdate}`, {
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
