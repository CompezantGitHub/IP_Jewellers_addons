odoo.define('jewellery_master.test',[], function (require) {
    "use strict";
    
    
    console.log("testhqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq");
    $(document).on('click', '#check', function(){
        try {
            var value1=$('#area_pincode').val()
            
                if(value1 === "" || value1 === null || value1 === undefined || value1.length !=6) {
                    console.log("The string is empty, null, or undefined.");
                    $('#message_response').text('Please enter 6 digit of your area pincode')
                    return;
                }
                console.log(value1)
                $('#message_response').text('Checking...')
                var data={'value':value1}
                fetch('/process-data', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)

                })
                .then(response => response.json())
                .then(data => $('#message_response').text(data.message))
                .catch(error => console.error('Error:', error));
            // Return or use the revised data
        } catch (error) {
            // Handle any errors that occur during the fetch or processing
            console.error("Error fetching and revising data:", error);
        }
        
     });
});

   
