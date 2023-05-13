/*=============== SHOW MODAL ===============*/
// const showModal = (openButton, modalContent) => {
//     const openBtn = document.getElementById(openButton),
//         modalContainer = document.getElementById(modalContent)

//     if (openBtn && modalContainer) {
//         openBtn.addEventListener('click', () => {
//             modalContainer.classList.add('show-modal')
//         })
//     }
// }

function ShowModal(modalContent) {
    modalContainer = document.getElementById(modalContent)
    modalContainer.classList.add('show-modal')
    document.querySelector("body").style.overflow = 'hidden';
}

// showModal('open-modal', 'modal-container')

/*=============== CLOSE MODAL ===============*/

function closeModal(modalContent) {
    modalContainer = document.getElementById(modalContent)
    modalContainer.classList.remove('show-modal')
    document.querySelector("body").style.overflow = 'visible';
}

function stopevent(event) {
    event.stopPropagation();
}
// closeBtn.forEach(c => c.addEventListener('click', closeModal))

var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }
    return false;
};

function titleCase(str) {
    let strLowerCase = str.toLowerCase();
    let wordArr = strLowerCase.split(" ").map(function(currentValue) {
        return currentValue[0].toUpperCase() + currentValue.substring(1);
    });

    return wordArr.join(" ");
}

function grade(total) {
    if (total <= 100 && total >= 90)
        return [10, "Outstanding"]
    else if (total >= 75)
        return [9, "A+"]
    else if (total >= 65)
        return [8, "A"]
    else if (total >= 55)
        return [7, "B+"]
    else if (total >= 50)
        return [6, "B"]
    else if (total >= 45)
        return [5, "C"]
    else if (total >= 40)
        return [4, "P"]
    else
        return [0, "F"]
}

var serializeForm = function(form) {
    var obj = {};
    var formData = new FormData(form);
    for (var key of formData.keys()) {
        obj[key] = formData.get(key);
    }
    return obj;
};


// download table data in csv
function download_csv(csv, filename) {
    var csvFile;
    var downloadLink;

    // CSV FILE
    csvFile = new Blob([csv], { type: "text/csv" });

    // Download link
    downloadLink = document.createElement("a");

    // File name
    downloadLink.download = filename;

    // We have to create a link to the file
    downloadLink.href = window.URL.createObjectURL(csvFile);

    // Make sure that the link is not displayed
    downloadLink.style.display = "none";

    // Add the link to your DOM
    document.body.appendChild(downloadLink);

    // Lanzamos
    downloadLink.click();
}

function export_table_to_csv(html, filename) {
    var csv = [];
    var rows = document.querySelectorAll("table tr");

    for (var i = 0; i < rows.length; i++) {
        var row = [],
            cols = rows[i].querySelectorAll("td, th");

        for (var j = 0; j < cols.length; j++)
            row.push('"' + cols[j].innerText + '"');

        csv.push(row.join(","));
    }

    // Download CSV
    download_csv(csv.join("\n"), filename);
}