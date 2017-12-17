/**
 * Created by Christian Cecilia on 12/04/17.
 */
function isValidEmailAddress(emailAddress) {
    var pattern = /^([a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+(\.[a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+)*|"((([ \t]*\r\n)?[ \t]+)?([\x01-\x08\x0b\x0c\x0e-\x1f\x7f\x21\x23-\x5b\x5d-\x7e\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|\\[\x01-\x09\x0b\x0c\x0d-\x7f\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))*(([ \t]*\r\n)?[ \t]+)?")@(([a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.)+([a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.?$/i;
    return pattern.test(emailAddress);
};

$(document).ready(function(){
	//add csrf token to headers
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": $("input[name='csrfmiddlewaretoken']").val()
        }
    });

    function dispalyEventDetails(event_id){
        //get event details and display popup
        $.ajax({
            type: "POST",
            url: "/event/details/",
            data: JSON.stringify({event_id: event_id}), 
            success: function(data){
                var event = JSON.parse(data.event);
                // clear out popup text
                $(
                    '.event-popup-name,'+
                    '.event-popup-description,'+
                    '.event-popup-start-date,'+
                    '.event-popup-location'
                ).empty();
                
                //fill in with event info
                if(event[0].fields.event_type == 'combat'){
                    $(".event-popup-type").attr({
                        'src': 'http://edassets.org/img/pilots-federation/combat/rank-9-combat.png',
                        'alt': event[0].fields.event_type
                    })
                }else if(event[0].fields.event_type == 'exploration'){
                    $(".event-popup-type").attr({
                        'src': 'http://edassets.org/img/pilots-federation/explorer/rank-9.png',
                        'alt': event[0].fields.event_type
                    })
                }else{
                    $(".event-popup-type").attr({
                        'src': 'http://edassets.org/img/pilots-federation/trading/rank-9-trading.png',
                        'alt': event[0].fields.event_type
                    })
                }
                console.log();
                $('.event-popup-name').text(event[0].fields.name);
                $('.event-popup-description').text(event[0].fields.description);
                $('.event-popup-start-date').text('Start Date:'+ event[0].fields.start_date);
                $('.event-popup-start-time').text('Start Time:'+ event[0].fields.start_time);
                $('.event-popup-end-date').text('End Date:' + event[0].fields.end_date);
                $('.event-popup-end-time').text('End Time:' + event[0].fields.end_time);
                $('.event-popup-location').text('Location:' + event[0].fields.location);
                $('.attedance').text(event[0].fields.attendees.length);
                $('input[name="event-id"]').val(event[0].pk);
                $('#event-details-popup').fadeIn(300);
            },
            fail: function(data){
                alert('unknown error occurred');
            }
        });
    };


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


    //Event location search
    $(".location-search-icon").click(function(e) {
        // get system query
    	var system_query = $("input[name='event-location']").val();
        
    	if(system_query.length > 2){
            // clear out table
    		$("#location-results-table").empty();

            // add loading animation 
            $(this).addClass('fa-pulse');

            $.ajax({
                type: "POST",
                url: '/search/systems/',
                data: JSON.stringify({system_query: system_query}), 
                success: function(data){
                    console.log(data);
                    // stop loading animation
                    $(".location-search-icon").removeClass('fa-pulse');
                    for ( i = 0; i < data.results.length; i++ ) { 
                        // create rows for slection table of top 5 results
                        result_html = '' +
                        '<tr class="location-result">' +
                            '<td>'+data.results[i].name+'</td' +
                        '</tr>';
                        $('#location-results-table').append($(result_html));
                    }

                },
                fail: function(data){
                    // stop loading animation
                    $(".location-search-icon").removeClass('fa-pulse');
                    // alert user of error
                    alert('unknown server error occurred');
                }
            });
    	}
    });


    //add location result to location
    $('#location-results-table').on('click', '.location-result', function() {
        console.log('test');
        //dec event id
        var result = $(this).text();

        // empty location table
        $("#location-results-table").empty();

        //fill location with result
        $("input[name='event-location']").val(result);
    });


    //Event create
    $("form[name='event-create-form']").submit(function(e) {
    	//get form inputs
    	var event_type = $("input[name='event-type']");
    	var form_inputs = [
    		$("input[name='event-title']"),
    		$("input[name='event-location']"),
			$(".event-description"),
			$("input[name='event-start-date']"),
			$("input[name='event-start-time']"),
			$("input[name='event-end-date']"),
			$("input[name='event-end-time']")
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

		if( !event_type.val() ){
    		//send user alert 
    		alert('please select an event type\ncombat, exploration, trading');
            return false
    	}

        // serialize and submit search form
        $.ajax({
            type: "POST",
            url: "/event/create/",
            data: $(this).serialize(), 
            success: function(data){
                //clear out create form
                for ( i = 0; i < form_inputs.length; i++ ) { 
                    form_inputs[i].val('');
                }
                event_type.val('');
                //uncheck event type
                $(".event-type-img").removeClass('event-type-selected');
                //display detail popup
                
                dispalyEventDetails(data.event_id);
            },
            fail: function(data){
                alert('unknown server error occurred');
            }
        });

        //Stop html form submission
        e.preventDefault(); 
    });


    //Event search select
    $(".event-search-input").keyup(function(e) {
    	//get search query
    	var event_search = $(this).val();

		if(event_search.length > 1){
			//serialize and submit search form
	        $.ajax({
	            type: "POST",
	            url: "/event/search/",
	            dataType: 'json',
	            data: JSON.stringify({event_search: event_search}), 
	            success: function(data){
	            	//clear any previous results
                	$('.event-search-results').empty();

                	//iterate through results 
                	var event_results = data.event_search_results;
			    	for ( i = 0; i < event_results.length; i++ ) { 

			    		//set null attendee count to 0
			    		if( !event_results[i].attendees ){
			    			var attendee_count = 0;
			    		}else{
			    			var attendee_count = event_results[i].attendees
			    		}

			    		//create event preview element
			    		var event_preview_html = ''+
			    		'<div class="event-preview" data-id="'+event_results[i].id+'">' +
			    			'<img class="event-type-img-sm" src="http://edassets.org/img/pilots-federation/combat/rank-9-combat.png" alt="Combat" data-type="combat"/>' +
			    			'<p>'+event_results[i].name+'</p>' +
			    			'<p>'+event_results[i].start_date+'</p>' + 
			    			'<span><i class="fa fa-users" aria-hidden="true"></i></span><span class="attendee-count">'+attendee_count+'</span>' +
		    			'</div>';

		    			//add preview to resuts section
	    				$('.event-search-results').append(event_preview_html);
					}
	            },
	            fail: function(data){
	                alert('unknown server error occurred');
	            }
	        });
		}		
    });


    //Show detail popup for event 
	$('.event-search-results').on('click', '.event-preview', function() {
		//dec event id
	    var event_id = $(this).attr('data-id');

        dispalyEventDetails(event_id);
	});


    //hide popups
	$('.cover-container, .remove-event-no').click(function(e) {
		$('#event-details-popup').hide();
		$("#confirm-removal-popup").hide();
	});


	//join event
	$("form[name='join-event']").submit(function(e) {
        // serialize and submit join form
        $.ajax({
            type: "POST",
            url: "/event/join/",
            data: $(this).serialize(), 
            success: function(data){
            	window.location.reload();
            },
            fail: function(data){
                alert('unknown server error occurred');
            }
        });

        //Stop html form submission
        e.preventDefault();
	});


    //edit event page change
	$('.edit-event').click(function(e) {
		var event_id = $('input[name="event-id"]').val();
		//navigate to edit page
		document.location.href = '/event/edit/'+event_id+'/';
	});


	//change date inputs type
	$('input[name="edit-event-start-date"], input[name="edit-event-end-date"]').click(function(e) {
		$(this).prop('type','date');
	});


	//change time inputs type
	$('input[name="edit-event-start-time"], input[name="edit-event-end-time"]').focusin(function(e) {
		$(this).prop('type','time');
	});


	//Event edit
    $("form[name='event-edit-form']").submit(function(e) {
    	//get form inputs
    	var event_title = $("input[name='event-title']");
    	var event_type = $("input[name='event-type']");
    	var event_location = $("input[name='event-location']");
    	var event_description = $(".event-description");
    	var user_id = $("input[name='event-creator-id']").val();
    	var event_id = $("input[name='event-creator-id']").val();

    	//check fields
    	if( !event_title.val() ){
	    	//add border
	    	event_title.css('border','1px solid red').focus();
	    	//reset input 
	    	setTimeout(function resetInput() {
                event_title.css("border","1px solid #c06400;");
            }, 3000);
            return false
    	}else if( !event_type.val() ){
    		//send user alert 
    		alert('please select an event type\ncombat, exploration, trading');
            return false
    	}else if( !event_location.val() ){
	    	//add border
	    	event_location.css('border','1px solid red').focus();
            return false
	    	//reset input 
	    	setTimeout(function resetInput() {
                event_location.css("border","1px solid #c06400;");
            }, 3000);
            return false
    	}else if( !event_description.val() ){
	    	//add border
	    	event_description.css('border','1px solid red').focus();
	    	//reset input 
	    	setTimeout(function resetInput() {
                event_description.css("border","1px solid #c06400;");
            }, 3000);
            return false
    	}

        // serialize and submit search form
        $.ajax({
            type: "POST",
            url: $(this).attr('action'),
            data: $(this).serialize(), 
            success: function(data){
                //refresh screen
                window.location.reload();
            },
            fail: function(data){
                alert('unknown server error occurred');
            }
        });

        //Stop html form submission
        e.preventDefault(); 
    });

    //Remove event btn
    $(".remove-event").click(function(e) {
    	//show confirmation popup
    	$("#confirm-removal-popup").show();
	});


    //Remove event confirm
    $(".remove-event-yes").click(function(e) {
    	var event_id = $('input[name="event-id"]').val();

    	// serialize and submit search form
        $.ajax({
            type: "POST",
            url: '/event/remove/',
            data: JSON.stringify({event_id: event_id}), 
            success: function(data){
                //refresh screen
                window.location.reload();
            },
            fail: function(data){
                alert('unknown server error occurred');
            }
        });

	});

});