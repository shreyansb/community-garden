cg.utils.getOrSetUserId = function() {
    // see if there is a user id in localStorage
    var user_id = localStorage.getItem('cg_user_id');
    if (!user_id) {
        user_id = cg.utils.uuid();
        localStorage.setItem('cg_user_id', user_id);
    }
    return user_id
};

cg.utils.uuid = function() {
    function S4() {
        return (((1+Math.random())*0x10000)|0).toString(16).substring(1);
    }
    return (S4()+S4()+"-"+S4()+"-"+S4()+"-"+S4()+"-"+S4()+S4()+S4());
};
