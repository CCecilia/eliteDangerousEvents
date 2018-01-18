$(document).ready(function(){
    let last_id = $("input[name='lfg-last-post-id']").val();
    (function worker() {
        $.ajax({    
            type: "POST",
            url: "/lfg/check/",
            data: JSON.stringify({last_id: last_id}),
            success: function(data) {
                if( data.status == 'success'){
                    console.log('starting for loop');
                    let new_posts = data.new_posts;

                    // check window reload is needed
                    if( new_posts.length < 10){
                        for( i in new_posts ){
                            console.log(new_posts[i]);
                            let discord_link;
                            let location;
                            let platform_icon;
                            let group_type_img;

                            // platform icon
                            if( new_posts[i].platform == 'XB' ) {
                                platform_icon = '<img class="event-platform-img-icon" src="/static/img/xbox-icon-ed-org.png" alt="XBox" data-type="XB" style="width:35%;"/>';
                            }else if( new_posts[i].platform == 'PS' ) {
                                platform_icon = '<img class="event-platform-img-icon" src="/static/img/Playstation-icon.png" alt="Playstation" data-type="PS" style="width:35%;"/>';
                            }else{
                                platform_icon = '<img class="event-platform-img-icon" src="/static/img/pc-icon.png" alt="PC" data-type="PC" style="width:35%;"/>';
                            }

                            // type ime
                            if( new_posts[i].post_type == 'combat' ) {
                                group_type_img = '<img class="event-type-img-sm" src="/static/img/rank-9-combat.png" alt="Combat" data-type="combat" style="width:35%;"/>';
                            } else if( new_posts[i].post_type == 'trade' ) {
                                group_type_img = '<img class="event-type-img-sm" src="/static/img/rank-9-trading.png" alt="Trade" data-type="trade" style="width:35%;"/>';
                            } else {
                                group_type_img = '<img class="event-type-img-sm" src="/static/img/rank-9-exploration.png" alt="Exploration" data-type="exploration" style="width:35%;"/>';
                            }

                            if( new_posts[i].discord_link === '' ) {
                                discord_link = 'Not Given';
                            } else {
                                discord_link = '<a href="'+new_posts[i].discord_link+'" target="_blank">'+String(new_posts[i].discord_link).substring(0,30)+'</a>'
                            }

                            if( new_posts[i].location === '' ) {
                                location = 'Not Given';
                            } else {
                                location = new_posts[i].location;
                            }

                            html = '<div class="row post-wrap">' +
                            '<div class="col-lg-2 text-center">' +
                                group_type_img +
                                '<br>' +
                                platform_icon + 
                            '</div>' +
                            '<div class="col-lg-4 text-left">' +
                                '<div class="row">' +
                                    '<div class="col-lg-5">' +
                                        '<p>Commander: '+new_posts[i].commander+'</p>' + 
                                        '<p>Rank: '+new_posts[i].rank+'</p>' +
                                        '<p>Ship: '+new_posts[i].ship+'</p>' +
                                    '</div>' +
                                    '<div class="col-lg-7 text-left">' +
                                        '<p>Discord: '+discord_link+'</p>' +
                                        '<p>Location: '+location+'</p>' +
                                    '</div>' +
                                '</div>' +
                            '</div>' +
                            '<div class="col-lg-4">' +
                                '<p>'+new_posts[i].message+'</p>' +
                            '</div>' +
                            '<div class="col-lg-1">' +
                                '<p class="center-vert">added now</p>' +
                            '</div>' +
                            '</div>' ;

                            $(".lfg-posts").prepend(html);
                            last_id = new_posts[i].id;
                        }
                    } else{
                        window.location.reload();
                    }
                    
                }
            },    
            complete: function() {
               setTimeout(worker, 30000);
            }
        });
    })();
});