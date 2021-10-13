const html = document.documentElement
const body = document.body
const menuLinks = document.querySelectorAll('.admin-menu a')
const collapseBtn = document.querySelector('.admin-menu .collapse-btn')
const toggleMobileMenu = document.querySelector('.toggle-mob-menu')
const switchInput = document.querySelector('.switch input')
const switchLabel = document.querySelector('.switch label')
const switchLabelText = switchLabel.querySelector('span:last-child')
const collapsedClass = 'collapsed'
const lightModeClass = 'light-mode'

/*TOGGLE HEADER STATE*/
collapseBtn.addEventListener('click', function () {
  body.classList.toggle(collapsedClass)
  this.getAttribute('aria-expanded') == 'true'
    ? this.setAttribute('aria-expanded', 'false')
    : this.setAttribute('aria-expanded', 'true')
  this.getAttribute('aria-label') == 'collapse menu'
    ? this.setAttribute('aria-label', 'expand menu')
    : this.setAttribute('aria-label', 'collapse menu')
})

/*TOGGLE MOBILE MENU*/
toggleMobileMenu.addEventListener('click', function () {
  body.classList.toggle('mob-menu-opened')
  this.getAttribute('aria-expanded') == 'true'
    ? this.setAttribute('aria-expanded', 'false')
    : this.setAttribute('aria-expanded', 'true')
  this.getAttribute('aria-label') == 'open menu'
    ? this.setAttribute('aria-label', 'close menu')
    : this.setAttribute('aria-label', 'open menu')
})

/*SHOW TOOLTIP ON MENU LINK HOVER*/
for (const link of menuLinks) {
  link.addEventListener('mouseenter', function () {
    if (
      body.classList.contains(collapsedClass) &&
      window.matchMedia('(min-width: 768px)').matches
    ) {
      const tooltip = this.querySelector('span').textContent
      this.setAttribute('title', tooltip)
    } else {
      this.removeAttribute('title')
    }
  })
}

/*TOGGLE LIGHT/DARK MODE*/
if (localStorage.getItem('dark-mode') === 'false') {
  html.classList.add(lightModeClass)
  switchInput.checked = false
  switchLabelText.textContent = 'Light'
}

switchInput.addEventListener('input', function () {
  html.classList.toggle(lightModeClass)
  if (html.classList.contains(lightModeClass)) {
    switchLabelText.textContent = 'Light'
    localStorage.setItem('dark-mode', 'false')
  } else {
    switchLabelText.textContent = 'Dark'
    localStorage.setItem('dark-mode', 'true')
  }
})

//js for switching between tabs

let currentActive = document.getElementById('attendanceTab')

function switchToCollection() {
  currentActive.style.display = 'none'
  document.getElementById('collectionTab').style.display = 'flex'
  currentActive = document.getElementById('collectionTab')
}

function switchToAttendance() {
  currentActive.style.display = 'none'
  document.getElementById('attendanceTab').style.display = 'flex'
  currentActive = document.getElementById('attendanceTab')
}
async function getAttendence(){
  date=document.getElementById('date')
  if(new Date(date.value)<new Date()){
    let token=JSON.parse(document.getElementById('mydata').textContent);
    let data=await fetch(`/getattendence/${token}/?date=${date.value}`)
    data=await data.json()
    data=data.data
    if(data.total!==undefined) {
      document.getElementById('totalStudents').innerHTML = data.total
      document.getElementById('totalPresentStudents').innerHTML = data.presentstudent
      document.getElementById('totalAbsentStudents').innerHTML = data.absentstudent
      document.getElementById('file_link').innerHTML=`<a href="/collegemanagement/iiitbhopal/static/userUploadedFiles/attendenceFiles/${data.filename}" download="true">Download</a>`
    }
  else{
      document.getElementById('totalStudents').innerHTML = ""
      document.getElementById('totalPresentStudents').innerHTML = ""
      document.getElementById('totalAbsentStudents').innerHTML = ""
    }
  }
else{
  alert("Invalid date")
    date.value=""
  }
}
