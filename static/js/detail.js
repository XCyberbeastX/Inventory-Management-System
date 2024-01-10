function PrintBarcode() {
    var printWindow = window.open('', '', 'height=400,width=800');
    printWindow.document.write('<html><body >');
    printWindow.document.write('<img src="'+ barcode + '" />');
    printWindow.document.write('</body></html>');
    printWindow.document.close();
    printWindow.focus();
    printWindow.onload = function () {
        printWindow.print();
        printWindow.close();
    };
}

function convertBrToNewline() {
    var descriptionTextarea = document.querySelector('#edit-mode textarea[name="description"]');
    if (descriptionTextarea) {
        descriptionTextarea.value = descriptionTextarea.value.replace(/<br\s*\/?>/gi, '\n');
    }
}

function convertNewlineToBr(event) {
    var descriptionTextarea = document.querySelector('#edit-mode textarea[name="description"]');
    if (descriptionTextarea) {
        descriptionTextarea.value = descriptionTextarea.value.replace(/\n/gi, '<br>');
    }
}

var editModeButton = document.querySelector('.toggle-btn');
if (editModeButton) {
    editModeButton.addEventListener('click', convertBrToNewline);
}

var editForm = document.querySelector('#edit-mode form');
if (editForm) {
    editForm.addEventListener('submit', convertNewlineToBr);
}

function confirmDeletionWithSweetAlert() {
    Swal.fire({
        title: 'Are you sure?',
        text: "Do you really want to delete " + name + "?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete!',
        cancelButtonText: 'No, cancel'
    }).then((result) => {
        if (result.isConfirmed) {
            deleteComponent(id);
        }
    });
}

function deleteComponent() {
    var form = document.createElement('form');
    form.method = 'POST';
    form.action = delete_url;
    document.body.appendChild(form);
    form.submit();
}

function sendIoState() {
    fetch('/update_io_state', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id: id })
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

document.getElementById('io-state-checkbox').addEventListener('change', sendIoState);