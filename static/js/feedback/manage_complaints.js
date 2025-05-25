// Ensure allComplaintsData is defined in a <script> tag in the HTML before this script is loaded.
// For example: <script>const allComplaintsData = {{ complaints_list|tojson|safe }};</script>

function showDetailsModal(complaintId) {
    if (typeof allComplaintsData === 'undefined') {
        console.error('allComplaintsData is not defined. Make sure it is set in the HTML template.');
        return;
    }

    const complaint = allComplaintsData.find(c => c.complaint_id === complaintId);

    if (!complaint) {
        console.error('Complaint not found for ID:', complaintId);
        return;
    }

    document.getElementById('modal-complaint-id').textContent = complaint.complaint_id;
    document.getElementById('modal-type').textContent = complaint.type;
    document.getElementById('modal-sender').textContent = complaint.sender;
    document.getElementById('modal-receiver').textContent = complaint.receiver || '管理员';
    document.getElementById('modal-time').textContent = complaint.time || 'N/A';
    document.getElementById('modal-current-status').textContent = complaint.status;
    document.getElementById('modal-handler').textContent = complaint.handler_username || 'N/A';
    document.getElementById('modal-last-updated').textContent = complaint.last_updated_time || 'N/A';
    document.getElementById('modal-content').textContent = complaint.content;
    document.getElementById('modal-status-select').value = complaint.status;
    
    const form = document.getElementById('update-status-form');
    if (form) { // Ensure form exists
        form.action = `/feedback/update_complaint_status/${complaint.complaint_id}`;
    } else {
        console.error('Form with ID "update-status-form" not found.');
    }

    const modal = document.getElementById('complaint-details-modal');
    if (modal) { // Ensure modal exists
        modal.style.display = 'block';
        document.getElementById('complaint-details-modal').classList.add('show');
    } else {
        console.error('Modal with ID "complaint-details-modal" not found.');
    }
}

function closeDetailsModal() {
    const modal = document.getElementById('complaint-details-modal');
    if (modal) {
        modal.style.display = 'none';
        document.getElementById('complaint-details-modal').classList.remove('show');
    }
}

// Event listener for closing the modal when clicking outside of it
window.addEventListener('click', function(event) {
    const modal = document.getElementById('complaint-details-modal');
    if (modal && event.target == modal) {
        closeDetailsModal();
    }
});

// Optional: Add event listener for ESC key to close modal
window.addEventListener('keydown', function(event) {
    const modal = document.getElementById('complaint-details-modal');
    if (modal && modal.style.display === 'block' && event.key === 'Escape') {
        closeDetailsModal();
    }
});