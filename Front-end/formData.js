document.querySelector('.schedule-options').addEventListener('submit', function(event) {
    event.preventDefault();  

    const formData = new FormData();
    formData.append('schedule', document.getElementById('pdfUpload').files[0]);
    formData.append('sleepSchedule', document.getElementById('sleepSchedule').value);
    formData.append('workSchedule', document.getElementById('workSchedule').value);
    formData.append('exercise', document.getElementById('exercise').value);
    formData.append('studyTime', document.getElementById('studyTime').value);
    formData.append('miscellaneous', document.getElementById('miscellaneous').value);

    fetch('http://127.0.0.1:5000', { 
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        displaySchedule(data.generated_schedule);  
    })
    .catch(error => console.error('Error:', error));
});

function displaySchedule(schedule) {
    const generatedSection = document.getElementById('generated-schedule');
    generatedSection.innerHTML = '';  
    const daysOfWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
    const scheduleLines = schedule.split("\n");
    
    daysOfWeek.forEach(day => {
        const dayHeader = document.createElement('h3');
        dayHeader.innerText = day;
        generatedSection.appendChild(dayHeader);

        const dayContent = document.createElement('p');
        dayContent.innerText = scheduleLines.filter(line => line.includes(day)).join("\n");
        generatedSection.appendChild(dayContent);
    });
}
