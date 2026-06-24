// Fetch company types and fill the dropdown
let companyTypes = {};

fetch("/company_type/")
  .then((response) => response.json())
  .then((data) => {
    const select = document.querySelector("#company_type");
    data.forEach((type) => {
      companyTypes[type.id] = type.name; // store id → name
      const option = document.createElement("option");
      option.value = type.id;
      option.text = type.name;
      select.appendChild(option);
    });
  });

// Fetch companies and fill the table
fetch("/Company/")
  .then((response) => response.json())
  .then((data) => {
    const tbody = document.querySelector("tbody");
    tbody.innerHTML = "";
    data.forEach((company) => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${company.id}</td>
        <td>${company.name}</td>
        <td>${company.email}</td>
        <td>${company.phone}</td>
        <td>${company.address}</td>
        <td>${companyTypes[company.company_Type] || company.company_Type}</td>
      `;
      tbody.appendChild(row);
    });
  });
document.querySelector("button").addEventListener("click", function () {
  const formData = new FormData();
  formData.append("name", document.querySelectorAll("input")[0].value);
  formData.append("email", document.querySelectorAll("input")[1].value);
  formData.append("phone", document.querySelectorAll("input")[2].value);
  formData.append("pan_no", document.querySelectorAll("input")[3].value);
  formData.append("address", document.querySelectorAll("input")[4].value);
  formData.append("established", document.querySelectorAll("input")[5].value);
  formData.append("company_Type", document.querySelector("select").value);
  formData.append("image", document.querySelectorAll("input")[6].files[0]);

  fetch("/Company/", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      alert("Company added!");
    });
});

document.querySelector("#submitBtn").addEventListener("click", function () {
  const formData = new FormData();
  formData.append("name", document.querySelector("#name").value);
  formData.append("email", document.querySelector("#email").value);
  formData.append("phone", document.querySelector("#phone").value);
  formData.append("pan_no", document.querySelector("#pan_no").value);
  formData.append("address", document.querySelector("#address").value);
  formData.append("established", document.querySelector("#established").value);
  formData.append(
    "company_Type",
    document.querySelector("#company_type").value,
  );

  const imageFile = document.querySelector("#image").files[0];
  if (imageFile) {
    formData.append("image", imageFile);
  }

  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

  fetch("/Company/", {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      alert("Company added successfully!");
    })
    .catch((error) => {
      alert("Something went wrong!");
    });
});
