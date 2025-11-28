document.addEventListener("DOMContentLoaded", function () {
    let logIdToDelete = null;

    // Bắt sự kiện mở modal xóa
    const deleteModal = document.getElementById("delete_log");
    deleteModal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget;
        logIdToDelete = button.getAttribute("data-idlog"); // Lấy id log
        console.log("Deleting log:", logIdToDelete);
    });

    // Khi nhấn nút "Delete"
    const confirmDeleteButton = document.getElementById("confirmDeleteButton");
    confirmDeleteButton.addEventListener("click", function () {
        if (logIdToDelete) {
            fetch(`/grades/${logIdToDelete}`, {
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
