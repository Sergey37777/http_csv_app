const get_files = document.querySelector("#form button");

get_files.addEventListener("click", getFiles, false);

async function getFiles(event) {
    event.preventDefault();
    const formContainer = document.querySelector(".form-container");
    let url = '/getFiles';
    let response = await fetch(url);
    let files = await response.json();
    console.log(files);
    const form = document.createElement("form");
    form.action = "/get/";
    form.id = "csv-list";
    const select = form.appendChild(document.createElement("select"));
    select.name = "id";
    select.classList.add("form-select");
    for (let i = 0; i < files.length; i++) {
        const option = select.appendChild(document.createElement("option"));
        option.value = `${i}`;
        option.textContent = files[i];
    }
    const btn = document.createElement("button");
    btn.type = "submit";
    btn.textContent = "Получить информацию из файла";
    btn.id = "get-info";
    btn.classList.add("btn");
    btn.classList.add("btn-success");
    const btn_delete = document.createElement("button");
    btn_delete.type = "submit";
    btn_delete.textContent = "Удалить файл с сервера";
    btn_delete.id = "get-info";
    btn_delete.classList.add("btn");
    btn_delete.classList.add("btn-danger");
    form.appendChild(btn);
    form.appendChild(btn_delete);
    formContainer.appendChild(form);
    formContainer.style.display = "flex";
    btn.addEventListener("click", fillTable)
    btn_delete.addEventListener("click", async (e) => {
        e.preventDefault();
        await fetch(form.action + `?id=${select.value}`, {method: "DELETE"});
        await window.location.reload();
    });
    /*
    btn.addEventListener("click", async (event) => {
        event.preventDefault();
        const response = await fetch(form.action + `?id=${select.value}`);
        const csvFile = await response.json();
        console.log(csvFile);
        const result = JSON.parse(csvFile);
        console.log(result);
        if (result["Error"]) {
            return Error("Выбран не CSV файл");
        }
        const table = document.createElement("table");
        table.classList.add("fl-table");
        table.id = "table-csv";
        const thead = document.createElement("thead");
        const tr = document.createElement("tr");
        for (const key in result) {
            const th = document.createElement("th");
            th.textContent = key;
            tr.appendChild(th);
        }
        thead.appendChild(tr)
        table.appendChild(thead);
        let i = 0;
        const tbody = document.createElement("tbody");
        const len = Object.values(result["id"]).length;
        while (i < len-1) {
            const tr = document.createElement("tr")
            for (const key in result) {
                const th = document.createElement("th");
                th.textContent = Object.values(result[key])[i];
                tr.appendChild(th);
            }
            tbody.appendChild(tr);
            i += 1;
        }
        table.appendChild(tbody);
        displayContainer.appendChild(table);
        console.dir(result);
        console.log(result);
    });

     */
}


async function fillTable(event) {
    event.preventDefault();
    const form = document.getElementById("csv-list");
    const select = document.querySelector("#csv-list select");
    const displayContainer = document.querySelector(".csv-container");
    const searchInput = document.createElement("input");
    searchInput.id = "myInput";
    searchInput.addEventListener("keyup", filterRows);
    searchInput.placeholder = "Отфильтровать по значению из первого столбца";
    await fetch(form.action + `?id=${select.value}`).then(res => res.json()).then(csv => {
        const table = document.createElement("table");
        table.id = "table-csv";
        table.classList.add("fl-table");
        table.innerHTML = "";


        table.innerHTML = "";
        for (let row of CSV.parse(String(csv))) {
            let tr = table.insertRow();
            for (let col of row) {
              let td = tr.insertCell();
              td.innerHTML = col;
            }
        }
        displayContainer.appendChild(searchInput);
        displayContainer.appendChild(table);
        sorting();
    });


    /*
    const form = document.getElementById("csv-list");
    const select = document.querySelector("#csv-list select");
    const displayContainer = document.querySelector(".csv-container");
    const inputForFilter = document.createElement("input");
    inputForFilter.id = "search";
    inputForFilter.type = "text";
    inputForFilter.placeholder = "Найти";
    displayContainer.appendChild(inputForFilter);
    event.preventDefault();
    const response = await fetch(form.action + `?id=${select.value}`);
    const csvFile = await response.json();
    console.log(csvFile);
    const result = JSON.parse(csvFile);
    console.log(result);
    if (result["Error"]) {
        return Error("Выбран не CSV файл");
    }
    const table = document.createElement("table");
    table.classList.add("fl-table");
    table.id = "table-csv";
    const thead = document.createElement("thead");
    const tr = document.createElement("tr");
    for (const key in result) {
        const th = document.createElement("th");
        th.textContent = key;
        tr.appendChild(th);
    }
    thead.appendChild(tr)
    table.appendChild(thead);
    let i = 0;
    const tbody = document.createElement("tbody");
    const len = Object.values(result["id"]).length;
    while (i < len-1) {
        const tr = document.createElement("tr")
        for (const key in result) {
            const th = document.createElement("th");
            th.textContent = Object.values(result[key])[i];
            tr.appendChild(th);
        }
        tbody.appendChild(tr);
        i += 1;
    }
    table.appendChild(tbody);
    displayContainer.appendChild(table);
    console.dir(result);
    console.log(result);
     */
}


function filterRows() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("table-csv");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0];
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}


function sorting() {
    const getCellValue = (tr, idx) => tr.children[idx].innerText || tr.children[idx].textContent;
    document.querySelectorAll('tbody tr:first-child td').forEach(tr => {
        tr.style.cursor = "pointer";
    })

    const comparer = (idx, asc) => (a, b) => ((v1, v2) =>
        v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2) ? v1 - v2 : v1.toString().localeCompare(v2)
        )(getCellValue(asc ? a : b, idx), getCellValue(asc ? b : a, idx));

    // do the work...
    document.querySelectorAll('tbody tr:first-child td').forEach(th => th.addEventListener('click', (() => {
        const table = th.closest('table');
        console.log(th);
        Array.from(table.querySelectorAll('tr:nth-child(n+2)'))
            .sort(comparer(Array.from(th.parentNode.children).indexOf(th), this.asc = !this.asc))
            .forEach(tr => table.appendChild(tr) );
    })));
}
