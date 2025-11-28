document.getElementById('getInfoBtn').addEventListener('click', () => {
    const planId = document.getElementById('PlanSelect').value;
    if (!planId) {
        alert('Please select a study plan!');
        return;
    }

    fetch(`/course/info/${planId}`)
        .then(response => {
            if (!response.ok) throw new Error('No subjects found');
            return response.json();
        })
        .then(data => {
            document.getElementById('totalHours').textContent = data.credit_of_discipline;
            document.getElementById('examFormat').textContent = data.exam_format;
        })
        .catch(err => {
            console.error(err);
            alert('An error occurred while retrieving subject information.');
            document.getElementById('totalHours').textContent = '-';
            document.getElementById('examFormat').textContent = '-';
        });
});