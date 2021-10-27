const html = document.documentElement;
const body = document.body;
const menuLinks = document.querySelectorAll(".admin-menu a");
const collapseBtn = document.querySelector(".admin-menu .collapse-btn");
const toggleMobileMenu = document.querySelector(".toggle-mob-menu");
const switchInput = document.querySelector(".switch input");
const switchLabel = document.querySelector(".switch label");
const switchLabelText = switchLabel.querySelector("span:last-child");
const collapsedClass = "collapsed";
const lightModeClass = "light-mode";

/*TOGGLE HEADER STATE*/
collapseBtn.addEventListener("click", function () {
  body.classList.toggle(collapsedClass);
  this.getAttribute("aria-expanded") == "true"
    ? this.setAttribute("aria-expanded", "false")
    : this.setAttribute("aria-expanded", "true");
  this.getAttribute("aria-label") == "collapse menu"
    ? this.setAttribute("aria-label", "expand menu")
    : this.setAttribute("aria-label", "collapse menu");
});

/*TOGGLE MOBILE MENU*/
toggleMobileMenu.addEventListener("click", function () {
  body.classList.toggle("mob-menu-opened");
  this.getAttribute("aria-expanded") == "true"
    ? this.setAttribute("aria-expanded", "false")
    : this.setAttribute("aria-expanded", "true");
  this.getAttribute("aria-label") == "open menu"
    ? this.setAttribute("aria-label", "close menu")
    : this.setAttribute("aria-label", "open menu");
});

/*SHOW TOOLTIP ON MENU LINK HOVER*/
for (const link of menuLinks) {
  link.addEventListener("mouseenter", function () {
    if (
      body.classList.contains(collapsedClass) &&
      window.matchMedia("(min-width: 768px)").matches
    ) {
      const tooltip = this.querySelector("span").textContent;
      this.setAttribute("title", tooltip);
    } else {
      this.removeAttribute("title");
    }
  });
}

/*TOGGLE LIGHT/DARK MODE*/
if (localStorage.getItem("dark-mode") === "false") {
  html.classList.add(lightModeClass);
  switchInput.checked = false;
  switchLabelText.textContent = "Light";
}

switchInput.addEventListener("input", function () {
  html.classList.toggle(lightModeClass);
  if (html.classList.contains(lightModeClass)) {
    switchLabelText.textContent = "Light";
    localStorage.setItem("dark-mode", "false");
  } else {
    switchLabelText.textContent = "Dark";
    localStorage.setItem("dark-mode", "true");
  }
});

//js for switching between tabs

let currentActive = document.getElementById("attendanceTab");

function switchToCollection() {
  currentActive.style.display = "none";
  document.getElementById("collectionTab").style.display = "flex";
  currentActive = document.getElementById("collectionTab");
}

function switchToAttendance() {
  currentActive.style.display = "none";
  document.getElementById("attendanceTab").style.display = "flex";
  currentActive = document.getElementById("attendanceTab");
}

let kuch;
async function getAttendence(date) {
  if (new Date(date) <= new Date()) {
    let token = JSON.parse(document.getElementById("mydata").textContent);
    let data = await fetch(
      `/getattendence/${token}/?date=${date}&subjectid=${
        document.getElementById("subjectid").value
      }`
    );
    data = await data.json();
    console.log("hi", data.analysis);
    kuch = data.analysis;

    let gridParent = document.getElementById("restOfTheDiv");
    while (gridParent.childElementCount - 1 != 0) {
      gridParent.removeChild(gridParent.lastChild);
    }

    for (let i = 0; i < data.analysis.Name.length; i++) {
      let newDiv = document.createElement("div");
      newDiv.className = "grid-column";

      let forId = document.createElement("div");
      forId.textContent = data.analysis["Student Id"][i];
      newDiv.appendChild(forId);

      let forName = document.createElement("div");
      forName.textContent = data.analysis["Name"][i];
      newDiv.appendChild(forName);

      let forPresent = document.createElement("div");
      forPresent.textContent = data.analysis["Present"][i];
      newDiv.appendChild(forPresent);

      let forAbsent = document.createElement("div");
      forAbsent.textContent = data.analysis["Absent"][i];
      newDiv.appendChild(forAbsent);

      let forPercentage = document.createElement("div");
      let percentage = `${
        (data.analysis["Present"][i] * 100) /
        (data.analysis["Present"][i] + data.analysis["Absent"][i])
      }`;
      forPercentage.textContent = parseInt(percentage) + "%";
      newDiv.appendChild(forPercentage);
      if (parseFloat(percentage) >= 75) {
        newDiv.style.color = "green";
      } else {
        newDiv.style.color = "red";
      }
      // newDiv.addEventListener('hover', () => {
      //   newDiv.style.
      // })
      gridParent.append(newDiv);
    }

    data = data.data;

    if (data.total !== undefined) {
      document.getElementById("totalStudents").innerHTML = data.total;
      document.getElementById("totalPresentStudents").innerHTML =
        data.presentstudent;
      document.getElementById("totalAbsentStudents").innerHTML =
        data.absentstudent;
      document.getElementById(
        "file_link"
      ).innerHTML = `<a href="/collegemanagement/iiitbhopal/static/userUploadedFiles/attendenceFiles/${data.filename}" download="true">Download Per Day</a><br><a href="/collegemanagement/iiitbhopal/static/userUploadedFiles/attendenceFiles/analysis${data.filename}" download="true">Download Analysis File</a>`;
    } else {
      document.getElementById("totalStudents").innerHTML = "";
      document.getElementById("totalPresentStudents").innerHTML = "";
      document.getElementById("totalAbsentStudents").innerHTML = "";
    }
  } else {
    alert("Invalid date");
  }
}
async function getSubjectid() {
  let token = JSON.parse(document.getElementById("mydata").textContent);
  let data = await fetch(`/getsubjectid/${token}/`);
  data = await data.json();
  data = data.data;
  console.log(data);
  let a = "";
  for (let i = 0; i < data.length; i++) {
    item = data[i];
    a += `<option value=${item.subjectid}>${item.name}/${item.subjectid}</option>`;
  }
  document.getElementById("subjectid").innerHTML = a;
}
getSubjectid();
