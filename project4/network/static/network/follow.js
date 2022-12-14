document.addEventListener('DOMContentLoaded',function(){
});

function edit_action(e,post)
{   console.log('edit has been clicked')
    const button =e.target;
    // console.log(button)
    const parent=button.parentElement;
    // console.log(parent)
    fetch(`/post/${post}`)
    .then(res=>res.json())
    .then(result=>{
        // console.log(result);
        const text=result.post;
        // the text_area 
        const  edit_text_area=document.createElement('textarea');
        edit_text_area.classList.add('edit_text_area')
        edit_text_area.value=text;
        //Getting the current text in the text area
        const current_text=edit_text_area.value
        //Save button
        const save=document.createElement('button');
        save.innerHTML='Save Edit';
        save.classList.add('btn','btn-primary','text-end','save_button','float-right');
        //cancel button
        const cancel=document.createElement('Cancel');
        cancel.innerHTML='Cancel'
        cancel.classList.add('btn','btn-outline-danger','float-left')
        //wrapper for the button needed for clearfix
        const edit_button_wrapper=document.createElement('div');
        edit_button_wrapper.classList.add('save_wrapper','clearfix','mt-2');
        edit_button_wrapper.append(cancel);
        edit_button_wrapper.append(save);
        post_node=parent.closest('.post');
        for(const child of post_node.children){
            if (child.className=='post_content')
            {   //child is post_content node

                child.innerHTML="";
                child.append(edit_text_area);
                child.append(edit_button_wrapper);
                cancel.addEventListener('click',()=>cancel_action(text,child,button,post_node));
                save.addEventListener('click',()=>save_action(post,child,current_text,button,edit_text_area));
                button.remove();
                break;
               
            }
        }
    })
}
function follow_action(action){
    console.log('follow button has been clicked')
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


function like_action(e,post){
    console.log('like button has been clicked')
    const button=e.target;
    fetch(`/post/${post}`,{
        method:'PUT'
    })
        .then(res=>res.json())
        .then(result=>{
            console.log(result)
            button.classList.toggle('fa-solid')
            button.classList.toggle('fa-regular')
            return result.likes
            }
        )
        .then(likes=> button.parentElement.nextElementSibling.innerHTML=likes);
}

function cancel_action(text,post_content_node,edit_button,post_node)
{   
    console.log('cancel has been clicked')
    post_content_node.innerHTML=" ";
    text=text.replaceAll('\n','<br>')
    post_content_node.innerHTML=text;
    post_content_node.style.backgroundColor='rgba(219, 214, 214, 0.4)';
    const node=post_node.querySelector(".edit_button_wrapper");
    // console.log(edit_button);
    // console.log(node);
    node.append(edit_button);
}

function save_action(post_id,post_content,text,edit_button,edit_text_area)
{
    //post_content is an html element 
    console.log('save button has been clicked')
    fetch(`/post/${post_id}`,{
        method:'POST',
        body:JSON.stringify({
            content:edit_text_area.value
        } )
    }).then(response=>response.json())
    .then(result=>{
        console.log(result);
        if (result.message=='Was sent empty content')
        {   
            post_content.innerHTML="";
            post_content.innerHTML=text.replaceAll('\n','<br>')
            const node=post_node.querySelector(".edit_button_wrapper");
            node.append(edit_button);

            // const error_message=document.createElement('div');
            // error_message.classList.add('error_message','alert','alert-danger')
            // error_message.innerHTML=result.message
            // console.log(error_message)
            post_content.insertAdjacentHTML('afterend',`<div class="error_message alert alert-danger mt-2">${result.message}</div>`)
        }
        else{
            if (result.change)
            {
                post_content.innerHTML="";
                post_content.innerHTML=result.content.replaceAll('\n','<br>');
                const node=post_node.querySelector(".edit_button_wrapper");
                node.append(edit_button);
                
            }
            else{
                if (result.message=='No changes made')
                {
                    post_content.innerHTML="";
                    post_content.innerHTML=text.replaceAll('\n','<br>');
                    const node=post_node.querySelector(".edit_button_wrapper");
                    node.append(edit_button);
                }
        
             }
        }

    })
    
}

