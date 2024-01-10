var currentMode = 'normal';
let fetchInterval;

let c_hover = "#e9ecef";
let c_nm_selected = "#dee2e6";
let c_unselected = "#ffffff";
let c_io_on = "#00ff00";
let c_io_on_hover = "#88ff00";

/**
 * Initializes the event listers on page load.
 */
document.addEventListener("DOMContentLoaded", function () {
    initRowEventListeners();
    setFetchInterval();
});

function initRowEventListeners() {
    var tableRows = document.querySelectorAll('#table-container tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('click', () => handleRowClick(row));
        row.addEventListener('mouseover', () => handleRowMouseOver(row));
        row.addEventListener('mouseout', () => handleRowMouseOut(row));
    });
}

function handleNormalSearch(event) {
    var searchTerm = event.target.value.toLowerCase();
    var tableRows = document.querySelectorAll('#table-container tbody tr');
    tableRows.forEach(function (row) {
        var text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchTerm) ? '' : 'none';
    });
}

/**
 * Fetches a barcode from the server and handles the response based on the current mode.
 */
function fetchBarcode() {
    fetch('/get_barcode')
        .then(response => response.json())
        .then(data => {
            if (data.barcode != "error") {
                document.getElementById('searchBar').value = data.barcode;

                switch (currentMode) {
                    case 'normal':
                        handleFetchBarcodeNormalMode(data.barcode);
                        break;
                    case 'scan':
                        handleFetchBarcodeScanMode(data.barcode);
                        break;
                    case 'io':
                        handleFetchBarcodeIOMode(data.barcode);
                        break;
                    case 'delete':
                        handleFetchBarcodeDeleteMode(data.barcode);
                        break;
                }
            }
        })
        .catch(error => console.error('Error:', error));
}

function handleFetchBarcodeNormalMode(barcode) {
    var searchTerm = barcode.toLowerCase();
    var tableRows = document.querySelectorAll('#table-container tbody tr');
    tableRows.forEach(function (row) {
        var idText = row.cells[0].textContent.toLowerCase();
        row.style.display = idText.includes(searchTerm) ? '' : 'none';
    });
}

function handleFetchBarcodeScanMode(barcode) {
    const url = "/detail?id=" + encodeURIComponent(barcode);
    const newTab = window.open(url, '_blank');
}

function handleFetchBarcodeIOMode(barcode) {
    var searchTerm = barcode.toLowerCase();
    var tableRows = document.querySelectorAll('#table-container tbody tr');
    tableRows.forEach(function (row) {
        var idText = row.cells[0].textContent.toLowerCase();
        if (idText.includes(searchTerm)) {
            toggleIoState(row);
        }
    });
}

function handleFetchBarcodeDeleteMode(barcode) {
    var searchTerm = barcode.toLowerCase();
    var tableRows = document.querySelectorAll('#table-container tbody tr');
    tableRows.forEach(function (row) {
        var idText = row.cells[0].textContent.toLowerCase();
        var nameText = row.cells[3].textContent.toLowerCase();
        if (idText.includes(searchTerm)) {
            confirmDeletionWithSweetAlert(idText, nameText)
        }
    });
}

function confirmDeletionWithSweetAlert(id, name) {
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

function deleteComponent(id) {
    var form = document.createElement('form');
    let url = delete_url.replace("0", id);
    form.method = 'POST';
    form.action = url;
    document.body.appendChild(form);
    form.submit();
}

function setFetchInterval() {
    clearInterval(fetchInterval);
    fetchInterval = setInterval(fetchBarcode, 3000);
}

document.getElementById('modeSelector').addEventListener('change', function (event) {
    var selectedMode = event.target.value;

    switch (selectedMode) {
        case 'normal':
            currentMode = 'normal';
            UpdateIOComponentsHighlight();
            break;
        case 'scan':
            currentMode = 'scan';
            UpdateIOComponentsHighlight();
            break;
        case 'io':
            currentMode = 'io';
            UpdateIOComponentsHighlight();
            break;
        case 'delete':
            currentMode = 'delete';
            UpdateIOComponentsHighlight();
            break;
    }
});

function UpdateIOComponentsHighlight() {
    var tableRows = document.querySelectorAll('#table-container tbody tr');
    tableRows.forEach(row => {
        var ioState = row.cells[1].textContent.trim();
        switch (currentMode) {
            case 'io':
                if (ioState === "True") {
                    row.style.backgroundColor = c_io_on;
                } else if (ioState === "False") {
                    row.style.backgroundColor = c_unselected;
                }
                break;
            default:
                row.style.backgroundColor = c_unselected;
                break;
        }
    });
}

function sendIoState(itemId) {
    fetch('/update_io_state', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id: itemId })
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

var selectedRow = null;
function handleRowClick(row) {
    if (currentMode === 'normal') {
        if (selectedRow === row) {
            const itemId = row.cells[0].textContent;
            if (currentMode === "normal") {
                window.location.href = "/detail?id=" + encodeURIComponent(itemId);
            }
        } else {
            if (selectedRow) {
                selectedRow.classList.remove('selected');
            }
            row.classList.add('selected');
            selectedRow = row;
        }
    } else if (currentMode === 'io') {
        toggleIoState(row);
    } else if (currentMode === 'delete') {
        var id = row.cells[0].textContent;
        var name = row.cells[3].textContent;
        confirmDeletionWithSweetAlert(id, name);
    }
}

function toggleIoState(row) {
    var ioStateCell = row.cells[1];
    var itemId = row.cells[0].textContent;
    var ioState = ioStateCell.textContent.trim();

    if (ioState === "True") {
        ioStateCell.textContent = "False";
    } else {
        ioStateCell.textContent = "True";
    }
    UpdateIOComponentsHighlight();
    sendIoState(itemId);
}

function handleRowMouseOver(row) {
    if (currentMode === 'normal') {
        row.style.backgroundColor = c_hover;
    } else if (currentMode === 'delete') {
        row.style.backgroundColor = c_hover;
    }
}

function handleRowMouseOut(row) {
    if (currentMode === 'normal') {
        if (row === selectedRow) {
            row.style.backgroundColor = c_nm_selected;
        } else {
            row.style.backgroundColor = c_unselected;
        }
    } else if (currentMode === 'delete') {
        row.style.backgroundColor = c_unselected;
    }
}

window.addEventListener("pageshow", function (event) {
    var historyTraversal = event.persisted ||
        (typeof window.performance != "undefined" &&
            window.performance.navigation.type === 2);
    if (historyTraversal) {
        window.location.reload();
    }
});