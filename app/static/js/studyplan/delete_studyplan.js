document.addEventListener("DOMContentLoaded", function () {
    let planIdToDelete = null;

    // Bắt sự kiện mở modal xóa
    const deleteModal = document.getElementById("delete_studyplan");
    deleteModal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget;
        planIdToDelete = button.getAttribute("data-idplan"); // Lấy id plan
        console.log("Deleting plan:", planIdToDelete);
    });

    // Khi nhấn nút "Delete"
    const confirmDeleteButton = document.getElementById("confirmDeleteButton");
    confirmDeleteButton.addEventListener("click", function () {
        if (planIdToDelete) {
            fetch(`/study_plan/${planIdToDelete}`, {
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
