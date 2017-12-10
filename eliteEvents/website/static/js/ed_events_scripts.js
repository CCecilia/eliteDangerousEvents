/**
 * Created by Christian Cecilia on 12/04/17.
 */
function isValidEmailAddress(emailAddress) {
    var pattern = /^([a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+(\.[a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+)*|"((([ \t]*\r\n)?[ \t]+)?([\x01-\x08\x0b\x0c\x0e-\x1f\x7f\x21\x23-\x5b\x5d-\x7e\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|\\[\x01-\x09\x0b\x0c\x0d-\x7f\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))*(([ \t]*\r\n)?[ \t]+)?")@(([a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.)+([a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.?$/i;
    return pattern.test(emailAddress);
};


$(document).ready(function(){
	//Event search form
    $("form[name='event-search-form']").submit(function(e) {
        //serialize and submit search form
        $.ajax({
            type: "POST",
            url: "/searchEvents/",
            data: $(this).serialize(), 
            success: function(data){
                alert('event search success'); 
            },
            fail: function(data){
                alert('event search failed'); 
            }
        });

        //Stop html form submission
        e.preventDefault(); 
    });


    //signin/register indentifiers
    $("signin, register").click(function(e) {
    	//remove active identfier
    	$("signin").removeClass('active-signin');
    	$("register").removeClass('active-signin');

    	//Add active class to clicked element
    	$(this).addClass('active-signin');

    	//toggle shown forms
    	$(".signin-form, .register-form").toggle();
    });


	//Register form
    $("form[name='register-form']").submit(function(e) {
    	console.log('validating form');
    	//validate
    	var form_inputs = [
    		$("input[name='register-username']"),
    		$("input[name='register-email']"),
    		$("input[name='register-password']"),
    		$("input[name='register-confirm-password']")
		];
    	
    	//check for blanks
    	for ( i = 0; i < form_inputs.length; i++ ) { 
		    if( !form_inputs[i].val() ){
		    	//add border
		    	form_inputs[i].css('border','1px solid red').focus();
		    	//reset input 
		    	setTimeout(function resetInput() {
	                form_inputs[i].css("border","1px solid #c06400;");
	            }, 3000);
		    	return false
		    }
		}

		//check email validatity
		if( !isValidEmailAddress(form_inputs[2].val()) ){
	    	//add border
	    	form_inputs[2].css('border','1px solid red').focus();
	    	//reset input 
	    	setTimeout(function resetInput() {
                form_inputs[2].css("border","1px solid #c06400;");
            }, 3000);

		}

		//confirm password
		if( form_inputs[2].val() !== form_inputs[3].val() ){
	    	//add border
	    	form_inputs[2].css('border','1px solid red').focus();
	    	form_inputs[3].css('border','1px solid red');
	    	//reset input 
	    	setTimeout(function resetInput() {
                form_inputs[2].css("border","1px solid #c06400;");
                form_inputs[3].css("border","1px solid #c06400;");
            }, 3000);
	    	return false
		}else{
	        // serialize and submit search form
	        $.ajax({
	            type: "POST",
	            url: "/register/",
	            data: $(this).serialize(), 
	            success: function(data){
	                if( data.status == 'success'){
	                	//redirect to homepage
	                	window.location.href = window.location.protocol + "//" + window.location.host + "/";
	                }else{
	                	$(".register-error").show().text(data.error_msg);
	                }
	            },
	            fail: function(data){
	                alert('unknown error occurred');
	            }
	        });
		}

        //Stop html form submission
        e.preventDefault(); 
    });

    //login form
    $("form[name='signin-form']").submit(function(e) {
    	console.log('log in')
    	//reset error if recurring attempt
    	$(".signin-error").hide();

    	//validate
		var username = $("input[name='signin-username']").val();
		var password = $("input[name='signin-password']").val();
    	
    	//check for blanks
	    if( !username || !password ){
	    	//add border
	    	$("input[name='signin-username'], input[name='signin-password']").css('border','1px solid red');
	    	//reset input 
	    	setTimeout(function resetInput() {
                $("input[name='signin-username'], input[name='signin-password']").css("border","1px solid #c06400;");
            }, 3000);
	    	return false

	    }else{
	    	// serialize and submit search form
	        $.ajax({
	            type: "POST",
	            url: "/login/",
	            data: $(this).serialize(), 
	            success: function(data){
	                if( data.status == 'success'){
	                	//redirect to homepage
	                	window.location.href = window.location.protocol + "//" + window.location.host + "/";
	                }else{
	                	$(".signin-error").show();
	                }
	            },
	            fail: function(data){
	                alert('unknown error occurred');
	            }
	        });
	    }

        //Stop html form submission
        e.preventDefault(); 
    });

    //Event type Select
    $(".event-type-img").click(function(e) {
    	//add select class to element
    	$(".event-type-img").removeClass('event-type-selected');
    	$(this).addClass('event-type-selected');
    	//add value to input
    	$("input[name='event-type']").val($(this).attr('data-type'));
    });

    //Event type Select
    $(".event-location").keyup(function(e) {
    	var query = $(this).val();

    	if(query.length > 2){
    		console.log('long enough for search');
    	}
    });

    //Event create
    $("form[name='event-create-form']").submit(function(e) {
    	//get data
    	var event_title = $("input[name='event-title']");
    	var event_type = $("input[name='event-type']");
    	var event_location = $("input[name='event-location']");
    	var event_description = $(".event-description");
    	var user_id = $("input[name='event-creator-id']").val();

    	//check fields
    	if( !event_title.val() ){
	    	//add border
	    	event_title.css('border','1px solid red').focus();
	    	//reset input 
	    	setTimeout(function resetInput() {
                event_title.css("border","1px solid #c06400;");
            }, 3000);
    	}else if( !event_type.val() ){
    		alert('please select an event type\ncombat, exploration, trading');
    	}else if( !event_location.val() ){
	    	//add border
	    	event_location.css('border','1px solid red').focus();
	    	//reset input 
	    	setTimeout(function resetInput() {
                event_location.css("border","1px solid #c06400;");
            }, 3000);
    		
    	}else if( !event_description.val() ){
	    	//add border
	    	event_description.css('border','1px solid red').focus();
	    	//reset input 
	    	setTimeout(function resetInput() {
                event_description.css("border","1px solid #c06400;");
            }, 3000);

    	}

        // serialize and submit search form
        $.ajax({
            type: "POST",
            url: "/event/create/",
            data: $(this).serialize(), 
            success: function(data){
                if( data.status == 'success'){
                	alert('event created');
                }else{
                	alert('event failed');
                }
            },
            fail: function(data){
                alert('unknown server error occurred');
            }
        });

        //Stop html form submission
        e.preventDefault(); 
    });
});