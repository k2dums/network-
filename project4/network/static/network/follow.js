document.addEventListener('DOMContentLoaded',function(){
 

    document.querySelector("#follow_btn").addEventListener('click',follow_action);
    document.querySelector("#unfollow_btn").addEventListener('click',unfollow_action);

});

function follow_action(){
    let follow=window.location.href;
    const by=document.querySelector(".user_logged_in").innerHTML;
    const re=new RegExp('.*\/(.*)');
    follow=follow.match(re)[1];
    console.log(`[FOLLOW] ${follow} by ${by}`);
}

function unfollow_action(){
    let unfollow=window.location.href;
    const by=document.querySelector(".user_logged_in").innerHTML;
    const re=new RegExp('.*\/(.*)');
    unfollow=unfollow.match(re)[1];
    console.log(`[UNFOLLOW] ${unfollow} by ${by}`);
}