document.addEventListener("DOMContentLoaded", function () {
    let studentIdToDelete = null;

    // Bắt sự kiện mở modal xóa
    const deleteModal = document.getElementById("delete_student");
    deleteModal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget;
        studentIdToDelete = button.getAttribute("data-idstudent"); // Lấy id student
        console.log("Deleting student:", studentIdToDelete);
    });

    // Khi nhấn nút "Delete"
    const confirmDeleteButton = document.getElementById("confirmDeleteButton");
    confirmDeleteButton.addEventListener("click", function () {
        if (studentIdToDelete) {
            fetch(`/student/${studentIdToDelete}`, {
                method: "DELETE"
            })
            .then(response => {
                if (response.ok) {
                    // Xóa thành công → reload trang
                    window.location.reload();
                } else {
                    alert("Error deleting student!");
                }
            })
            .catch(error => console.error("Error:", error));
        }
    });
});
