        document.getElementById("signup-form").addEventListener("submit", function(event) {

            let pass1 = document.getElementById("id_password1").value;

            let pass2 = document.getElementById("id_password2").value;



            if (pass1 !== pass2) {

                event.preventDefault();

                alert("Passwords do not match!");

            }

        });