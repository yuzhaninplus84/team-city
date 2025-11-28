document.addEventListener("DOMContentLoaded", function () {
    const viewModal = document.getElementById("view_course");

    viewModal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget;
        const courseId = button.getAttribute("data-idcourse");
        console.log(courseId);
        const modalBody = viewModal.querySelector(".modal-body");
        modalBody.innerHTML = "<p>Loading...</p>";

        // Gọi API Flask để lấy dữ liệu khóa học
        fetch(`/course/${courseId}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    modalBody.innerHTML = `<p class="text-danger">${data.error}</p>`;
                } else {
                    modalBody.innerHTML = `
                        <ul class="list-group">
                            <li class="list-group-item"><b>ID:</b> ${data.id_course}</li>
                            <li class="list-group-item"><b>Name:</b> ${data.name_course}</li>
                            <li class="list-group-item"><b>Credit Hours:</b> ${data.total_hours}</li>
                            <li class="list-group-item"><b>Number of Years:</b> ${data.number_year}</li>
                            <li class="list-group-item"><b>Description:</b> ${data.description}</li>
                        </ul>
                    `;
                }
            })
            .catch(error => {
                modalBody.innerHTML = `<p class="text-danger">Error: ${error}</p>`;
            });
    });
});
