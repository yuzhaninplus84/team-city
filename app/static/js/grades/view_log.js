document.addEventListener("DOMContentLoaded", function () {
    const viewModal = document.getElementById("view_log");
    console.log(viewModal);
    viewModal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget;
        const logId = button.getAttribute("data-idlog");
        console.log(logId);
        const modalBody = viewModal.querySelector(".modal-body");
        modalBody.innerHTML = "<p>Loading...</p>";
        console.log(logId);
        // Gọi API Flask để lấy dữ liệu kế hoạch học tập
fetch(`/grades/${logId}`)
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            modalBody.innerHTML = `<p class="text-danger">${data.error}</p>`;
        } else {
            modalBody.innerHTML = `
                <ul class="list-group">
                    <li class="list-group-item"><b>Id Progress Log:</b> ${data.id_log}</li>
                    <li class="list-group-item"><b>Semester:</b> ${data.semester}</li>
                    <li class="list-group-item"><b>Student ID:</b> ${data.student_id}</li>
                    <li class="list-group-item"><b>Course ID:</b> ${data.course_id}</li>
                    <li class="list-group-item"><b>Grade:</b> ${data.grade}</li>
                </ul>
            `;
        }
    })
            .catch(error => {
                modalBody.innerHTML = `<p class="text-danger">Error: ${error}</p>`;
            });
    });
});