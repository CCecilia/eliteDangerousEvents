/**
 * Created by Christian Cecilia on 12/04/17.
 */
var time_zone = Intl.DateTimeFormat().resolvedOptions().timeZone;

function isValidEmailAddress(emailAddress) {
    let pattern = /^([a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+(\.[a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+)*|"((([ \t]*\r\n)?[ \t]+)?([\x01-\x08\x0b\x0c\x0e-\x1f\x7f\x21\x23-\x5b\x5d-\x7e\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|\\[\x01-\x09\x0b\x0c\x0d-\x7f\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))*(([ \t]*\r\n)?[ \t]+)?")@(([a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.)+([a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.?$/i;
    return pattern.test(emailAddress);
}

function normalizeStartEndDT(datetime) {
    let utc_date = new Date(datetime);
    let local_dt = utc_date.toLocaleString().split(',');
    let time_with_seconds = local_dt[1].split(':');

    //  reconstruct time with out seconds
    let hours = time_with_seconds[0];
    let mins = time_with_seconds[1];
    let am_pm = time_with_seconds[2].split(' ')[1];
    let formatted_time = `${hours}:${mins} ${am_pm}`;

    return {
        date: local_dt[0],
        time: formatted_time
    };
}



$(document).ready(function(){
	//add csrf token to headers
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": $("input[name='csrfmiddlewaretoken']").val()
        }
    });

    // set user's timezone
    let tz_form = encodeURI(`timezone=${time_zone}`);
    $.ajax({
        type: "POST",
        url: "/setUserTz/",
        data: tz_form
    });

    function dispalyEventDetails(event_id){
        //get event details and display popup
        $.ajax({
            type: "POST",
            url: "/event/details/",
            data: JSON.stringify({event_id: event_id}), 
            success: function(data){
                let event = JSON.parse(data.event);
                let event_data = event[0].fields;

                // clear out popup text
                $(
                    '.event-popup-name,'+
                    '.event-popup-description,'+
                    '.event-popup-start-date,'+
                    '.event-popup-location'
                ).empty(); 

                //fill in with event info
                if(event_data.event_type == 'combat'){
                    $(".event-popup-type").attr({
                        'src': '/static/img/rank-9-combat.png',
                        'alt': event[0].fields.event_type
                    })
                }else if(event_data.event_type == 'exploration'){
                    $(".event-popup-type").attr({
                        'src': '/static/img/rank-9-exploration.png',
                        'alt': event_data.event_type
                    })
                }else{
                    $(".event-popup-type").attr({
                        'src': '/static/img/rank-9-trading.png',
                        'alt': event_data.event_type
                    })
                }

                if(event_data.platform == 'PC'){
                    $(".event-popup-platform").attr({
                        'src': '/static/img/pc-icon.png',
                        'alt': event_data.platform
                    })
                }else if(event_data.platform == 'XB'){
                    $(".event-popup-platform").attr({
                        'src': '/static/img/xbox-icon-ed-org.png',
                        'alt': event_data.platform
                    })
                }else{
                    $(".event-popup-platform").attr({
                        'src': '/static/img/Playstation-icon.png',
                        'alt': event_data.platform
                    })
                }

                let start_date = normalizeStartEndDT(event_data.start_date)
                let end_date = normalizeStartEndDT(event_data.end_date)

                $('.event-popup-name').text(event_data.name);
                $('.event-popup-description').text(event_data.description);
                $('.event-popup-start-date').text('Start Date: '+ start_date.date);
                $('.event-popup-start-time').text('Start Time: '+ start_date.time);
                $('.event-popup-end-date').text('End Date: ' + end_date.date);
                $('.event-popup-end-time').text('End Time: ' + end_date.time);
                $('.event-popup-location').text('Location: ' + event_data.location);
                $('.attendance').text(event_data.attendees.length);
                $('input[name="event-id"]').val(event[0].pk);
                $('#event-details-popup').fadeIn(600);
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
    	let form_inputs = [
    		$("input[name='register-username']"),
    		$("input[name='register-email']"),
    		$("input[name='register-password']"),
    		$("input[name='register-confirm-password']")
		];
    	
    	//check for blanks
    	for ( i in form_inputs ) { 
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
		let username = $("input[name='signin-username']").val();
		let password = $("input[name='signin-password']").val();
    	
    	//check for blanks
	    if( !username || !password ){
	    	//add border
	    	$("input[name='signin-username'], input[name='signin-password']").css('border','1px solid red');
	    	//reset input 
	    	setTimeout(function resetInput() {
                $("input[name='signin-username'], input[name='signin-password']").css("border","1px solid #c06400;");
            }, 3000);
	    	return false;

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


    //platform type Select
    $(".platform-type-img").click(function(e) {
        //add select class to element
        $(".platform-type-img").removeClass('platform-type-selected');
        $(this).addClass('platform-type-selected');

        //add value to input
        $("input[name='platform-type']").val($(this).attr('data-type'));
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
    $("input[name='event-location'],input[name='lfg-location']").keyup(function(e) {
        // get system query
    	let system_query = $(this).val();
        
    	if(system_query.length > 2){
            // clear out table
    		$("#location-results-table").empty();

            $.ajax({
                type: "POST",
                url: "/search/systems/",
                data: JSON.stringify({system_query: system_query}), 
                success: function(data){
                    console.log(data);
                    // stop loading animation
                    $(".location-search-icon").removeClass("fa-pulse");
                    for ( i = 0; i < data.results.length; i++ ) { 
                        // create rows for slection table of top 5 results
                        result_html = '' +
                        '<tr class="location-result">' +
                            '<td>'+data.results[i].name+'</td' +
                        '</tr>';
                        $('#location-results-table').append($(result_html));
                    }

                    // clear table after 10s
                    setTimeout(function(){
                        // empty location table
                        $("#location-results-table").empty();
                    }, 10000);

                },
                fail: function(data){
                    // alert user of error
                    alert("unknown server error occurred");
                }
            });
    	}
    });


    //add location result to location
    $('#location-results-table').on("click", ".location-result", function() {
        console.log('test');
        //dec event id
        let result = $(this).text();

        // empty location table
        $("#location-results-table").empty();

        //fill location with result
        $("input[name='event-location']").val(result);
        $("input[name='lfg-location']").val(result);
    });


    //Event create
    $("form[name='event-create-form']").submit(function(e) {
        //Stop html form submission
        e.preventDefault(); 

    	//get form inputs
        let event_type = $("input[name='event-type']");
    	let platform_type = $("input[name='platform-type']");
        
    	let form_inputs = [
    		$("input[name='event-title']"),
    		$("input[name='event-location']"),
			$(".event-description"),
			$("input[name='event-start-date']"),
			$("input[name='event-start-time']"),
			$("input[name='event-end-date']"),
			$("input[name='event-end-time']")
		];
    	
    	//check for blanks
    	for ( i in form_inputs ) { 
		    if( !form_inputs[i].val() ){
		    	//add border
		    	form_inputs[i].css('border','1px solid red').focus();
		    	//reset input 
		    	setTimeout(function resetInput() {
	                form_inputs[i].css("border","1px solid #c06400;");
	            }, 3000);
		    	return false;
		    }
		}

		if( !event_type.val() ){
    		//send user alert 
    		alert('please select an event type\ncombat, exploration, trading');
            return false
    	} 

        if( !platform_type.val() ){
            //send user alert 
            alert('please select an platform\nXbox, Playstation, PC');
            return false
        }

        // serialize and submit search form
        // let formData = $(this).serialize()
        // formData = formData + encodeURI(`&time-zone=${time_zone}`);

        $.ajax({
            type: "POST",
            url: "/event/create/",
            data: $(this).serialize(), 
            success: function(data){
                if( data.status === 'success' ){
                    // clear out create form
                    for ( i in form_inputs ) { 
                        form_inputs[i].val('');
                    }
                    event_type.val('');
                    platform_type.val('');
                    $("input[name='discord-link']");
                    //uncheck event type
                    $(".event-type-img").removeClass('event-type-selected');
                    $(".platform-type-img").removeClass('platform-type-selected');
                    
                    //display detail popup
                    dispalyEventDetails(data.event_id);
                }else{
                    window.alert(data.error_msg);
                }
                    
            },
            fail: function(data){
                alert('unknown server error occurred');
            }
        });
    });


    //Event search select
    $(".event-search-input").keyup(function(e) {
    	//get search query
    	let event_search = $(this).val();

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
                	let event_results = data.event_search_results;
			    	for ( i in event_results ) { 
                        let attendee_count;
                        let platform_icon;

			    		//set null attendee count to 0
			    		if( !event_results[i].attendees ) {
			    			attendee_count = 0;
			    		}else {
			    			attendee_count = event_results[i].attendees;
			    		}

                        // platform icon
                        if( event_results[i].platform == 'XB' ) {
                            platform_icon = '<img class="event-platform-img-icon" src="/static/img/xbox-icon-ed-org.png" alt="XBox" data-type="XB"/>';
                        }else if( event_results[i].platform == 'PS' ) {
                            platform_icon = '<img class="event-platform-img-icon" src="/static/img/Playstation-icon.png" alt="Playstation" data-type="PS"/>';
                        }else{
                            platform_icon = '<img class="event-platform-img-icon" src="/static/img/pc-icon.png" alt="PC" data-type="PC"/>';
                        }

                        // truncate event name if nes
                        let event_name;
                        if( event_results[i].name.length > 20 ){
                            event_name = String(event_results[i].name).substring(0,20);
                        }else{
                            event_name = event_results[i].name;
                        }

			    		//create event preview element
			    		let event_preview_html = ''+
			    		'<div class="event-preview" data-id="'+event_results[i].id+'">' +
			    			'<img class="event-type-img-sm" src="http://edassets.org/img/pilots-federation/combat/rank-9-combat.png" alt="Combat" data-type="combat"/>' +
			    			'<p>'+event_name+'</p>' +
			    			'<p>'+event_results[i].start_date+'</p>' + 
                            '<span>'+platform_icon+'</span>' +
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
	$(".event-search-results").on("click", ".event-preview", function() {
		//dec event id
	    let event_id = $(this).attr('data-id');

        dispalyEventDetails(event_id);
	});

    //
    $(".featured-event-preview").click(function(e) {
        //dec event id
        let event_id = $(this).attr('data-id');

        dispalyEventDetails(event_id);
    });


    //hide popups
	$(".cover-container, .remove-event-no").click(function(e) {
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
	$(".edit-event").click(function(e) {
		let event_id = $('input[name="event-id"]').val();
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
        //Stop html form submission
        e.preventDefault();

    	//get form inputs
    	let event_title = $("input[name='event-title']");
        let event_type = $("input[name='event-type']");
    	let platform_type = $("input[name='platform-type']");
    	let event_location = $("input[name='event-location']");
    	let event_description = $(".event-description");
    	let user_id = $("input[name='event-creator-id']").val();
    	let event_id = $("input[name='event-creator-id']").val();

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
        }else if( !platform_type.val() ){
    		//send user alert 
    		alert('please select an event platform\nXbox, Playstation, Pc');
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

        // serialize and submit edit form
        $.ajax({
            type: "POST",
            url: $(this).attr('action'),
            data: $(this).serialize(), 
            success: function(data){
                if( data.status === 'success'){
                    //refresh screen
                    window.location.reload();
                }else{
                    alert(data.error_msg);
                }   
            },
            fail: function(data){
                alert('unknown server error occurred');
            }
                
        });        
    });


    //Remove event btn
    $(".remove-event").click(function(e) {
    	//show confirmation popup
    	$("#confirm-removal-popup").show();
	});


    //Remove event confirm
    $(".remove-event-yes").click(function(e) {
        let event_id = $('input[name="event-id"]').val();

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


    //Event Share
    $(".share-event, .share-cancel").click(function(e) {
        //toggle event options shown
        $(".event-option").toggle();
        $(".event-share-option").toggle();      
    });


    //show signin popup
    $(".show-signin-required-popup, .hide-signin-required-popup").click(function(e) {
        $('#signin-required-popup').toggle()      
    });


    //toggle lfg post form
    $(".toggle-lfg-post").click(function(e){
        $(this).toggleClass('fa-chevron-down');
        $(this).toggleClass('fa-chevron-up');
        $('.lfg-form-wrap').slideToggle();
    });


    //lfg create
    $("form[name='lfg-post-form']").submit(function(e){
        //Stop html form submission
        e.preventDefault();

        // check form inputs
        let group_type = $("input[name='event-type']");
        let platform_type = $("input[name='platform-type']");
        let commander_name = $("input[name='commander-name']");

        if( !group_type.val() ){
            //send user alert 
            alert('please select an event type\ncombat, exploration, trading');
            return false
        }else if( !platform_type.val() ){
            //send user alert 
            alert('please select an event platform\nXbox, Playstation, Pc');
            return false
        }else if( !commander_name.val() ){
            //add border
            commander_name.css('border','1px solid red').focus();
            //reset input 
            setTimeout(function resetInput() {
                commander_name.css("border","1px solid #c06400;");
            }, 3000);
            return false
        }

        // serialize and submit edit form
        $.ajax({
            type: "POST",
            url: $(this).attr('action'),
            data: $(this).serialize(), 
            success: function(data){
                if( data.status === 'success'){
                    //refresh screen
                    window.location.reload();
                }else{
                    alert(data.error_msg);
                }   
            },
            fail: function(data){
                alert('unknown server error occurred');
            }
                
        });
    });

});