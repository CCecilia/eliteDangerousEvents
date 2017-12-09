/**
 * Created by Christian Cecilia on 12/04/17.
 */
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
        //serialize and submit search form
        $.ajax({
            type: "POST",
            url: "/register/",
            data: $(this).serialize(), 
            success: function(data){
                alert('user registered'); 
            },
            fail: function(data){
                alert('register failed'); 
            }
        });

        //Stop html form submission
        e.preventDefault(); 
    });
});