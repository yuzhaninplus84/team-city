document.addEventListener("DOMContentLoaded", function () {
    let courseIdToDelete = null;

    // Bắt sự kiện mở modal xóa
    const deleteModal = document.getElementById("delete_course");
    deleteModal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget;
        courseIdToDelete = button.getAttribute("data-idcourse"); // Lấy id course
        console.log("Deleting course:", courseIdToDelete);
    });

    // Khi nhấn nút "Delete"
    const confirmDeleteButton = document.getElementById("confirmDeleteButton");
    confirmDeleteButton.addEventListener("click", function () {
        if (courseIdToDelete) {
            fetch(`/course/${courseIdToDelete}`, {
                method: "DELETE"
            })
            .then(response => {
                if (response.ok) {
                    // Xóa thành công → reload trang
                    window.location.reload();
                } else {
                    alert("Error deleting course!");
                }
            })
            .catch(error => console.error("Error:", error));
        }
    });
});
