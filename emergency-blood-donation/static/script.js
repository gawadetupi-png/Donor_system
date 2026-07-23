// Retrieve registered donors from LocalStorage or start with empty list

// ------------------- DONOR REGISTRATION -------------------
document.getElementById("donorForm").addEventListener("submit", async function(e){

    e.preventDefault();

    const donor = {

        fullName: document.getElementById("fullName").value,
        phone: document.getElementById("phone").value,
        gender: document.getElementById("gender").value,
        bloodGroup: document.getElementById("bloodGroup").value,
        location: document.getElementById("location").value

    };

    const response = await fetch("/register",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify(donor)

    });

    const data = await response.json();

    alert(
`🎉 Registration Successful!

    Name : ${data.name}

    Donor ID : ${data.donorId}

    Please save your Donor ID for future reference.

    Thank you for joining the Ajit Dada Youth Foundation Blood Donor Network. ❤️`
);

    this.reset();

});

// ------------------- PUBLIC SEARCH FOR EVERYONE -------------------
async function searchDonors() {
    try {
        const location = document.getElementById("publicSearchLocation").value.trim();
        const blood = document.getElementById("publicSearchBloodGroup").value;

        console.log("Searching:", location, blood);

        const response = await fetch(
            `/search?location=${encodeURIComponent(location)}&bloodGroup=${encodeURIComponent(blood)}`
        );

        if (!response.ok) {
            throw new Error("Server Error");
        }

        const donors = await response.json();

        console.log(donors);

        const table = document.getElementById("publicDonorTable");
        const body = document.getElementById("publicDonorTableBody");

        table.classList.remove("hidden");   // Show table
        body.innerHTML = "";

        if (donors.length === 0) {
            body.innerHTML = `
                <tr>
                    <td colspan="5">No Donors Found</td>
                </tr>
            `;
            return;
        }

        donors.forEach(d => {
            body.innerHTML += `
                <tr>
                    <td>${d.fullName}</td>
                    <td>${d.bloodGroup}</td>
                    <td>${d.gender}</td>
                    <td>${d.location}</td>
                    <td>${d.phone}</td>
                </tr>
            `;
        });

    } catch (error) {
        console.error(error);
        alert(error);
    }
}
// ------------------- ADMIN AUTH & ALL RECORDS VIEW -------------------
const modal = document.getElementById('loginModal');
const loginBtn = document.getElementById('adminLoginBtn');
const logoutBtn = document.getElementById('adminLogoutBtn');
const closeBtn = document.getElementById('closeModal');
const adminDashboard = document.getElementById('adminDashboard');

loginBtn.addEventListener('click', () => modal.classList.remove('hidden'));
closeBtn.addEventListener('click', () => modal.classList.add('hidden'));

// Admin Login
document.getElementById('loginForm').addEventListener('submit', function(e) {
  e.preventDefault();
  
  const user = document.getElementById('username').value;
  const pass = document.getElementById('password').value;

  if (user === 'admin' && pass === 'admin123') {
    alert('Admin Login Successful!');
    modal.classList.add('hidden');
    loginBtn.classList.add('hidden');
    logoutBtn.classList.remove('hidden');
    adminDashboard.classList.remove('hidden');
    renderAdminAllRecords();
  } else {
    alert('Invalid Credentials! Try: admin / admin123');
  }
});

// Admin Logout
logoutBtn.addEventListener('click', () => {
  loginBtn.classList.remove('hidden');
  logoutBtn.classList.add('hidden');
  adminDashboard.classList.add('hidden');
});

// Render All Registered Donors for Admin
async function renderAdminAllRecords(){

    const response=await fetch("/getDonors");

    const donors=await response.json();

    document.getElementById("totalDonorsCount").innerHTML=donors.length;

    const body=document.getElementById("adminDonorTableBody");

    body.innerHTML="";

    donors.forEach((d,index)=>{

        body.innerHTML+=`

        <tr>

        <td>${index+1}</td>

        <td>${d.fullName}</td>

        <td>${d.phone}</td>
        
        <td>${d.gender}</td>

        <td>${d.bloodGroup}</td>

        <td>${d.location}</td>

        </tr>

        `;

    });

}