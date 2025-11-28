document.addEventListener("DOMContentLoaded", function () {
    let logIdToUpdate = null;

    // Khi mở modal Update
    const updateModal = document.getElementById("update_log");
    updateModal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget;
        logIdToUpdate = button.getAttribute("data-idlog");
        console.log(logIdToUpdate)
        // Lấy thông tin sinh viên từ server
        fetch(`/grades/${logIdToUpdate}`)
            .then(response => response.json())
            .then(data => {
                // Đổ dữ liệu vào form
                document.getElementById("update_id_log").value = data.id_log;
                document.getElementById("update_semester").value = data.semester;
                document.getElementById("update_student_id").value = data.student_id;
                document.getElementById("update_course_id").value = data.course_id;
                document.getElementById("update_grade").value = data.grade;
            });
    });

    // Khi nhấn nút "Update"
    document.getElementById("confirmUpdateButton").addEventListener("click", function () {
        const formData = new FormData(document.getElementById("updateLogForm"));
        fetch(`/grades/${logIdToUpdate}`, {
            method: "PUT",
            body: formData
        })
        .then(response => {
            if (response.ok) {
                window.location.reload();
            } else {
                alert("Error updating log!");
            }
        })
        .catch(error => console.error("Error:", error));
    });
});
