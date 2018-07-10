function repeatMe(){
        
        $.ajax({
            type:'GET',
            url:"/api/get_caller_list/",
            dataType:"json",
            success:function(data){
                // console.log(data);
                // console.log(onuser);
                var onuser='';
                for(i=0;i<data.length;i++){
                    // $('#data').text(data[i].username);
                    onuser+=(
                        // '<tr><td>'+data[i].fullname+'<br>'+data[i].username+'</td><tr>'
                        // '<tr><td><h4 class="ui image header"><img src="'+data[i].profile_image+'" class="ui mini rounded image" ><div class="content"><a href="'+data[i].profile_url+'" class="name">'+data[i].fullname+'</a><div class="sub header">@<a href="'+data[i].profile_url+'" class="username">'+data[i].username+'</a></div></div></h4></td><td><button type="button" class="ui red button" onclick="watchLive("'+data[i].username+'", "'+data[i].profile_url+'")"><i class="play icon"></i>WatchLive</button></td></tr>'
                        '<tr><td><h4 class="ui image header"><img src="'+data[i].profile_image+'" class="ui mini rounded image" ><div class="content"><a href="'+data[i].profile_url+'" class="name">'+data[i].fullname+'</a><div class="sub header">@<a href="'+data[i].profile_url+'" class="username">'+data[i].username+'</a></div></div></h4></td><td id="callButton"><button type="button" class="ui inverted teal button" id="myBtn" onclick="return startCall('+"'"+data[i].username+"'"+')">Call</button></td></tr>'
                    );
                    // console.log(onuser);
                }
                //console.log(onuser);
                $('#onlineuser').empty();
                $('#onlineuser').append(onuser);  
            }
        });
        $.ajax({
            type:'GET',
            url:"/api/get_streamers_list/",
            dataType:"json",
            success:function(data){
                // console.log(data);
                // console.log(onuser);
                var onuser='';
                for(i=0;i<data.length;i++){
                    // $('#data').text(data[i].username);
                    onuser+=(
                        // '<tr><td>'+data[i].fullname+'<br>'+data[i].username+'</td><tr>'
                        '<tr><td><h4 class="ui image header"><img src="'+data[i].profile_image+'" class="ui mini rounded image" ><div class="content"><a href="'+data[i].profile_url+'" class="name">'+data[i].fullname+'</a><div class="sub header">@<a href="'+data[i].profile_url+'" class="username">'+data[i].username+'</a></div></div></h4></td><td><button type="button" class="ui red button" onclick="watchLive('+"'"+data[i].username+"'"+','+"'"+data[i].stream_url+"'"+')"><i class="play icon"></i>WatchLive</button></td></tr>'
                        //'<tr><td><h4 class="ui image header"><img src="'+data[i].profile_image+'" class="ui mini rounded image" ><div class="content"><a href="'+data[i].profile_url+'" class="name">'+data[i].fullname+'</a><div class="sub header">@<a href="'+data[i].profile_url+'" class="username">'+data[i].username+'</a></div></div></h4></td><td id="callButton"><button type="button" class="ui inverted teal button" id="myBtn" onclick="return startCall('+"'"+data[i].username+"'"+')">Call</button></td></tr>'
                    );
                    // console.log(onuser);
                }
                //console.log(onuser);
                $('#streamers').empty();
                $('#streamers').append(onuser);  
            }
        });

        $.ajax({
            type:'GET',
            url:"/api/get_room_list/",
            dataType:"json",
            success:function(data){
                // console.log(data);
                // console.log(onuser);
                var onuser='';
                for(i=0;i<data.length;i++){
                    // $('#data').text(data[i].username);
                    onuser+=(
                        // '<tr><td>'+data[i].fullname+'<br>'+data[i].username+'</td><tr>'
                        // '<tr><td><h4 class="ui image header"><img src="'+data[i].profile_image+'" class="ui mini rounded image" ><div class="content"><a href="'+data[i].profile_url+'" class="name">'+data[i].fullname+'</a><div class="sub header">@<a href="'+data[i].profile_url+'" class="username">'+data[i].username+'</a></div></div></h4></td><td><button type="button" class="ui red button" onclick="watchLive("'+data[i].username+'", "'+data[i].profile_url+'")"><i class="play icon"></i>WatchLive</button></td></tr>'
                        '<tr><td><h4 class="ui image header"><img src="'+data[i].profile_image+'" class="ui mini rounded image" ><div class="content"><a href="'+data[i].profile_url+'" class="name">'+data[i].fullname+'</a><div class="sub header">@<a href="'+data[i].profile_url+'" class="username">'+data[i].username+'</a></div></div></h4></td><td id="callButton"><a href="' + data[i].room_url +'"type="button" class="ui inverted teal button" id="myBtn">View Room</a></td></tr>'
                    );
                    // console.log(onuser);
                }
                //console.log(onuser);
                $('#onlineroom').empty();
                $('#onlineroom').append(onuser);
            }
        });
        repeater = setTimeout(repeatMe, 10000);
    
}
$('.stop').click(function(){
    console.log('stopped');
    clearTimeout(repeater);
    });

repeatMe();
/* function fetchFollowers(){
    $.ajax({
        type: "GET",
        url: '{% url "home:getFollowers" %}',
        success: (data)=>{
            var datas = data.results;
            console.log(datas);
            datas.forEach((follower)=>{
                {#console.log(follower);#}
                var header = $('#header');
                // header.append("<img src='" + follower.profile_image +"'class='ui mini rounded image' >" +
                // '<div>@<a href="' + follower.profile_url + '"class="username">'+ follower.username + '</a></div>');
                // $('#callButton').append('<button type="button" class="ui inverted teal button" id="myBtn" onclick="return startCall(' + follower.username + ')">Call</button>'+ '<br>');
            })
        },
        complete: (data)=>{
            setTimeout(fetchFollowers, 15000);
        }
    })
}
$(document).ready(()=>{
    setTimeout(fetchFollowers, 15000);
}); */
