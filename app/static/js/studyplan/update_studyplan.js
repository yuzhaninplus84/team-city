document.addEventListener("DOMContentLoaded", function () {
    let studyplanIdToUpdate = null;

    // Khi mở modal Update
    const updateModal = document.getElementById("update_studyplan");
    updateModal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget;
        studyplanIdToUpdate = button.getAttribute("data-idplan");
        console.log(studyplanIdToUpdate)
        // Lấy thông tin sinh viên từ server
        fetch(`/study_plan/${studyplanIdToUpdate}`)
            .then(response => response.json())
            .then(data => {
                // Đổ dữ liệu vào form
                document.getElementById("update_id_plan").value = data.id_plan;
                document.getElementById("update_id_course").value = data.id_course;
                document.getElementById("update_discipline").value = data.discipline;
                document.getElementById("update_semester").value = data.semester;
                document.getElementById("update_credit_of_discipline").value = data.credit_of_discipline;
                document.getElementById("update_exam_format").value = data.exam_format;
            });
    });

    // Khi nhấn nút "Update"
    document.getElementById("confirmUpdateButton").addEventListener("click", function () {
        const formData = new FormData(document.getElementById("updateStudyplanForm"));
        fetch(`/study_plan/${studyplanIdToUpdate}`, {
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
