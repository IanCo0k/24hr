document.addEventListener('DOMContentLoaded', async function() {
    const timeSlotSelect = document.getElementById('timeSlot');
    const tableBody = document.getElementById('timeSlotsTable').getElementsByTagName('tbody')[0];

    // Function to render HTML elements for time slots
    function renderTimeSlots() {
        for (let hour = 0; hour < 24; hour++) {
            const time = new Date(2023, 2, 14, 21 + hour, 0); // Adjust the date and month accordingly
            const timeString = time.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true });
            const day = time.getDate() === 14 ? 'March 14' : 'March 15';
            const formattedTimeSlot = `${day} - ${timeString}`;

            // Add option to select dropdown
            const option = document.createElement('option');
            option.value = option.textContent = formattedTimeSlot;
            timeSlotSelect.appendChild(option);
        }
    }

    // Function to fetch signups from the server and render HTML elements
    async function fetchSignupsAndRender() {
        try {
            const response = await fetch('https://chefc0ok.pythonanywhere.com/signups');
            if (!response.ok) {
                throw new Error('Failed to fetch signups');
            }
            const data = await response.json();
            // Clear existing table
            tableBody.innerHTML = '';
            // Render time slots and signups data
            renderTimeSlots();
            data.time_slots.forEach(slot => {
                const row = tableBody.insertRow();
                row.innerHTML = `<td>${slot.time}</td><td class="name-cell">${slot.signups.map(signup => signup.name).join('<br>')}</td><td class="group-cell">${slot.signups.map(signup => signup.group).join('<br>')}</td>`;
            });
        } catch (error) {
            console.error(error);
        }
    }

    // Render time slots initially and fetch signups
    renderTimeSlots();
    await fetchSignupsAndRender();

    // Function to handle form submission
    function handleFormSubmission(event) {
        event.preventDefault(); // Prevent form from submitting traditionally

        const name = document.getElementById('name').value.trim();
        const group = document.getElementById('group').value.trim();
        const timeSlot = document.getElementById('timeSlot').value;

        // Send signup data to the Flask API
        fetch('https://chefc0ok.pythonanywhere.com/sign-up', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ timeSlot, name, group })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(error => Promise.reject(error));
            }
            return response.json();
        })
        .then(data => {
            // Signup successful, fetch signups again and update UI
            fetchSignupsAndRender();
        })
        .catch(error => {
            // Signup failed, handle error
            console.error(error);
        });

        // Reset form fields
        this.reset();
    }

    // Add event listener to form submission
    document.getElementById('signupForm').addEventListener('submit', handleFormSubmission);
});
