
document.querySelector('button').addEventListener('click',function clickHandler(e){

    // this.removeEventListener('click',clickHandler);

    e.preventDefault();
    var self = this;
    setTimeout(function(){
        self.className = 'loading';
        self.innerHTML = 'Loading ...';
    },10);
});
