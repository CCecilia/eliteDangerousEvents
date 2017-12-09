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
});