

function goConf(){
    if (confirm("Είστε σίγουροι ότι θέλετε να προχωρήσετε στη διαγραφή;")) {
        $.ajax({
            url: '/casedetails?id=5fa52c3f7a9100759970603a',
            type: 'DELETE',
            success: function(result) {
               console.log("yes")
            }
        });
    } else {
        console.log("νο");
    }
}
