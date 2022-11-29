document.addEventListener('DOMContentLoaded',function(){
    if (document.querySelector("#follow_btn"))
    {document.querySelector("#follow_btn").addEventListener('click',()=>follow_action("follow"));
    }

    if (document.querySelector("#unfollow_btn"))
    {document.querySelector("#unfollow_btn").addEventListener('click',()=>follow_action("unfollow"));
    }
   

});

function follow_action(action){
    let follow=window.location.href;
    const by=document.querySelector(".user_logged_in").innerHTML;
    const re=new RegExp('.*\/(.*)');
    follow=follow.match(re)[1];
 

    if (action=="follow"){
        console.log(`[FOLLOW] ${follow} by ${by}`);
        action=true;
    }
        
    if (action=="unfollow"){
        console.log(`[UNFOLLOW] ${follow} by ${by}`);
        action=false;
    }

    fetch(`/user/${follow}`,{
        method:'PUT',
        body:JSON.stringify({
            follow:action
        })
    }).then(()=>window.location.reload());
}
