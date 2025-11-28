document.addEventListener("DOMContentLoaded", function () {
    const viewModal = document.getElementById("view_studyplan");
    console.log(viewModal);
    viewModal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget;
        const studyPlanId = button.getAttribute("data-idplan");
        console.log(studyPlanId);
        const modalBody = viewModal.querySelector(".modal-body");
        modalBody.innerHTML = "<p>Loading...</p>";
        console.log(studyPlanId);
        // Gọi API Flask để lấy dữ liệu kế hoạch học tập
fetch(`/study_plan/${studyPlanId}`)
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            modalBody.innerHTML = `<p class="text-danger">${data.error}</p>`;
        } else {
            modalBody.innerHTML = `
                <ul class="list-group">
                    <li class="list-group-item"><b>ID:</b> ${data.id_plan}</li>
                    <li class="list-group-item"><b>ID course:</b> ${data.id_course}</li>
                    <li class="list-group-item"><b>Credit Hours:</b> ${data.discipline}</li>
                    <li class="list-group-item"><b>Number of Years:</b> ${data.semester}</li>
                    <li class="list-group-item"><b>Description:</b> ${data.credit_of_discipline}</li>
                    <li class="list-group-item"><b>Description:</b> ${data.exam_format}</li>
                </ul>
            `;
        }
    })
            .catch(error => {
                modalBody.innerHTML = `<p class="text-danger">Error: ${error}</p>`;
            });
    });
});

