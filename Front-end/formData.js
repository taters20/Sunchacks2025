// formData.js


document.querySelector('.schedule-options').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent default form submission
    
    // Capture input values
    const pdfFile = document.getElementById('pdfUpload').files[0];
    const sleepSchedule = document.getElementById('sleepSchedule').value;
    const workSchedule = document.getElementById('workSchedule').value;
    const exercise = document.getElementById('exercise').value;
    const studyTime = document.getElementById('studyTime').value;
    const miscellaneous = document.getElementById('miscellaneous').value;
    
    // Log values to the console for debugging
    console.log("User Input:");
    console.log("PDF File:", pdfFile);
    console.log("Sleep Schedule:", sleepSchedule);
    console.log("Work Schedule:", workSchedule);
    console.log("Exercise:", exercise);
    console.log("Study Time:", studyTime);
    console.log("Miscellaneous:", miscellaneous);

    // FormData for submission
    const formData = new FormData();
    formData.append('schedule', pdfFile);
    formData.append('sleepSchedule', sleepSchedule);
    formData.append('workSchedule', workSchedule);
    formData.append('exercise', exercise);
    formData.append('studyTime', studyTime);
    formData.append('miscellaneous', miscellaneous);

    // Fetch request to the backend
    fetch('http://127.0.0.1:5000/schedule', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
      .then(data => {
          console.log(data.generated_schedule);  // Log generated schedule
          displaySchedule(data.generated_schedule); // Display the schedule on the page
      })
      .catch(error => console.error('Error:', error));
});

// Function to display the generated schedule
function displaySchedule(schedule) {
    const generatedScheduleDiv = document.getElementById('generatedSchedule');
    generatedScheduleDiv.innerHTML = `<h3>Generated Schedule:</h3><p>${schedule}</p>`;
}
