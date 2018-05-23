$(document).ready(function(){
    var stripeFormModule = $(".stripe-payment-form")
    var stripeModuleToken = stripeFormModule.attr("data-token")
    var stripeModuleNextUrl = stripeFormModule.attr("data-next-url")
    var stripeModuleBtnTitle = stripeFormModule.attr("data-btn-title") || "Submit"
    console.log(stripeModuleToken, stripeModuleNextUrl)
    var stripeTemplate = $.templates("#stripeTemplate")
    var stripeTemplateDataContext = {
        publishKey: stripeModuleToken,
        nextUrl: stripeModuleNextUrl,
        btnTitle: stripeModuleBtnTitle

    }
    var stripeTemplateHtml = stripeTemplate.render(stripeTemplateDataContext)
    stripeFormModule.html(stripeTemplateHtml)

    var paymentForm = $(".payment-form")

    if (paymentForm.length > 1){
        alert("More than one payment form exist")
        paymentForm.css("display", "none")
    } else if (paymentForm.length == 1) {

        var pubKey = paymentForm.attr("data-token")
        var nextUrl = paymentForm.attr("data-next-url")
        // Create a Stripe client.
    var stripe = Stripe(pubKey);
    
    
    // Create an instance of Elements.
    var elements = stripe.elements();
    
    // Custom styling can be passed to options when creating an Element.
    // (Note that this demo uses a wider set of styles than the guide below.)
    var style = {
      base: {
        color: '#32325d',
        lineHeight: '18px',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
          color: '#aab7c4'
        }
      },
      invalid: {
        color: '#fa755a',
        iconColor: '#fa755a'
      }
    };
    
    // Create an instance of the card Element.
    var card = elements.create('card', {style: style});
    
    // Add an instance of the card Element into the `card-element` <div>.
    card.mount('#card-element');
    
    // Handle real-time validation errors from the card Element.
    card.addEventListener('change', function(event) {
      var displayError = document.getElementById('card-errors');
      if (event.error) {
        displayError.textContent = event.error.message;
      } else {
        displayError.textContent = '';
      }
    });
    
    // Handle form submission.
    var form = document.getElementById('payment-form');
    form.addEventListener('submit', function(event) {
      event.preventDefault();
    
      stripe.createToken(card).then(function(result) {
        if (result.error) {
          // Inform the user if there was an error.
          var errorElement = document.getElementById('card-errors');
          errorElement.textContent = result.error.message;
        } else {
          // Send the token to your server.
          stripeTokenHandler(nextUrl, result.token);
        }
      });
    });

    function redirectToNext(nextPath, timeoffset){
        if (nextPath) {
            setTimeout(function(){
                window.location.href = nextPath
            }, timeoffset)
        }
    }

    function stripeTokenHandler(nextUrl, token){
        console.log(token)
        var paymentMethodEndpoint = 'create/'
        var data = {
            'token': token.id
        }
        $.ajax({
            data: data,
            url: paymentMethodEndpoint,
            method: "POST",
            success: function(data){
                console.log(data)
                var successMsg = data.message || "Your card has been added"
                card.clear()
                if (nextUrl){
                    successMsg = successMsg + "Redirecting..."
                }
                if ($.alert){
                    $.alert(successMsg)
                } else {
                    alert(successMsg)
                }
                redirectToNext(nextUrl, 1500)
            },
            error: function(error){
                console.log(error)
            }
        })
    }
}
})