
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
    if (confirm("Είστε σίγουροι ότι θέλετε να προχωρήσετε στη διαγραφή;")) {
        $.ajax({
            url: '/profile?id='+idPat,
            type: 'DELETE',
            success: function(result) {
                document.write(result);;
            }
        });
    }
}