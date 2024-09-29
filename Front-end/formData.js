// formData.js

document.querySelector('.schedule-options').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent default form submission
    
    const formData = new FormData();
    formData.append('schedule', document.getElementById('pdfUpload').files[0]);
    formData.append('sleepSchedule', document.getElementById('sleepSchedule').value);
    formData.append('workSchedule', document.getElementById('workSchedule').value);
    formData.append('exercise', document.getElementById('exercise').value);
    formData.append('studyTime', document.getElementById('studyTime').value);
    formData.append('miscellaneous', document.getElementById('miscellaneous').value);

    fetch('/schedule', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
      .then(data => {
          console.log(data.generated_schedule);
          displaySchedule(data.generated_schedule); // Call function to display the schedule
      })
      .catch(error => console.error('Error:', error));
});

// Function to display the generated schedule
function displaySchedule(schedule) {
    const scheduleContainer = document.getElementById('generatedSchedule'); // Ensure this ID exists in your HTML
    scheduleContainer.innerHTML = ''; // Clear previous schedule if any
    scheduleContainer.innerHTML = `<h3>Generated Schedule:</h3><pre>${schedule}</pre>`; // Display the schedule
}
