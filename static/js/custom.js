$(document).ready(function () {
    $('.increment-btn').click(function (e) { 
        e.preventDefault();

        var inc_value=$(this).closest('.product_data').find('.qty-input').val();
        var value =parseInt(inc_value,10);
        value=isNaN(value) ? 0 :value;
        if(value<10)
        {
            value++;
            $(this).closest('.product_data').find('.qty-input').val(value);
        }
        
    });
    
    $('.decrement-btn').click(function (e) { 
        e.preventDefault();

        var inc_value=$(this).closest('.product_data').find('.qty-input').val();
        var value =parseInt(inc_value,10);
        value=isNaN(value) ? 0 :value;
        if(value>1)
        {
            value--;
            $(this).closest('.product_data').find('.qty-input').val(value);
        }
        
    });
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
            var token=$('input[name=csrfmiddlewaretoken').val(); 
    
            if(fname==""||lname==""|| phone==""||email==""||address==""||pincode==""||state==""||city==""||country=="")
            {
                swal("Alert!","All fields are mandatory","error");
                return false;
            }
            else{
                $.ajax({
                    type: "GET",
                    url: "/proccedtopay",
                    success: function (response) {
                        //console.log(response);
                        var options = {
                            "key": "rzp_test_xRXu7nh3MHMiaw", // Enter the Key ID generated from the Dashboard
                            "amount": 1*100,
                            "currency": "INR",
                            "name":"Ekart",
                            "description": "Thank You",
                            "image": "https://s3.amazonaws.com/rzp-mobile/images/rzp.jpg",
                            //"order_id":"",
                            "handler":function(responseb){
                                alert(responseb.razorpay_payment_id);
                                data={
                                    " fname":fname,
                                    " lname":lname,
                                    " phone":phone,
                                    " email":email,
                                    " address":address,
                                    " pincode":pincode,
                                    " state":state,
                                    " city":city,
                                    " country":country,
                                    "payment_mode":"Razor Pay",
                                    "payment_id":responseb.razorpay_payment_id,
                                    csrfmiddlewaretoken:token
                                }
                                $.ajax({
                                    method: "POST",
                                    url: "/placeorder",
                                    data: data,
                                    success: function (responsec) {
                                        swal("Congratulations!",responsec,"scuccess").then((value) => {
                                            window.location.href='/myorder'
                                        });

                                    }
                                });
                                
                
                
                            },
                            "prefill":
                                {
                                "name":fname+""+lname,
                                "email": email,
                                "contact": phone,
                            },
                            "theme":{
                                "color":"#3399cc"
                            }
                            
                        };
                        var rzp1 = new Razorpay(options);
                        rzp1.open();
                    }
                });
                
            }
        });
    });


    $('.delete').click(function (e) { 
        e.preventDefault();
        var product_id=$(this).closest('.product_data').find('.prod_id').val();
        var token=$('input[name=csrfmiddlewaretoken').val(); 
        $.ajax({
            type: "POST",
            url: "/delete",
            data: {
                'product_id':product_id,
                 csrfmiddlewaretoken: token},
            success: function (response) {
                console.log(response) 
                $('.cartdata').load(location.href + " .cartdata");
                    
            }
        });
    });
    $(document).on('click','.wishdelete',function (e) {
        e.preventDefault();
        var product_id=$(this).closest('.product_data').find('.prod_id').val();
        var token=$('input[name=csrfmiddlewaretoken').val(); 
        $.ajax({
            type: "POST",
            url: "/wishdelete",
            data: {
                'product_id':product_id,
                 csrfmiddlewaretoken: token},
            success: function (response) {
                console.log(response) 
                $('.wishdata').load(location.href + " .wishdata");
                    
            }
        });
    });
    
    $('.addToCartBtn').click(function (e) { 
        e.preventDefault();
        var product_id=$(this).closest('.product_data').find('.prod_id').val();
        var product_qty=$(this).closest('.product_data').find('.qty-input').val();
        var token=$('input[name=csrfmiddlewaretoken').val();
        $.ajax({
            type: "POST",
            url: "/add-to-cart",
            data:{
                'product_id':product_id,
                'product_qty':product_qty,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
              console.log(response) 
              alertify.success(response.status)
            }
        });
        
    });

    $('.addToWishlist').click(function (e) { 
        e.preventDefault();
        var product_id=$(this).closest('.product_data').find('.prod_id').val();
        var token=$('input[name=csrfmiddlewaretoken').val();
        $.ajax({
            type: "POST",
            url: "/add-to-wishlist",
            data:{
                'product_id':product_id,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
              console.log(response) 
              alertify.success(response.status)
            }
        });
        
    });


    $('.changeQuantity').click(function (e) { 
        e.preventDefault();
        var product_id=$(this).closest('.product_data').find('.prod_id').val();
        var product_qty=$(this).closest('.product_data').find('.qty-input').val();
        var token=$('input[name=csrfmiddlewaretoken').val();
        $.ajax({
            type: "POST",
            url: "/update",
            data:{
                'product_id':product_id,
                'product_qty':product_qty,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
              console.log(response) 
              //alertify.success(response.status)
            }
        });
        
    });
    
});
