document.getElementById('countBtn').addEventListener('click', () => {
    const formOfStudy = document.getElementById('formSelect').value;
    if (!formOfStudy) {
        alert('Please select training type!');
        return;
    }

    fetch(`/students/count/${formOfStudy}`)
        .then(response => {
            if (!response.ok) throw new Error('Error calling API');
            return response.json();
        })
        .then(data => {
            const resultEl = document.getElementById('result');
            resultEl.textContent = `Number of students in the form "${data.form_of_study}": ${data.count}`;
        })
        .catch(err => {
            console.error(err);
            alert('An error occurred while retrieving data.');
        });
});