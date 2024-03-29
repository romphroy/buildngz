let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "US" - add your country code
        componentRestrictions: {'country': ['us', 'in',]},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}


function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        console.log('place name=>', place.name)
    }

    // get the address components and assign them to the fields
    // console.log(place)
    var geocoder = new google.maps.Geocoder()
    var address = document.getElementById('id_address').value

    geocoder.geocode({'address': address}, function(results, status){
        if(status == google.maps.GeocoderStatus.OK){
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();

            // console.log('long=>', longitude)
            
            $('#id_latitude').val(latitude);
            $('#id_longitude').val(longitude);
        }
    });

    // loop through the address componant and assign other address data
    // console.log(place)
    $('#id_address').val(place.name);
    for(var i=0; i<place.address_components.length; i++){
        for(var j=0; j<place.address_components[i].types.length; j++){
            // get country
            if(place.address_components[i].types[j] == 'country'){
                $('#id_country').val(place.address_components[i].long_name);
            }
            // get state
            if(place.address_components[i].types[j] == 'administrative_area_level_1'){
                $('#id_state').val(place.address_components[i].short_name);
            }
            // get street number
            // if(place.address_components[i].types[j] == 'street_number'){
            //     $('#id_address').val(place.address_components[i].long_name);
            // }
            // get street
            // if(place.address_components[i].types[j] == 'route'){
            //     address += $('#id_address').val(place.address_components[i].long_name);
            // }
            // get City
            if(place.address_components[i].types[j] == 'locality'){
                $('#id_city').val(place.address_components[i].long_name);
            }
            // get postal code
            if(place.address_components[i].types[j] == 'postal_code'){
                $('#id_zip_code').val(place.address_components[i].long_name);
            }// else{
            //     $('#id_zip_code').val("");
            // }
        }
    }
            // $('#id_city').val(city);
            // $('#id_state').val(state);
            // $('#id_zip').val(postal_code);
}


$(document).ready(function(){
    // Add to cart
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();
        
        product_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        $.ajax({
            type: 'GET', 
            url: url, 
            success: function(response){
                console.log(response)
                if(response.status == 'login_required'){
                    swal(response.message, '', 'info').then(function(){
                        window.location = '/login';
                    })
                }if(response.status == 'Failed'){
                    swal(response.message, '', 'error')
                }else{
                    console.log(response.cart_counter['cart_count'])
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+product_id).html(response.qty);

                    // Discount and total amounts
                    applyCartAmounts(
                        response.cart_amount['discount'], 
                        response.cart_amount['total']
                    )
                }
            }
        })       
    })

    // Place the cart item quantity on load
    $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#'+the_id).html(qty)
    })

    // Decrease cart
    $('.decrease_cart').on('click', function(e){
        e.preventDefault();
        
        product_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        cart_id = $(this).attr('id');

        $.ajax({
            type: 'GET', 
            url: url, 
            success: function(response){
                console.log(response)
                if(response.status == 'login_required'){
                    swal(response.message, '', 'info').then(function(){
                        window.location = '/login';
                    })
                }else if(response.status == 'Failed'){
                    swal(response.message, '', 'error')
                }else{
                    console.log(response.cart_counter['cart_count'])
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+product_id).html(response.qty);
                   
                    // Discount and total amounts
                    applyCartAmounts(
                        response.cart_amount['discount'], 
                        response.cart_amount['total']
                    )

                    if(window.location.pathname == '/cart/'){
                        removeCartItem(response.qty, cart_id);
                    checkEmptyCart();
                    }                    
                }
            }
        })       
    })


    // Delete item from cart
    $('.delete_cart').on('click', function(e){
        e.preventDefault();
        
        cart_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        $.ajax({
            type: 'GET', 
            url: url, 
            success: function(response){
                console.log(response)
                if(response.status == 'Failed'){
                    swal(response.message, '', 'error')
                }else{
                    console.log(response.cart_counter['cart_count'])
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    swal(response.status, response.message, 'success')
                    
                    // Discount and total amounts
                    applyCartAmounts(
                        response.cart_amount['discount'], 
                        response.cart_amount['total']
                    )

                    removeCartItem(0, cart_id);
                    checkEmptyCart();
                }
            }
        })       
    })

    // Delete the cart element if the qty is zero
    function removeCartItem(cartItemQty, cart_id){
        if(cartItemQty <= 0){
            // remove the cart item element
            document.getElementById("cart-item-"+cart_id).remove()
        }
    }


    // Empty cart check
    function checkEmptyCart(){
        var cart_counter = document.getElementById('cart_counter').innerHTML
        if(cart_counter == 0){
            document.getElementById("empty-cart").style.display = "block";
        }
    }


    // Apply cart amounts
    function applyCartAmounts(discount, total){
        if(window.location.pathname == '/cart/'){
            $('#discount').html(discount)
            $('#total').html(total)
        }
    }
});