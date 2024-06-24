$(document).ready(function () {
    $('.payCheck').click(function (e) { 
        e.preventDefault();
        var fname=$("[name='fname']").val();
        var lname=$("[name='lname']").val();
        var phone=$("[name='phone']").val();
        var email=$("[name='email']").val();
        var address=$("[name='address']").val();
        var pincode=$("[name='pincode']").val();
        var state=$("[name='state']").val();
        var city=$("[name='city']").val();
        var country=$("[name='country']").val();

        if(fname==""||lname==""|| phone==""||email==""||address==""||pincode==""||state==""||city==""||country=="")
        {
            alert("All fields are mandatory")
            return false;
        }
        else{
            var options = {
                "key": "[YOUR_KEY_ID]", // Enter the Key ID generated from the Dashboard
                "amount": "1000",
                "currency": "INR",
                "description": "Acme Corp",
                "image": "https://s3.amazonaws.com/rzp-mobile/images/rzp.jpg",
                "order_id":"",
                "handler":function(response){
                    alert(response.razorpay_payment_id);
                    alert(response.razorpay_order_id);
                    alert(response.razorpay_signature)
    
    
                },
                "prefill":
                    {
                    "email": "gaurav.kumar@example.com",
                    "contact": +919900000000,
                },
                "notes":{
                    "address":"Address"
                },
                "theme":{
                    "color":"#3399cc"
                }
                
            };
            var rzp1 = new Razorpay(options);
            rzp1.open();
        }

        


        
        
    });
});