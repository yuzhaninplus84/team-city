document.getElementById('getGradesBtn').addEventListener('click', () => {
    const studentId = document.getElementById('studentIdInput').value.trim();
    const semester = document.getElementById('semesterInput').value.trim();

    if (!studentId) {
        alert('Please enter student ID!');
        return;
    }

    let url = `/grades/student/${studentId}`;
    if (semester) {
        url += `?semester=${semester}`;
    }

    fetch(url)
        .then(response => {
            if (!response.ok) throw new Error('No data found');
            return response.json();
        })
        .then(data => {
            const tbody = document.getElementById('gradesTableBody');
            tbody.innerHTML = '';

            if (data.length === 0) {
                tbody.innerHTML = '<tr><td colspan="4">No points</td></tr>';
                return;
            }

            data.forEach(log => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${log.id_log}</td>
                    <td>${log.semester}</td>
                    <td>${log.course_id}</td>
                    <td>${log.grade}</td>
                `;
                tbody.appendChild(row);
            });
        })
        .catch(err => {
            console.error(err);
            alert('An error occurred while retrieving data.');
        });
});