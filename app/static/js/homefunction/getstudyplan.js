document.addEventListener('DOMContentLoaded', () => {
    const courseSelect = document.getElementById('courseSelect');
    const tbody = document.getElementById('studyPlanTableBody');

    courseSelect.addEventListener('change', () => {
        const courseId = courseSelect.value;
        tbody.innerHTML = ""; // clear table trước

        if (!courseId) return;

        fetch(`/get_study_plans/${courseId}`)
            .then(res => res.json())
            .then(response => {
                if (response.success) {
                    response.plans.forEach(plan => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${plan.id_plan}</td>
                            <td>${plan.discipline}</td>
                            <td>${plan.semester}</td>
                            <td>${plan.credit_of_discipline}</td>
                            <td>${plan.exam_format}</td>
                        `;
                        tbody.appendChild(row);
                    });
                } else {
                    alert("Error: " + response.message);
                }
            })
            .catch(err => {
                console.error(err);
                alert("Unable to load course data!");
            });
    });
});
