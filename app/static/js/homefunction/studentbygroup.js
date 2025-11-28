document.getElementById('getGroupBtn').addEventListener('click', () => {
    const groupNumber = document.getElementById('groupInput').value.trim();
    if (!groupNumber) {
        alert('Please enter group/class number!');
        return;
    }

    fetch(`/students/group/${groupNumber}`)
        .then(response => {
            if (!response.ok) throw new Error('Group/class not found');
            return response.json();
        })
        .then(data => {
            const tbody = document.getElementById('studentTableBody');
            tbody.innerHTML = '';

            if (data.length === 0) {
                tbody.innerHTML = '<tr><td colspan="4">There are no students in this group.</td></tr>';
                return;
            }

            data.forEach(student => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${student.id_student}</td>
                    <td>${student.full_name}</td>
                    <td>${student.group_number}</td>
                    <td>${student.form_of_study}</td>
                `;
                tbody.appendChild(row);
            });
        })
        .catch(err => {
            console.error(err);
            alert('An error occurred while retrieving data.');
        });
});