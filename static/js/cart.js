var updateBtns= document.getElementsByClassName("update-cart")

for(var i=0;i < updateBtns.length;i++)
{
    updateBtns[i].addEventListener("click",function(){
        var productID= this.dataset.product
        var action= this.dataset.action

        console.log("Product ID: "+productID+" Action: "+action)

        console.log("User: "+ user)

        if (user==="AnonymousUser")
        {
            console.log("User is not authenticated...")
        }
        else
        {
            UpdateUserOrder(productID,action)

        }
    })
}

function UpdateUserOrder(productID,action)
{
    console.log("User is authenticated. Sending data...")

    var url = "/update_cart/"    //goes to the  url path of update_cart

    fetch(url,{
        method:"POST",
        headers:{
            "Content-Type":"application/json",
            "X-CSRFToken":csrftoken
        },
        body:JSON.stringify({"productID":productID,"action":action})
    })
    .then((response)=>{return response.json()})
    .then((data)=>{location.reload()})
}

function addCookieItem(productID,action)
{
    console.log("User is not authenticated...")

    if (action==="add")
    {
        if(cart[productID]==undefined)
        {
            cart[productID]={"quantity":1}
        }
        else{
            cart[productID]["quantity"]+=1
        }
    }

    if (action==="remove")
    {
        cart[productID]["quantity"]-=1

        if(cart[productID]["quantity"]===0)
        {
            console.log("Item should be deleted")
            delete cart[productID]
        }
    }
    console.log("CART: "+ cart)
    document.cookie='cart='+JSON.stringify(cart) + ";domain=;path=/"

    location.reload()
}

var search=document.getElementById("me-2")
search.addEventListener("click",function(){
    this.style.backgroundColor="#2E2E2E";
})