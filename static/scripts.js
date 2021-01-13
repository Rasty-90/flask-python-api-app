
window.onload = function() {
    var ur = localStorage.getItem("useRole");
    var noneButtons = document.querySelectorAll(".button-un")
    var uButtons = document.querySelectorAll(".button-uu")
    var loginLi = document.getElementById("login")

    switch(ur) {
        case "admin":
            loginLi.href="/logout"
            loginLi.innerHTML="Αποσύνδεση"
          break;
        case "user":
            for ( var i=0; i<uButtons.length;i++){
                uButtons[i].disabled=true;
            }
            loginLi.href="/logout"
            loginLi.innerHTML="Αποσύνδεση"
          break;
        default:
            for ( var i=0; i<noneButtons.length;i++){
                noneButtons[i].disabled=true;
            }
            for ( var i=0; i<uButtons.length;i++){
                uButtons[i].disabled=true;
            }
            loginLi.href="/login"
            loginLi.innerHTML="Σύνδεση"
      }

  };

function caseDelConf(){
    var queryString =window.location.search.substring(1);
    const urlParams = new URLSearchParams(queryString);
    const idCase = urlParams.get('id')
    if (confirm("Είστε σίγουροι ότι θέλετε να προχωρήσετε στη διαγραφή;")) {
        $.ajax({
            url: '/casedetails?id='+idCase,
            type: 'DELETE',
            success: function(result) {
                document.write(result);;
            }
        });
    }
}

function patDelConf(){
    var queryString =window.location.search.substring(1);
    const urlParams = new URLSearchParams(queryString);
    const idPat = urlParams.get('id')
    if (confirm("Είστε σίγουροι ότι θέλετε να προχωρήσετε στη διαγραφή; H διαγραφή ασθενούς θα διαγράψει και όλα τα σχετικά περιστατικά")) {
        $.ajax({
            url: '/profile?id='+idPat,
            type: 'DELETE',
            success: function(result) {
                document.write(result);;
            }
        });
    }
}

function getRole(role){
    userRole=role
    //assigns the user role variable to the local Storage so that it can persist through the various pages of the app
    localStorage.setItem("useRole",userRole);
}

function disableContent(useRole){
    if (useRole=="user"){
        console.log(useRole)
    }
}